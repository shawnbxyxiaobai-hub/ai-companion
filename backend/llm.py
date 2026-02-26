"""
AI集成模块
支持接入各种LLM
"""
import os
import json
from typing import Optional, List, Dict

class LLMProvider:
    """LLM提供商基类"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """发送聊天请求"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI provider"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        super().__init__(api_key)
        self.model = model
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """调用OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI调用失败: {str(e)}"


class ClaudeProvider(LLMProvider):
    """Claude provider"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-opus"):
        super().__init__(api_key)
        self.model = model
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """调用Claude API"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key or os.getenv("ANTHROPIC_API_KEY"))
            
            # 转换消息格式
            system = ""
            claude_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    system = msg["content"]
                else:
                    claude_messages.append(msg)
            
            response = client.messages.create(
                model=self.model,
                system=system,
                messages=claude_messages,
                **kwargs
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude调用失败: {str(e)}"


class DeepSeekProvider(LLMProvider):
    """DeepSeek provider"""
    
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        super().__init__(api_key)
        self.model = model
        self.base_url = "https://api.deepseek.com"
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """调用DeepSeek API"""
        try:
            import requests
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key or os.getenv('DEEPSEEK_API_KEY')}"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"DeepSeek调用失败: {str(e)}"


class MockProvider(LLMProvider):
    """模拟Provider - 用于测试"""
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """返回模拟回复"""
        last_message = messages[-1]["content"] if messages else ""
        
        responses = [
            "我明白了！",
            "这是一个很有趣的话题～",
            "让我想想...",
            "好的，我会记住的！",
            "有什么我可以帮你的吗？"
        ]
        
        # 简单根据输入返回不同回复
        if "你好" in last_message:
            return "你好呀！有什么想聊的吗？"
        elif "名字" in last_message:
            return "我叫小白，是你的AI伙伴！"
        elif "天气" in last_message:
            return "今天天气不错哦～"
        else:
            import random
            return random.choice(responses)


class LLMManager:
    """LLM管理器"""
    
    PROVIDERS = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "deepseek": DeepSeekProvider,
        "mock": MockProvider
    }
    
    def __init__(self, provider: str = "mock", **kwargs):
        provider_class = self.PROVIDERS.get(provider, MockProvider)
        self.provider = provider_class(**kwargs)
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """发送聊天"""
        return self.provider.chat(messages, **kwargs)
    
    def change_provider(self, provider: str, **kwargs):
        """切换提供商"""
        provider_class = self.PROVIDERS.get(provider, MockProvider)
        self.provider = provider_class(**kwargs)


# 使用示例
if __name__ == "__main__":
    # 使用模拟Provider
    llm = LLMManager("mock")
    messages = [{"role": "user", "content": "你好"}]
    print(llm.chat(messages))
    
    # 切换到DeepSeek
    llm.change_provider("deepseek", api_key="your-key", model="deepseek-chat")
    print(llm.chat(messages))
