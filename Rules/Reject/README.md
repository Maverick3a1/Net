# Reject

从 [AI](../AI)、[Bank](../Bank)、[Broker](../Broker)、[Crypto](../Crypto) 各分类规则里拉出来的**广告 / 跟踪 / 遥测**条目，合并成一个拒绝列表，每个平台一个文件：

| 平台 | 文件 | 格式 |
| --- | --- | --- |
| Surge | [`Surge/Reject.list`](Surge/Reject.list) | `RULE-SET` |
| Shadowrocket | [`Shadowrocket/Reject.list`](Shadowrocket/Reject.list) | `RULE-SET` |
| Clash / mihomo | [`Clash/Reject.yaml`](Clash/Reject.yaml) | rule-provider，`behavior: classical` |

文件按分类分段（`# AI / OpenAI`、`# Bank / HSBC` ……）。条目来源：上游自己标记的（v2fly `@ads` / `@telemetry`），以及各分类 `config` 里 `reject` 列出的域名。这些条目不会再出现在各分类自己的规则和 `_All` 合集里。

## 使用方法

`Reject` 配 `REJECT`，放在各个 `_All` 前面。

### Surge / Shadowrocket

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/Maverick3a1/Net/main/Rules/Reject/Surge/Reject.list,REJECT
```

Shadowrocket 把路径里的 `Surge` 换成 `Shadowrocket`。

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

rules:
  - RULE-SET,Reject,REJECT
```

## 生成方式

这里的文件不要手动编辑。每个分类的 `scripts/build.py` 运行时，会调用 [`scripts/reject.py`](scripts/reject.py) 只替换自己那一段，其他分类的段落保持不变，所以各分类可以单独构建。要加拒绝条目，改对应分类 `config` 里的 `reject`，再运行该分类的 `build.py`。
