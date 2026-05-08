# Digital Oracle MCP Server

基于 [digital-oracle](https://github.com/komako-workshop/digital-oracle) 项目封装的 MCP Server，将金融市场价格数据封装为 14 个 MCP Tools。

## 数据源

| Provider | 数据类型 | 用途 |
|----------|---------|------|
| PolymarketProvider | 预测市场合约 | 地缘政治、经济事件概率定价 |
| KalshiProvider | 二元合约 | 美国监管事件市场 |
| YahooPriceProvider | 价格历史 | 股票/ETF/外汇/商品 |
| USTreasuryProvider | 国债收益率 | 利率曲线、通胀预期 |
| CftcCotProvider | 期货持仓 | 机构仓位方向 (smart money) |
| CoinGeckoProvider | 加密现货 | BTC/ETH 价格、市值 |
| EdgarProvider | SEC 内部人交易 | Form 4 买卖信号 |
| BisProvider | 央行数据 | 政策利率、信贷/GDP 缺口 |
| DeribitProvider | 加密衍生品 | 期货期限结构、期权 IV |
| FearGreedProvider | 市场情绪 | CNN 恐惧贪婪指数 |
| CMEFedWatchProvider | 利率概率 | FOMC 会议市场定价 |
| YFinanceProvider | 期权链 | IV、Greeks、put/call ratio |
| WebSearchProvider | 网页搜索 | VIX、CDS 等补充数据 |

## MCP Tools

| Tool | 说明 |
|------|------|
| `get_polymarket_events` | 查询 Polymarket 预测市场事件 |
| `get_kalshi_markets` | 查询 Kalshi 监管二元合约 |
| `get_price_history` | 查询 Yahoo Finance 价格历史 |
| `get_yield_curve` | 查询美国国债收益率曲线 |
| `get_cftc_positions` | 查询 CFTC 期货机构持仓 |
| `get_crypto_prices` | 查询 CoinGecko 加密货币价格 |
| `get_insider_trades` | 查询 SEC 内部人交易 (Form 4) |
| `get_policy_rates` | 查询 BIS 央行政策利率 |
| `get_futures_curve` | 查询 Deribit 加密期货期限结构 |
| `get_fear_greed_index` | 查询 CNN 恐惧贪婪指数 |
| `get_fed_rate_probs` | 查询 CME FedWatch 美联储利率概率 |
| `get_options_chain` | 查询 Yahoo Finance 期权链 |
| `web_search` | 网页搜索补充数据 |
| `multi_signal_query` | 并行获取多数据源交叉验证 |

## 安装

```bash
pip install digital-oracle-mcp
```

或使用 uvx：

```bash
uvx digital-oracle-mcp
```

## MCP 客户端配置

### Claude Code / Cursor

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

### 通用 stdio 配置

```json
{
  "mcpServers": {
    "digital-oracle": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "EDGAR_USER_EMAIL": "your_email@example.com"
      }
    }
  }
}
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `EDGAR_USER_EMAIL` | SEC EDGAR API User-Agent（查询内部人交易时必需，可使用任意邮箱） |

## 依赖

- Python >= 3.10
- fastmcp >= 2.0

## License

MIT © komako-workshop
