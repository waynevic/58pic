# 移动端 Codex 入门教程 Web App

这是一个面向业务同学（零开发基础）的教程型网页，包含 5 个章节，讲解如何在手机上使用 Codex，并用白话解释 Git / 分支 / Commit / PR 等概念。

## 本地预览

直接双击 `index.html` 即可打开，或用任意静态服务器：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000`。

## 可以发布到 GitHub Pages（github.io）吗？

可以，已支持。你有两种方式：

### 方式 A：仓库设置里一键发布（最简单）

1. 把代码推送到 GitHub 仓库。
2. 进入仓库 **Settings → Pages**。
3. 在 **Build and deployment** 中选择：
   - **Source**: `Deploy from a branch`
   - **Branch**: `main`（或你的默认分支）
   - **Folder**: `/ (root)`
4. 保存后等待 1~3 分钟，GitHub 会生成访问地址：
   - `https://<你的用户名>.github.io/<仓库名>/`

### 方式 B：使用仓库内置 GitHub Actions 自动部署（已配置）

本仓库已提供 `.github/workflows/deploy-pages.yml`。启用步骤：

1. 将当前分支合并到 `main` 并推送。
2. 打开 GitHub 仓库的 **Actions**，确认 `Deploy static site to GitHub Pages` 工作流运行成功。
3. 进入 **Settings → Pages**，确认 Source 为 **GitHub Actions**。
4. 发布地址通常为：
   - `https://<你的用户名>.github.io/<仓库名>/`

## 目录说明

- `index.html`：教程内容结构（5 章节）
- `styles.css`：移动端优先样式
- `script.js`：章节切换 + 复制模板交互
- `.github/workflows/deploy-pages.yml`：自动发布到 GitHub Pages
