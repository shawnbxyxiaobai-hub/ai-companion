"""
通知系统
支持多种通知方式
"""
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import requests

class Notifier:
    """通知基类"""
    
    def send(self, title: str, content: str, **kwargs) -> bool:
        """发送通知"""
        raise NotImplementedError


class EmailNotifier(Notifier):
    """邮件通知"""
    
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str, use_tls: bool = True):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    def send(self, title: str, content: str, to: str = None, **kwargs) -> bool:
        """发送邮件"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to or self.username
            msg['Subject'] = title
            
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False


class BarkNotifier(Notifier):
    """Bark推送 (iOS)"""
    
    def __init__(self, bark_key: str):
        self.bark_key = bark_key
        self.api_url = f"https://api.day.app/{bark_key}"
    
    def send(self, title: str, content: str, **kwargs) -> bool:
        """发送Bark通知"""
        try:
            data = {
                "title": title,
                "body": content,
                "sound": kwargs.get("sound", "default")
            }
            
            # 可选参数
            if kwargs.get("icon"):
                data["icon"] = kwargs["icon"]
            if kwargs.get("group"):
                data["group"] = kwargs["group"]
            
            response = requests.post(self.api_url, json=data, timeout=10)
            return response.status_code == 200
        except:
            return False


class ServerChanNotifier(Notifier):
    """Server酱推送"""
    
    def __init__(self, sendkey: str):
        self.sendkey = sendkey
        self.api_url = f"https://sctapi.ftqq.com/{sendkey}.send"
    
    def send(self, title: str, content: str, **kwargs) -> bool:
        """发送Server酱通知"""
        try:
            data = {
                "title": title,
                "desp": content
            }
            
            response = requests.post(self.api_url, data=data, timeout=10)
            return response.json().get("code") == 0
        except:
            return False


class TelegramNotifier(Notifier):
    """Telegram推送"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    def send(self, title: str, content: str, **kwargs) -> bool:
        """发送Telegram通知"""
        try:
            data = {
                "chat_id": self.chat_id,
                "text": f"*{title}*\n\n{content}",
                "parse_mode": "Markdown"
            }
            
            response = requests.post(self.api_url, json=data, timeout=10)
            return response.json().get("ok", False)
        except:
            return False


class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.notifiers: List[Notifier] = []
    
    def add_notifier(self, notifier: Notifier):
        """添加通知器"""
        self.notifiers.append(notifier)
    
    def notify(self, title: str, content: str, **kwargs) -> dict:
        """发送通知到所有渠道"""
        results = {}
        
        for notifier in self.notifiers:
            name = notifier.__class__.__name__
            success = notifier.send(title, content, **kwargs)
            results[name] = "✅ 成功" if success else "❌ 失败"
        
        return results


# 使用示例
if __name__ == "__main__":
    # 创建通知管理器
    manager = NotificationManager()
    
    # 添加Bark通知
    # manager.add_notifier(BarkNotifier("your-bark-key"))
    
    # 添加Server酱
    # manager.add_notifier(ServerChanNotifier("your-sendkey"))
    
    # 发送通知
    results = manager.notify("测试通知", "这是一条测试消息")
    
    for name, status in results.items():
        print(f"{name}: {status}")
