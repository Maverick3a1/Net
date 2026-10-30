# Net

自用的 Clash / Surge 分流规则集和 Surge 模块。

## 规则集

| 目录 | 内容 | 合集规则 |
| --- | --- | --- |
| [Rules/AI](Rules/AI) | 美国主流 AI 服务（OpenAI、Anthropic、xAI、Gemini、Perplexity、Copilot、Meta AI） | `AI` |
| [Rules/Bank](Rules/Bank) | 香港银行（发钞行、本地 / 中资 / 外资零售银行、虚拟银行）和 Wise | `Bank` |
| [Rules/Broker](Rules/Broker) | 互联网港美股券商（富途、老虎、长桥、盈透、嘉信等） | `Broker` |
| [Rules/Crypto](Rules/Crypto) | 全球主流加密货币交易所（Binance、OKX、Coinbase 等） | `Crypto` |

每个目录下都有 `Surge/`（RULE-SET / DOMAIN-SET）和 `Clash/`（classical / domain / ipcidr）两套文件，具体规则列表和用法见各目录的 README。

GitHub Actions（[`update-rulesets.yml`](.github/workflows/update-rulesets.yml)）每天 **北京时间 03:00** 依次运行每个 `Rules/<name>/scripts/build.py`，规则有变化才提交；某个目录构建失败不影响其他目录。新增规则目录只要放好 `scripts/build.py`，就会自动纳入。

raw 地址格式：

```
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<name>/Surge/<Name>.list
https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/<name>/Clash/<Name>.yaml
```

## Surge 模块

| 模块 | 说明 |
| --- | --- |
| [APNs.sgmodule](SurgeModule/APNs.sgmodule) | 让 Surge 接管 APNs 流量，解决部分 App 收不到推送 |
| [SpeedTest.sgmodule](SurgeModule/SpeedTest.sgmodule) | 把 Ookla Speedtest 和 Fast.com 的测速流量交给指定策略 |
| [system-dns.sgmodule](SurgeModule/system-dns.sgmodule) | 使用纯海外 DNS 解析（需当前网络能直接访问海外 DNS） |

安装地址：`https://raw.githubusercontent.com/Maverick3a1/Net/main/SurgeModule/<file>.sgmodule`
