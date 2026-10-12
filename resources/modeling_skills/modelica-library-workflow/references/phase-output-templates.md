# Phase Output Templates

以下模板仅在用户请求结构化阶段记录或成套文档时按需选用。删去本轮无关章节；字段存在不授权执行加载、检查、仿真、结果读取或生成独立报告。

职责说明：

- 本文件是可选记录字段的来源；完成判定以 `acceptance-checklist.md` 为准，父级验证范围不被字段扩大
- `templates/task-output-template.md` 是将这些阶段模板拼装成一次完整任务输出的总模板
- 若后续调整字段，优先改本文件，再检查总模板是否需要同步

---

## 1. 任务识别结果

```md
## 任务识别结果
- 当前对象：
- 目标领域：
- 任务类型：
- 本轮目标：
- 交付粒度：
- 工具链：
- 中文化范围：
- 当前信息缺口：
```

---

## 2. 顶层结构方案

````md
## 顶层结构方案
- 顶层库名：
- 正式包名策略：
- 目录式 package：是 / 否
- 是否需要维护 `package.order`：是 / 否
- 顶层 package 树：

```text
<LibraryName>
  UsersGuide
  Examples
  ...
```
````

---

## 3. 公用层归位结果

```md
## 公用层归位结果
- `Interfaces`：
- `Utilities`：
- `Sources`：
- `Sensors`：
- 标准库接口迁移策略：
- 当前仍未收口的公用内容：
```

---

## 4. 业务包推进结果

```md
## 业务包推进结果
- 首个业务包：
- 是否建立 `Basics`：是 / 否
- 当前已落地内容：
- 当前未落地内容：
- 对现有结构的影响：
```

---

## 5. Examples/Tests 状态

```md
## Examples/Tests 状态
- `Examples` 入口：
- `Tests` 入口：
- 是否已分离：是 / 否
- 当前完成层级：plan-complete / files-modified / structure-level-verified / run-level-verified
- 说明：
```

---

## 6. 静态自检结果

```md
## 静态自检结果
- 顶层结构检查：通过 / 不通过
- 公用层归位检查：通过 / 不通过
- 接口规则检查：通过 / 不通过
- 图面与图标检查：通过 / 不通过
- 中文化一致性检查：通过 / 不通过
- 问题清单：
  1.
  2.
- 修复建议：
  1.
  2.
```

---

## 7. Sysplorer 验证结果

每项按实际记通过/失败；未请求为 `not_required`，已请求未执行为 `blocked`（说明未执行原因）。仅列本轮约定对象，不能把“未运行”当作骨架任务未完成。

```md
## Sysplorer 验证结果
- 顶层库加载与打开：
- `Examples` `check`：
- `Examples` `translate`：
- `Examples` 运行验证：
- `Tests` `check`：
- `Tests` `translate`：
- `Tests` 运行验证：
- 已验证范围：
- 未验证范围：
```

---

## 8. 修复记录

```md
## 修复记录
### 问题 1
- 现象：
- 问题类别：
- 根因判断：
- 修复动作：
- 修复结果：
```
