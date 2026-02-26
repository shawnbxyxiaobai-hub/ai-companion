"""
定时任务管理
支持各种定时任务
"""
import time
import threading
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional
import json

class Task:
    """任务"""
    
    def __init__(self, name: str, func: Callable, interval: int = None, cron: str = None):
        self.name = name
        self.func = func
        self.interval = interval  # 间隔秒数
        self.cron = cron          # cron表达式
        self.last_run = None
        self.enabled = True
        self.running = False
    
    def should_run(self) -> bool:
        """检查是否应该运行"""
        if not self.enabled or self.running:
            return False
        
        if self.interval:
            if not self.last_run:
                return True
            elapsed = (datetime.now() - self.last_run).total_seconds()
            return elapsed >= self.interval
        
        return False
    
    def run(self):
        """运行任务"""
        self.running = True
        try:
            self.func()
            self.last_run = datetime.now()
        except Exception as e:
            print(f"任务执行错误: {e}")
        finally:
            self.running = False


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.running = False
        self.thread = None
    
    def add_interval_task(self, name: str, func: Callable, interval_seconds: int):
        """添加间隔任务"""
        task = Task(name, func, interval=interval_seconds)
        self.tasks.append(task)
        return task
    
    def add_cron_task(self, name: str, func: Callable, cron: str):
        """添加Cron任务"""
        task = Task(name, func, cron=cron)
        self.tasks.append(task)
        return task
    
    def remove_task(self, name: str):
        """移除任务"""
        self.tasks = [t for t in self.tasks if t.name != name]
    
    def start(self):
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("任务调度器已启动")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("任务调度器已停止")
    
    def _run_loop(self):
        """运行循环"""
        while self.running:
            for task in self.tasks:
                if task.should_run():
                    print(f"执行任务: {task.name}")
                    task.run()
            time.sleep(1)
    
    def list_tasks(self) -> List[Dict]:
        """列出所有任务"""
        return [
            {
                "name": t.name,
                "enabled": t.enabled,
                "interval": t.interval,
                "last_run": t.last_run.isoformat() if t.last_run else None
            }
            for t in self.tasks
        ]


# 全局调度器
scheduler = TaskScheduler()


# 预设任务
def health_check_task():
    """健康检查任务"""
    print("健康检查...")


def cleanup_task():
    """清理任务"""
    print("清理临时文件...")


def backup_task():
    """备份任务"""
    print("数据备份...")


def notification_task():
    """通知任务"""
    print("发送通知...")


# 添加预设任务
def setup_default_tasks():
    """设置默认任务"""
    scheduler.add_interval_task("health_check", health_check_task, 3600)      # 每小时
    scheduler.add_interval_task("cleanup", cleanup_task, 86400)           # 每天
    scheduler.add_interval_task("backup", backup_task, 86400)              # 每天
    scheduler.add_interval_task("notification_check", notification_task, 1800)  # 每30分钟


if __name__ == "__main__":
    # 设置任务
    setup_default_tasks()
    
    # 启动
    scheduler.start()
    
    # 列出任务
    print("\n当前任务:")
    for task in scheduler.list_tasks():
        print(f"  - {task['name']}: interval={task['interval']}s")
    
    # 保持运行
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        scheduler.stop()
