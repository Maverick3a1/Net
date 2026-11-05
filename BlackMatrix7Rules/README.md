# BlackMatrix7Rules

按 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 的规则组织方式，自己从上游重新生成的 17 个规则集（Surge / Shadowrocket / Clash）。

**不是**复制 blackmatrix7 生成好的规则文件，而是：

- 用它各规则集 README 里公开的「数据来源」「子规则」「排除规则」和合并方式（快照存在 [`config/rulesets.json`](config/rulesets.json)）；
- 每次运行都直接从这些上游下载、解析、合并、去重，再按它的文件格式输出。

GitHub Actions（[`blackmatrix7-rules.yml`](../.github/workflows/blackmatrix7-rules.yml)）每天 **北京时间 01:00** 运行一次；`config/` 或 `scripts/` 有改动推送到 `main` 时也会立即重新生成。

## 规则列表

<!-- RULES:START -->
| Rule set | 内容 | 规则数 | Surge | Shadowrocket | Clash |
| --- | --- | ---: | --- | --- | --- |
| **Lan** | 🧸 本地局域网地址 | 154 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Surge/Lan_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Surge/Lan.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Surge/Lan_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Shadowrocket/Lan.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Shadowrocket/Lan_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Clash/Lan_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Lan/Clash/Lan_Domain.yaml) |
<!-- RULES:END -->

## 文件

每个规则集一个目录：`BlackMatrix7Rules/<名称>/<平台>/<文件>`，文件和 blackmatrix7 同名同用法。

| 平台 | 文件 | 用法 |
| --- | --- | --- |
| Surge | `<名称>_All.list` / `<名称>_All_No_Resolve.list` | Surge 5.21.0 (2952) 以上，单独用 `RULE-SET` |
| Surge | `<名称>.list` / `<名称>_Resolve.list` + `<名称>_Domain.list` | 旧版 Surge：`RULE-SET`（非域名规则）+ `DOMAIN-SET`（域名） |
| Shadowrocket | `<名称>.list` / `<名称>_Resolve.list` + `<名称>_Domain.list` | `RULE-SET` + `DOMAIN-SET` |
| Clash / mihomo | `<名称>_Classical.yaml` / `<名称>_Classical_No_Resolve.yaml` | 单独用，`behavior: classical` |
| Clash / mihomo | `<名称>.yaml` / `<名称>_No_Resolve.yaml` + `<名称>_Domain.yaml` | `classical`（非域名规则）+ `domain` |
| Clash / mihomo | `<名称>_Domain.txt`、`<名称>_Domain_For_Clash.txt`、`<名称>.list` | 文本格式（`format: text`） |
| Surge / Shadowrocket | `<名称>_MITM.sgmodule`（Shadowrocket 另有 `.conf`） | 规则里有 URL-REGEX 时，从正则推导出的 MITM 主机名，仅供参考 |

`_Resolve` / 不带 `_No_Resolve` 的版本 IP 规则不带 `no-resolve`。

和 blackmatrix7 一样：Clash 不含 URL-REGEX、USER-AGENT 和 AND / OR / NOT 规则；Shadowrocket 不含 AND / OR / NOT，IPv6 段写成 `IP-CIDR`。

## 处理方式

对每个规则集：合并它的所有数据来源和子规则 → 去掉排除规则里有的（相同，或属于排除规则里的 `DOMAIN-SUFFIX` / IP 段）→ 应用 [`config/overrides.json`](config/overrides.json) 的人工调整 → 按该规则集徽章标明的方式合并：

- 去重；
- `DOMAIN` 并入覆盖它的 `DOMAIN-SUFFIX`；`DOMAIN-SUFFIX` 并入上级 `DOMAIN-SUFFIX`；
- 标明了「DOMAIN 与 DOMAIN-KEYWORD 合并」的（如 Advertising），`DOMAIN` 并入包含它的 `DOMAIN-KEYWORD`；
- IP-CIDR(6) 合并相邻 / 重叠的网段；
- 从 URL-REGEX 推导 MITM 主机名并合并。

支持的上游格式：Surge / Quantumult X / Clash classical 规则、Clash payload（domain / ipcidr）、DOMAIN-SET、纯域名列表、hosts、AdBlock `||domain^`、sgmodule 的 `[Rule]`、m3u / URL 列表（取主机名）。

**防误删**：某个规则集一次缩水到上次的一半以下（通常是上游挂了），保留上次的文件，并在 Actions 里给出警告。单个上游下载失败时跳过它、继续生成。

## 和 blackmatrix7 的已知差异

- 不做「移除无法解析的域名」（每天几十万次 DNS 查询），所以条目会比它多一些（例如 DouYin）。
- blackmatrix7 的生成器不开源，它会丢掉一部分上游的 `DOMAIN-KEYWORD`（如过于宽泛的 `usage`、`logger`），筛选标准没有公开；这里照上游保留。
- URL-REGEX 按上游原样保留，不改写成 `https?:\/\/` 的形式。
- 少数上游（`rules.kr328.app`、`ruleset.isagood.day`）在部分网络下无法访问，访问不到的那天会少这部分（例如 LinkedIn 只有这两个来源）。

## 人工调整（编辑广告）

[`config/overrides.json`](config/overrides.json) 里按规则集写 `add`（追加）和 `remove`（删除，等于它或属于它的规则都会删掉），每条形如 `DOMAIN-SUFFIX,example.com`。目前只给 Advertising 用：通过 [Telegram 机器人](../bots/reject-bot) 选「编辑广告」并确认后写入，推送后 Actions 会立即重新生成。

## 本地运行

```bash
python3 BlackMatrix7Rules/scripts/build.py              # 全部
python3 BlackMatrix7Rules/scripts/build.py Advertising  # 只生成某几个
```
