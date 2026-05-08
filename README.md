# Digital Oracle MCP Server

基于 [digital-oracle](https://github.com/komako-workshop/digital-oracle) 项目封装的 MCP Server，提供 14 个金融市场价格数据工具。

## 14 个 MCP Tools

| Tool | 说明 |
|------|------|
| `get_polymarket_events` | Polymarket 预测市场事件 |
| `get_kalshi_markets` | Kalshi 监管二元合约 |
| `get_price_history` | Yahoo Finance 价格历史 |
| `get_yield_curve` | 美国国债收益率曲线 |
| `get_cftc_positions` | CFTC 期货机构持仓 |
| `get_crypto_prices` | CoinGecko 加密货币价格 |
| `get_insider_trades` | SEC 内部人交易 (Form 4) |
| `get_policy_rates` | BIS 央行政策利率 |
| `get_futures_curve` | Deribit 加密期货期限结构 |
| `get_fear_greed_index` | CNN 恐惧贪婪指数 |
| `get_fed_rate_probs` | CME FedWatch 美联储利率概率 |
| `get_options_chain` | Yahoo Finance 期权链 |
| `web_search` | 网页搜索 |
| `multi_signal_query` | 多数据源并行查询 |

## 安装

```bash
pip install digital-oracle-mcp
```

## 使用方式

### 本地 stdio 模式（Claude Code / Cursor）

```bash
digital-oracle-mcp
```

或：

```bash
uvx digital-oracle-mcp
```

### Claude Code / Cursor 配置

```json
{
  "mcpServers": {
    "digital-oracle": {
      "command": "uvx",
      "args": ["digital-oracle-mcp"],
      "env": {
        "EDGAR_USER_EMAIL": "your_email@example.com"
      }
    }
  }
}
```

## 云端部署

### Smithery.ai

1. 访问 https://smithery.ai
2. GitHub 登录
3. 搜索 `mzxsuperman/digital-oracle-mcp`
4. 点击部署

Smithery 会通过 `smithery.yaml` 自动识别并部署。

### 魔搭 ModelScope

访问 https://modelscope.cn/mcp/servers/create?template=customize
- 选择 "可托管部署"
- 填写包名：`digital-oracle-mcp`
- 或使用 GitHub 仓库地址

## 环境变量

| 变量 | 说明 |
|------|------|
| `EDGAR_USER_EMAIL` | SEC EDGAR API User-Agent（查询内部人交易时需要，可使用任意邮箱） |

## 依赖

- Python >= 3.10
- fastmcp >= 2.0

## License

MIT © komako-workshop
