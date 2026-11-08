# Crypto

全球主流加密货币交易所（Binance、OKX、Bybit、Coinbase、Bitget、Upbit、Gate、MEXC、HTX、KuCoin、Kraken、Crypto.com、Bithumb、BingX、Bitfinex、Bitstamp、Gemini、bitFlyer、Deribit、Hyperliquid）的 Clash / Surge / Shadowrocket 分流规则。所有交易所合并成一个规则集 **`Crypto_All`**，一条规则全部覆盖。

## 规则文件

<!-- RULES:START -->
| 平台 | 规则文件 |
| --- | --- |
| Surge | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_All_Domain.list) |
| Shadowrocket | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_All_Domain.list) |
| Clash / mihomo | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All_IP.yaml) |

`Crypto_All` 共 154 条域名规则、10 个 IP 段，收录以下 20 个交易所：

| 交易所 | 说明 | 域名 | IP |
| --- | --- | ---: | ---: |
| Binance | Binance, Binance.US, BNB Chain | 49 | 0 |
| OKX | OKX (formerly OKEx), OKX Wallet, X Layer | 11 | 0 |
| Bybit | Bybit | 23 | 0 |
| Coinbase | Coinbase, Coinbase Advanced, Base App (Coinbase Wallet) | 4 | 0 |
| Bitget | Bitget | 8 | 0 |
| Upbit | Upbit (Dunamu) | 2 | 0 |
| Gate | Gate (Gate.com, Gate.io) | 13 | 0 |
| MEXC | MEXC | 3 | 0 |
| HTX | HTX (formerly Huobi) | 10 | 0 |
| KuCoin | KuCoin, KuCoin TH, KuCoin TR | 8 | 0 |
| Kraken | Kraken, Kraken Pro | 7 | 3 |
| CryptoCom | Crypto.com App and Exchange | 1 | 0 |
| Bithumb | Bithumb | 2 | 0 |
| BingX | BingX (formerly Bingbon) | 3 | 0 |
| Bitfinex | Bitfinex | 1 | 0 |
| Bitstamp | Bitstamp | 2 | 0 |
| Gemini | Gemini Exchange (not Google Gemini) | 1 | 2 |
| bitFlyer | bitFlyer | 2 | 0 |
| Deribit | Deribit | 2 | 5 |
| Hyperliquid | Hyperliquid | 2 | 0 |
<!-- RULES:END -->

## 使用方法

`Reject`（广告 / 跟踪 / 遥测，见下文）配 `REJECT`，放在 `Crypto_All` 前面。

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Surge/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Surge/Crypto_All.list,Crypto
```

### Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Shadowrocket/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Shadowrocket/Crypto_All.list,Crypto
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
  Crypto_All:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Crypto/Clash/Crypto_All.yaml
    path: ./ruleset/Crypto_All.yaml
    interval: 86400

rules:
  - RULE-SET,Reject,REJECT
  - RULE-SET,Crypto_All,Crypto
```

### 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/Crypto_All.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/Crypto_All_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快） |
| `Shadowrocket/Crypto_All.list` | Shadowrocket `RULE-SET`（内容同 Surge 版） |
| `Shadowrocket/Crypto_All_Domain.list` | Shadowrocket `DOMAIN-SET`（仅域名） |
| `Clash/Crypto_All.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/Crypto_All_Domain.yaml` | mihomo rule-provider，`behavior: domain`（仅域名） |
| `Clash/Crypto_All_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅 IP 段） |

想完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。文件内按交易所分段（`# Binance`、`# OKX` ……），方便查找某条规则属于谁。

## 广告 / 跟踪 / 遥测

上游自己标记的 v2fly `@ads` / `@telemetry` 条目，以及 [`config`](config) 里 `reject` 列出的域名，不会出现在 `Crypto_All` 里，而是写进所有分类共用的 [`Rules/Reject`](../Reject)（Crypto 段）。

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`binance`、`okx`、`bybit`、`gateio`、`huobi`、`kucoin`、`kraken`、`bitflyer`、`deribit`），去掉标记为 `@cn` 的条目 |
| 域名 | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)（`Binance`、`OKX`，按平台分别取 `rule/Surge`、`rule/Shadowrocket`、`rule/Clash`） |
| 域名 | [`config/exchanges.jsonc`](config/exchanges.jsonc) 中手工维护的条目（v2fly 没有单独列表的交易所，以及从官网实际引用的资源域名中补充的 CDN / 区域站） |
| 域名 | 对照 v2fly `category-cryptocurrency`、blackmatrix7、ACL4SSR、GeQ1an 和社区规则（[smllbboomm/Crypto-Rules](https://github.com/smllbboomm/Crypto-Rules)、[lyq3/proxy-rules](https://github.com/lyq3/proxy-rules) 等），以及 [crt.sh](https://crt.sh/) 证书透明度记录找出的遗漏；逐个核实证书 / 跳转 / 页面后才收录 |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各交易所自有 ASN 实际宣告的网段：Kraken (Payward) `AS1072`、Gemini `AS6651` / `AS50363` / `AS203107`、Upbit (Dunamu) `AS10154`、Deribit `AS207856` |

其余交易所主要托管在 AWS / Cloudflare / 阿里云等共用网段上，收录 IP 会误伤其他流量，所以只用域名匹配。

**平台一一对应**：blackmatrix7 按客户端分别发布文件，Surge 版只取对方的 Surge 文件、Shadowrocket 版只取 Shadowrocket 文件、Clash 版只取 Clash 文件；v2fly、RIPEstat 和手工条目三个平台共用。

## 收录原则

- 停放或出售的同名域名、区块浏览器等第三方服务一律不收；
- 过于宽泛的后缀（如 `amazonaws.com`、`cloudflare.net`、`github.io`、`onelink.me`）会被拒绝，避免把无关流量带进去，列表见 `global_deny_suffix`。

## 构建与更新

Claude 云端定时任务每周一 **北京时间 03:30** 运行：先执行 `scripts/build.py` 重新拉取各交易所的域名和 IP 段，再搜索、核实新的域名，有变化就开 PR 到 `main`，合并后生效。

每次生成时会：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 跳过上游的 regexp 规则（Clash 和 Surge 无法通用）；
- **防误删**：任一交易所的数据源拉取失败，或者某个交易所的规则一次缩水超过 50%，就保留上一版 `Crypto_All`，并在构建输出里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

本地运行只需要 Python 3.9+ 标准库，在本目录执行：

```bash
python3 scripts/build.py
```

## 添加交易所或规则

编辑 [`config/exchanges.jsonc`](config/exchanges.jsonc)：

```jsonc
{
  "name": "Example",                 // 在 Crypto_All 里的分段名
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

改完后在本目录运行 `python3 scripts/build.py` 重新生成，把配置和生成的文件一起提交（`main` 上不会自动重新生成）。

## License

[MIT](LICENSE)
