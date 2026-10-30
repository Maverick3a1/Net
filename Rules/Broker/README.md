# Broker

互联网港美股券商（富途、老虎、长桥、盈立、华盛、雪盈、艾德、华泰国际、Webull、盈透、嘉信、Firstrade、Robinhood）的 **Clash / Surge 分流规则集**。

GitHub Actions 每天 **北京时间 03:00** 自动运行：重新拉取各家的域名和 IP 段，只要有变化就提交。

## 规则列表

<!-- RULES:START -->
| Ruleset | Description | Domains | IP | Surge | Clash |
| --- | --- | ---: | ---: | --- | --- |
| **Futu** | 富途证券: 富途牛牛, moomoo | 26 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Futu.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Futu_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Futu.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Futu_Domain.yaml) |
| **Tiger** | 老虎证券: Tiger Trade, Tiger Brokers | 20 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Tiger.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Tiger_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Tiger.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Tiger_Domain.yaml) |
| **Longbridge** | 长桥证券: Longbridge, LongPort | 12 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Longbridge.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Longbridge_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Longbridge.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Longbridge_Domain.yaml) |
| **uSMART** | 盈立证券: uSMART | 23 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/uSMART.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/uSMART_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/uSMART.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/uSMART_Domain.yaml) |
| **Valuable** | 华盛证券: 华盛通, Valuable | 3 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Valuable.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Valuable_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Valuable.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Valuable_Domain.yaml) |
| **Snowball** | 雪盈证券 Snowball Securities | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Snowball.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Snowball_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Snowball.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Snowball_Domain.yaml) |
| **Eddid** | 艾德证券: Eddid ONE | 5 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Eddid.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Eddid_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Eddid.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Eddid_Domain.yaml) |
| **HuataiIntl** | 华泰国际: 涨乐全球通 | 1 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/HuataiIntl.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/HuataiIntl_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/HuataiIntl.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/HuataiIntl_Domain.yaml) |
| **Webull** | 微牛 Webull | 26 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Webull.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Webull_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Webull.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Webull_Domain.yaml) |
| **IBKR** | 盈透证券 Interactive Brokers | 21 | 13 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/IBKR.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/IBKR_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/IBKR.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/IBKR_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/IBKR_IP.yaml) |
| **Schwab** | 嘉信理财 Charles Schwab, thinkorswim | 9 | 17 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Schwab.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Schwab_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Schwab.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Schwab_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Schwab_IP.yaml) |
| **Firstrade** | 第一证券 Firstrade | 3 | 0 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Firstrade.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Firstrade_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Firstrade.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Firstrade_Domain.yaml) |
| **Robinhood** | Robinhood | 4 | 2 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Robinhood.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Robinhood_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Robinhood.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Robinhood_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Robinhood_IP.yaml) |
| **Broker** | All brokers above combined | 154 | 32 | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Broker.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Broker_Domain.list) | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker_IP.yaml) |
<!-- RULES:END -->

`Broker` 是以上所有券商的合集，一条规则全部覆盖。

## 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/<Name>.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/<Name>_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快；不含关键字和 IP） |
| `Clash/<Name>.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/<Name>_Domain.yaml` | mihomo rule-provider，`behavior: domain`（不含关键字和 IP） |
| `Clash/<Name>_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅当该券商有 IP 段时生成） |

想要完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。

## 使用方法

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Broker.list,Broker
# 或者按券商分开：
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Futu.list,HK
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/IBKR.list,US
# DOMAIN-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Webull_Domain.list,US
```

### Clash / mihomo

```yaml
rule-providers:
  Broker:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker.yaml
    path: ./ruleset/Broker.yaml
    interval: 86400

rules:
  - RULE-SET,Broker,Broker
```

## 收录原则

只收录这些港美股券商**自己使用**的域名，不收内地券商（以及与内地券商共用）的域名：

- 雪盈证券只收 `snowballsecurities.com`。`xueqiu.com`、`imedao.com` 是雪球 App 和内地券商 A 股交易共用的，`danjuanfunds.com` 等属于内地蛋卷基金，都不收录；
- 华泰国际只收香港站 `htsc.com.hk`，不收内地华泰证券的 `htsc.com.cn`；
- 券商境内技术公司的 `.cn` 域名（如富途 `futu.cn`、老虎 `tigerbbs.cn`、长桥 `longbridge.cn`）是券商自家 App 在用的，予以保留；
- 每次生成都会和 v2fly `category-securities-cn`（内地证券公司列表）比对：命中的条目自动剔除并在 Actions 里给出警告；这份黑名单拉取失败时，本次不发布任何规则。

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`futu`、`itiger`、`longbridge`、`ibkr`、`schwab`），去掉标记为 `@ads` 的条目 |
| 域名 | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)（`TigerFintech`） |
| 域名 | [`config/brokers.jsonc`](config/brokers.jsonc) 中手工维护的条目：都用 TLS 证书主体或券商官网前端代码核实过归属 |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各券商自有 ASN 实际宣告的网段：盈透 `AS11449` / `AS27163` / `AS27164` / `AS40711` / `AS400227` / `AS9096` / `AS207241` / `AS212141`，嘉信 `AS1399` / `AS6949`，Robinhood `AS29981` |

> 中资券商和 Webull 的服务器基本都在阿里云、腾讯云、AWS 等共用云上，没有自有 ASN，所以不收录 IP。

每次生成时还会做这些处理：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 过于宽泛的后缀（如 `amazonaws.com`、`myqcloud.com`、`udesk.cn`）会被拒绝，避免把无关流量带进去，列表见 `global_deny_suffix`；
- 上游 regexp 规则 Clash 和 Surge 无法通用，所以跳过；
- **防误删**：某个数据源拉取失败，或者某个规则集一次缩水超过 50%，就保留上一版文件，并在 Actions 里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

## 本地运行

只依赖 Python 3.9+ 标准库：

```bash
python3 scripts/build.py
```

## 添加券商或规则

编辑 [`config/brokers.jsonc`](config/brokers.jsonc)：

```jsonc
{
  "name": "Example",                 // 输出文件名
  "description": "Example Securities",
  "sources": [
    {"type": "v2fly", "list": "example"},          // v2fly 数据文件名
    {"type": "blackmatrix7", "list": "Example"},   // blackmatrix7 Surge 规则名
    {"type": "asn", "asn": 12345}                  // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.com"],
  "domain": ["api.example.net"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

推送到 `main` 后会自动触发重新生成。也可以在 Actions 页面手动运行 **Update rulesets**。

## License

[MIT](LICENSE)
