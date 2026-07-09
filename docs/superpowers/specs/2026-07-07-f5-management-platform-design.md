# F5设备管理平台 - 设计文档

## 一、项目概述

### 1.1 项目背景
本平台旨在为运维人员提供F5设备的统一管理能力，支持负载均衡器（BIG-IP）和DNS设备的集中监控、配置管理、故障排查和报表分析。

### 1.2 目标用户
- **管理员**：拥有平台全部权限，负责系统配置和用户管理
- **运维人员**：拥有设备管理和配置权限，负责日常运维操作
- **只读用户**：仅拥有查看权限，用于审计和监控

### 1.3 核心功能

| 模块 | 功能 |
|------|------|
| 设备管理 | 设备注册、连接管理、集群管理（主备/N+M） |
| 设备监控 | 实时状态、性能指标、健康检查 |
| 配置管理 | 虚拟服务器、池成员、规则、证书管理 |
| 故障排查 | 日志查看、流量分析、故障定位 |
| 报表分析 | 流量统计、性能趋势、可用性报告 |
| 批量操作 | 批量配置、批量升级 |
| 权限管理 | 用户管理、角色权限、操作审计 |

---

## 二、技术架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户访问层                               │
│                      浏览器 / API客户端                          │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTP/HTTPS
┌───────────────────────▼─────────────────────────────────────────┐
│                        前端应用 (Vue 3)                          │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐        │
│  │ 设备监控   │ │ 配置管理   │ │ 故障排查   │ │ 报表分析   │        │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘        │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                      │
│  │ 批量操作   │ │ 用户管理   │ │ 系统设置   │                      │
│  └───────────┘ └───────────┘ └───────────┘                      │
└───────────────────────┬─────────────────────────────────────────┘
                        │ RESTful API
┌───────────────────────▼─────────────────────────────────────────┐
│                        后端服务 (Python/FastAPI)                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│  │ 认证模块     │ │ 设备管理模块 │ │ 监控模块     │                │
│  └─────────────┘ └─────────────┘ └─────────────┘                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│  │ 配置管理模块 │ │ 日志分析模块 │ │ 报表模块     │                │
│  └─────────────┘ └─────────────┘ └─────────────┘                │
│  ┌─────────────┐ ┌─────────────┐                                │
│  │ 批量操作模块 │ │ 权限管理模块 │                                │
│  └─────────────┘ └─────────────┘                                │
└───────────────────────┬─────────────────────────────────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
┌───▼──────┐      ┌─────▼──────┐      ┌────▼────────┐
│  MySQL   │      │ ClickHouse │      │  Redis      │
│(关系数据)│      │(时序/日志) │      │ (缓存/会话) │
└──────────┘      └────────────┘      └─────────────┘
```

### 2.2 技术选型

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 前端框架 | Vue | 3.x | 类型安全，组件化开发 |
| TypeScript | TypeScript | 5.x | 类型系统 |
| UI组件库 | Element Plus | 2.x | 企业级组件库 |
| 图表库 | ECharts | 5.x | 数据可视化 |
| 状态管理 | Pinia | 2.x | 状态管理 |
| 路由 | Vue Router | 4.x | SPA路由 |
| 构建工具 | Vite | 6.x | 快速构建 |
| 后端框架 | FastAPI | 0.115+ | 高性能API |
| ORM | SQLAlchemy | 2.x | 数据库ORM |
| 认证 | JWT | - | 无状态认证 |
| 缓存 | Redis | 7.x | 会话和缓存 |
| 关系数据库 | MySQL | 8.x | 结构化数据存储 |
| 时序数据库 | ClickHouse | 24.x | 时序数据和日志 |
| 任务队列 | Celery | 5.x | 异步任务 |
| 消息代理 | Redis | 7.x | Celery broker |

### 2.3 目录结构

```
f5-management-platform/
├── frontend/                    # 前端应用
│   ├── src/
│   │   ├── components/          # 公共组件
│   │   ├── views/               # 页面视图
│   │   ├── router/              # 路由配置
│   │   ├── stores/              # Pinia状态管理
│   │   ├── api/                 # API封装
│   │   ├── utils/               # 工具函数
│   │   └── styles/              # 全局样式
│   ├── package.json
│   └── vite.config.ts
├── backend/                     # 后端服务
│   ├── app/
│   │   ├── api/                 # API路由
│   │   ├── core/                # 核心配置
│   │   ├── models/              # 数据库模型
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # 业务逻辑
│   │   ├── utils/               # 工具函数
│   │   └── main.py              # 入口文件
│   ├── requirements.txt
│   └── Dockerfile
├── deploy/                      # 部署配置
│   ├── docker-compose.yml       # Docker Compose配置
│   └── k8s/                     # Kubernetes配置
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
└── docs/                        # 文档
    └── superpowers/
        └── specs/               # 设计文档
```

---

## 三、核心模块设计

### 3.1 设备管理模块

#### 3.1.1 设备管理

**功能：**
- 设备注册与配置
- 设备连接管理（SSH/REST API）
- 设备状态监控
- 设备详情查看

**数据模型：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | string | 设备名称 |
| type | enum | 设备类型（BIG-IP/DNS） |
| ip_address | string | 设备IP地址 |
| port | int | 管理端口 |
| username | string | 登录用户名 |
| password | string | 加密存储的密码 |
| version | string | 设备版本号 |
| status | enum | 状态（在线/离线/健康/异常） |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

#### 3.1.2 集群管理

**功能：**
- 集群创建与配置
- 集群状态监控
- 故障切换管理
- 配置同步
- 集群成员管理
- 集群性能聚合

**集群类型：**

| 类型 | 说明 |
|------|------|
| Active-Standby | 主备集群，一台主设备处理流量 |
| N+M | N台主设备+M台备用设备 |

**数据模型：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | string | 集群名称 |
| type | enum | 集群类型 |
| status | enum | 集群状态（健康/告警/故障） |
| created_at | datetime | 创建时间 |

**集群成员关系：**

| 字段 | 类型 | 说明 |
|------|------|------|
| cluster_id | int | 集群ID |
| device_id | int | 设备ID |
| role | enum | 角色（主/备） |
| priority | int | 优先级 |
| status | enum | 成员状态 |

### 3.2 监控模块

**功能：**
- 实时性能指标采集（CPU、内存、磁盘、网络）
- 健康检查状态监控
- 指标阈值告警
- 历史趋势展示

**数据模型（ClickHouse）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| device_id | int | 设备ID |
| metric_type | string | 指标类型（cpu/memory/disk/network） |
| value | float | 指标值 |
| timestamp | datetime | 采集时间 |

### 3.3 配置管理模块

**功能：**
- 虚拟服务器管理
- 池成员管理
- 规则管理（iRules）
- 证书管理与关联

**数据模型：**

**虚拟服务器：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | string | 名称 |
| device_id | int | 所属设备 |
| ip_address | string | VIP地址 |
| port | int | 端口 |
| protocol | enum | 协议（TCP/UDP/HTTP/HTTPS） |
| status | enum | 状态（启用/禁用） |

**池（Pool）：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | string | 池名称 |
| device_id | int | 所属设备 |
| load_balancing | enum | 负载均衡算法 |

**池成员：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| pool_id | int | 所属池 |
| ip_address | string | 成员IP |
| port | int | 端口 |
| status | enum | 状态（启用/禁用） |

**证书：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | string | 证书名称 |
| cert_data | text | 证书内容 |
| key_data | text | 私钥内容 |
| expires_at | datetime | 过期时间 |
| status | enum | 状态（有效/即将过期/已过期） |

### 3.4 日志分析模块

**功能：**
- 日志采集与存储
- 日志搜索与过滤
- 流量分析
- 故障定位辅助

**数据模型（ClickHouse）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| device_id | int | 设备ID |
| log_type | string | 日志类型 |
| level | enum | 日志级别（INFO/WARN/ERROR/DEBUG） |
| message | text | 日志内容 |
| timestamp | datetime | 时间戳 |

### 3.5 报表模块

**功能：**
- 流量统计报表
- 性能趋势报表
- 可用性报告
- 自定义报表

### 3.6 批量操作模块

**功能：**
- 批量配置下发
- 批量设备升级
- 批量健康检查

### 3.7 权限管理模块

**功能：**
- 用户管理
- 角色管理（管理员、运维人员、只读用户）
- 操作审计日志

**数据模型：**

**用户：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| username | string | 用户名 |
| password | string | 加密密码 |
| email | string | 邮箱 |
| role_id | int | 角色ID |
| status | enum | 状态（启用/禁用） |

**角色：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | string | 角色名称 |
| permissions | json | 权限列表 |

**操作日志：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| user_id | int | 用户ID |
| action | string | 操作类型 |
| target | string | 操作目标 |
| detail | json | 操作详情 |
| timestamp | datetime | 操作时间 |

---

## 四、API设计

### 4.1 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/logout | 用户登出 |
| GET | /api/auth/me | 获取当前用户 |

### 4.2 设备管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/devices | 获取设备列表 |
| POST | /api/devices | 创建设备 |
| GET | /api/devices/{id} | 获取设备详情 |
| PUT | /api/devices/{id} | 更新设备 |
| DELETE | /api/devices/{id} | 删除设备 |

### 4.3 集群管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/clusters | 获取集群列表 |
| POST | /api/clusters | 创建集群 |
| GET | /api/clusters/{id} | 获取集群详情 |
| PUT | /api/clusters/{id} | 更新集群 |
| DELETE | /api/clusters/{id} | 删除集群 |
| POST | /api/clusters/{id}/members | 添加集群成员 |
| DELETE | /api/clusters/{id}/members/{device_id} | 移除集群成员 |
| POST | /api/clusters/{id}/failover | 手动故障切换 |

### 4.4 监控接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/monitor/devices | 获取设备状态 |
| GET | /api/monitor/metrics/{device_id} | 获取设备指标 |
| GET | /api/monitor/alerts | 获取告警列表 |

### 4.5 配置管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/config/virtual-servers | 获取虚拟服务器列表 |
| POST | /api/config/virtual-servers | 创建虚拟服务器 |
| PUT | /api/config/virtual-servers/{id} | 更新虚拟服务器 |
| DELETE | /api/config/virtual-servers/{id} | 删除虚拟服务器 |
| GET | /api/config/pools | 获取池列表 |
| POST | /api/config/pools | 创建池 |
| GET | /api/config/certificates | 获取证书列表 |
| POST | /api/config/certificates | 上传证书 |
| POST | /api/config/certificates/{id}/associate | 关联证书 |

### 4.6 日志分析接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/logs | 查询日志 |
| GET | /api/logs/analysis | 日志分析 |

### 4.7 批量操作接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/batch/config | 批量配置下发 |
| POST | /api/batch/upgrade | 批量升级 |

### 4.8 用户管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/users | 获取用户列表 |
| POST | /api/users | 创建用户 |
| PUT | /api/users/{id} | 更新用户 |
| DELETE | /api/users/{id} | 删除用户 |

### 4.9 操作日志接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/audit/logs | 查询操作日志 |

---

## 五、部署方案

### 5.1 Docker Compose

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:pass@mysql:3306/f5_platform
      - CLICKHOUSE_URL=http://clickhouse:8123
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mysql
      - clickhouse
      - redis

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=f5_platform
    volumes:
      - mysql-data:/var/lib/mysql

  clickhouse:
    image: clickhouse/clickhouse-server:24.3
    volumes:
      - clickhouse-data:/var/lib/clickhouse

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  mysql-data:
  clickhouse-data:
  redis-data:
```

### 5.2 Kubernetes

**Deployment：**
- frontend-deployment.yaml
- backend-deployment.yaml

**Service：**
- frontend-service.yaml (NodePort/LoadBalancer)
- backend-service.yaml (ClusterIP)

**Ingress：**
- ingress.yaml (路由转发)

**ConfigMap：**
- 数据库连接配置
- 环境变量配置

**Secret：**
- 数据库密码
- JWT密钥

---

## 六、安全设计

### 6.1 认证
- JWT无状态认证
- Token过期时间设置
- 密码加密存储（bcrypt）

### 6.2 权限控制
- RBAC基于角色的权限控制
- 接口级别的权限校验
- 操作审计日志

### 6.3 数据安全
- 敏感数据加密存储
- 传输层加密（HTTPS）
- 数据库访问控制

---

## 七、性能优化

### 7.1 缓存策略
- Redis缓存设备状态
- 缓存常用配置数据
- 定时刷新缓存

### 7.2 异步处理
- Celery异步任务队列
- 批量操作异步执行
- 日志采集异步处理

### 7.3 数据库优化
- ClickHouse处理时序数据
- MySQL索引优化
- 读写分离（可选）

---

## 八、后续扩展

1. **告警通知**：集成邮件、短信、钉钉等通知渠道
2. **自动化运维**：支持自动化脚本执行
3. **多租户**：支持多租户隔离
4. **API网关**：支持API访问控制和限流
5. **CI/CD集成**：支持配置版本管理和自动化部署
