"""
简单的Web UI
基于Flask的网页界面
"""
from flask import Flask, render_template_string, request, jsonify
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app as fastapi_app
from backend.app.chat import chat
from backend.app.memory import get_user, get_memories
from backend.app.reminder import get_reminders

app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>随身AI伴侣</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container { max-width: 600px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .header h1 { font-size: 24px; }
        .chat-box {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 300px;
            max-height: 400px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 80%;
        }
        .message.user {
            background: #667eea;
            color: white;
            margin-left: auto;
        }
        .message.ai {
            background: #f0f0f0;
            color: #333;
        }
        .input-box {
            display: flex;
            gap: 10px;
        }
        .input-box input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 24px;
            outline: none;
            font-size: 16px;
        }
        .input-box input:focus {
            border-color: #667eea;
        }
        .input-box button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 24px;
            cursor: pointer;
            font-size: 16px;
        }
        .input-box button:hover {
            background: #5568d3;
        }
        .stats {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .stats h3 { margin-bottom: 10px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .stat-item {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value { font-size: 24px; font-weight: bold; color: #667eea; }
        .stat-label { font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 随身AI伴侣</h1>
            <p>比Siri更聪明，比ChatGPT更懂你</p>
        </div>
        
        <div class="stats">
            <h3>📊 用户统计</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value" id="memoryCount">0</div>
                    <div class="stat-label">记忆数量</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="reminderCount">0</div>
                    <div class="stat-label">提醒数量</div>
                </div>
            </div>
        </div>
        
        <div class="chat-box" id="chatBox">
            <div class="message ai">
                你好！我是你的随身AI伴侣～ 有什么想聊的吗？
            </div>
        </div>
        
        <div class="input-box">
            <input type="text" id="messageInput" placeholder="输入消息..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">发送</button>
        </div>
    </div>
    
    <script>
        const userId = 'web_user_' + Date.now();
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            // 显示用户消息
            addMessage(message, 'user');
            input.value = '';
            
            // 发送请求
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({user_id: userId, message: message})
                });
                const data = await response.json();
                addMessage(data.reply, 'ai');
            } catch (e) {
                addMessage('抱歉，出错了～', 'ai');
            }
        }
        
        function addMessage(text, type) {
            const chatBox = document.getElementById('chatBox');
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.textContent = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }
        
        // 加载统计
        async function loadStats() {
            try {
                const response = await fetch('/api/stats/' + userId);
                const data = await response.json();
                document.getElementById('memoryCount').textContent = data.memory_count || 0;
                document.getElementById('reminderCount').textContent = data.reminder_count || 0;
            } catch (e) {}
        }
        
        loadStats();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """对话API"""
    data = request.json
    result = chat(data.get('user_id', 'default'), data.get('message', ''))
    return jsonify(result)

@app.route('/api/stats/<user_id>')
def stats_api(user_id):
    """统计API"""
    memories = get_memories(user_id)
    reminders = get_reminders(user_id)
    return jsonify({
        "memory_count": len(memories),
        "reminder_count": len(reminders),
        "active_reminders": len([r for r in reminders if r.get('enabled', False)])
    })

def run_web_ui(port=5000):
    """运行Web UI"""
    print(f"Web UI已启动: http://localhost:{port}")
    app.run(port=port, debug=True)

if __name__ == "__main__":
    run_web_ui()
