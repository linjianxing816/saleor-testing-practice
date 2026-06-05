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
└── manual/                   # 手动功能测试
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

## 接口自动化测试覆盖 (13 用例)

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
