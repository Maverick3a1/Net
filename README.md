# Net

自用的 Clash / Surge / Shadowrocket 分流规则集和 Surge 模块。

## 规则集

| 目录 | 内容 | 合集 |
| --- | --- | --- |
| [Rules/AI](Rules/AI) | 美国主流 AI 服务（OpenAI、Anthropic、xAI、Gemini、Perplexity、Copilot、Meta AI） | `AI_All` |
| [Rules/Bank](Rules/Bank) | 香港银行（发钞行、本地 / 中资 / 外资零售银行、虚拟银行）和 Wise | `Bank_All` |
| [Rules/Broker](Rules/Broker) | 互联网港美股券商（富途、老虎、长桥、盈透、嘉信等）、TradingView、券商共用 SDK / IP | `Broker_All` |
| [Rules/Crypto](Rules/Crypto) | 全球主流加密货币交易所（Binance、OKX、Coinbase 等） | `Crypto_All` |
| [Rules/Reject](Rules/Reject) | 从以上所有分类拉出来的广告 / 跟踪 / 遥测条目 | `Reject` |

每个目录下都有 `Surge/`、`Shadowrocket/`（RULE-SET / DOMAIN-SET）和 `Clash/`（classical / domain / ipcidr）三套文件，合集规则统一以 `_All` 结尾，具体规则列表和用法见各目录的 README。

各分类里的广告 / 跟踪 / 遥测条目统一放进 [`Rules/Reject`](Rules/Reject)：每个平台只有一个 `Reject` 文件（`Surge/Reject.list`、`Shadowrocket/Reject.list`、`Clash/Reject.yaml`），按分类分段，配 `REJECT`，放在各个 `_All` 前面。也可以把域名的文字或截图发给 [Telegram 机器人](bots/reject-bot)：Claude 判断后发给你确认，确认后直接写进 `Rules/Reject` 的 `Manual` 段。

Claude 云端定时任务每周一凌晨（北京时间）分别处理一个目录：Bank 02:00、Broker 02:30、AI 03:00、Crypto 03:30。每个任务先运行该目录的 `scripts/build.py` 刷新上游，再搜索并核实新的域名，有变化就开 PR 到 `main`，合并后生效。任务的提示词保存在 claude.ai 的定时任务里，不在仓库中。新增规则目录需要另建一个对应的定时任务；`Rules/Personal` 没有 `build.py`，需要手动维护。

所有上游每次构建都会重新拉取：

| 上游 | 用于 | 平台对应 |
| --- | --- | --- |
| [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) | AI、Crypto、Broker、Bank | 不分平台，三个平台共用 |
| [RIPEstat](https://stat.ripe.net/)（按 ASN 查宣告网段） | AI、Crypto、Broker、Bank | 不分平台 |
| [Anthropic IP 文档](https://platform.claude.com/docs/en/api/ip-addresses) | AI | 不分平台 |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | Crypto（`Binance`、`OKX`）、Broker（`TigerFintech`） | Surge ← Surge、Shadowrocket ← Shadowrocket、Clash ← Clash |
| [forecho/broker-rules](https://github.com/forecho/broker-rules) | Broker（`Broker`）、Bank（`Bank`） | Surge ← Surge、Shadowrocket ← Shadowrocket、Clash ← Clash |

raw 地址格式：

```
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<name>/Surge/<Name>.list
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<name>/Shadowrocket/<Name>.list
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<name>/Clash/<Name>.yaml
```

## Surge 模块

| 模块 | 导入 | 说明 |
| --- | --- | --- |
| [APNs.sgmodule](SurgeModule/APNs.sgmodule) | [导入 Surge](https://maverick3a1.github.io/Net/install.html?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaverick3a1%2FNet%2Fmain%2FSurgeModule%2FAPNs.sgmodule) | 让 Surge 接管 APNs 流量，解决部分 App 收不到推送 |
| [SpeedTest.sgmodule](SurgeModule/SpeedTest.sgmodule) | [导入 Surge](https://maverick3a1.github.io/Net/install.html?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaverick3a1%2FNet%2Fmain%2FSurgeModule%2FSpeedTest.sgmodule) | 把 Ookla Speedtest 和 Fast.com 的测速流量交给指定策略 |
| [system-dns.sgmodule](SurgeModule/system-dns.sgmodule) | [导入 Surge](https://maverick3a1.github.io/Net/install.html?url=https%3A%2F%2Fraw.githubusercontent.com%2FMaverick3a1%2FNet%2Fmain%2FSurgeModule%2Fsystem-dns.sgmodule) | 使用纯海外 DNS 解析（需当前网络能直接访问海外 DNS） |

安装地址：`https://raw.githubusercontent.com/Maverick3a1/Net/main/SurgeModule/<file>.sgmodule`
