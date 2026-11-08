# Broker

互联网港美股券商（富途、老虎、长桥、盈立、华盛、雪盈、艾德、华泰国际、复星、卓锐、Webull、盈透、嘉信、Firstrade、Robinhood）的 Clash / Surge / Shadowrocket 分流规则，另含 TradingView 和券商 App 共用的 SDK / 云服务器 IP（`BrokerShared` 段）。全部合并成一个规则集 **`Broker_All`**，一条规则全部覆盖。

## 规则文件

<!-- RULES:START -->
| 平台 | 规则文件 |
| --- | --- |
| Surge | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Broker_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Broker_All_Domain.list) |
| Shadowrocket | [RULE-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Shadowrocket/Broker_All.list) · [DOMAIN-SET](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Shadowrocket/Broker_All_Domain.list) |
| Clash / mihomo | [classical](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker_All.yaml) · [domain](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker_All_Domain.yaml) · [ipcidr](https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker_All_IP.yaml) |

`Broker_All` 共 283 条域名规则、95 个 IP 段，收录以下 17 个券商：

| 券商 | 说明 | 域名 | IP |
| --- | --- | ---: | ---: |
| Futu | 富途证券: 富途牛牛, moomoo | 55 | 0 |
| Tiger | 老虎证券: Tiger Trade, Tiger Brokers | 49 | 0 |
| Longbridge | 长桥证券: Longbridge, LongPort | 15 | 0 |
| uSMART | 盈立证券: uSMART | 24 | 0 |
| Valuable | 华盛证券: 华盛通, Valuable | 8 | 0 |
| Snowball | 雪盈证券 Snowball Securities | 4 | 0 |
| Eddid | 艾德证券: Eddid ONE | 5 | 0 |
| HuataiIntl | 华泰国际: 涨乐全球通 | 2 | 0 |
| Fosun | 复星国际证券: 复星恒利, 复星财富 | 4 | 0 |
| ZR | 卓锐证券 Sharp Point | 2 | 0 |
| Webull | 微牛 Webull | 27 | 0 |
| IBKR | 盈透证券 Interactive Brokers | 41 | 13 |
| Schwab | 嘉信理财 Charles Schwab, thinkorswim | 31 | 17 |
| Firstrade | 第一证券 Firstrade | 3 | 0 |
| Robinhood | Robinhood | 6 | 2 |
| TradingView | TradingView 图表 / 行情 | 4 | 0 |
| BrokerShared | 券商 App 共用 SDK 域名和云服务器 IP | 3 | 63 |
<!-- RULES:END -->

## 使用方法

`Reject`（广告 / 跟踪 / 遥测，见下文）配 `REJECT`，放在 `Broker_All` 前面。

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Surge/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Surge/Broker_All.list,Broker
```

### Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Shadowrocket/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Shadowrocket/Broker_All.list,Broker
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
  Broker_All:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Broker/Clash/Broker_All.yaml
    path: ./ruleset/Broker_All.yaml
    interval: 86400

rules:
  - RULE-SET,Reject,REJECT
  - RULE-SET,Broker_All,Broker
```

### 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/Broker_All.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/Broker_All_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快） |
| `Shadowrocket/Broker_All.list` | Shadowrocket `RULE-SET`（内容同 Surge 版） |
| `Shadowrocket/Broker_All_Domain.list` | Shadowrocket `DOMAIN-SET`（仅域名） |
| `Clash/Broker_All.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/Broker_All_Domain.yaml` | mihomo rule-provider，`behavior: domain`（仅域名） |
| `Clash/Broker_All_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅 IP 段） |

想完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。文件内按券商分段（`# Futu`、`# IBKR` ……），方便查找某条规则属于谁。

## 广告 / 跟踪 / 遥测

上游自己标记的 v2fly `@ads` / `@telemetry` 条目，以及 [`config`](config) 里 `reject` 列出的域名，不会出现在 `Broker_All` 里，而是写进所有分类共用的 [`Rules/Reject`](../Reject)（Broker 段）。

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`futu`、`itiger`、`longbridge`、`ibkr`、`schwab`） |
| 域名 | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)（`TigerFintech`，按平台分别取 `rule/Surge`、`rule/Shadowrocket`、`rule/Clash`） |
| 域名 | [`config/brokers.jsonc`](config/brokers.jsonc) 中手工维护的条目：都用 TLS 证书主体或券商官网前端代码核实过归属 |
| 域名 | 社区规则（[imdp6/hk-broker-rules](https://github.com/imdp6/hk-broker-rules)、[yindudegugezhanghao-lgtm/hk-brokers-rules](https://github.com/yindudegugezhanghao-lgtm/hk-brokers-rules)、[LingJingMaster/Shadowrocket-Rules](https://github.com/LingJingMaster/Shadowrocket-Rules) 等）和 [crt.sh](https://crt.sh/) 证书透明度记录里证书 O= 为该券商的域名；逐个核实证书归属 / 跳转 / 页面后才收录 |
| 域名 / IP | [forecho/broker-rules](https://github.com/forecho/broker-rules)：`Broker` 规则按平台分别取 `rule/Surge/Broker.list`、`rule/Shadowrocket/Broker.list`、`rule/Clash/Broker.yaml`，再按对方 `Source/broker/*.conf` 归到各券商（`futu.conf` → Futu、`hstong.conf` → Valuable 等）；不属于任何已对应 conf 的规则（共用 SDK、云服务器网段、对方以后新增的券商）归到 `BrokerShared`。其中的埋点域名（AppsFlyer、`play-analytics.com`、moomoo 采集入口）放进 `Reject` |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各券商自有 ASN 实际宣告的网段：盈透 `AS11449` / `AS27163` / `AS27164` / `AS40711` / `AS400227` / `AS9096` / `AS207241` / `AS212141`，嘉信 `AS1399` / `AS6949`，Robinhood `AS29981` |

中资券商和 Webull 的服务器基本都在阿里云、腾讯云、AWS 等共用云上，没有自有 ASN，无法按 ASN 收录 IP；`BrokerShared` 里的云服务器网段来自 forecho/broker-rules 的实测，难以归属单一券商，统一放在一起。

**平台一一对应**：blackmatrix7、forecho 这类按客户端分别发布文件的上游，Surge 版只取对方的 Surge 文件、Shadowrocket 版只取 Shadowrocket 文件、Clash 版只取 Clash 文件；v2fly、RIPEstat 和手工条目三个平台共用。

## 收录原则

只收这些港美股券商**自己使用**的域名，不收内地券商（以及与内地券商共用）的域名：

- 雪盈证券只收 `snowballsecurities.com`。`xueqiu.com`、`imedao.com` 是雪球 App 和内地券商 A 股交易共用的，`danjuanfunds.com` 等属于内地蛋卷基金，都不收；
- 华泰国际只收香港站 `htsc.com.hk`，不收内地华泰证券的 `htsc.com.cn`；
- 券商境内技术公司的 `.cn` 域名（如富途 `futu.cn`、老虎 `tigerbbs.cn`、长桥 `longbridge.cn`）是券商自家 App 在用的，予以保留；
- 每次生成都会和 v2fly `category-securities-cn`（内地证券公司列表）比对：命中的条目自动剔除并在构建输出里给出警告；这份黑名单拉取失败时，本次不发布任何规则；
- 停放域名、同名的其他公司、测试和内部域名一律不收；
- 过于宽泛的后缀（如 `amazonaws.com`、`myqcloud.com`、`udesk.cn`）会被拒绝，列表见 `global_deny_suffix`。

## 构建与更新

Claude 云端定时任务每周一 **北京时间 02:30** 运行：先执行 `scripts/build.py` 重新拉取各家的域名和 IP 段，再搜索、核实新的域名，有变化就开 PR 到 `main`，合并后生效。

每次生成时会：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 跳过上游的 regexp 规则（Clash 和 Surge 无法通用）；
- **防误删**：任一券商的数据源拉取失败，或者某家券商的规则一次缩水超过 50%，就保留上一版 `Broker_All`，并在构建输出里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

本地运行只需要 Python 3.9+ 标准库，在本目录执行：

```bash
python3 scripts/build.py
```

## 添加券商或规则

编辑 [`config/brokers.jsonc`](config/brokers.jsonc)：

```jsonc
{
  "name": "Example",                 // 在 Broker_All 里的分段名
  "description": "Example Securities",
  "sources": [
    {"type": "v2fly", "list": "example"},          // v2fly 数据文件名
    {"type": "blackmatrix7", "list": "Example"},   // blackmatrix7 规则名（三个平台分别拉取）
    {"type": "forecho", "list": "Broker", "conf": "example"},  // forecho Source/broker/example.conf
    {"type": "asn", "asn": 12345}                  // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.com"],
  "domain": ["api.example.net"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

改完后在本目录运行 `python3 scripts/build.py` 重新生成，把配置和生成的文件一起提交（`main` 上不会自动重新生成）。

## License

[MIT](LICENSE)
