# 随身AI伙伴 - 使用说明书

## 一、产品简介

随身AI伙伴是一个"比Siri更聪明、比ChatGPT更懂你"的AI智能助手，具备记忆能力、情感陪伴和智能提醒功能。

## 二、快速开始

### 1. 环境要求

- Python 3.8+
- Windows / macOS / Linux

### 2. 安装步骤

```bash
# 克隆项目
git clone https://github.com/shawnbxyxiaobai-hub/ai-companion.git
cd ai-companion/backend

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置

```bash
# 复制配置示例文件
cp .env.example .env

# 编辑 .env 文件（可选）
# 目前默认使用模拟回复，如需接入真实LLM请配置相应API密钥
```

### 4. 启动服务

```bash
# 启动后端服务
python -m app.main

# 或使用uvicorn
uvicorn app.main:app --reload
```

### 5. 访问

- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 三、API使用指南

### 1. 对话接口

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "你好"}'
```

响应：
```json
{
  "reply": "你好呀！今天过得怎么样？😊",
  "emotion": "neutral"
}
```

### 2. 创建用户

```bash
curl -X POST "http://localhost:8000/api/user/user123?name=张三"
```

### 3. 获取记忆

```bash
curl "http://localhost:8000/api/memory/user123"
```

### 4. 添加记忆

```bash
curl -X POST "http://localhost:8000/api/memory/user123?content=用户喜欢打篮球&memory_type=preference&importance=4"
```

### 5. 创建提醒

```bash
curl -X POST "http://localhost:8000/api/reminder/user123?title=喝水提醒&content=该喝水了&reminder_type=interval&time=60"
```

### 6. 获取提醒列表

```bash
curl "http://localhost:8000/api/reminder/user123"
```

## 四、功能说明

### 1. 记忆型对话

- 系统会自动记住用户的偏好和习惯
- 每次对话都会参考历史记忆
- 支持提取重要信息自动保存

### 2. 情绪识别

- 自动识别用户情绪（积极/消极/中性）
- 根据情绪调整回复风格
- 消极情绪时给予安慰和鼓励

### 3. 智能提醒

- 支持定时提醒、间隔提醒、事件提醒
- 可设置多个提醒
- 可以启用/禁用提醒

## 五、测试

```bash
# 运行测试
cd backend
pytest test_app.py -v
```

## 六、扩展开发

### 接入真实LLM

修改 `app/chat.py` 中的对话生成逻辑，接入OpenAI或Claude API：

```python
import openai

def generate_reply_with_llm(message: str, system_prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content
```

### 添加新功能

1. 在 `app/models.py` 添加数据模型
2. 在对应模块实现逻辑
3. 在 `app/main.py` 添加路由

## 七、常见问题

### Q: 为什么回复是固定的？
A: 目前使用模拟回复，需要配置真实LLM API才能启用智能对话。

### Q: 如何查看日志？
A: 启动服务后，所有请求会显示在终端。

### Q: 数据存储在哪里？
A: 当前使用 SQLite，数据存储在 `memory.db` 文件中。

## 八、后续规划

- [ ] 接入真实LLM API
- [ ] 开发移动端App
- [ ] 添加语音功能
- [ ] 增强记忆能力（RAG）
- [ ] 添加多平台支持

---

*文档版本：1.0.0*
*更新时间：2026-02-25*
