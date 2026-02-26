"""
数据可视化
生成简单的统计图表
"""
import json
from typing import List, Dict, Any

class ChartGenerator:
    """图表生成器"""
    
    @staticmethod
    def generate_bar_chart(data: Dict[str, int], title: str = "") -> str:
        """生成柱状图 (ASCII)"""
        if not data:
            return "无数据"
        
        max_val = max(data.values())
        max_len = max(len(str(k)) for k in data.keys())
        
        lines = []
        if title:
            lines.append(f"📊 {title}")
            lines.append("")
        
        for label, value in data.items():
            bar_len = int((value / max_val) * 20) if max_val > 0 else 0
            bar = "█" * bar_len
            lines.append(f"{label:>{max_len}} | {bar} {value}")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_pie_chart(data: Dict[str, int], title: str = "") -> str:
        """生成饼图 (ASCII)"""
        if not data:
            return "无数据"
        
        total = sum(data.values())
        if total == 0:
            return "无数据"
        
        # 简化的饼图表示
        lines = []
        if title:
            lines.append(f"📊 {title}")
            lines.append("")
        
        for label, value in data.items():
            pct = (value / total) * 100
            bar_len = int(pct / 5)
            bar = "▓" * bar_len + "░" * (20 - bar_len)
            lines.append(f"{label}: {bar} {pct:.1f}%")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_line_chart(data: List[int], labels: List[str] = None, title: str = "") -> str:
        """生成折线图 (ASCII)"""
        if not data:
            return "无数据"
        
        max_val = max(data)
        min_val = min(data)
        range_val = max_val - min_val if max_val > min_val else 1
        
        lines = []
        if title:
            lines.append(f"📈 {title}")
            lines.append("")
        
        # 绘制
        for i, value in enumerate(data):
            y = int(((value - min_val) / range_val) * 4)
            line = "▄" * y + "●" + "▀" * (4 - y)
            
            if labels and i < len(labels):
                lines.append(f"{labels[i]:>10} | {line} {value}")
            else:
                lines.append(f"{i+1:>10} | {line} {value}")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_table(data: List[Dict], columns: List[str] = None) -> str:
        """生成表格"""
        if not data:
            return "无数据"
        
        # 自动获取列
        if columns is None:
            columns = list(data[0].keys())
        
        # 计算列宽
        widths = {col: len(col) for col in columns}
        for row in data:
            for col in columns:
                val = str(row.get(col, ""))
                widths[col] = max(widths[col], len(val))
        
        # 表头
        header = " | ".join(col.ljust(widths[col]) for col in columns)
        separator = "-+-".join("-" * widths[col] for col in columns)
        
        lines = [header, separator]
        
        # 数据行
        for row in data:
            line = " | ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns)
            lines.append(line)
        
        return "\n".join(lines)


class StatsCalculator:
    """统计计算器"""
    
    @staticmethod
    def mean(numbers: List[float]) -> float:
        """平均值"""
        return sum(numbers) / len(numbers) if numbers else 0
    
    @staticmethod
    def median(numbers: List[float]) -> float:
        """中位数"""
        if not numbers:
            return 0
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        if n % 2 == 0:
            return (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2
        else:
            return sorted_nums[n//2]
    
    @staticmethod
    def mode(numbers: List[float]) -> float:
        """众数"""
        if not numbers:
            return 0
        from collections import Counter
        return Counter(numbers).most_common(1)[0][0]
    
    @staticmethod
    def std(numbers: List[float]) -> float:
        """标准差"""
        if not numbers:
            return 0
        avg = StatsCalculator.mean(numbers)
        variance = sum((x - avg) ** 2 for x in numbers) / len(numbers)
        return variance ** 0.5
    
    @staticmethod
    def summary(numbers: List[float]) -> Dict:
        """汇总统计"""
        return {
            "count": len(numbers),
            "sum": sum(numbers),
            "mean": StatsCalculator.mean(numbers),
            "median": StatsCalculator.median(numbers),
            "mode": StatsCalculator.mode(numbers),
            "min": min(numbers) if numbers else 0,
            "max": max(numbers) if numbers else 0,
            "std": StatsCalculator.std(numbers)
        }


# 使用示例
if __name__ == "__main__":
    # 柱状图
    print(ChartGenerator.generate_bar_chart(
        {"Python": 100, "Java": 80, "JavaScript": 60, "Go": 40},
        "编程语言使用    
    print()
统计"
    ))
    
    # 饼图
    print(ChartGenerator.generate_pie_chart(
        {"A": 30, "B": 45, "C": 25},
        "投票结果"
    ))
    
    print()
    
    # 表格
    print(ChartGenerator.generate_table([
        {"name": "张三", "score": 95},
        {"name": "李四", "score": 87},
        {"name": "王五", "score": 92}
    ]))
