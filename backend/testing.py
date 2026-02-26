"""
测试工具
测试辅助函数
"""
import time
import functools
from typing import Callable, Any

class Timer:
    """计时器"""
    
    def __init__(self, name: str = ""):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"{self.name} 耗时: {elapsed:.4f}秒")
    
    @staticmethod
    def measure(func: Callable) -> Any:
        """测量函数执行时间"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"{func.__name__} 耗时: {elapsed:.4f}秒")
            return result
        return wrapper


class MockRequest:
    """模拟请求"""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockResponse:
    """模拟响应"""
    
    def __init__(self, status_code: int = 200, json_data: dict = None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text
    
    def json(self):
        return self._json_data


class TestCase:
    """测试用例基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
    
    def run(self) -> bool:
        """运行测试"""
        try:
            self.setUp()
            self.test()
            self.tearDown()
            self.passed = True
            print(f"✅ {self.name}")
            return True
        except Exception as e:
            self.passed = False
            self.error = str(e)
            print(f"❌ {self.name}: {e}")
            return False
    
    def setUp(self):
        """前置设置"""
        pass
    
    def test(self):
        """测试逻辑"""
        raise NotImplementedError
    
    def tearDown(self):
        """后置清理"""
        pass


class TestSuite:
    """测试套件"""
    
    def __init__(self, name: str):
        self.name = name
        self.cases = []
        self.results = []
    
    def add_test(self, test_case: TestCase):
        """添加测试用例"""
        self.cases.append(test_case)
    
    def run(self):
        """运行所有测试"""
        print(f"\n{'='*50}")
        print(f"运行测试套件: {self.name}")
        print(f"{'='*50}\n")
        
        passed = 0
        failed = 0
        
        for case in self.cases:
            if case.run():
                passed += 1
            else:
                failed += 1
        
        print(f"\n{'='*50}")
        print(f"测试完成: {passed}通过, {failed}失败")
        print(f"{'='*50}")
        
        return passed, failed


# 使用示例
if __name__ == "__main__":
    # 使用计时器
    with Timer("模拟操作"):
        time.sleep(0.1)
    
    # 使用装饰器计时
    @Timer.measure
    def slow_function():
        time.sleep(0.1)
        return "完成"
    
    slow_function()
    
    # 测试套件
    class ExampleTest(TestCase):
        def test(self):
            assert 1 + 1 == 2
        
        def test_fail(self):
            assert 1 + 1 == 3
    
    suite = TestSuite("示例测试")
    suite.add_test(ExampleTest("加法测试"))
    suite.add_test(ExampleTest("失败测试"))
    suite.run()
