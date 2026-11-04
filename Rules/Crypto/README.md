# Crypto

全球主流加密货币交易所（Binance、OKX、Bybit、Coinbase、Bitget、Upbit、Gate、MEXC、HTX、KuCoin、Kraken、Crypto.com、Bithumb、BingX、Bitfinex、Bitstamp、Gemini、bitFlyer、Deribit、Hyperliquid）的 **Clash / Surge / Shadowrocket 分流规则集**。

Claude 云端定时任务每周一 **北京时间 03:30** 自动运行：重新拉取各交易所的域名和 IP 段，再搜索、核实新的域名，有变化就开 PR 到 `main`，合并后生效。

## 规则列表

<!-- RULES:START -->
| Ruleset | Description | Domains | IP | Surge | Shadowrocket | Clash |
| --- | --- | ---: | ---: | --- | --- | --- |
| **Binance** | Binance, Binance.US, BNB Chain | 47 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Binance.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Binance_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Binance.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Binance_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Binance.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Binance_Domain.yaml) |
| **OKX** | OKX (formerly OKEx), OKX Wallet, X Layer | 10 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/OKX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/OKX_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/OKX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/OKX_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/OKX.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/OKX_Domain.yaml) |
| **Bybit** | Bybit | 21 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bybit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bybit_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bybit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bybit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bybit.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bybit_Domain.yaml) |
| **Coinbase** | Coinbase, Coinbase Advanced, Base App (Coinbase Wallet) | 4 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Coinbase.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Coinbase_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Coinbase.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Coinbase_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Coinbase.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Coinbase_Domain.yaml) |
| **Bitget** | Bitget | 6 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitget.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitget_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bitget.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bitget_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitget.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitget_Domain.yaml) |
| **Upbit** | Upbit (Dunamu) | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Upbit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Upbit_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Upbit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Upbit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Upbit.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Upbit_Domain.yaml) |
| **Gate** | Gate (Gate.com, Gate.io) | 11 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gate.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gate_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Gate.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Gate_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gate.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gate_Domain.yaml) |
| **MEXC** | MEXC | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/MEXC.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/MEXC_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/MEXC.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/MEXC_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/MEXC.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/MEXC_Domain.yaml) |
| **HTX** | HTX (formerly Huobi) | 10 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/HTX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/HTX_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/HTX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/HTX_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/HTX.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/HTX_Domain.yaml) |
| **KuCoin** | KuCoin, KuCoin TH, KuCoin TR | 7 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/KuCoin.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/KuCoin_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/KuCoin.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/KuCoin_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/KuCoin.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/KuCoin_Domain.yaml) |
| **Kraken** | Kraken, Kraken Pro | 5 | 3 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Kraken.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Kraken_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Kraken.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Kraken_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Kraken.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Kraken_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Kraken_IP.yaml) |
| **CryptoCom** | Crypto.com App and Exchange | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/CryptoCom.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/CryptoCom_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/CryptoCom.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/CryptoCom_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/CryptoCom.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/CryptoCom_Domain.yaml) |
| **Bithumb** | Bithumb | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bithumb.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bithumb_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bithumb.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bithumb_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bithumb.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bithumb_Domain.yaml) |
| **BingX** | BingX (formerly Bingbon) | 3 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/BingX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/BingX_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/BingX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/BingX_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/BingX.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/BingX_Domain.yaml) |
| **Bitfinex** | Bitfinex | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitfinex.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitfinex_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bitfinex.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bitfinex_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitfinex.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitfinex_Domain.yaml) |
| **Bitstamp** | Bitstamp | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitstamp.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitstamp_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bitstamp.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Bitstamp_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitstamp.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitstamp_Domain.yaml) |
| **Gemini** | Gemini Exchange (not Google Gemini) | 1 | 2 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gemini.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gemini_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Gemini.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Gemini_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gemini.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gemini_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gemini_IP.yaml) |
| **bitFlyer** | bitFlyer | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/bitFlyer.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/bitFlyer_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/bitFlyer.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/bitFlyer_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/bitFlyer.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/bitFlyer_Domain.yaml) |
| **Deribit** | Deribit | 2 | 5 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Deribit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Deribit_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Deribit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Deribit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Deribit.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Deribit_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Deribit_IP.yaml) |
| **Hyperliquid** | Hyperliquid | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Hyperliquid.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Hyperliquid_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Hyperliquid.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Hyperliquid_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Hyperliquid.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Hyperliquid_Domain.yaml) |
| **Crypto_All** | All exchanges above combined | 140 | 10 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_All_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_All_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All_IP.yaml) |
| **Crypto_Reject** | Ads, tracking and telemetry from the exchange rules above | 4 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_Reject.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_Reject_Domain.list) | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_Reject.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_Reject_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_Reject.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_Reject_Domain.yaml) |
<!-- RULES:END -->

`Crypto_All` 是以上所有交易所的合集，一条规则全部覆盖。

`Crypto_Reject` 是从以上规则里拉出来的**广告 / 跟踪 / 遥测**条目：上游自己标记的（v2fly `@ads` / `@telemetry`），以及 [`config`](config) 里 `reject` 列出的域名。这些条目只出现在 `Crypto_Reject` 里，不再出现在各自的规则和 `Crypto_All` 里。`Crypto_Reject` 配 `REJECT`，放在 `Crypto_All` 前面。

## 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/<Name>.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/<Name>_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快；不含关键字和 IP） |
| `Shadowrocket/<Name>.list` | Shadowrocket `RULE-SET`（内容同 Surge 版） |
| `Shadowrocket/<Name>_Domain.list` | Shadowrocket `DOMAIN-SET`（仅域名，不含关键字和 IP） |
| `Clash/<Name>.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/<Name>_Domain.yaml` | mihomo rule-provider，`behavior: domain`（不含关键字和 IP） |
| `Clash/<Name>_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅当该交易所有 IP 段时生成） |

想要完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。

## 使用方法

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_All.list,Crypto
# 或者按交易所分开：
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Binance.list,JP
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/OKX.list,SG
# DOMAIN-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Coinbase_Domain.list,US
```

### Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_All.list,Crypto
# 也可以按交易所分开：
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Binance.list,JP
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/OKX.list,SG
# DOMAIN-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Coinbase_Domain.list,US
```

也可以在 Shadowrocket 的「配置 → 规则 → 添加规则」中选择 `RULE-SET`，填入上面的 raw 地址。

### Clash / mihomo

```yaml
rule-providers:
  Crypto_Reject:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_Reject.yaml
    path: ./ruleset/Crypto_Reject.yaml
    interval: 86400
  Crypto_All:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All.yaml
    path: ./ruleset/Crypto_All.yaml
    interval: 86400

rules:
  - RULE-SET,Crypto_Reject,REJECT
  - RULE-SET,Crypto_All,Crypto
```

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`binance`、`okx`、`bybit`、`gateio`、`huobi`、`kucoin`、`kraken`、`bitflyer`、`deribit`），去掉标记为 `@cn` 的条目；标记为 `@ads` / `@telemetry` 的放进 `Crypto_Reject` |
| 域名 | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)（`Binance`、`OKX`，按平台分别取 `rule/Surge`、`rule/Shadowrocket`、`rule/Clash`） |
| 域名 | [`config/exchanges.jsonc`](config/exchanges.jsonc) 中手工维护的条目（v2fly 没有单独列表的交易所，以及从官网实际引用的资源域名中补充的 CDN / 区域站） |
| 域名 | 对照 v2fly `category-cryptocurrency`、blackmatrix7、ACL4SSR、GeQ1an 和社区规则（[smllbboomm/Crypto-Rules](https://github.com/smllbboomm/Crypto-Rules)、[lyq3/proxy-rules](https://github.com/lyq3/proxy-rules) 等），以及 [crt.sh](https://crt.sh/) 证书透明度记录找出的遗漏；逐个核实证书 / 跳转 / 页面后才收录，停放或出售的同名域名、区块浏览器等第三方服务一律不收 |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各交易所自有 ASN 实际宣告的网段：Kraken (Payward) `AS1072`、Gemini `AS6651` / `AS50363` / `AS203107`、Upbit (Dunamu) `AS10154`、Deribit `AS207856` |

其余交易所主要托管在 AWS / Cloudflare / 阿里云等共用网段上，收录 IP 会误伤其他流量，所以只用域名匹配。

每次生成时还会做这些处理：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 过于宽泛的后缀（如 `amazonaws.com`、`cloudflare.net`、`github.io`、`onelink.me`）会被拒绝，避免把无关流量带进去，列表见 `global_deny_suffix`；
- **平台一一对应**：blackmatrix7 按客户端分别发布文件，Surge 版只取对方的 Surge 文件、Shadowrocket 版只取对方的 Shadowrocket 文件、Clash 版只取对方的 Clash 文件；v2fly、RIPEstat 和手工条目不分平台，三个平台共用；
- 上游 regexp 规则 Clash 和 Surge 无法通用，所以跳过；
- **防误删**：某个数据源拉取失败，或者某个规则集一次缩水超过 50%，就保留上一版文件，并在构建输出里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

## 本地运行

只依赖 Python 3.9+ 标准库：

```bash
python3 scripts/build.py
```

## 添加交易所或规则

编辑 [`config/exchanges.jsonc`](config/exchanges.jsonc)：

```jsonc
{
  "name": "Example",                 // 输出文件名
  "description": "Example Exchange",
  "sources": [
    {"type": "v2fly", "list": "example"},   // v2fly 数据文件名
    {"type": "blackmatrix7", "list": "Example"},  // blackmatrix7 规则名（三个平台分别拉取）
    {"type": "asn", "asn": 12345}           // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.com"],
  "domain": ["api.example.io"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

改完配置后，在本目录运行 `python3 scripts/build.py` 重新生成，再把配置和生成的文件一起提交（`main` 上不会自动重新生成）。

## License

[MIT](LICENSE)
