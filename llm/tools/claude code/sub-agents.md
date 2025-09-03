# sub agents

## 包含需求、架构、实现、测试、重构的agent设计

在claude code的使用中，可以定义一些sub-agents来为自己自动化完成工作。为了遵循软件开发流程和保证质量，需确保覆盖 **Discovery → Architecture → Implementation** 以及 **TDD 的 Red–Green–Refactor 循环**。

---

### 1. Discovery & Planning Phase

#### 1.1 Product Manager Agent

* **职责**：

  * 定义业务需求、目标和用户故事。
  * 确保需求符合市场和用户价值。
* **输入**：业务目标、用户调研。
* **输出**：需求文档、用户故事。

#### 1.2 Requirement Reviewer Agent

* **职责**：

  * 审查 Product Manager 的需求，验证完整性和一致性。
  * 确认需求与整体业务目标一致。
* **输入**：需求文档。
* **输出**：审核后的需求规范。

#### 1.3 Requirement & Test Translator Agent

* **职责**：

  * 将业务需求转化为 **可测试的条件与验收标准**。
  * 生成初始的测试用例大纲。
* **输入**：需求规范。
* **输出**：可测试的验收条件 (TDD: Red 阶段准备)。

---

### 2. Architecture & Design Phase

#### 2.1 Software Architect Agent

* **职责**：

  * 设计整体系统架构（技术栈、模块划分、数据模型）。
  * 明确接口和依赖关系。
* **输入**：需求规范。
* **输出**：架构设计文档。

#### 2.2 Architecture Reviewer Agent

* **职责**：

  * 审查架构设计是否符合业务目标和非功能性要求（性能、安全、可扩展性）。
* **输入**：架构设计文档。
* **输出**：确认或反馈意见。

#### 2.3 Test Designer Agent

* **职责**：

  * 基于需求与架构，编写详细的单元测试和集成测试用例。
  * 确保覆盖边界情况与异常场景。
* **输入**：需求规范 + 架构设计。
* **输出**：可执行的测试用例 (TDD: Red)。

---

### 3. Implementation Phase

#### 3.1 Backend Engineer Agent

* **职责**：

  * 实现后端业务逻辑、数据处理、数据库访问。
  * 先通过最少代码让测试用例通过。
* **输入**：测试用例 + 架构规范。
* **输出**：后端代码 (TDD: Green)。

#### 3.2 Frontend Engineer Agent

* **职责**：

  * 实现前端界面、交互和用户体验。
  * 与后端接口联调，确保功能可用。
* **输入**：测试用例 + 架构规范。
* **输出**：前端代码 (TDD: Green)。

#### 3.3 Implementation Reviewer Agent

* **职责**：

  * 审查前后端代码的逻辑正确性、可维护性和风格一致性。
* **输入**：实现代码。
* **输出**：审查报告与改进建议。

#### 3.4 Integration & Regression Tester Agent

* **职责**：

  * 自动执行跨模块集成测试。
  * 在每次迭代中进行回归测试，确保新功能未破坏旧功能。
* **输入**：全部实现代码。
* **输出**：集成测试结果 (TDD: Green)。

#### 3.5 Refactor & Code Quality Agent

* **职责**：

  * 检测代码坏味道（重复、复杂度过高、不一致命名）。
  * 给出重构建议并在修改后回归运行测试。
* **输入**：已实现的代码 + 测试结果。
* **输出**：优化后的代码 (TDD: Refactor)。

---

## Mermaid流程图
````mermaid
flowchart TD

    subgraph Discovery & Planning
        PM[1.1 Product Manager]
        RPlan[1.2 Reviewer (Planning)]
        ReqTest[1.3 Requirement & Test Translator]
    end

    subgraph Architecture & Design
        Arch[2.1 Software Architect]
        RArch[2.2 Reviewer (Architecture)]
        TDesigner[2.3 Test Designer]
    end

    subgraph Implementation
        BE[3.1 Backend Engineer]
        FE[3.2 Frontend Engineer]
        ImplRev[3.3 Reviewer (Implementation)]
        IntTest[3.4 Integration & Regression Tester]
        Refactor[3.5 Refactor & Code Quality Agent]
    end

    %% Connections
    PM --> RPlan --> ReqTest
    ReqTest --> Arch --> RArch --> TDesigner
    TDesigner --> BE --> IntTest
    TDesigner --> FE --> IntTest
    IntTest --> Refactor --> ImplRev

    %% TDD labels
    ReqTest -.->|Red| TDesigner
    BE -.->|Green| IntTest
    FE -.->|Green| IntTest
    Refactor -.->|Refactor| ImplRev
````

## Agent 与 TDD 对应关系

* **Red 阶段**：

  * Requirement & Test Translator Agent
  * Test Designer Agent

* **Green 阶段**：

  * Backend Engineer Agent
  * Frontend Engineer Agent
  * Integration & Regression Tester Agent

* **Refactor 阶段**：

  * Refactor & Code Quality Agent

## 构建agent
> mkdir -p ~/.claude/agents
> 将 agents 中的 *.md 文件复制到 ~/.claude/agents 目录下
> 重启 claude-code

## ref
* [sub-agents](https://github.com/dl-ezo/claude-code-sub-agents)
* [sub-agents doc](https://docs.anthropic.com/en/docs/claude-code/sub-agents)]