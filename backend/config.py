"""
配置管理
支持多环境配置
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """配置类"""
    
    _instance = None
    _config = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.env = os.getenv("APP_ENV", "development")
        self.config_dir = Path(__file__).parent.parent / "config"
    
    def load(self, config_file: str = None):
        """加载配置"""
        if config_file:
            config_path = self.config_dir / config_file
        else:
            config_path = self.config_dir / f"{self.env}.json"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            # 使用默认配置
            self._config = self._get_default_config()
        
        return self
    
    def _get_default_config(self) -> Dict:
        """默认配置"""
        return {
            "app": {
                "name": "随身AI伴侣",
                "version": "1.1.0",
                "debug": True
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000
            },
            "database": {
                "path": "memory.db"
            },
            "ai": {
                "default_persona": "warm",
                "max_memories": 100
            },
            "reminder": {
                "enabled": True,
                "default_interval": 60
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """设置配置"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_file: str = None):
        """保存配置"""
        if config_file:
            config_path = self.config_dir / config_file
        else:
            config_path = self.config_dir / f"{self.env}.json"
        
        self.config_dir.mkdir(exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
    
    def __getitem__(self, key: str) -> Any:
        """支持 config['key'] 访问"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any):
        """支持 config['key'] = value 设置"""
        self.set(key, value)


# 默认配置实例
config = Config()


# 使用示例
if __name__ == "__main__":
    # 加载配置
    config.load()
    
    # 读取配置
    print(f"应用名称: {config.get('app.name')}")
    print(f"调试模式: {config.get('app.debug')}")
    print(f"服务器端口: {config.get('server.port')}")
    
    # 修改配置
    config.set('app.debug', False)
    config.save()
