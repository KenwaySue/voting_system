cat > README.md << 'EOF'
# 🗳️ 总统选举投票系统

一个基于 Django 开发的安全、实时的在线投票系统。该系统允许用户注册账户、参与总统选举投票、查看实时统计结果，并提供了管理后台用于管理选举和候选人。

## ✨ 功能特性
用户认证系统：完整的注册、登录、退出流程，支持会话过期自动登出。
实时投票：使用 AJAX 技术，无需刷新页面即可完成投票并即时更新数据。
安全防护：
防止重复投票（同一用户同一选举仅限一次）。
IP 地址记录。
SQL 注入防护（Django ORM）。
CSRF 跨站请求伪造防护。
结果统计：
自动计算票数百分比。
实时排序候选人与结果。
管理后台：基于 Django Admin，可视化管理选举、候选人及查看投票详情。
API 接口：提供 JSON 格式的数据接口 (/elections/api/results/)，方便第三方集成。

### 用户功能
- ✅ 用户注册与登录系统
- ✅ 候选人信息浏览
- ✅ 安全的投票系统
- ✅ 实时投票结果查看
- ✅ 响应式界面设计

### 管理功能
- ✅ 选举活动管理
- ✅ 候选人信息管理
- ✅ 投票数据统计
- ✅ 实时数据监控
- ✅ 系统日志查看

## 📋 前置要求
Python 3.8 或更高版本
pip (Python 包管理器)

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Django 4.2.7
- SQLite3（开发环境）

### 安装步骤

1. 克隆项目
```bash
git clone <你的仓库地址>
cd voting_system

2. 创建虚拟环境
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. 安装 Django
pip install django

4. 创建管理员账户
为了进入后台添加选举和候选人，你需要创建一个超级用户：
python manage.py createsuperuser

5. 运行开发服务器
python manage.py runserver

6. 访问地址
网站首页: http://127.0.0.1:8000/

管理后台: http://127.0.0.1:8000/admin/

API接口: http://127.0.0.1:8000/api/results/

voting_system/
voting_system/
├── elections/ # 主应用程序
│ ├── migrations/ # 数据库迁移文件
│ ├── static/ # 静态文件
│ │ └── elections/ # CSS, JS, 图片
│ │ └── style.css
│ ├── templates/ # HTML 模板
│ │ └── elections/ # 应用模板目录
│ │ ├── base.html # 基础模板 (导航栏/页脚)
│ │ ├── index.html # 投票主界面
│ │ ├── login.html # 登录页
│ │ ├── register.html # 注册页
│ │ └── … # 其他页面
│ ├── admin.py # 管理后台配置
│ ├── models.py # 数据模型
│ ├── urls.py # 应用路由
│ └── views.py # 视图逻辑
├── voting_system/ # 项目配置目录
│ ├── settings.py # 全局设置
│ ├── urls.py # 根路由配置
│ └── …
├── db.sqlite3 # SQLite 数据库文件 (默认不提交到 Git)
├── manage.py # Django 命令行工具
└── README.md # 项目说明文件

🔧 技术栈
1. 后端技术：
Python 3.8+: 编程语言，提供了丰富的库支持。
Django 4.x: 核心 Web 框架。
SQLite 3 (开发环境): 轻量级文件数据库，无需单独配置服务器即可运行。

2. 前端技术
HTML5: 页面结构。
CSS3: 样式设计，用于布局和美化（包括响应式设计）。
JavaScript (ES6+): 实现页面的动态交互。
JQuery: 简化 DOM 操作和 AJAX 请求。
AJAX: 实现无刷新投票体验，提升用户体验。
FontAwesome: 图标库，用于界面图标（如用户、投票、设置图标）。

3. 版本控制
Git: 用于代码版本管理和团队协作。
GitHub/GitLab: 远程代码托管平台。

⚙️ 配置说明

开发环境
1. 复制环境变量示例
cp .env.example .env

2. 修改环境变量
# .env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

生产环境

设置 DEBUG=False+ HTTPS

配置安全的 SECRET_KEY

使用生产级数据库（PostgreSQL推荐）

配置Web服务器（Nginx）

📊 数据模型
系统包含以下主要模型：

Candidate: 候选人信息

Election: 选举活动

Vote: 投票记录

User: 用户信息（扩展Django内置用户）

🔒 安全特性
用户身份验证和授权

CSRF保护

SQL注入防护

XSS防护

安全的密码存储

投票IP记录

🖥️ 界面截图
投票首页: 展示候选人信息，支持投票

结果页面: 实时显示投票统计和图表

管理后台: 系统管理和数据监控

登录/注册: 用户认证页面

🤝 贡献指南
Fork 项目

创建功能分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

创建 Pull Request

📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

📞 联系方式
项目维护者：KenwaySue
项目链接：https://github.com/KenwaySue/voting_system.git

🙏 致谢
感谢所有为这个项目提供帮助和贡献的人。
EOF

## 步骤7：添加项目文档和许可

```bash
# 添加README.md
git add README.md

# 创建许可证文件（可选）
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2023 总统选举投票系统

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
