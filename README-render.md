# 亮哥游戏库 · Render 动态部署版

> 本版本是**带后台的完整动态版**（`/admin` 可在线增删分类和游戏，数据存 `data.json`），
> 可一键部署到 **Render**（免费，支持 Python 后端，输入网址即可访问）。

## ✨ 与静态版的区别

| 能力 | 静态版 (Vercel/Cloudflare) | **本动态版 (Render)** |
|------|--------------------------|----------------------|
| 前端页面 | ✅ | ✅ |
| `/admin` 在线管理 | ❌ | ✅ |
| 分类/游戏无限添加 | 改代码 | 后台点几下 |
| 数据持久化 | 无（改 json 重部署） | ✅ data.json 运行时读写 |
| 免费 | ✅ | ✅（750h/月，会休眠） |

---

## 🚀 部署步骤（全程手机浏览器，30 分钟）

### 第一步：把代码传到 GitHub

1. 手机浏览器开 **github.com** 或装 GitHub App → 注册/登录
2. 新建仓库 `liangge-youxiku`（Public 或 Private 都行）
3. 把本项目**所有文件**上传到仓库根目录，最终结构见下方「项目结构」
   > ⚠️ 关键：`index.html`、`server.py`、`data.json`、`render.yaml` 必须在**根目录**，别套一层文件夹

### 第二步：连 Render 部署

1. 手机浏览器开 **render.com** → 注册（建议用 GitHub 账号登录）
2. 登录后点 **New + → Web Service** → 选 **Build and deploy from a Git repository**
3. 授权 GitHub → 选中 `liangge-youxiku` 仓库
4. 配置项按下面填：

   | 字段 | 填什么 |
   |------|--------|
   | Name | `liangge-youxiku`（随意） |
   | Region | Oregon（默认） |
   | Branch | `main` |
   | **Runtime** | **Python 3** |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `python3 server.py` |
   | Plan | **Free**（免费） |

5. 点 **Create Web Service**
6. 等 2~3 分钟，日志出现 `🚀 亮哥游戏库 启动中` → 顶部给一个网址：
   ```
   https://liangge-youxiku.onrender.com
   ```
   点开就是前台，`/admin` 是后台。

> 💡 也可直接根目录的 `render.yaml`：Render 检测到后会**自动填好上面所有配置**（Blueprint 模式）。

### 第三步：验证

- 前台：`https://你的项目.onrender.com/` → 看到 15 分类 + 游戏列表
- 后台：`https://你的项目.onrender.com/admin` → 登录（默认 `admin / admin123`）
- 在线加游戏：登录后台 → 游戏管理 → 填表单保存 → 前台刷新即出现

---

## 📁 项目结构（务必与此一致）

```
liangge-youxiku/
├── server.py            # 后端（已支持 PORT 环境变量 + DATA_FILE 环境变量）
├── data.json            # 数据库（运行时自动读写，分类+游戏）
├── admin.html           # 后台页面
├── index.html           # 前台页面
├── style.css            # 样式
├── app.js               # 前台逻辑
├── games.js             # 前台游戏数据（动态版也可保留，后台为准）
├── requirements.txt     # Python 依赖（标准库，无需安装）
├── Procfile             # Render 启动：web: python3 server.py
├── render.yaml          # Render Blueprint 一键配置
├── test_render.py       # 本地验证脚本（部署前自测）
└── README-render.md     # 本文件
```

---

## ⚠️ 重要提醒

1. **默认密码必须改**：上线后第一件事，后台「站点设置」或直接改 `data.json` 里 admin 的密码（md5 值）
2. **免费版会休眠**：15 分钟无访问，服务暂停；下次访问需等 30~60 秒唤醒（正常现象）
3. **数据持久化**：Render Free 的本地磁盘**重启后可能重置** → 重要数据建议定期从后台导出，或升级付费盘
4. **备案/广告**：国内接广告联盟需备案域名 + 国内服务器，Render 在海外，仅适合测试/小流量
5. **改代码后自动部署**：推送到 GitHub 后 Render 自动重新部署（约 1 分钟）

---

## 🔧 本地自测（可选）

```bash
cd liangge-style
python3 test_render.py
# 通过: 11/11 即表示一切正常，可放心部署
```

---

## 📝 上线前必改清单

- [ ] 修改默认后台密码（admin / admin123）
- [ ] 替换 `data.json` 里的示例备案号 `京ICP备XXXXXXXX号` 为你自己的
- [ ] 把游戏 `link` 换成真实、合规的下载地址
- [ ] 检查 `games.js` 与 `data.json` 数据一致（动态版以后台 data.json 为准）
- [ ] 绑定自定义域名（可选）：Render → Settings → Custom Domains
