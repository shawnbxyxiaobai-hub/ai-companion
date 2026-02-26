"""
插件系统
支持扩展功能
"""
import os
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Callable, Any

class Plugin:
    """插件基类"""
    
    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = ""
    
    def __init__(self):
        self.enabled = True
    
    def on_load(self):
        """加载时调用"""
        pass
    
    def on_unload(self):
        """卸载时调用"""
        pass
    
    def register_handlers(self, app):
        """注册处理器"""
        pass


class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.handlers: Dict[str, List[Callable]] = {}
    
    def discover_plugins(self) -> List[str]:
        """发现插件"""
        if not self.plugin_dir.exists():
            return []
        
        plugins = []
        for file in self.plugin_dir.glob("*.py"):
            if file.stem.startswith("_"):
                continue
            plugins.append(file.stem)
        
        return plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """加载插件"""
        try:
            # 动态导入模块
            module = importlib.import_module(f"{self.plugin_dir.name}.{plugin_name}")
            
            # 查找插件类
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) 
                    and issubclass(obj, Plugin) 
                    and obj != Plugin):
                    
                    plugin = obj()
                    plugin.on_load()
                    self.plugins[plugin.name] = plugin
                    print(f"已加载插件: {plugin.name} v{plugin.version}")
                    return True
            
            return False
        
        except Exception as e:
            print(f"加载插件失败: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.on_unload()
            del self.plugins[plugin_name]
            return True
        return False
    
    def get_plugin(self, name: str) -> Plugin:
        """获取插件"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict]:
        """列出插件"""
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "enabled": p.enabled
            }
            for p in self.plugins.values()
        ]
    
    def register_handler(self, event: str, handler: Callable):
        """注册事件处理器"""
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)
    
    def emit(self, event: str, *args, **kwargs):
        """触发事件"""
        if event in self.handlers:
            for handler in self.handlers[event]:
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    print(f"事件处理错误: {e}")


# 全局插件管理器
plugin_manager = PluginManager()


# 示例插件
class HelloPlugin(Plugin):
    """示例插件"""
    
    name = "hello"
    version = "1.0.0"
    description = "打印欢迎消息"
    
    def on_load(self):
        print("Hello插件已加载!")


class LoggerPlugin(Plugin):
    """日志插件"""
    
    name = "logger"
    version = "1.0.0"
    description = "记录对话日志"
    
    def __init__(self):
        super().__init__()
        self.log_file = "chat.log"
    
    def log_message(self, user_id: str, message: str, reply: str):
        """记录消息"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{user_id}] {message} -> {reply}\n")


# 使用示例
if __name__ == "__main__":
    # 创建管理器
    manager = PluginManager()
    
    # 发现插件
    print("发现插件:", manager.discover_plugins())
    
    # 加载示例插件
    manager.load_plugin("hello")
    
    # 列出插件
    print("\n已加载插件:")
    for p in manager.list_plugins():
        print(f"  - {p['name']} v{p['version']}: {p['description']}")
