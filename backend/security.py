"""
安全工具
加密、签名等
"""
import hashlib
import hmac
import secrets
import base64
from cryptography.fernet import Fernet
from typing import Optional

class SecurityUtils:
    """安全工具"""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """生成随机Token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """生成盐值"""
        return base64.b64encode(secrets.token_bytes(length)).decode()
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple:
        """哈希密码"""
        if salt is None:
            salt = SecurityUtils.generate_salt()
        
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        return base64.b64encode(pwd_hash).decode(), salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """验证密码"""
        new_hash, _ = SecurityUtils.hash_password(password, salt)
        return hmac.compare_digest(new_hash, hashed)
    
    @staticmethod
    def md5(text: str) -> str:
        """MD5哈希"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def sha256(text: str) -> str:
        """SHA256哈希"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def hmac_sha256(key: str, message: str) -> str:
        """HMAC-SHA256"""
        return hmac.new(
            key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()


class Encryptor:
    """加密器"""
    
    def __init__(self, key: bytes = None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)
        self.key = key
    
    def encrypt(self, text: str) -> str:
        """加密"""
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt(self, encrypted: str) -> str:
        """解密"""
        return self.cipher.decrypt(encrypted.encode()).decode()
    
    @classmethod
    def from_key(cls, key: str):
        """从密钥创建"""
        return cls(key.encode())


class TokenManager:
    """Token管理器"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_token(self, user_id: str, expires_in: int = 3600) -> str:
        """创建Token"""
        import json
        from datetime import datetime, timedelta
        
        payload = {
            "user_id": user_id,
            "exp": (datetime.now() + timedelta(seconds=expires_in)).timestamp()
        }
        
        import base64
        header = base64.b64encode(json.dumps({"alg": "HS256"}).encode()).decode()
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()
        
        signature = SecurityUtils.hmac_sha256(self.secret_key, f"{header}.{payload_b64}")
        
        return f"{header}.{payload_b64}.{signature}"
    
    def verify_token(self, token: str) -> Optional[str]:
        """验证Token"""
        try:
            import json
            import base64
            
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            header, payload_b64, signature = parts
            
            # 验证签名
            expected_sig = SecurityUtils.hmac_sha256(self.secret_key, f"{header}.{payload_b64}")
            if not hmac.compare_digest(signature, expected_sig):
                return None
            
            # 解析payload
            payload = json.loads(base64.b64decode(payload_b64))
            
            # 检查过期
            from datetime import datetime
            if payload.get("exp", 0) < datetime.now().timestamp():
                return None
            
            return payload.get("user_id")
        
        except:
            return None


# 使用示例
if __name__ == "__main__":
    # 测试加密
    enc = Encryptor()
    encrypted = enc.encrypt("Hello World!")
    print(f"加密: {encrypted}")
    print(f"解密: {enc.decrypt(encrypted)}")
    
    # 测试密码哈希
    hashed, salt = SecurityUtils.hash_password("password123")
    print(f"密码验证: {SecurityUtils.verify_password('password123', hashed, salt)}")
    
    # 测试Token
    tm = TokenManager("secret-key")
    token = tm.create_token("user123")
    print(f"Token: {token}")
    print(f"验证: {tm.verify_token(token)}")
