# AI伴侣App - 技术方案

## 概述

移动端App技术方案，基于React Native开发。

## 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 框架 | React Native | 0.72+ |
| 语言 | TypeScript | 5.0+ |
| 状态管理 | Zustand | 4.0+ |
| UI库 | React Native Paper | 5.0+ |
| 导航 | React Navigation | 6.0+ |
| 网络 | Axios | 1.0+ |
| 本地存储 | AsyncStorage | 1.0+ |
| 推送 | @react-native-firebase/messaging | 14.0+ |

## 项目结构

```
App/
├── src/
│   ├── components/     # 通用组件
│   ├── screens/        # 页面
│   ├── services/       # API服务
│   ├── stores/        # 状态管理
│   ├── hooks/         # 自定义Hook
│   ├── utils/         # 工具函数
│   ├── types/         # 类型定义
│   └── constants/     # 常量
├── android/           # Android配置
├── ios/               # iOS配置
└── index.js           # 入口
```

## 页面设计

### 1. 聊天页面 (ChatScreen)
- 消息列表
- 输入框
- 快捷操作按钮
- 语音输入

### 2. 发现页面 (DiscoverScreen)
- AI技能推荐
- 工具箱
- 快捷入口

### 3. 提醒页面 (ReminderScreen)
- 提醒列表
- 添加提醒
- 提醒设置

### 4. 我的页面 (ProfileScreen)
- 用户信息
- 设置
- 记忆管理
- 人格设置

## API对接

```typescript
// API服务
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://your-server:8000',
});

export const chat = (message: string) => 
  api.post('/api/chat', { user_id, message });

export const getMemories = () => 
  api.get(`/api/memory/${user_id}`);
```

## 状态管理

```typescript
// 用户状态
import { create } from 'zustand';

interface UserStore {
  userId: string;
  name: string;
  setUser: (id: string, name: string) => void;
}

export const useUserStore = create<UserStore>((set) => ({
  userId: '',
  name: '',
  setUser: (id, name) => set({ userId: id, name }),
}));
```

## 下一步计划

1. 初始化React Native项目
2. 搭建基础框架
3. 实现聊天界面
4. 对接后端API
5. 添加推送功能

---

*文档版本：1.0.0*
*更新时间：2026-02-26*
