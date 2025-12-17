cat > README.md << 'EOF'
# 🗳️ 总统选举投票系统

基于Django的现代化总统选举投票系统，提供完整的在线投票解决方案。

## ✨ 功能特性

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

3. 安装依赖
pip install -r requirements.txt

4. 数据库设置
python manage.py migrate
python manage.py createsuperuser

5. 创建示例数据
python manage.py create_sample_data

6. 运行开发服务器
python manage.py runserver

7. 访问地址
网站首页: http://127.0.0.1:8000/

管理后台: http://127.0.0.1:8000/admin/

API接口: http://127.0.0.1:8000/api/results/

voting_system/
├── voting_system/           # Django项目配置
├── elections/               # 主要应用
│   ├── models.py           # 数据模型
│   ├── views.py            # 视图函数
│   ├── urls.py             # URL路由
│   ├── admin.py            # 管理后台
│   ├── data.py             # 数据模型类
│   └── management/         # 自定义命令
├── templates/              # 模板文件
│   └── elections/
│       ├── base.html       # 基础模板
│       ├── index.html      # 首页
│       ├── login.html      # 登录页
│       ├── register.html   # 注册页
│       ├── results.html    # 结果页
│       └── admin.html      # 管理页
├── static/                 # 静态文件
│   └── elections/
│       └── style.css       # 样式表
└── requirements.txt        # 依赖列表

🔧 技术栈
后端框架: Django 4.2.7

前端技术: HTML5, CSS3, JavaScript, jQuery

数据库: SQLite3（开发），支持PostgreSQL/MySQL（生产）

图标库: Font Awesome 6.4.0

图表: Canvas Confetti（庆祝效果）

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
设置 DEBUG=False

配置安全的 SECRET_KEY

使用生产级数据库（PostgreSQL推荐）

配置Web服务器（Nginx + Gunicorn）

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
项目维护者：[你的名字]
项目链接：[GitHub仓库地址]

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

# 添加许可证文件
git add LICENSE

# 提交文档
git commit -m "添加项目文档和许可证

- 创建详细的README.md文档
- 添加MIT许可证文件
- 更新项目说明和安装指南"