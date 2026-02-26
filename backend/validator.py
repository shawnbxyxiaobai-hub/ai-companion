"""
验证器
数据验证工具
"""
import re
from typing import Any, Optional
from datetime import datetime

class Validator:
    """验证器基类"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号 (中国)"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """验证URL"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """验证用户名 (3-20位字母数字下划线)"""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password(password: str) -> tuple:
        """
        验证密码强度
        返回: (是否有效, 错误信息)
        """
        if len(password) < 8:
            return False, "密码至少8位"
        
        if not re.search(r'[a-zA-Z]', password):
            return False, "密码需要包含字母"
        
        if not re.search(r'\d', password):
            return False, "密码需要包含数字"
        
        return True, ""
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """验证日期"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_json(json_str: str) -> bool:
        """验证JSON"""
        import json
        try:
            json.loads(json_str)
            return True
        except:
            return False
    
    @staticmethod
    def sanitize_html(html: str) -> str:
        """清理HTML标签"""
        # 简单清理
        import re
        clean = re.sub(r'<[^>]+>', '', html)
        return clean.strip()
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """验证IP地址"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        
        parts = ip.split('.')
        return all(0 <= int(p) <= 255 for p in parts)


class FormValidator:
    """表单验证器"""
    
    def __init__(self):
        self.errors = {}
    
    def add_error(self, field: str, message: str):
        """添加错误"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def get_errors(self) -> dict:
        """获取所有错误"""
        return self.errors
    
    def clear_errors(self):
        """清空错误"""
        self.errors = {}
    
    def validate_field(self, field: str, value: Any, rules: list) -> bool:
        """验证单个字段"""
        valid = True
        
        for rule in rules:
            rule_name, *params = rule.split(':')
            
            if rule_name == "required":
                if not value:
                    self.add_error(field, f"{field}不能为空")
                    valid = False
            
            elif rule_name == "min":
                if value and len(str(value)) < int(params[0]):
                    self.add_error(field, f"{field}至少{params[0]}位")
                    valid = False
            
            elif rule_name == "max":
                if value and len(str(value)) > int(params[0]):
                    self.add_error(field, f"{field}最多{params[0]}位")
                    valid = False
            
            elif rule_name == "email":
                if value and not Validator.validate_email(value):
                    self.add_error(field, "邮箱格式不正确")
                    valid = False
            
            elif rule_name == "phone":
                if value and not Validator.validate_phone(value):
                    self.add_error(field, "手机号格式不正确")
                    valid = False
        
        return valid


# 使用示例
if __name__ == "__main__":
    # 测试验证器
    print("邮箱验证:", Validator.validate_email("test@example.com"))
    print("手机验证:", Validator.validate_phone("13800138000"))
    print("URL验证:", Validator.validate_url("https://example.com"))
    print("密码验证:", Validator.validate_password("abc12345"))
    
    # 测试表单验证
    fv = FormValidator()
    fv.validate_field("username", "john", ["required", "min:3", "max:20"])
    fv.validate_field("email", "invalid", ["required", "email"])
    fv.validate_field("password", "123", ["required", "min:8"])
    
    print("\n表单错误:")
    for field, errors in fv.get_errors().items():
        print(f"  {field}: {errors}")
