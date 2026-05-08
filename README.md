# Digital Oracle MCP Server

基于 [digital-oracle](https://github.com/komako-workshop/digital-oracle) 项目封装的 MCP Server，将金融市场价格数据封装为 13 个 MCP Tools。

## 功能特性

- **13 个 MCP Tools**：覆盖预测市场、股票、期权、国债、加密货币、机构持仓等数据源
- **零依赖**：12/14 个 Provider 只需 Python 标准库
- **并行获取**：支持多数据源并行查询 (`gather`)
- **stdio + SSE 双模式**：本地使用 stdio，云端部署 SSE

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

### 本地使用 (stdio 模式)

```bash
pip install digital-oracle-mcp
digital-oracle-mcp
```

或使用 uvx：

```bash
uvx digital-oracle-mcp
```

### Docker 部署 (SSE 模式)

```bash
docker build -t digital-oracle-mcp .
docker run -p 8800:8800 digital-oracle-mcp
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `EDGAR_USER_EMAIL` | SEC EDGAR API User-Agent（内部人交易查询必需） | `1255897343@qq.com` |

## 使用示例

### MCP 客户端配置

#### 通义灵码 / Claude Code / Cursor

```json
{
  "mcpServers": {
    "digital-oracle": {
      "command": "uvx",
      "args": ["digital-oracle-mcp"],
      "env": {
        "EDGAR_USER_EMAIL": "1255897343@qq.com"
      }
    }
  }
}
```

#### SSE 模式（魔搭托管）

```json
{
  "mcpServers": {
    "digital-oracle": {
      "type": "sse",
      "url": "https://modelscope.cn/api/v1/mcp/servers/{用户名}/digital-oracle/sse",
      "headers": {
        "Authorization": "Bearer {MODELSCOPE_API_TOKEN}"
      }
    }
  }
}
```

### Docker + SSE

```json
{
  "mcp": {
    "servers": {
      "digital-oracle": {
        "url": "http://localhost:8800/sse",
        "trust": "trusted"
      }
    }
  }
}
```

## 云端部署

### 魔搭 MCP 广场（推荐）

1. 发布到 PyPI（包已包含 `[project.scripts]` 入口点）
2. 访问 https://modelscope.cn/mcp/servers/create?template=customize
3. 填写信息并选择"可托管部署"

### Smithery.ai

1. 代码推到 GitHub
2. 访问 https://smithery.ai 用 GitHub 登录
3. 点击 "Deploy New Server"，选择仓库

## 依赖

- Python >= 3.10
- fastmcp >= 2.0
- yfinance（仅期权链和价格历史需要）

```bash
uv pip install yfinance
```

## License

MIT © komako-workshop
