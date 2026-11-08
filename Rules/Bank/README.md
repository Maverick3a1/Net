# Bank

香港银行（发钞行、本地 / 中资 / 外资零售银行、虚拟银行）和 Wise 的 Clash / Surge / Shadowrocket 分流规则。所有银行合并成一个规则集 **`Bank_All`**，一条规则全部覆盖。

## 规则文件

<!-- RULES:START -->
| 平台 | 规则文件 |
| --- | --- |
| Surge | [RULE-SET](Surge/Bank_All.list) · [DOMAIN-SET](Surge/Bank_All_Domain.list) |
| Shadowrocket | [RULE-SET](Shadowrocket/Bank_All.list) · [DOMAIN-SET](Shadowrocket/Bank_All_Domain.list) |
| Clash / mihomo | [classical](Clash/Bank_All.yaml) · [domain](Clash/Bank_All_Domain.yaml) · [ipcidr](Clash/Bank_All_IP.yaml) |

`Bank_All` 共 126 条域名规则、59 个 IP 段，收录以下 29 个银行：

| 银行 | 说明 | 域名 | IP |
| --- | --- | ---: | ---: |
| HSBC | HSBC 汇丰银行（香港） | 53 | 6 |
| StandardChartered | Standard Chartered 渣打银行（香港） | 5 | 34 |
| BOCHK | Bank of China (Hong Kong) 中银香港 | 7 | 1 |
| HangSeng | Hang Seng Bank 恒生银行 | 2 | 0 |
| BEA | The Bank of East Asia 东亚银行 | 3 | 0 |
| DBS | DBS Bank (Hong Kong) 星展银行（香港） | 2 | 2 |
| Citibank | Citibank (Hong Kong) 花旗银行（香港） | 2 | 6 |
| DahSing | Dah Sing Bank 大新银行 | 2 | 0 |
| CNCBI | China CITIC Bank International 中信银行（国际） | 3 | 0 |
| CMBWingLung | CMB Wing Lung Bank 招商永隆银行 | 2 | 0 |
| ICBCAsia | ICBC (Asia) 工银亚洲 | 5 | 2 |
| CCBAsia | China Construction Bank (Asia) 建行亚洲 | 3 | 2 |
| OCBC | OCBC Bank (Hong Kong) 华侨银行（香港） | 2 | 1 |
| Fubon | Fubon Bank (Hong Kong) 富邦银行（香港） | 2 | 0 |
| NCB | Nanyang Commercial Bank 南洋商业银行 | 2 | 3 |
| Chiyu | Chiyu Banking Corporation 集友银行 | 2 | 0 |
| ShacomBank | Shanghai Commercial Bank 上海商业银行 | 2 | 0 |
| ChongHing | Chong Hing Bank 创兴银行 | 1 | 0 |
| BoComHK | Bank of Communications (Hong Kong) 交通银行（香港） | 2 | 2 |
| ZABank | ZA Bank 众安银行 | 6 | 0 |
| Mox | Mox Bank | 2 | 0 |
| WeLab | WeLab Bank 汇立银行 | 1 | 0 |
| Livi | livi bank 理慧银行 | 2 | 0 |
| EleBank | EleBank 大象银行（原 Airstar Bank 天星银行） | 2 | 0 |
| PAOB | Ping An OneConnect Bank 平安壹账通银行 | 2 | 0 |
| Fusion | Fusion Bank 富融银行 | 1 | 0 |
| AntBank | Ant Bank (Hong Kong) 蚂蚁银行（香港） | 2 | 0 |
| Wise | Wise（原 TransferWise） | 5 | 0 |
| BankShared | 银行 App 共用的第三方服务（风控 / 反欺诈 / 应用加固 / 客服 SDK） | 1 | 0 |
<!-- RULES:END -->

## 使用方法

`Reject`（广告 / 跟踪 / 遥测，见下文）配 `REJECT`，放在 `Bank_All` 前面。

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Surge/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Surge/Bank_All.list,Bank
```

### Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Shadowrocket/Reject.list,REJECT
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Shadowrocket/Bank_All.list,Bank
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
  Bank_All:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Clash/Bank_All.yaml
    path: ./ruleset/Bank_All.yaml
    interval: 86400

rules:
  - RULE-SET,Reject,REJECT
  - RULE-SET,Bank_All,Bank
```

### 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/Bank_All.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/Bank_All_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快） |
| `Shadowrocket/Bank_All.list` | Shadowrocket `RULE-SET`（内容同 Surge 版） |
| `Shadowrocket/Bank_All_Domain.list` | Shadowrocket `DOMAIN-SET`（仅域名） |
| `Clash/Bank_All.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/Bank_All_Domain.yaml` | mihomo rule-provider，`behavior: domain`（仅域名） |
| `Clash/Bank_All_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅 IP 段） |

想完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。文件内按银行分段（`# HSBC`、`# ZABank` ……），方便查找某条规则属于谁。

## 广告 / 跟踪 / 遥测

上游自己标记的 v2fly `@ads` / `@telemetry` 条目，以及 [`config`](config) 里 `reject` 列出的域名，不会出现在 `Bank_All` 里，而是写进所有分类共用的 [`Rules/Reject`](../Reject)（Bank 段）。

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`hsbc`、`standardchartered`、`wise`），去掉标记为 `@cn` 的条目，以及 `hsbc-cn` 里的内地域名 |
| 域名 | [`config/banks.jsonc`](config/banks.jsonc) 中手工维护的条目（取自各行官网首页实际引用的主机名，如 Wise 自有的 CloudFront 分发） |
| 域名 | 社区规则（[klchai/personal-rule](https://github.com/klchai/personal-rule)、[gz4zzxc/rule](https://github.com/gz4zzxc/rule)、[LeventLei/shadowrocket-rules](https://github.com/LeventLei/shadowrocket-rules) 等）和 [crt.sh](https://crt.sh/) 证书透明度记录里证书 O= 为该银行的域名；逐个核实证书归属 / 跳转后才收录 |
| 域名 | [forecho/broker-rules](https://github.com/forecho/broker-rules)：`Bank` 规则按平台分别取 `rule/Surge/Bank.list`、`rule/Shadowrocket/Bank.list`、`rule/Clash/Bank.yaml`，再按对方 `Source/bank/*.conf` 归到 HSBC、众安、大象、Wise；其中的埋点 / 统计域名放进 `Reject` |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各行香港实体的自有 ASN 实际宣告的网段：HSBC `AS9221`、渣打 `AS24112` / `AS38166`、中银香港 `AS24396`、东亚 `AS137452`、星展香港 `AS133852`、花旗香港 `AS24568`、工银亚洲 `AS17487`、建行亚洲 `AS38475`、华侨香港 `AS4828`、南商 `AS152712`、交行香港 `AS133926`、WeLab `AS150700`、Wise `AS208550`（WeLab、Wise 目前没有宣告网段，有了会自动收录） |

**平台一一对应**：forecho 这类按客户端分别发布文件的上游，Surge 版只取对方的 Surge 文件、Shadowrocket 版只取 Shadowrocket 文件、Clash 版只取 Clash 文件；v2fly、RIPEstat 和手工条目三个平台共用。

## 收录原则

- 停放域名、同名的其他公司、内地业务、证券 / 保险子公司一律不收；
- 中资行的母行域名（`ccb.com`、`bankcomm.com`、`icbc.com.cn` 等）是内地业务，只收香港子域名或个别网银主机，并列入 `global_deny_suffix` 防止误收；
- 恒生中国 `hangseng.com.cn`、集友内地 `cybchina.com.cn`、汇丰中国 `hsbc.com.cn` 等内地域名不收；
- HSBC 的 v2fly 列表包含汇丰各国站点（如 `hsbc.co.uk`），一并收录；
- forecho 银行规则里 App 依赖的第三方 SDK：埋点 / 统计类（AppsFlyer、Firebase `crashlytics.com` / `app-measurement.com`、Mixpanel、Tealium、Lytics、Optimizely、AppDynamics）放进 `Reject`；风控 / 客服类（ThreatMetrix `online-metrix.net`、BioCatch `we-stats.com`、AWS WAF、LivePerson）银行会核对它们的出口 IP，保留在 `Bank_All`。forecho 规则里出现没对应到任何银行的 conf 时，构建输出会给出警告；
- 共用 CDN（支付宝 `alipayobjects.com`、Contentful `ctfassets.net` 等）不收。

## 构建与更新

Claude 云端定时任务每周一 **北京时间 02:00** 运行：先执行 `scripts/build.py` 重新拉取各家的域名和 IP 段，再搜索、核实新的域名，有变化就开 PR 到 `main`，合并后生效。

每次生成时会：

- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 跳过上游的 regexp 规则（Clash 和 Surge 无法通用）；
- **防误删**：任一银行的数据源拉取失败，或者某家银行的规则一次缩水超过 50%，就保留上一版 `Bank_All`，并在构建输出里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

本地运行只需要 Python 3.9+ 标准库，在本目录执行：

```bash
python3 scripts/build.py
```

## 添加银行或规则

编辑 [`config/banks.jsonc`](config/banks.jsonc)：

```jsonc
{
  "name": "Example",                 // 在 Bank_All 里的分段名
  "description": "Example Bank",
  "sources": [
    {"type": "v2fly", "list": "example"},   // v2fly 数据文件名
    {"type": "forecho", "list": "Bank", "conf": "example"},  // forecho Source/bank/example.conf
    {"type": "asn", "asn": 12345}           // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.com.hk"],
  "domain": ["ebank.example.com"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

改完后在本目录运行 `python3 scripts/build.py` 重新生成，把配置和生成的文件一起提交（`main` 上不会自动重新生成）。

## License

[MIT](LICENSE)
