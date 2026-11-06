# Net

自用的 Clash / Surge / Shadowrocket 分流规则集和 Surge 模块。

## 规则集

### 分类合集

每个分类只发布一个合集规则集（`<分类>_All`），各厂商在文件里分段，不再单独发布。

| 目录 | 内容 | 规则集 |
| --- | --- | --- |
| [Rules/AI](Rules/AI) | 美国主流 AI 服务（OpenAI、Anthropic、xAI、Gemini、Perplexity、Copilot、Meta AI） | `AI_All` |
| [Rules/Bank](Rules/Bank) | 香港银行（发钞行、本地 / 中资 / 外资零售银行、虚拟银行）和 Wise | `Bank_All` |
| [Rules/Broker](Rules/Broker) | 互联网港美股券商（富途、老虎、长桥、盈透、嘉信等）、TradingView、券商共用 SDK / IP | `Broker_All` |
| [Rules/Crypto](Rules/Crypto) | 全球主流加密货币交易所（Binance、OKX、Coinbase 等） | `Crypto_All` |
| [Rules/Reject](Rules/Reject) | 从以上各分类拉出来的广告 / 跟踪 / 遥测条目 | `Reject` |

每个目录下都有三套文件：`Surge/`、`Shadowrocket/`（RULE-SET / DOMAIN-SET）和 `Clash/`（classical / domain / ipcidr）。具体用法见各目录的 README。

### BlackMatrix7Rules

[BlackMatrix7Rules](BlackMatrix7Rules)：按 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) 的规则组织方式，从上游自行生成的 17 个规则集（Advertising、Lan、Global、Google、Apple、Microsoft 等），由 GitHub Actions 每天北京时间 01:00 更新。

## 使用方法

raw 地址格式：

```
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<分类>/Surge/<分类>_All.list
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<分类>/Shadowrocket/<分类>_All.list
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<分类>/Clash/<分类>_All.yaml
```

规则顺序：`Reject` 配 `REJECT`，放在所有 `_All` 前面。`Reject` 每个平台只有一个文件（`Surge/Reject.list`、`Shadowrocket/Reject.list`、`Clash/Reject.yaml`），按分类分段。

## 更新方式

| 目录 | 方式 | 时间（北京时间） |
| --- | --- | --- |
| Rules/Bank | Claude 云端定时任务 | 每周一 02:00 |
| Rules/Broker | Claude 云端定时任务 | 每周一 02:30 |
| Rules/AI | Claude 云端定时任务 | 每周一 03:00 |
| Rules/Crypto | Claude 云端定时任务 | 每周一 03:30 |
| Rules/Reject | 随各分类构建更新；`Manual` 段由 Telegram 机器人写入 | — |
| Rules/Personal | 手动维护（没有 `build.py`） | — |
| BlackMatrix7Rules | GitHub Actions | 每天 01:00 |

每个定时任务先运行该目录的 `scripts/build.py` 刷新上游，再搜索并核实新的域名，有变化就开 PR 到 `main`，合并后生效。任务的提示词保存在 claude.ai 的定时任务里，不在仓库中；新增规则目录需要另建一个对应的定时任务。

### 上游

所有上游每次构建都会重新拉取：

| 上游 | 用于 | 平台对应 |
| --- | --- | --- |
| [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) | AI、Crypto、Broker、Bank | 不分平台，三个平台共用 |
| [RIPEstat](https://stat.ripe.net/)（按 ASN 查宣告网段） | AI、Crypto、Broker、Bank | 不分平台 |
| [Anthropic IP 文档](https://platform.claude.com/docs/en/api/ip-addresses) | AI | 不分平台 |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | Crypto（`Binance`、`OKX`）、Broker（`TigerFintech`） | Surge ← Surge、Shadowrocket ← Shadowrocket、Clash ← Clash |
| [forecho/broker-rules](https://github.com/forecho/broker-rules) | Broker（`Broker`）、Bank（`Bank`） | Surge ← Surge、Shadowrocket ← Shadowrocket、Clash ← Clash |

### Telegram 机器人

把域名的文字或截图发给 [Telegram 机器人](bots/reject-bot)：Claude 会建议每个域名加到 `Rules/Reject` 还是某个分类的条目（如 `AI` 里的 `OpenAI` 段），也可以编辑 BlackMatrix7Rules 的广告列表。你点按钮确认后直接写入 `main`。

## Surge 模块

| 模块 | 导入 | 说明 |
| --- | --- | --- |
| [APNs.sgmodule](SurgeModule/APNs.sgmodule) | [导入 Surge](https://maverick3a1.github.io/Net/install.html?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaverick3a1%2FNet%2Fmain%2FSurgeModule%2FAPNs.sgmodule) | 让 Surge 接管 APNs 流量，解决部分 App 收不到推送 |
| [SpeedTest.sgmodule](SurgeModule/SpeedTest.sgmodule) | [导入 Surge](https://maverick3a1.github.io/Net/install.html?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaverick3a1%2FNet%2Fmain%2FSurgeModule%2FSpeedTest.sgmodule) | 把 Ookla Speedtest 和 Fast.com 的测速流量交给指定策略 |
| [system-dns.sgmodule](SurgeModule/system-dns.sgmodule) | [导入 Surge](https://maverick3a1.github.io/Net/install.html?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaverick3a1%2FNet%2Fmain%2FSurgeModule%2Fsystem-dns.sgmodule) | 使用纯海外 DNS 解析（需当前网络能直接访问海外 DNS） |

安装地址：`https://raw.githubusercontent.com/Maverick3a1/Net/main/SurgeModule/<file>.sgmodule`
