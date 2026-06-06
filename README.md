# Saleor 全流程测试实践

基于 [Saleor](https://github.com/saleor/saleor) 开源电商平台的全流程测试实践项目。

## 测试范围

| 测试类型 | 工具/技术栈 | 用例数 | 通过率 |
|---------|------------|--------|--------|
| 接口测试 | Postman + GraphQL | 10 | 100% |
| 接口自动化 | Python + requests + pytest | 13 | 100% |
| 性能测试 | Apache JMeter | 10 | 0% 错误率 |
| UI 自动化 | Python + Selenium + pytest | 5 | 100% |
| 手动功能测试 | 测试用例设计 | 15 | 100% |

## 项目结构

```
saleor-testing-practice/
├── README.md
├── postman/                  # Postman 接口测试
│   ├── Saleor GraphQL Core Practice.postman_collection.json
│   └── Saleor Local.postman_environment.json
├── automation/               # 接口自动化测试 (Python + pytest)
│   ├── tests/                # 13 个测试用例
│   ├── graphql/              # GraphQL query/mutation 定义
│   ├── clients/              # API 客户端封装
│   ├── conftest.py
│   ├── pytest.ini
│   └── requirements.txt
├── performance/              # 性能测试 (JMeter)
│   ├── 01_基础连通性测试.jmx
│   ├── 02 登录 Token 提取.jmx
│   ├── 03_Channel提取.jmx
│   ├── 04_商品列表查询.jmx
│   ├── 05_商品变体提取.jmx
│   ├── 06_Checkout创建.jmx
│   ├── 07_最小购物车链路.jmx
│   ├── 08_商品列表压测.jmx
│   ├── 09_购物车链路压测.jmx
│   ├── 10_混合业务场景压测.jmx
│   ├── report/               # HTML 性能报告
│   └── result_10.jtl
├── ui/                       # UI 自动化测试 (Selenium)
│   ├── tests/
│   │   ├── test_dashboard_open.py
│   │   ├── test_dashboard_products.py
│   │   ├── conftest.py
│   │   └── screenshots/
│   ├── config.py
│   └── requirements.txt
├── zentao/                    # 禅道测试管理截图
│   ├── 01-项目首页.png
│   ├── 02-用例列表.png
│   ├── 03-用例详情-TC001.png
│   ├── 04-缺陷列表.png
│   ├── 05-模块分类.png
│   └── 06-测试套件.png
└── manual/                    # 手动功能测试
    └── 测试用例执行总结.txt
```

## 环境搭建

```bash
# 1. 克隆 Saleor 官方仓库并启动 Docker 环境
git clone https://github.com/saleor/saleor
cd saleor && docker compose up -d

# 2. 安装接口自动化依赖
pip install -r automation/requirements.txt

# 3. 安装 UI 自动化依赖
pip install -r ui/requirements.txt
```

## 运行测试

```bash
# 接口自动化测试
cd automation && pytest -v

# UI 自动化测试
cd ui && pytest -v

# 性能测试
jmeter -n -t performance/10_混合业务场景压测.jmx -l results.jtl -e -o report/
```

## 测试亮点

- 完整的全流程测试实践，覆盖接口/性能/UI/手动
- 从零搭建 Docker 多服务测试环境（Saleor API + Dashboard + PostgreSQL + Redis）
- GraphQL 接口自动化：覆盖 query 查询、mutation 操作、token 鉴权、权限校验、错误响应
- JMeter 性能测试：从单接口连通性到完整购物车链路压测
- Selenium UI 自动化：Dashboard 登录、商品管理页面操作、截图验证
- 手动测试用例：覆盖功能、边界、异常场景

## 各模块测试说明

### 接口自动化测试 (13 用例)

用例覆盖了从基础连通性到完整购物车操作的全流程：

| 编号 | 测试内容 | 说明 |
|------|---------|------|
| API-01 | shop 基础查询 | 验证基础接口连通性 |
| API-02 | 错误字段测试 | 验证 GraphQL 错误响应 |
| API-03 | 未登录查询 channels | 验证权限控制 |
| API-04 | tokenCreate 登录 | 获取认证 token |
| API-05 | 带 token 查询 me | 验证 token 有效性 |
| API-06 | 带 token 查询 channels | 验证授权后接口访问 |
| API-07 | 提取 channel_slug | 数据提取与传递 |
| API-08 | 查询 products 商品列表 | 渠道维度商品查询 |
| API-09 | 查询商品 variants | 规格查询与 variant_id 提取 |
| API-10 | 创建 checkout | 购物车创建 |
| API-11 | 查询 checkout | 验证 checkout 存在 |
| API-12 | 更新 checkout 数量 | 修改购物车商品数量 |
| API-13 | 删除 checkout 商品行 | 购物车行删除 |

用例设计思路：从前到后模拟真实用户操作链路，每个步骤的数据传递到下一个步骤，形成完整的端到端接口测试流程。

### 性能测试 (10 个场景)

使用 JMeter 覆盖了从单接口调试到混合业务压测的完整压测场景：

| 编号 | 场景 | 说明 |
|------|------|------|
| JM-01 | 基础连通性测试 | 验证接口可达性 |
| JM-02 | 登录 Token 提取 | 正则提取 token 供后续使用 |
| JM-03 | Channel 提取 | JSON 提取 channel_slug |
| JM-04 | 商品列表查询 | 单接口性能基准测试 |
| JM-05 | 商品变体提取 | 提取 variant_id |
| JM-06 | Checkout 创建 | 购物车创建接口压测 |
| JM-07 | 最小购物车链路 | 登录→查商品→创建购物车串联 |
| JM-08 | 商品列表压测 | 高并发商品查询 |
| JM-09 | 购物车链路压测 | 完整购物车流程并发 |
| JM-10 | 混合业务场景压测 | 多接口混合负载 |

### UI 自动化测试 (5 用例)

基于 Selenium + pytest，验证 Saleor Dashboard 的核心操作：

| 编号 | 测试内容 | 说明 |
|------|---------|------|
| UI-01 | Dashboard 登录 | 自动登录并验证跳转成功 |
| UI-02 | Products 入口冒烟 | 验证商品管理页面可正常进入 |
| UI-03 | 创建商品弹窗 | 打开 Create Product 弹窗并截图 |
| UI-04 | 搜索输入 | 搜索框输入与清空功能验证 |
| UI-05 | 页面滚动 | 验证页面滚动到底部无异常 |

### 手动功能测试 (15 用例)

覆盖功能、边界、异常三大类场景，详见 `manual/测试用例执行总结.txt`。

### 禅道测试管理

使用禅道 22.2 开源版进行测试流程管理，覆盖用例管理、缺陷跟踪、测试套件组织：

| 管理内容 | 数量 | 说明 |
|---------|------|------|
| 项目 | 1 个 | Saleor电商平台测试（Scrum） |
| 模块 | 6 个 | 登录 / Home / Products / Categories / Orders / Customers |
| 测试用例 | 15 条 | TC001-TC015，含测试步骤 |
| 缺陷 | 3 条 | BUG-001 ~ BUG-003 |
| 测试套件 | 1 个 | 第一轮测试套件 |
| 测试单 | 1 个 | 第一轮测试 |

禅道部署在本地 Windows 环境（Apache + MySQL），通过数据库批量导入用例和缺陷数据，截图留存在 `zentao/` 目录。

---

## 总结

本项目以 Saleor 开源电商平台为测试对象，从零搭建 Docker 多服务测试环境，完整实践了软件测试的四个核心方向：

- **接口测试**：从 Postman 手工调试到 Python 自动化脚本，覆盖 GraphQL query/mutation/鉴权/权限/异常
- **性能测试**：JMeter 从单接口基准到混合业务压测，包含 HTML 可视化报告
- **UI 自动化**：Selenium 驱动 Dashboard 操作，截图留证
- **手动测试**：功能/边界/异常用例设计与执行
- **测试管理**：禅道项目管理工具，涵盖用例管理、缺陷跟踪、测试套件

五个模块互相补充，形成了一套完整的电商平台质量保障方案。
