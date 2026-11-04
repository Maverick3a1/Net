# reject-bot

把域名的文字或截图发给这个 Telegram 机器人，Claude 会告诉你每个域名适合加到哪个列表：

- **Reject**：广告 / 跟踪 / 遥测，写进 [`Rules/Reject`](../../Rules/Reject) 的 `Manual` 段；
- **某个分类条目**：例如 `AI/OpenAI`、`Bank/HSBC`、`Broker/Futu`、`Crypto/Binance`，写进对应分类的 `config`，并重新生成规则。

你在 Telegram 里点按钮选定后才会写入，都直接进 `main`。

## 怎么工作

```
你 ──文字 / 截图──▶ Worker（存进 KV，回复「已收到」，并通过 API 触发云端任务）
                       ▲   │
       GET /api/pending │   │ POST /api/verdict/<id>（每个域名的建议目标）
                       │   ▼
            Claude 云端任务「Reject 待办判断」（收到消息就触发，每天 23:00 兜底一次）
                           │
Worker ──每个域名的建议 + 按钮（1 → AI/OpenAI、1 → Reject、跳过 1 …）──▶ 你
你点按钮：
  → Reject        Worker 立即用 GitHub API 提交 manual.json 和三个 Reject 文件
  → 分类/条目     Worker 记为「已确认」并再次触发云端任务；任务读 GET /api/approved，
                  改该分类的 config、运行 build.py、推送到 main，
                  再用 POST /api/applied/<id>/<i> 回报，消息上显示提交号或失败原因
```

- 只处理 `TELEGRAM_USER_ID` 发来的消息和按钮，其他人一律忽略。
- Worker 不调用任何 AI，判断和分类写入都交给云端任务。连着发几条消息时，只要触发的那次运行还没开始读队列，就不再重复触发（单个任务每小时最多触发 30 次）；运行会反复读队列直到清空。触发失败的等每天 23:00 兜底处理。
- 建议目标只会是 `Reject` 或配置里已有的条目（不含 `BrokerShared`）；属于新公司的域名不能自动新建条目，只会在说明里提到。
- 已经收录的不会重复添加：Reject 显示「已存在」，分类显示「已收录，无需修改」。
- 分类写入仍受各分类自己的规则约束（过宽后缀、内地券商等会被拒绝，并在消息上写明原因）。写入时 `build.py` 会顺带刷新该分类的上游数据，一起提交。
- 排队的消息 30 天后自动过期。
- 各分类的 `build.py` 和 `python3 Rules/Reject/scripts/reject.py` 都会按 `manual.json` 重新生成 `Manual` 段，所以要删掉 Reject 里的某条，改 `manual.json` 再运行 `reject.py` 就行。

## 部署

需要 Cloudflare 账号（免费版即可），在本目录下操作。

1. 在 Telegram 里找 [@BotFather](https://t.me/BotFather) 创建机器人，拿到 Bot Token。再找 [@userinfobot](https://t.me/userinfobot) 查到你自己的数字用户 ID。
2. 在 GitHub 创建 [fine-grained token](https://github.com/settings/personal-access-tokens/new)：Repository access 只选 `Maverick3a1/Net`，权限只开 **Contents: Read and write**。
3. 登录 Cloudflare，并创建 KV：

   ```bash
   npx wrangler login
   ```

   ```bash
   npx wrangler kv namespace create QUEUE
   ```

   把输出里的 `id` 填进 [`wrangler.toml`](wrangler.toml) 的 `REPLACE_WITH_KV_NAMESPACE_ID`。
4. 逐个设置密钥。命令里只写名字，回车后它会提示你粘贴值（不要把值写在命令里）。`WEBHOOK_SECRET` 和 `ROUTINE_TOKEN` 自己随机生成，例如用 `openssl rand -hex 32`：

   ```bash
   npx wrangler secret put TELEGRAM_TOKEN
   ```

   ```bash
   npx wrangler secret put TELEGRAM_USER_ID
   ```

   ```bash
   npx wrangler secret put WEBHOOK_SECRET
   ```

   ```bash
   npx wrangler secret put ROUTINE_TOKEN
   ```

   ```bash
   npx wrangler secret put GITHUB_TOKEN
   ```

   最后一个是云端任务的 API 触发 token：打开 [「Reject 待办判断」](https://claude.ai/code/routines/trig_015eZU6NkN8XakECnAymSpWc) → Edit → Trigger 一栏点 **+** → **API** → **Generate token**（只显示一次）：

   ```bash
   npx wrangler secret put CLAUDE_ROUTINE_TOKEN
   ```

5. 部署，记下输出的地址（`https://reject-bot.<你的子域>.workers.dev`）：

   ```bash
   npx wrangler deploy
   ```

6. 注册 Telegram webhook（把地址和 `ROUTINE_TOKEN` 换成你的）：

   ```bash
   curl -X POST -H "Authorization: Bearer <ROUTINE_TOKEN>" https://reject-bot.<你的子域>.workers.dev/api/setup
   ```

7. 在 [claude.ai 的云端环境设置](https://claude.ai/code) 里，给「Reject 待办判断」用的环境：
   - 加环境变量 `REJECT_BOT_URL`（第 5 步的地址）和 `REJECT_BOT_TOKEN`（`ROUTINE_TOKEN` 的值）；
   - 网络访问放行 `reject-bot.<你的子域>.workers.dev`（以及 `dns.google`）。

   然后打开 [「Reject 待办判断」](https://claude.ai/code/routines/trig_015eZU6NkN8XakECnAymSpWc)并启用它。写入分类时它会按提示词直接推送到 `main`，不需要额外设置；只有 `main` 开了 GitHub 分支保护 / rulesets、且不允许你连接给 Claude 的 GitHub 账号推送时才会失败，消息上会显示「没有推送 main 的权限」。
8. 给机器人发 `/help` 试一下，再发一个域名，几分钟内应该收到判断结果。

兜底时间改了的话，同时改 `wrangler.toml` 里的 `JUDGE_SCHEDULE`（只用于回复里的提示）并重新部署。

## 开发

```bash
npm test
```

测试会模拟 Telegram、GitHub 和 KV，走一遍「发消息 → 排队 → 建议 → 点按钮 → 提交 Reject / 交给云端任务写入分类」，并核对 Worker 写出的文件和 `reject.py` 生成的结果逐字节一致。
