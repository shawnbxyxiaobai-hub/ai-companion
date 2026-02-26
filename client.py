#!/usr/bin/env python3
"""
随身AI伴侣 - CLI客户端
命令行交互界面
"""
import requests
import json
import os

API_BASE = "http://localhost:8000"

class AIClient:
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.base_url = API_BASE
    
    def chat(self, message: str) -> dict:
        """发送消息"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"user_id": self.user_id, "message": message}
        )
        return response.json()
    
    def create_user(self, name: str = "用户"):
        """创建用户"""
        response = requests.post(
            f"{self.base_url}/api/user/{self.user_id}",
            params={"name": name}
        )
        return response.json()
    
    def get_memories(self, memory_type: str = None):
        """获取记忆"""
        url = f"{self.base_url}/api/memory/{self.user_id}"
        if memory_type:
            url += f"?memory_type={memory_type}"
        response = requests.get(url)
        return response.json()
    
    def add_memory(self, content: str, memory_type: str = "preference", importance: int = 3):
        """添加记忆"""
        response = requests.post(
            f"{self.base_url}/api/memory/{self.user_id}",
            params={
                "content": content,
                "memory_type": memory_type,
                "importance": importance
            }
        )
        return response.json()
    
    def create_reminder(self, title: str, content: str = "", reminder_type: str = "fixed", time: str = "09:00"):
        """创建提醒"""
        response = requests.post(
            f"{self.base_url}/api/reminder/{self.user_id}",
            params={
                "title": title,
                "content": content,
                "reminder_type": reminder_type,
                "time": time
            }
        )
        return response.json()
    
    def get_reminders(self):
        """获取提醒列表"""
        response = requests.get(f"{self.base_url}/api/reminder/{self.user_id}")
        return response.json()
    
    def detect_emotion(self, message: str):
        """检测情绪"""
        response = requests.post(
            f"{self.base_url}/api/emotion/detect",
            json={"user_id": self.user_id, "message": message}
        )
        return response.json()
    
    def get_persona(self, persona_type: str = "warm"):
        """获取人格"""
        response = requests.get(f"{self.base_url}/api/persona/{persona_type}")
        return response.json()
    
    def list_personas(self):
        """列出所有人格"""
        response = requests.get(f"{self.base_url}/api/personas")
        return response.json()
    
    def get_stats(self):
        """获取统计"""
        response = requests.get(f"{self.base_url}/api/stats/{self.user_id}")
        return response.json()


def main():
    client = AIClient()
    
    print("=" * 50)
    print("欢迎使用随身AI伴侣 CLI")
    print("=" * 50)
    
    # 创建用户
    client.create_user("CLI用户")
    print("用户创建成功！")
    
    while True:
        print("\n请选择操作:")
        print("1. 对话")
        print("2. 查看记忆")
        print("3. 添加记忆")
        print("4. 创建提醒")
        print("5. 查看提醒")
        print("6. 情绪检测")
        print("7. 查看人格")
        print("8. 用户统计")
        print("0. 退出")
        
        choice = input("\n请输入选项: ").strip()
        
        if choice == "0":
            print("再见！")
            break
        
        elif choice == "1":
            message = input("请输入消息: ")
            result = client.chat(message)
            print(f"\nAI回复: {result.get('reply')}")
            print(f"情绪: {result.get('emotion')}")
        
        elif choice == "2":
            memories = client.get_memories()
            print(f"\n记忆数量: {len(memories.get('memories', []))}")
            for m in memories.get('memories', [])[:5]:
                print(f"  - {m.get('content')}")
        
        elif choice == "3":
            content = input("请输入记忆内容: ")
            memory_type = input("记忆类型 (preference/habit/emotion/event): ")
            importance = int(input("重要性 (1-5): ") or "3")
            result = client.add_memory(content, memory_type, importance)
            print(f"\n{result.get('message')}")
        
        elif choice == "4":
            title = input("请输入提醒标题: ")
            content = input("提醒内容: ")
            reminder_type = input("类型 (fixed/interval): ")
            time = input("时间 (HH:MM 或分钟): ")
            result = client.create_reminder(title, content, reminder_type, time)
            print(f"\n{result.get('message')}")
        
        elif choice == "5":
            reminders = client.get_reminders()
            print(f"\n提醒数量: {len(reminders.get('reminders', []))}")
            for r in reminders.get('reminders', [])[:5]:
                print(f"  - {r.get('title')}: {r.get('content')}")
        
        elif choice == "6":
            message = input("请输入要检测情绪的消息: ")
            result = client.detect_emotion(message)
            print(f"\n情绪: {result.get('emotion')}")
            print(f"回应: {result.get('response')}")
        
        elif choice == "7":
            personas = client.list_personas()
            print("\n可用人格:")
            for key, value in personas.get('personas', {}).items():
                print(f"  - {key}: {value.get('name')} - {value.get('description')}")
        
        elif choice == "8":
            stats = client.get_stats()
            print("\n用户统计:")
            print(f"  记忆数量: {stats.get('memory_count')}")
            print(f"  提醒数量: {stats.get('reminder_count')}")
            print(f"  活跃提醒: {stats.get('active_reminders')}")


if __name__ == "__main__":
    main()
