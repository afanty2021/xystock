[根目录](../../CLAUDE.md) > **llm**

# llm 模块文档

## 模块职责

llm 模块负责封装和管理大语言模型（LLM）的交互，提供统一的接口供其他模块调用。支持多种AI模型服务，实现智能分析功能，并记录使用情况以便成本控制。

## 入口与启动

### 主要入口文件
- **`openai_client.py`**：OpenAI API增强封装客户端
- **`usage_logger.py`**：Token使用记录和统计
- **`__init__.py`**：模块初始化和导出

### 快速使用示例

```python
from llm.openai_client import OpenAIClient

# 初始化客户端（自动从配置读取API密钥）
client = OpenAIClient()

# 发送聊天请求
response = client.chat_completion(
    messages=[{"role": "user", "content": "分析这支股票"}],
    model="deepseek-chat",
    temperature=0.7
)
```

## 对外接口

### OpenAIClient 类

#### 核心方法

```python
class OpenAIClient:
    def __init__(self,
                 api_key: Optional[str] = None,
                 usage_logger: Optional[UsageLogger] = None)

    def chat_completion(self,
                       messages: List[Dict[str, str]],
                       model: str = None,
                       temperature: float = 0.7,
                       max_tokens: int = None,
                       stream: bool = False) -> str
    """发送聊天完成请求"""

    def async_chat_completion(self,
                             messages: List[Dict[str, str]],
                             model: str = None,
                             temperature: float = 0.7) -> str
    """异步聊天完成请求"""

    def get_model_info(self, model: str) -> Dict[str, Any]
    """获取模型信息"""

    def estimate_tokens(self, text: str) -> int
    """估算文本的token数量"""
```

#### 高级功能

```python
# 带重试机制的请求
client.chat_completion_with_retry(
    messages,
    max_retries=3,
    backoff_factor=2
)

# 流式响应
for chunk in client.stream_completion(messages):
    print(chunk, end='')

# 批量处理
responses = client.batch_completion(
    message_list,
    max_concurrent=5
)
```

### UsageLogger 类

```python
class UsageLogger:
    def log_request(self,
                    model: str,
                    prompt_tokens: int,
                    completion_tokens: int,
                    cost: float)
    """记录API使用情况"""

    def get_daily_usage(self, date: str) -> Dict[str, Any]
    """获取指定日期的使用统计"""

    def get_model_usage(self, model: str) -> Dict[str, Any]
    """获取指定模型的使用统计"""

    def export_usage_report(self,
                           start_date: str,
                           end_date: str) -> pd.DataFrame
    """导出使用报告"""
```

## 关键依赖与配置

### 外部依赖
- **openai**: OpenAI官方Python SDK
- **tiktoken**: Token计算工具
- **pandas**: 数据处理
- **loguru**: 日志记录

### 配置管理

```toml
[LLM_OPENAI]
API_KEY = "sk-xxx"
BASE_URL = ""  # 可选，用于兼容其他服务
TIMEOUT = 60
MAX_RETRIES = 3

[LLM_LOGGING]
USAGE_LOG_FILE = "logs/openai_usage.csv"
ENABLE_LOGGING = true
LOG_LEVEL = "INFO"

[LLM_CACHE]
ENABLE_CACHE = false
CACHE_TTL = 3600
```

### 支持的模型

#### OpenAI 官方模型
- `gpt-4o`: 最新的GPT-4模型
- `gpt-4o-mini`: 轻量版GPT-4
- `gpt-3.5-turbo`: 经典GPT-3.5

#### DeepSeek 系列
- `deepseek-chat`: 通用对话模型
- `deepseek-reasoner`: 推理专用模型

#### 阿里百炼系列
- `qwen-plus`: 平衡性能和成本
- `qwen-max`: 最高性能
- `qwen-turbo`: 快速响应

## 数据模型

### APIRequest 请求记录
```python
@dataclass
class APIRequest:
    timestamp: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    response_time: float
    success: bool
``### ModelConfig 模型配置
```python
@dataclass
class ModelConfig:
    model_id: str
    max_tokens: int
    temperature_range: Tuple[float, float]
    cost_per_1k_tokens: Dict[str, float]  # prompt/completion
    supports_streaming: bool
    supports_functions: bool
```

## 测试与质量

### 测试覆盖
- ✅ API连接测试
- ✅ Token计算测试
- ✅ 错误处理测试
- ⏳ 性能压力测试待实施

### 质量保证
1. **重试机制**：自动处理网络错误和API限流
2. **超时控制**：防止长时间等待
3. **日志记录**：完整的请求和响应日志
4. **成本监控**：实时跟踪API使用成本

## 使用最佳实践

### 1. 成本优化
```python
# 选择合适的模型
model = "deepseek-chat"  # 经济实用
model = "deepseek-reasoner"  # 复杂分析

# 控制输出长度
response = client.chat_completion(
    messages,
    max_tokens=1000  # 限制输出长度
)

# 使用缓存（如果启用）
client.chat_completion_cached(messages, ttl=3600)
```

### 2. 错误处理
```python
try:
    response = client.chat_completion(messages)
except OpenAIError as e:
    logger.error(f"API请求失败: {e}")
    # 使用备用方案或返回默认结果
```

### 3. 异步处理
```python
import asyncio

async def analyze_stocks(stock_list):
    tasks = [
        client.async_chat_completion(messages)
        for messages in stock_list
    ]
    results = await asyncio.gather(*tasks)
    return results
```

## 常见问题

### Q: 如何切换不同的模型提供商？
A: 修改配置文件中的 `BASE_URL` 和 `API_KEY`，系统会自动适配。

### Q: 如何控制API调用成本？
A: 使用 `UsageLogger` 监控使用情况，选择合适的模型，限制输出长度。

### Q: 如何处理大文本输入？
A: 使用文本分块处理，或选择支持长上下文的模型（如 `qwen-max-longcontext`）。

### Q: 如何实现自定义的prompt模板？
A: 在其他模块（如 `stock/analysis_prompts.py`）中定义，通过参数传递给LLM客户端。

## 相关文件清单

```
llm/
├── __init__.py          # 模块导出
├── openai_client.py     # OpenAI客户端封装
└── usage_logger.py      # 使用统计记录
```

## 变更记录

### 2025-12-07 22:48:54
- ✨ 创建模块文档
- 📝 定义LLM接口和使用规范
- 💡 提供成本优化建议

---

*该模块是整个系统AI能力的核心，建议定期检查API使用情况和成本。*