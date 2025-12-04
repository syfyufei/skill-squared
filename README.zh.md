# Skill-Squared

用于管理和维护 Claude Code skills 的元技能 - 创建项目、添加命令、同步到市场以及验证结构。

## 安装

在 Claude Code 中，首先注册市场：

```bash
/plugin marketplace add syfyufei/skill-squared
```

然后从市场安装插件：

```bash
/plugin install skill-squared@skill-squared-marketplace
```

### 验证安装

检查命令是否出现：

```bash
/help
```

```
# 应该看到 4 个命令：
# /skill-squared:create - 创建新技能项目结构
# /skill-squared:command - 向现有技能添加斜杠命令
# /skill-squared:sync - 将技能从独立仓库同步到市场
# /skill-squared:validate - 验证技能结构和配置
```

## 使用

### 创建新技能

创建包含所有必要文件的完整技能项目：

```bash
/skill-squared:create
```

或使用自然语言：
```
"创建一个名为 data-analyzer 的新技能"
```

### 添加命令

向现有技能添加新的斜杠命令：

```bash
/skill-squared:command
```

或使用自然语言：
```
"向我的技能添加一个名为 process-data 的命令"
```

### 同步到市场

将技能从独立仓库同步到市场：

```bash
/skill-squared:sync
```

或使用自然语言：
```
"将我的 data-analyzer 技能同步到 adrian-marketplace"
```

### 验证技能

验证技能结构和配置：

```bash
/skill-squared:validate
```

或使用自然语言：
```
"验证我的技能结构"
```

## 功能

- **完整项目生成**：使用模板创建完全配置的技能项目
- **命令管理**：轻松创建和注册斜杠命令
- **市场同步**：将技能同步到市场仓库
- **验证**：全面的结构和配置验证
- **模板系统**：可定制的模板与变量替换
- **双仓库模式**：独立开发 + 市场分发

## 架构

Skill-Squared 遵循**双仓库模式**：

### 独立仓库（开发）
- 完整技能实现
- 独立版本控制
- 自包含安装
- 开发和测试

### 市场仓库（分发）
- 聚合多个技能
- 仅复制 skill.md 和命令
- 用户一站式安装
- 从独立仓库同步

## 工作流程

1. **创建**技能：`/skill-squared:create`
2. **定制** `skills/{skill-name}.md` 中的技能逻辑
3. **添加命令**：`/skill-squared:command`
4. **验证**结构：`/skill-squared:validate`
5. **测试**安装：`cd skill-name && ./install.sh`
6. **同步**到市场：`/skill-squared:sync`
7. **提交**并推送两个仓库

## 文档

- **[命令参考](./docs/commands-reference.md)** - 完整命令文档
- **[模板指南](./docs/template-guide.md)** - 模板定制
- **[最佳实践](./docs/best-practices.md)** - 技能开发指南

## 配置

Skill-Squared 使用 `config/config.json` 进行：
- 验证规则（必需文件、前置字段）
- 同步设置（备份、要同步的文件）
- 模板路径和变量
- 默认值

## 许可证

MIT 许可证 - 详见 [LICENSE](./LICENSE)

---

**版本**：0.1.0
**作者**：Adrian <syfyufei@gmail.com>
**仓库**：https://github.com/syfyufei/skill-squared

*用于开发技能的技能*
