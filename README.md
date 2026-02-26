# 随身AI伴侣 v1.1.0

比Siri更聪明、比ChatGPT更懂你的随身AI伙伴

## 功能特性

### 核心功能
- [x] 记忆型对话
- [x] 智能提醒
- [x] 情感陪伴

### 新增功能 (v1.1)
- [x] 情感引擎 - 智能情绪检测与回应
- [x] 增强记忆引擎 - 多类型记忆提取
- [x] 工具引擎 - 天气/计算/翻译/提醒
- [x] 人格引擎 - 温暖/幽默/专业/可爱
- [x] CLI客户端 - 命令行交互

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python -m app.main
# 或
uvicorn app.main:app --reload
```

### 3. 使用CLI客户端

```bash
python client.py
```

### 4. API文档

访问 http://localhost:8000/docs 查看所有API

## API列表

### 对话
- `POST /api/chat` - 发送消息

### 用户
- `GET /api/user/{user_id}` - 获取用户
- `POST /api/user/{user_id}` - 创建用户

### 记忆
- `GET /api/memory/{user_id}` - 获取记忆
- `POST /api/memory/{user_id}` - 添加记忆

### 提醒
- `GET /api/reminder/{user_id}` - 获取提醒
- `POST /api/reminder/{user_id}` - 创建提醒
- `GET /api/reminder/suggestions` - 推荐提醒

### 扩展
- `POST /api/emotion/detect` - 情绪检测
- `GET /api/persona/{type}` - 获取人格
- `GET /api/personas` - 人格列表
- `GET /api/tools` - 工具列表
- `POST /api/tool/execute` - 执行工具
- `GET /api/stats/{user_id}` - 用户统计

## 项目结构

```
ai-companion/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # 主入口
│   │   ├── models.py       # 数据模型
│   │   ├── chat.py         # 对话模块
│   │   ├── memory.py       # 记忆模块
│   │   ├── reminder.py     # 提醒模块
│   │   ├── advanced.py     # 进阶功能
│   │   └── api扩展.py      # 扩展API
│   ├── client.py           # CLI客户端
│   ├── requirements.txt
│   └── test_app.py
├── CHANGELOG.md
└── README.md
```

## 使用示例

### Python调用

```python
import requests

# 对话
response = requests.post("http://localhost:8000/api/chat", json={
    "user_id": "user1",
    "message": "你好"
})
print(response.json())
# {"reply": "你好呀！今天过得怎么样？😊", "emotion": "neutral"}

# 情绪检测
response = requests.post("http://localhost:8000/api/emotion/detect", json={
    "user_id": "user1",
    "message": "我今天很开心！"
})
print(response.json())
# {"emotion": "positive", "response": "听到你这么说我也好开心呀！"}
```

## 技术栈

- FastAPI
- SQLite
- Python 3.8+

## License

MIT
