# 随身AI伴侣 - 版本更新日志

## 2026-02-26 v1.1.0

### 新增功能

1. **情感引擎 (EmotionEngine)**
   - 智能情绪检测
   - 根据情绪生成个性化回复
   - 支持积极/消极/中性三种情绪

2. **智能提醒引擎 (ReminderEngine)**
   - 预设提醒模板
   - 喝水、运动、眼保健操等健康提醒
   - 早安/晚安问候

3. **记忆引擎增强 (MemoryEngine)**
   - 多种记忆类型：偏好、习惯、情绪、事件、人物、事实
   - 自动从对话中提取记忆
   - 重要性分级

4. **工具引擎 (ToolEngine)**
   - 天气查询
   - 计算器
   - 翻译
   - 提醒设置

5. **人格引擎 (PersonaEngine)**
   - 温暖型
   - 幽默型
   - 专业型
   - 可爱型

6. **扩展API**
   - /api/emotion/detect - 情绪检测
   - /api/reminder/suggestions - 推荐提醒
   - /api/tool/execute - 执行工具
   - /api/tools - 可用工具列表
   - /api/persona/{type} - 获取人格设置
   - /api/personas - 人格列表
   - /api/memory/extract - 提取记忆
   - /api/stats/{user_id} - 用户统计

## 2026-02-25 v1.0.0

### 初始版本
- 基础对话功能
- 记忆系统
- 提醒功能
