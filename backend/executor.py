"""
命令执行器
安全执行系统命令
"""
import subprocess
import shlex
from typing import Tuple, Optional, List

class CommandExecutor:
    """命令执行器"""
    
    # 允许的命令白名单
    ALLOWED_COMMANDS = {
        "ls": ["ls", "-la"],
        "dir": ["dir"],
        "pwd": ["pwd"],
        "cat": ["cat"],
        "grep": ["grep"],
        "find": ["find"],
        "git": ["git", "--version"],
        "python": ["python", "--version"],
        "node": ["node", "--version"],
        "pip": ["pip", "list"],
    }
    
    def __init__(self, allowed_only: bool = True):
        self.allowed_only = allowed_only
    
    def execute(self, command: str, timeout: int = 30) -> Tuple[int, str, str]:
        """
        执行命令
        返回: (返回码, stdout, stderr)
        """
        # 安全检查
        if self.allowed_only:
            if not self._is_allowed(command):
                return (-1, "", f"命令不允许执行: {command}")
        
        try:
            # 分割命令
            args = shlex.split(command)
            
            # 执行
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False
            )
            
            return result.returncode, result.stdout, result.stderr
        
        except subprocess.TimeoutExpired:
            return (-1, "", "命令执行超时")
        except Exception as e:
            return (-1, "", str(e))
    
    def _is_allowed(self, command: str) -> bool:
        """检查命令是否允许"""
        # 获取命令名
        cmd_name = shlex.split(command)[0] if command else ""
        
        # 检查白名单
        for allowed in self.ALLOWED_COMMANDS.keys():
            if command.startswith(allowed) or cmd_name == allowed:
                return True
        
        return False
    
    def list_allowed(self) -> List[str]:
        """列出允许的命令"""
        return list(self.ALLOWED_COMMANDS.keys())


class ScriptRunner:
    """脚本运行器"""
    
    def __init__(self, script_dir: str = "scripts"):
        self.script_dir = script_dir
    
    def run_script(self, script_name: str, args: List[str] = None) -> Tuple[int, str, str]:
        """运行脚本"""
        import os
        
        script_path = os.path.join(self.script_dir, script_name)
        
        if not os.path.exists(script_path):
            return (-1, "", f"脚本不存在: {script_name}")
        
        # 根据扩展名选择解释器
        ext = os.path.splitext(script_name)[1]
        
        if ext == ".py":
            cmd = ["python", script_path]
        elif ext == ".js":
            cmd = ["node", script_path]
        elif ext == ".sh":
            cmd = ["bash", script_path]
        elif ext == ".bat":
            cmd = ["cmd", "/c", script_path]
        else:
            return (-1, "", f"不支持的脚本类型: {ext}")
        
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return (-1, "", str(e))
    
    def list_scripts(self) -> List[str]:
        """列出可用脚本"""
        import os
        
        if not os.path.exists(self.script_dir):
            return []
        
        return [f for f in os.listdir(self.script_dir) 
                if os.path.isfile(os.path.join(self.script_dir, f))]


# 使用示例
if __name__ == "__main__":
    executor = CommandExecutor(allowed_only=True)
    
    # 列出允许的命令
    print("允许的命令:", executor.list_allowed())
    
    # 执行允许的命令
    code, stdout, stderr = executor.execute("python --version")
    print(f"返回码: {code}")
    print(f"输出: {stdout}")
    
    # 尝试执行不允许的命令
    code, stdout, stderr = executor.execute("rm -rf /")
    print(f"返回码: {code}")
    print(f"错误: {stderr}")
