# Bank

香港银行（发钞行、本地 / 中资 / 外资零售银行、虚拟银行）和 Wise 的 **Clash / Surge / Shadowrocket 分流规则集**。

GitHub Actions 每天 **北京时间 03:00** 自动运行：重新拉取各家的域名和 IP 段，只要有变化就提交。

## 规则列表

<!-- RULES:START -->
| Ruleset | Description | Domains | IP | Surge | Shadowrocket | Clash |
| --- | --- | ---: | ---: | --- | --- | --- |
| **HSBC** | HSBC 汇丰银行（香港） | 44 | 6 | [RULE-SET](Surge/HSBC.list) · [DOMAIN-SET](Surge/HSBC_Domain.list) | [RULE-SET](Shadowrocket/HSBC.list) · [DOMAIN-SET](Shadowrocket/HSBC_Domain.list) | [classical](Clash/HSBC.yaml) · [domain](Clash/HSBC_Domain.yaml) · [ipcidr](Clash/HSBC_IP.yaml) |
| **StandardChartered** | Standard Chartered 渣打银行（香港） | 5 | 34 | [RULE-SET](Surge/StandardChartered.list) · [DOMAIN-SET](Surge/StandardChartered_Domain.list) | [RULE-SET](Shadowrocket/StandardChartered.list) · [DOMAIN-SET](Shadowrocket/StandardChartered_Domain.list) | [classical](Clash/StandardChartered.yaml) · [domain](Clash/StandardChartered_Domain.yaml) · [ipcidr](Clash/StandardChartered_IP.yaml) |
| **BOCHK** | Bank of China (Hong Kong) 中银香港 | 2 | 1 | [RULE-SET](Surge/BOCHK.list) · [DOMAIN-SET](Surge/BOCHK_Domain.list) | [RULE-SET](Shadowrocket/BOCHK.list) · [DOMAIN-SET](Shadowrocket/BOCHK_Domain.list) | [classical](Clash/BOCHK.yaml) · [domain](Clash/BOCHK_Domain.yaml) · [ipcidr](Clash/BOCHK_IP.yaml) |
| **HangSeng** | Hang Seng Bank 恒生银行 | 2 | 0 | [RULE-SET](Surge/HangSeng.list) · [DOMAIN-SET](Surge/HangSeng_Domain.list) | [RULE-SET](Shadowrocket/HangSeng.list) · [DOMAIN-SET](Shadowrocket/HangSeng_Domain.list) | [classical](Clash/HangSeng.yaml) · [domain](Clash/HangSeng_Domain.yaml) |
| **BEA** | The Bank of East Asia 东亚银行 | 2 | 0 | [RULE-SET](Surge/BEA.list) · [DOMAIN-SET](Surge/BEA_Domain.list) | [RULE-SET](Shadowrocket/BEA.list) · [DOMAIN-SET](Shadowrocket/BEA_Domain.list) | [classical](Clash/BEA.yaml) · [domain](Clash/BEA_Domain.yaml) |
| **DBS** | DBS Bank (Hong Kong) 星展银行（香港） | 2 | 2 | [RULE-SET](Surge/DBS.list) · [DOMAIN-SET](Surge/DBS_Domain.list) | [RULE-SET](Shadowrocket/DBS.list) · [DOMAIN-SET](Shadowrocket/DBS_Domain.list) | [classical](Clash/DBS.yaml) · [domain](Clash/DBS_Domain.yaml) · [ipcidr](Clash/DBS_IP.yaml) |
| **Citibank** | Citibank (Hong Kong) 花旗银行（香港） | 2 | 6 | [RULE-SET](Surge/Citibank.list) · [DOMAIN-SET](Surge/Citibank_Domain.list) | [RULE-SET](Shadowrocket/Citibank.list) · [DOMAIN-SET](Shadowrocket/Citibank_Domain.list) | [classical](Clash/Citibank.yaml) · [domain](Clash/Citibank_Domain.yaml) · [ipcidr](Clash/Citibank_IP.yaml) |
| **DahSing** | Dah Sing Bank 大新银行 | 1 | 0 | [RULE-SET](Surge/DahSing.list) · [DOMAIN-SET](Surge/DahSing_Domain.list) | [RULE-SET](Shadowrocket/DahSing.list) · [DOMAIN-SET](Shadowrocket/DahSing_Domain.list) | [classical](Clash/DahSing.yaml) · [domain](Clash/DahSing_Domain.yaml) |
| **CNCBI** | China CITIC Bank International 中信银行（国际） | 1 | 0 | [RULE-SET](Surge/CNCBI.list) · [DOMAIN-SET](Surge/CNCBI_Domain.list) | [RULE-SET](Shadowrocket/CNCBI.list) · [DOMAIN-SET](Shadowrocket/CNCBI_Domain.list) | [classical](Clash/CNCBI.yaml) · [domain](Clash/CNCBI_Domain.yaml) |
| **CMBWingLung** | CMB Wing Lung Bank 招商永隆银行 | 2 | 0 | [RULE-SET](Surge/CMBWingLung.list) · [DOMAIN-SET](Surge/CMBWingLung_Domain.list) | [RULE-SET](Shadowrocket/CMBWingLung.list) · [DOMAIN-SET](Shadowrocket/CMBWingLung_Domain.list) | [classical](Clash/CMBWingLung.yaml) · [domain](Clash/CMBWingLung_Domain.yaml) |
| **ICBCAsia** | ICBC (Asia) 工银亚洲 | 3 | 2 | [RULE-SET](Surge/ICBCAsia.list) · [DOMAIN-SET](Surge/ICBCAsia_Domain.list) | [RULE-SET](Shadowrocket/ICBCAsia.list) · [DOMAIN-SET](Shadowrocket/ICBCAsia_Domain.list) | [classical](Clash/ICBCAsia.yaml) · [domain](Clash/ICBCAsia_Domain.yaml) · [ipcidr](Clash/ICBCAsia_IP.yaml) |
| **CCBAsia** | China Construction Bank (Asia) 建行亚洲 | 1 | 2 | [RULE-SET](Surge/CCBAsia.list) · [DOMAIN-SET](Surge/CCBAsia_Domain.list) | [RULE-SET](Shadowrocket/CCBAsia.list) · [DOMAIN-SET](Shadowrocket/CCBAsia_Domain.list) | [classical](Clash/CCBAsia.yaml) · [domain](Clash/CCBAsia_Domain.yaml) · [ipcidr](Clash/CCBAsia_IP.yaml) |
| **OCBC** | OCBC Bank (Hong Kong) 华侨银行（香港） | 2 | 1 | [RULE-SET](Surge/OCBC.list) · [DOMAIN-SET](Surge/OCBC_Domain.list) | [RULE-SET](Shadowrocket/OCBC.list) · [DOMAIN-SET](Shadowrocket/OCBC_Domain.list) | [classical](Clash/OCBC.yaml) · [domain](Clash/OCBC_Domain.yaml) · [ipcidr](Clash/OCBC_IP.yaml) |
| **Fubon** | Fubon Bank (Hong Kong) 富邦银行（香港） | 1 | 0 | [RULE-SET](Surge/Fubon.list) · [DOMAIN-SET](Surge/Fubon_Domain.list) | [RULE-SET](Shadowrocket/Fubon.list) · [DOMAIN-SET](Shadowrocket/Fubon_Domain.list) | [classical](Clash/Fubon.yaml) · [domain](Clash/Fubon_Domain.yaml) |
| **NCB** | Nanyang Commercial Bank 南洋商业银行 | 1 | 3 | [RULE-SET](Surge/NCB.list) · [DOMAIN-SET](Surge/NCB_Domain.list) | [RULE-SET](Shadowrocket/NCB.list) · [DOMAIN-SET](Shadowrocket/NCB_Domain.list) | [classical](Clash/NCB.yaml) · [domain](Clash/NCB_Domain.yaml) · [ipcidr](Clash/NCB_IP.yaml) |
| **Chiyu** | Chiyu Banking Corporation 集友银行 | 2 | 0 | [RULE-SET](Surge/Chiyu.list) · [DOMAIN-SET](Surge/Chiyu_Domain.list) | [RULE-SET](Shadowrocket/Chiyu.list) · [DOMAIN-SET](Shadowrocket/Chiyu_Domain.list) | [classical](Clash/Chiyu.yaml) · [domain](Clash/Chiyu_Domain.yaml) |
| **ShacomBank** | Shanghai Commercial Bank 上海商业银行 | 1 | 0 | [RULE-SET](Surge/ShacomBank.list) · [DOMAIN-SET](Surge/ShacomBank_Domain.list) | [RULE-SET](Shadowrocket/ShacomBank.list) · [DOMAIN-SET](Shadowrocket/ShacomBank_Domain.list) | [classical](Clash/ShacomBank.yaml) · [domain](Clash/ShacomBank_Domain.yaml) |
| **ChongHing** | Chong Hing Bank 创兴银行 | 1 | 0 | [RULE-SET](Surge/ChongHing.list) · [DOMAIN-SET](Surge/ChongHing_Domain.list) | [RULE-SET](Shadowrocket/ChongHing.list) · [DOMAIN-SET](Shadowrocket/ChongHing_Domain.list) | [classical](Clash/ChongHing.yaml) · [domain](Clash/ChongHing_Domain.yaml) |
| **BoComHK** | Bank of Communications (Hong Kong) 交通银行（香港） | 2 | 2 | [RULE-SET](Surge/BoComHK.list) · [DOMAIN-SET](Surge/BoComHK_Domain.list) | [RULE-SET](Shadowrocket/BoComHK.list) · [DOMAIN-SET](Shadowrocket/BoComHK_Domain.list) | [classical](Clash/BoComHK.yaml) · [domain](Clash/BoComHK_Domain.yaml) · [ipcidr](Clash/BoComHK_IP.yaml) |
| **ZABank** | ZA Bank 众安银行 | 3 | 0 | [RULE-SET](Surge/ZABank.list) · [DOMAIN-SET](Surge/ZABank_Domain.list) | [RULE-SET](Shadowrocket/ZABank.list) · [DOMAIN-SET](Shadowrocket/ZABank_Domain.list) | [classical](Clash/ZABank.yaml) · [domain](Clash/ZABank_Domain.yaml) |
| **Mox** | Mox Bank | 1 | 0 | [RULE-SET](Surge/Mox.list) · [DOMAIN-SET](Surge/Mox_Domain.list) | [RULE-SET](Shadowrocket/Mox.list) · [DOMAIN-SET](Shadowrocket/Mox_Domain.list) | [classical](Clash/Mox.yaml) · [domain](Clash/Mox_Domain.yaml) |
| **WeLab** | WeLab Bank 汇立银行 | 1 | 0 | [RULE-SET](Surge/WeLab.list) · [DOMAIN-SET](Surge/WeLab_Domain.list) | [RULE-SET](Shadowrocket/WeLab.list) · [DOMAIN-SET](Shadowrocket/WeLab_Domain.list) | [classical](Clash/WeLab.yaml) · [domain](Clash/WeLab_Domain.yaml) |
| **Livi** | livi bank 理慧银行 | 1 | 0 | [RULE-SET](Surge/Livi.list) · [DOMAIN-SET](Surge/Livi_Domain.list) | [RULE-SET](Shadowrocket/Livi.list) · [DOMAIN-SET](Shadowrocket/Livi_Domain.list) | [classical](Clash/Livi.yaml) · [domain](Clash/Livi_Domain.yaml) |
| **EleBank** | EleBank 大象银行（原 Airstar Bank 天星银行） | 2 | 0 | [RULE-SET](Surge/EleBank.list) · [DOMAIN-SET](Surge/EleBank_Domain.list) | [RULE-SET](Shadowrocket/EleBank.list) · [DOMAIN-SET](Shadowrocket/EleBank_Domain.list) | [classical](Clash/EleBank.yaml) · [domain](Clash/EleBank_Domain.yaml) |
| **PAOB** | Ping An OneConnect Bank 平安壹账通银行 | 2 | 0 | [RULE-SET](Surge/PAOB.list) · [DOMAIN-SET](Surge/PAOB_Domain.list) | [RULE-SET](Shadowrocket/PAOB.list) · [DOMAIN-SET](Shadowrocket/PAOB_Domain.list) | [classical](Clash/PAOB.yaml) · [domain](Clash/PAOB_Domain.yaml) |
| **Fusion** | Fusion Bank 富融银行 | 1 | 0 | [RULE-SET](Surge/Fusion.list) · [DOMAIN-SET](Surge/Fusion_Domain.list) | [RULE-SET](Shadowrocket/Fusion.list) · [DOMAIN-SET](Shadowrocket/Fusion_Domain.list) | [classical](Clash/Fusion.yaml) · [domain](Clash/Fusion_Domain.yaml) |
| **AntBank** | Ant Bank (Hong Kong) 蚂蚁银行（香港） | 1 | 0 | [RULE-SET](Surge/AntBank.list) · [DOMAIN-SET](Surge/AntBank_Domain.list) | [RULE-SET](Shadowrocket/AntBank.list) · [DOMAIN-SET](Shadowrocket/AntBank_Domain.list) | [classical](Clash/AntBank.yaml) · [domain](Clash/AntBank_Domain.yaml) |
| **Wise** | Wise（原 TransferWise） | 4 | 0 | [RULE-SET](Surge/Wise.list) · [DOMAIN-SET](Surge/Wise_Domain.list) | [RULE-SET](Shadowrocket/Wise.list) · [DOMAIN-SET](Shadowrocket/Wise_Domain.list) | [classical](Clash/Wise.yaml) · [domain](Clash/Wise_Domain.yaml) |
| **Bank_All** | All banks above combined | 93 | 59 | [RULE-SET](Surge/Bank_All.list) · [DOMAIN-SET](Surge/Bank_All_Domain.list) | [RULE-SET](Shadowrocket/Bank_All.list) · [DOMAIN-SET](Shadowrocket/Bank_All_Domain.list) | [classical](Clash/Bank_All.yaml) · [domain](Clash/Bank_All_Domain.yaml) · [ipcidr](Clash/Bank_All_IP.yaml) |
<!-- RULES:END -->

`Bank_All` 是以上所有银行（含 Wise）的合集，一条规则全部覆盖。

## 文件格式

| 文件 | 用途 |
| --- | --- |
| `Surge/<Name>.list` | Surge `RULE-SET`（域名 + `IP-CIDR,...,no-resolve`） |
| `Surge/<Name>_Domain.list` | Surge `DOMAIN-SET`（仅域名，匹配更快；不含关键字和 IP） |
| `Shadowrocket/<Name>.list` | Shadowrocket `RULE-SET`（内容同 Surge 版） |
| `Shadowrocket/<Name>_Domain.list` | Shadowrocket `DOMAIN-SET`（仅域名，不含关键字和 IP） |
| `Clash/<Name>.yaml` | Clash / mihomo rule-provider，`behavior: classical` |
| `Clash/<Name>_Domain.yaml` | mihomo rule-provider，`behavior: domain`（不含关键字和 IP） |
| `Clash/<Name>_IP.yaml` | mihomo rule-provider，`behavior: ipcidr`（仅当该银行有 IP 段时生成） |

想要完整覆盖就用 classical / RULE-SET；`_Domain` + `_IP` 组合匹配更快，但会丢掉少量 `DOMAIN-KEYWORD` 规则。

## 使用方法

### Surge

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Surge/Bank_All.list,Bank
# 或者按银行分开：
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Surge/HSBC.list,HK
# DOMAIN-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Surge/ZABank_Domain.list,HK
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Surge/Wise.list,HK
```

### Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Shadowrocket/Bank_All.list,Bank
# 也可以按银行分开：
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Shadowrocket/HSBC.list,HK
# DOMAIN-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Shadowrocket/ZABank_Domain.list,HK
# RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Shadowrocket/Wise.list,HK
```

也可以在 Shadowrocket 的「配置 → 规则 → 添加规则」中选择 `RULE-SET`，填入上面的 raw 地址。

### Clash / mihomo

```yaml
rule-providers:
  Bank_All:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Bank/Clash/Bank_All.yaml
    path: ./ruleset/Bank_All.yaml
    interval: 86400

rules:
  - RULE-SET,Bank_All,Bank
```

## 数据来源

| 类型 | 来源 |
| --- | --- |
| 域名 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)（`hsbc`、`standardchartered`、`wise`），去掉标记为 `@ads` / `@cn` 的条目，以及 `hsbc-cn` 里的内地域名 |
| 域名 | [`config/banks.jsonc`](config/banks.jsonc) 中手工维护的条目（取自各行官网首页实际引用的主机名，如 Wise 自有的 CloudFront 分发） |
| IP | [RIPEstat](https://stat.ripe.net/) 查询各行香港实体的自有 ASN 实际宣告的网段：HSBC `AS9221`、渣打 `AS24112` / `AS38166`、中银香港 `AS24396`、东亚 `AS137452`、星展香港 `AS133852`、花旗香港 `AS24568`、工银亚洲 `AS17487`、建行亚洲 `AS38475`、华侨香港 `AS4828`、南商 `AS152712`、交行香港 `AS133926`、WeLab `AS150700`、Wise `AS208550`（WeLab、Wise 目前没有宣告网段，有了会自动收录） |

注意事项：

- 中资行的母行域名（`ccb.com`、`bankcomm.com`、`icbc.com.cn` 等）是内地业务，只收录香港子域名或个别网银主机，并列入 `global_deny_suffix` 防止误收；
- 恒生中国 `hangseng.com.cn`、集友内地 `cybchina.com.cn`、汇丰中国 `hsbc.com.cn` 等内地域名不收录；
- HSBC 的 v2fly 列表包含汇丰各国站点（如 `hsbc.co.uk`），一并收录；
- 共用 CDN（支付宝 `alipayobjects.com`、Contentful `ctfassets.net` 等）不收录；
- 校验域名 / CIDR 格式，被上级后缀覆盖的条目自动去重，IP 段自动合并；
- 上游 regexp 规则 Clash 和 Surge 无法通用，所以跳过；
- **防误删**：某个数据源拉取失败，或者某个规则集一次缩水超过 50%，就保留上一版文件，并在 Actions 里给出警告；
- 只在规则内容真正变化时才重写文件，所以文件头里的 `UPDATED` 就是规则最后一次变化的时间。

## 本地运行

只依赖 Python 3.9+ 标准库：

```bash
python3 scripts/build.py
```

## 添加银行或规则

编辑 [`config/banks.jsonc`](config/banks.jsonc)：

```jsonc
{
  "name": "Example",                 // 输出文件名
  "description": "Example Bank",
  "sources": [
    {"type": "v2fly", "list": "example"},   // v2fly 数据文件名
    {"type": "asn", "asn": 12345}           // 通过 RIPEstat 查询宣告网段
  ],
  "domain_suffix": ["example.com.hk"],
  "domain": ["ebank.example.com"],
  "domain_keyword": [],
  "ip_cidr": [],
  "exclude": []                      // 要从结果中删除的条目
}
```

推送到 `main` 后会自动触发重新生成。也可以在 Actions 页面手动运行 **Update rulesets**。

## License

[MIT](LICENSE)
