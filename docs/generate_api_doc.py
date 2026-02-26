"""
API文档生成
自动生成API文档
"""
import os
from datetime import datetime

class APIDocGenerator:
    """API文档生成器"""
    
    def __init__(self):
        self.endpoints = []
    
    def add_endpoint(self, method: str, path: str, description: str, params: dict = None, response: str = None):
        """添加端点"""
        self.endpoints.append({
            "method": method,
            "path": path,
            "description": description,
            "params": params or {},
            "response": response
        })
    
    def generate_markdown(self) -> str:
        """生成Markdown文档"""
        lines = [
            "# API接口文档",
            "",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            ""
        ]
        
        for ep in self.endpoints:
            # 方法标签
            method_emoji = {
                "GET": "� GET",
                "POST": "📝 POST",
                "PUT": "✏️ PUT",
                "DELETE": "🗑️ DELETE",
                "PATCH": "🔧 PATCH"
            }
            
            emoji = method_emoji.get(ep["method"], ep["method"])
            
            lines.append(f"## {emoji} {ep['path']}")
            lines.append("")
            lines.append(f"**描述**: {ep['description']}")
            lines.append("")
            
            # 参数
            if ep["params"]:
                lines.append("**参数**:")
                lines.append("")
                lines.append("| 参数名 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|")
                
                for name, info in ep["params"].items():
                    required = "✅" if info.get("required") else "❌"
                    ptype = info.get("type", "string")
                    desc = info.get("description", "")
                    lines.append(f"| {name} | {ptype} | {required} | {desc} |")
                
                lines.append("")
            
            # 响应示例
            if ep["response"]:
                lines.append("**响应示例**:")
                lines.append("```json")
                lines.append(ep["response"])
                lines.append("```")
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def save(self, filepath: str = "docs/API.md"):
        """保存文档"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown())
        
        return filepath


# 示例
if __name__ == "__main__":
    generator = APIDocGenerator()
    
    # 添加端点
    generator.add_endpoint(
        "POST", "/api/chat",
        "发送消息并获取AI回复",
        {
            "user_id": {"type": "string", "required": True, "description": "用户ID"},
            "message": {"type": "string", "required": True, "description": "消息内容"}
        },
        '{"reply": "你好呀！", "emotion": "neutral"}'
    )
    
    generator.add_endpoint(
        "GET", "/api/memory/{user_id}",
        "获取用户记忆",
        {
            "user_id": {"type": "string", "required": True, "description": "用户ID"},
            "memory_type": {"type": "string", "required": False, "description": "记忆类型"}
        }
    )
    
    # 生成并保存
    filepath = generator.save()
    print(f"API文档已生成: {filepath}")
