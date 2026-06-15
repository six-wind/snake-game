# 🐍 贪吃蛇游戏

一个精美的贪吃蛇 PWA 游戏，支持在手机和电脑上玩，可添加到手机主屏幕，支持离线游玩。

## 🎮 玩法

- **📱 手机**: 在屏幕上滑动控制蛇的方向
- **⌨️ 电脑**: 使用方向键或 WASD 键控制
- 吃到红色食物得分，蛇身变长，速度加快
- 撞墙或撞到自己则游戏结束

## 🚀 快速部署到手机

### 方法一：GitHub Pages（免费，推荐）

1. 将整个 `snake-game` 文件夹上传到你自己的 GitHub 仓库
2. 在仓库 Settings → Pages 中启用 GitHub Pages
3. 用手机浏览器打开 `https://你的用户名.github.io/仓库名/`
4. **Android**: 浏览器会自动提示"添加到主屏幕"
5. **iPhone**: 点击浏览器底部的分享按钮 → "添加到主屏幕"

### 方法二：本地局域网部署

```bash
# 进入游戏目录
cd snake-game

# Python 方式（任选一种）
python -m http.server 8000

# 或 Node.js 方式
npx serve .
```

然后在手机上访问 `http://你的电脑IP:8000`

### 方法三：Netlify / Vercel（免费）

直接将 `snake-game` 文件夹拖到 [Netlify](https://app.netlify.com/drop) 即可部署。

## 📲 安装到手机

| 平台 | 操作 |
|------|------|
| **Android + Chrome** | 打开网址 → 点击弹出提示"添加到主屏幕" |
| **iPhone + Safari** | 打开网址 → 点击分享按钮 → "添加到主屏幕" |
| **电脑 Chrome** | 地址栏右侧点击安装图标 |

安装后可以像普通 App 一样使用，**没有网络也能玩**！

## 📁 文件说明

```
snake-game/
├── index.html          # 游戏主文件（HTML+CSS+JS）
├── manifest.json       # PWA 配置文件
├── sw.js              # Service Worker（离线缓存）
├── icons/
│   ├── icon-192.png   # 应用图标 192x192
│   └── icon-512.png   # 应用图标 512x512
└── generate_icons.py  # 图标生成脚本
```

## ✨ 特性

- 🎨 精美霓虹风格界面
- 📱 触屏滑动操控
- ⌨️ 键盘方向键支持
- 🏆 最高分本地记录
- 📳 粒子特效
- 🌐 PWA 离线支持
- 📲 可安装到主屏幕
