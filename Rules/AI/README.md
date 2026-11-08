# AI

美国主流 AI 服务（OpenAI、Anthropic、xAI Grok、Google Gemini、Perplexity、Copilot、Meta AI）的 Clash / Surge / Shadowrocket 分流规则。所有厂商合并成一个规则集 **`AI_All`**，一条规则全部覆盖。

## 规则文件

<!-- RULES:START -->
| 平台 | 规则文件 |
| --- | --- |
| Surge | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Surge/AI_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Surge/AI_All_Domain.list) |
| Shadowrocket | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Shadowrocket/AI_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Shadowrocket/AI_All_Domain.list) |
| Clash / mihomo | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Clash/AI_All.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Clash/AI_All_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Clash/AI_All_IP.yaml) |

`AI_All` 共 148 条域名规则、5 个 IP 段，收录以下 7 个厂商：

| 厂商 | 说明 | 域名 | IP |
| --- | --- | ---: | ---: |
| OpenAI | OpenAI: ChatGPT, Sora, Codex, OpenAI API | 23 | 0 |
| Anthropic | Anthropic: Claude, Claude Code, Claude API | 19 | 4 |
| xAI | xAI: Grok, Grok API | 6 | 1 |
| Gemini | Google: Gemini, AI Studio, NotebookLM, DeepMind, Jules, Antigravity | 74 | 0 |
| Perplexity | Perplexity AI | 5 | 0 |
| Copilot | Microsoft Copilot and GitHub Copilot | 14 | 0 |
| MetaAI | Meta AI and Llama | 7 | 0 |
<!-- RULES:END -->

## 使用方法

`Reject`（广告 / 跟踪 / 遥测，见下文）配 `REJECT`，放在 `AI_All` 前面。

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Surge/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Surge/AI_All.list,AI
```

### Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Shadowrocket/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Shadowrocket/AI_All.list,AI
```

也可以在 Shadowrocket 的「配置 → 规则 → 添加规则」里选 `RULE-SET`，填入上面的 raw 地址。

### Clash / mihomo

```yaml
rule-providers:
  Reject:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Clash/Reject.yaml
    path: ./ruleset/Reject.yaml
    interval: 86400
  AI_All:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/AI/Clash/AI_All.yaml
    path: ./ruleset/AI_All.yaml
    interval: 86400

rules:
  - RULE-SET,Reject,REJECT
  - RULE-SET,AI_All,AI
```

### 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/AI_All.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/AI_All_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快） |
| `Shadowrocket/AI_All.list` | Shadowrocket `RULE-SET`（内容同 Surge 版） |
| `Shadowrocket/AI_All_Domain.list` | Shadowrocket `DOMAIN-SET`（仅域名） |
| `Clash/AI_All.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/AI_All_Domain.yaml` | mihomo rule-provider，`behavior: domain`（仅域名） |
| `Clash/AI_All_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅 IP 段） |

想完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。文件内按厂商分段（`# OpenAI`、`# Anthropic` ……），方便查找某条规则属于谁。

## 广告 / 跟踪 / 遥测

上游自己标记的 v2fly `@ads` / `@telemetry` 条目，以及 [`config`](config) 里 `reject` 列出的域名，不会出现在 `AI_All` 里，而是写进所有分类共用的 [`Rules/Reject`](../Reject)（AI 段）。

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`openai`、`anthropic`、`xai`、`google-deepmind`、`perplexity`、`github-copilot`），去掉标记为 `@cn` 的条目 |
| 域名 | [`config/vendors.jsonc`](config/vendors.jsonc) 中手工维护的补充条目 |
| 域名 | 对照 v2fly `category-ai-!cn`、[SukkaW](https://ruleset.skk.moe/List/non_ip/ai.conf)、blackmatrix7、ACL4SSR 和社区 AI 规则（[thimper/surge-ai-rules](https://github.com/thimper/surge-ai-rules)、[imjasondai/surge-rules](https://github.com/imjasondai/surge-rules) 等）找出的遗漏；逐个核实证书 / NS / 跳转后才收录 |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各厂商自有 ASN 实际宣告的网段：OpenAI `AS401864`、Anthropic `AS399358` / `AS400243` / `AS401551`、xAI `AS400297` |
| IP | [Anthropic IP 地址文档](https://platform.claude.com/docs/en/api/ip-addresses) 中的 *Inbound* 段（出站 IP 和已停用的 IP 不收录） |

## 收录原则

- 共用的第三方服务和通用 Google / Microsoft 主机一律不收；
- 过于宽泛的后缀（如 `google.com`、`googleapis.com`、`azureedge.net`、`x.com`）会被拒绝，避免把无关流量带进去，列表见 `global_deny_suffix`。

## 构建与更新

Claude 云端定时任务每周一 **北京时间 03:00** 运行：先执行 `scripts/build.py` 重新拉取各家的域名和 IP 段，再搜索、核实新的域名，有变化就开 PR 到 `main`，合并后生效。

每次生成时会：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 跳过上游的 regexp 规则（Clash 和 Surge 无法通用）；
- **防误删**：任一厂商的数据源拉取失败，或者某个厂商的规则一次缩水超过 50%，就保留上一版 `AI_All`，并在构建输出里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

本地运行只需要 Python 3.9+ 标准库，在本目录执行：

```bash
python3 scripts/build.py
```

## 添加厂商或规则

编辑 [`config/vendors.jsonc`](config/vendors.jsonc)：

```jsonc
{
  "name": "Example",                 // 在 AI_All 里的分段名
  "description": "Example AI",
  "sources": [
    {"type": "v2fly", "list": "example"},   // v2fly 数据文件名
    {"type": "asn", "asn": 12345}           // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.ai"],
  "domain": ["api.example.com"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

改完后在本目录运行 `python3 scripts/build.py` 重新生成，把配置和生成的文件一起提交（`main` 上不会自动重新生成）。

## License

[MIT](LICENSE)
