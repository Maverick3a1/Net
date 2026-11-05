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
| **Advertising** | 🧸 去广告 | 305300 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Surge/Advertising_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Surge/Advertising.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Surge/Advertising_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Shadowrocket/Advertising.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Shadowrocket/Advertising_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Clash/Advertising_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Advertising/Clash/Advertising_Domain.yaml) |
| **PayPal** | 🧸 PayPal | 247 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Surge/PayPal_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Surge/PayPal.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Surge/PayPal_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Shadowrocket/PayPal.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Shadowrocket/PayPal_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Clash/PayPal_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/PayPal/Clash/PayPal_Domain.yaml) |
| **LinkedIn** | 🧸 LinkedIn | 12 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Surge/LinkedIn_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Surge/LinkedIn.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Surge/LinkedIn_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Shadowrocket/LinkedIn.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Shadowrocket/LinkedIn_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Clash/LinkedIn_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/LinkedIn/Clash/LinkedIn_Domain.yaml) |
| **WeChat** | 🧸 微信 | 343 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Surge/WeChat_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Surge/WeChat.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Surge/WeChat_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Shadowrocket/WeChat.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Shadowrocket/WeChat_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Clash/WeChat_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/WeChat/Clash/WeChat_Domain.yaml) |
| **DouYin** | 🧸 抖音 | 46 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Surge/DouYin_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Surge/DouYin.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Surge/DouYin_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Shadowrocket/DouYin.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Shadowrocket/DouYin_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Clash/DouYin_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/DouYin/Clash/DouYin_Domain.yaml) |
| **TikTok** | 🧸 TikTok | 39 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Surge/TikTok_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Surge/TikTok.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Surge/TikTok_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Shadowrocket/TikTok.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Shadowrocket/TikTok_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Clash/TikTok_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/TikTok/Clash/TikTok_Domain.yaml) |
| **Spotify** | 🧸 Spotify | 25 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Surge/Spotify_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Surge/Spotify.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Surge/Spotify_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Shadowrocket/Spotify.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Shadowrocket/Spotify_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Clash/Spotify_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Spotify/Clash/Spotify_Domain.yaml) |
| **YouTube** | 🧸 YouTube | 186 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Surge/YouTube_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Surge/YouTube.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Surge/YouTube_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Shadowrocket/YouTube.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Shadowrocket/YouTube_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Clash/YouTube_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/YouTube/Clash/YouTube_Domain.yaml) |
| **Reddit** | 🧸 Reddit | 8 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Surge/Reddit_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Surge/Reddit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Surge/Reddit_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Shadowrocket/Reddit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Shadowrocket/Reddit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Clash/Reddit_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Reddit/Clash/Reddit_Domain.yaml) |
| **Google** | 🧸 Google | 692 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Surge/Google_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Surge/Google.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Surge/Google_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Shadowrocket/Google.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Shadowrocket/Google_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Clash/Google_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Google/Clash/Google_Domain.yaml) |
| **Apple** | 🧸 Apple | 1621 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Surge/Apple_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Surge/Apple.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Surge/Apple_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Shadowrocket/Apple.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Shadowrocket/Apple_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Clash/Apple_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Apple/Clash/Apple_Domain.yaml) |
| **Microsoft** | 🧸 Microsoft | 712 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Surge/Microsoft_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Surge/Microsoft.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Surge/Microsoft_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Shadowrocket/Microsoft.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Shadowrocket/Microsoft_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Clash/Microsoft_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Microsoft/Clash/Microsoft_Domain.yaml) |
| **Xbox** | 🧸 Xbox | 38 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Surge/Xbox_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Surge/Xbox.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Surge/Xbox_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Shadowrocket/Xbox.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Shadowrocket/Xbox_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Clash/Xbox_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Xbox/Clash/Xbox_Domain.yaml) |
| **SteamCN** | 🧸 SteamCN | 16 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Surge/SteamCN_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Surge/SteamCN.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Surge/SteamCN_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Shadowrocket/SteamCN.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Shadowrocket/SteamCN_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Clash/SteamCN_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/SteamCN/Clash/SteamCN_Domain.yaml) |
| **Steam** | 🧸 Steam | 67 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Surge/Steam_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Surge/Steam.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Surge/Steam_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Shadowrocket/Steam.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Shadowrocket/Steam_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Clash/Steam_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Steam/Clash/Steam_Domain.yaml) |
| **Global** | 🧸 Global | 29024 | [All](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Surge/Global_All.list) · [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Surge/Global.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Surge/Global_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Shadowrocket/Global.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Shadowrocket/Global_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Clash/Global_Classical.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules/Global/Clash/Global_Domain.yaml) |
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

支持的上游格式：Surge / Quantumult X / Clash classical 规则、Clash payload（domain / ipcidr）、DOMAIN-SET、纯域名列表、hosts、AdBlock `||domain^`、sgmodule 的 `[Rule]`、m3u / URL 列表（取主机名），以及 `v2fly:<列表名>`（v2fly/domain-list-community，跟随 `include:`）。

**防误删**：某个规则集一次缩水到上次的一半以下（通常是上游挂了），保留上次的文件，并在 Actions 里给出警告。单个上游下载失败时跳过它、继续生成。

## 和 blackmatrix7 的已知差异

- 不做「移除无法解析的域名」（每天几十万次 DNS 查询），所以条目会比它多一些（例如 DouYin）。
- blackmatrix7 的生成器不开源，它会丢掉一部分上游的 `DOMAIN-KEYWORD`（如过于宽泛的 `usage`、`logger`），筛选标准没有公开；这里照上游保留。
- URL-REGEX 按上游原样保留，不改写成 `https?:\/\/` 的形式。
- `rules.kr328.app` 已经停止解析（2026-11-05 起在 GitHub Actions 上也解析不到），依赖它的 22 个来源都缺了，主要影响 Global 排除的国内规则；`ruleset.isagood.day` 在部分网络下也访问不到。
- LinkedIn 原本只有两个 `rules.kr328.app` 来源，已换成 v2fly 的 `linkedin` 列表（`config/rulesets.json` 里写作 `v2fly:linkedin`，原来源记在 `replaced`）。

## 与 blackmatrix7 的差异日志

每次全量生成后，会下载 blackmatrix7 当前发布的 Surge 规则（有 `_All.list` 用它，否则用 `<名称>.list`），和刚生成的结果逐条比较，写进 [`logs/<日期>.md`](logs)（同一天多次运行覆盖当天的文件，只保留最近 30 天）：

- 每个规则集的总数、相同条数、只有一方有的条数；
- 「其中未被覆盖」：对方连更宽的规则（上级 DOMAIN-SUFFIX、包含在域名里的 DOMAIN-KEYWORD、包含它的 IP 段）都没有的，也就是真正的行为差异；
- 每个规则集按类型的条数对比，以及双方各自未被覆盖的规则（最多列 30 条）；
- 本次没能下载的上游，以及 blackmatrix7 那边规则的更新时间。

## 人工调整（编辑广告）

[`config/overrides.json`](config/overrides.json) 里按规则集写 `add`（追加）和 `remove`（删除，等于它或属于它的规则都会删掉），每条形如 `DOMAIN-SUFFIX,example.com`。目前只给 Advertising 用：通过 [Telegram 机器人](../bots/reject-bot) 选「编辑广告」并确认后写入，推送后 Actions 会立即重新生成。

## 本地运行

```bash
python3 BlackMatrix7Rules/scripts/build.py              # 全部
python3 BlackMatrix7Rules/scripts/build.py Advertising  # 只生成某几个
```
