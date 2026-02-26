"""
知识库问答系统
基于简单关键词匹配的问答
"""
import re
from typing import List, Dict, Optional

class QAPair:
    """问答对"""
    
    def __init__(self, question: str, answer: str, keywords: List[str] = None):
        self.question = question
        self.answer = answer
        self.keywords = keywords or self._extract_keywords(question)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单分词
        words = re.findall(r'\w+', text.lower())
        # 过滤停用词
        stopwords = {'的', '是', '了', '在', '和', '有', '我', '你', '他', '她', '它', '吗', '呢', '啊', '吧', '呀'}
        return [w for w in words if w not in stopwords and len(w) > 1]


class KnowledgeBase:
    """知识库"""
    
    def __init__(self):
        self.qa_pairs: List[QAPair] = []
        self._load_default_knowledge()
    
    def _load_default_knowledge(self):
        """加载默认知识"""
        default_qa = [
            ("你好", "你好呀！有什么可以帮你的吗？", ["你好", "hello"]),
            ("你叫什么", "我叫小白，是你的AI伙伴！", ["名字", "叫"]),
            ("你能做什么", "我可以陪你聊天、回答问题、设置提醒、管理记忆等很多事情～", ["能", "做", "功能"]),
            ("天气怎么样", "今天天气很不错哦！出门记得带好心情～", ["天气"]),
            ("几点了", "现在的时间是...", ["几点", "时间"]),
            ("你是谁", "我是小白，一个温暖的AI伙伴～", ["谁", "身份"]),
            ("谢谢", "不客气！很高兴能帮到你！", ["谢谢", "感谢"]),
            ("再见", "再见！有空再聊～", ["再见", "拜拜"]),
            ("心情不好", "别难过，我在这里陪你～有什么想说的吗？", ["难过", "伤心", "心情"]),
            ("无聊", "那我们聊聊天吧！你想聊什么？", ["无聊", "闷"]),
        ]
        
        for q, a, k in default_qa:
            self.qa_pairs.append(QAPair(q, a, k))
    
    def add_qa(self, question: str, answer: str):
        """添加问答对"""
        self.qa_pairs.append(QAPair(question, answer))
    
    def search(self, query: str) -> Optional[str]:
        """搜索答案"""
        query_keywords = set(re.findall(r'\w+', query.lower()))
        
        best_match = None
        best_score = 0
        
        for qa in self.qa_pairs:
            # 计算匹配分数
            score = len(query_keywords & set(qa.keywords))
            
            # 问句包含查询
            if qa.question.lower() in query.lower():
                score += 5
            
            # 关键词匹配
            for kw in qa.keywords:
                if kw in query.lower():
                    score += 2
            
            if score > best_score:
                best_score = score
                best_match = qa
        
        if best_score > 0:
            return best_match.answer
        
        return None
    
    def get_all_questions(self) -> List[str]:
        """获取所有问题"""
        return [qa.question for qa in self.qa_pairs]


class QAEngine:
    """问答引擎"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.fallback_responses = [
            "这个问题我不太确定呢...",
            "让我想想...",
            "我好像不太明白你的意思～",
            "可以换个方式问我吗？",
            "我还需要学习更多知识！"
        ]
    
    def ask(self, question: str) -> str:
        """提问"""
        # 搜索知识库
        answer = self.knowledge_base.search(question)
        
        if answer:
            return answer
        
        # 随机返回兜底回复
        import random
        return random.choice(self.fallback_responses)
    
    def teach(self, question: str, answer: str):
        """教新知识"""
        self.knowledge_base.add_qa(question, answer)
        return "我学会了！谢谢你的教导～"


# 使用示例
if __name__ == "__main__":
    engine = QAEngine()
    
    # 测试问答
    questions = [
        "你好呀",
        "你叫什么名字",
        "你能做什么",
        "我心情不好"
    ]
    
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {engine.ask(q)}")
        print()
    
    # 教新知识
    engine.teach("今天星期几", "今天是星期四！")
    print("Q: 今天星期几")
    print(f"A: {engine.ask('今天星期几')}")
