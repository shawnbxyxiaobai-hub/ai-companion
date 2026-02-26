"""
Webhook集成
支持钉钉、企业微信、飞书等webhook通知
"""
import requests
import json
from typing import Dict, Any, Optional

class WebhookNotifier:
    """Webhook通知器"""
    
    # 支持的平台
    PLATFORMS = {
        "dingtalk": "钉钉",
        "wework": "企业微信",
        "feishu": "飞书",
        "slack": "Slack",
        "discord": "Discord"
    }
    
    def __init__(self, platform: str, webhook_url: str):
        self.platform = platform
        self.webhook_url = webhook_url
    
    def send_text(self, content: str) -> bool:
        """发送文本消息"""
        if self.platform == "dingtalk":
            return self._send_dingtalk_text(content)
        elif self.platform == "feishu":
            return self._send_feishu_text(content)
        elif self.platform == "slack":
            return self._send_slack_text(content)
        else:
            return self._send_generic_text(content)
    
    def _send_dingtalk_text(self, content: str) -> bool:
        """发送钉钉消息"""
        data = {
            "msgtype": "text",
            "text": {"content": f"🤖 AI伴侣: {content}"}
        }
        try:
            r = requests.post(self.webhook_url, json=data, timeout=10)
            return r.json().get("errcode") == 0
        except:
            return False
    
    def _send_feishu_text(self, content: str) -> bool:
        """发送飞书消息"""
        data = {
            "msg_type": "text",
            "content": {"text": f"🤖 AI伴侣: {content}"}
        }
        try:
            r = requests.post(self.webhook_url, json=data, timeout=10)
            return r.json().get("code") == 0
        except:
            return False
    
    def _send_slack_text(self, content: str) -> bool:
        """发送Slack消息"""
        data = {"text": f"🤖 AI伴侣: {content}"}
        try:
            r = requests.post(self.webhook_url, json=data, timeout=10)
            return r.status_code == 200
        except:
            return False
    
    def _send_generic_text(self, content: str) -> bool:
        """发送通用消息"""
        try:
            r = requests.post(self.webhook_url, json={"text": content}, timeout=10)
            return r.status_code in [200, 201]
        except:
            return False
    
    def send_card(self, title: str, content: str, extra: Dict[str, Any] = None) -> bool:
        """发送卡片消息"""
        if self.platform == "dingtalk":
            return self._send_dingtalk_card(title, content, extra)
        elif self.platform == "feishu":
            return self._send_feishu_card(title, content, extra)
        return self.send_text(f"{title}\n{content}")
    
    def _send_dingtalk_card(self, title: str, content: str, extra: Dict = None) -> bool:
        """发送钉钉卡片"""
        # 简化版markdown消息
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"## {title}\n{content}"
            }
        }
        try:
            r = requests.post(self.webhook_url, json=data, timeout=10)
            return r.json().get("errcode") == 0
        except:
            return False
    
    def _send_feishu_card(self, title: str, content: str, extra: Dict = None) -> bool:
        """发送飞书卡片"""
        data = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": title}},
                "elements": [
                    {"tag": "div", "text": {"tag": "plain_text", "content": content}}
                ]
            }
        }
        try:
            r = requests.post(self.webhook_url, json=data, timeout=10)
            return r.json().get("code") == 0
        except:
            return False


# 使用示例
if __name__ == "__main__":
    # 配置webhook
    DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
    
    # 创建通知器
    notifier = WebhookNotifier("dingtalk", DINGTALK_WEBHOOK)
    
    # 发送通知
    if notifier.send_text("你好！这是测试消息"):
        print("发送成功！")
    else:
        print("发送失败")
