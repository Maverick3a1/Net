# Rules4Crypto

全球主流加密货币交易所（Binance、OKX、Bybit、Coinbase、Bitget、Upbit、Gate、MEXC、HTX、KuCoin、Kraken、Crypto.com、Bithumb、BingX、Bitfinex、Bitstamp、Gemini、bitFlyer、Deribit、Hyperliquid）的 **Clash / Surge 分流规则集**。

GitHub Actions 每天 **北京时间 03:00** 自动运行：重新拉取各交易所的域名和 IP 段，只要有变化就提交。

## 规则列表

<!-- RULES:START -->
| Ruleset | Description | Domains | IP | Surge | Clash |
| --- | --- | ---: | ---: | --- | --- |
| **Binance** | Binance, Binance.US, BNB Chain | 45 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Binance.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Binance_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Binance.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Binance_Domain.yaml) |
| **OKX** | OKX (formerly OKEx), OKX Wallet, X Layer | 9 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/OKX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/OKX_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/OKX.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/OKX_Domain.yaml) |
| **Bybit** | Bybit | 16 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bybit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bybit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bybit.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bybit_Domain.yaml) |
| **Coinbase** | Coinbase, Coinbase Advanced, Coinbase Wallet | 3 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Coinbase.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Coinbase_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Coinbase.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Coinbase_Domain.yaml) |
| **Bitget** | Bitget | 6 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitget.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitget_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitget.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitget_Domain.yaml) |
| **Upbit** | Upbit (Dunamu) | 2 | 1 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Upbit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Upbit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Upbit.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Upbit_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Upbit_IP.yaml) |
| **Gate** | Gate (Gate.com, Gate.io) | 8 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gate.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gate_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gate.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gate_Domain.yaml) |
| **MEXC** | MEXC | 3 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/MEXC.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/MEXC_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/MEXC.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/MEXC_Domain.yaml) |
| **HTX** | HTX (formerly Huobi) | 10 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/HTX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/HTX_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/HTX.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/HTX_Domain.yaml) |
| **KuCoin** | KuCoin, KuCoin TH, KuCoin TR | 7 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/KuCoin.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/KuCoin_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/KuCoin.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/KuCoin_Domain.yaml) |
| **Kraken** | Kraken, Kraken Pro | 4 | 3 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Kraken.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Kraken_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Kraken.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Kraken_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Kraken_IP.yaml) |
| **CryptoCom** | Crypto.com App and Exchange | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/CryptoCom.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/CryptoCom_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/CryptoCom.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/CryptoCom_Domain.yaml) |
| **Bithumb** | Bithumb | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bithumb.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bithumb_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bithumb.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bithumb_Domain.yaml) |
| **BingX** | BingX (formerly Bingbon) | 3 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/BingX.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/BingX_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/BingX.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/BingX_Domain.yaml) |
| **Bitfinex** | Bitfinex | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitfinex.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitfinex_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitfinex.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitfinex_Domain.yaml) |
| **Bitstamp** | Bitstamp | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitstamp.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Bitstamp_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitstamp.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Bitstamp_Domain.yaml) |
| **Gemini** | Gemini Exchange (not Google Gemini) | 1 | 2 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gemini.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Gemini_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gemini.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gemini_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Gemini_IP.yaml) |
| **bitFlyer** | bitFlyer | 2 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/bitFlyer.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/bitFlyer_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/bitFlyer.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/bitFlyer_Domain.yaml) |
| **Deribit** | Deribit | 2 | 5 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Deribit.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Deribit_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Deribit.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Deribit_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Deribit_IP.yaml) |
| **Hyperliquid** | Hyperliquid | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Hyperliquid.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Hyperliquid_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Hyperliquid.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Hyperliquid_Domain.yaml) |
| **Crypto** | All exchanges above combined | 128 | 11 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_IP.yaml) |
<!-- RULES:END -->

`Crypto` 是以上所有交易所的合集，一条规则全部覆盖。

## 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/<Name>.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/<Name>_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快；不含关键字和 IP） |
| `Clash/<Name>.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/<Name>_Domain.yaml` | mihomo rule-provider，`behavior: domain`（不含关键字和 IP） |
| `Clash/<Name>_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅当该交易所有 IP 段时生成） |

想要完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。

## 使用方法

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto.list,Crypto
# 或者按交易所分开：
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Binance.list,JP
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/OKX.list,SG
# DOMAIN-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Coinbase_Domain.list,US
```

### Clash / mihomo

```yaml
rule-providers:
  Crypto:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto.yaml
    path: ./ruleset/Crypto.yaml
    interval: 86400

rules:
  - RULE-SET,Crypto,Crypto
```

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`binance`、`okx`、`bybit`、`gateio`、`huobi`、`kucoin`、`kraken`、`bitflyer`、`deribit`），去掉标记为 `@ads` / `@cn` 的条目 |
| 域名 | [`config/exchanges.jsonc`](config/exchanges.jsonc) 中手工维护的条目（v2fly 没有单独列表的交易所，以及从官网实际引用的资源域名中补充的 CDN / 区域站） |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各交易所自有 ASN 实际宣告的网段：Kraken (Payward) `AS1072`、Gemini `AS6651` / `AS50363` / `AS203107`、Upbit (Dunamu) `AS10154`、Deribit `AS207856` |

其余交易所主要托管在 AWS / Cloudflare / 阿里云等共用网段上，收录 IP 会误伤其他流量，所以只用域名匹配。

每次生成时还会做这些处理：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 过于宽泛的后缀（如 `amazonaws.com`、`cloudflare.net`、`github.io`、`onelink.me`）会被拒绝，避免把无关流量带进去，列表见 `global_deny_suffix`；
- 上游 regexp 规则 Clash 和 Surge 无法通用，所以跳过；
- **防误删**：某个数据源拉取失败，或者某个规则集一次缩水超过 50%，就保留上一版文件，并在 Actions 里给出警告；
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
    {"type": "asn", "asn": 12345}           // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.com"],
  "domain": ["api.example.io"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

推送到 `main` 后会自动触发重新生成。也可以在 Actions 页面手动运行 **Update rulesets**。

## License

[MIT](LICENSE)
