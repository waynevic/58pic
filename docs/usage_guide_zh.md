# TikTok 点赞数采集工具使用说明

本文档介绍如何在本地环境中安装并使用 `tiktok_like_scraper.py` 脚本，批量获取 TikTok 作品的点赞数。

## 1. 环境准备
1. 安装 Python 3.8 及以上版本。
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
   > 第一次安装 Playwright 时，`playwright install` 会自动下载 Chromium、Firefox、WebKit 三种浏览器驱动。若只需要其中一种，可执行 `playwright install chromium` 等定向下载命令。

## 2. 准备采集列表
- **直接在命令行传参**：
  ```bash
  python tiktok_like_scraper.py --urls https://www.tiktok.com/@user/video/123 https://www.tiktok.com/@user/video/456
  ```
- **使用文本文件批量导入**：
  1. 将多个 TikTok 作品链接逐行写入 `urls.txt`（支持 `#` 开头的注释行）。
  2. 运行脚本时带上 `--input-file urls.txt`。

## 3. 运行脚本
常见命令示例：
```bash
python tiktok_like_scraper.py \
  --input-file urls.txt \
  --output result.csv \
  --browser chromium \
  --delay 1.5
```
参数说明：
- `--browser`：选择浏览器内核，取值 `chromium` / `firefox` / `webkit`，默认 `chromium`。
- `--headless`：无界面模式，适合服务器环境；不加该参数则会显示浏览器窗口。
- `--timeout`：等待点赞数出现的最长时间（毫秒），默认 20000。
- `--delay`：访问每个链接之间的间隔时间（秒），可根据网络状况调节。
- `--output`：将结果保存为 CSV 文件，便于后续统计。

## 4. 查看结果
- 终端会打印一个表格，展示每条链接的原始点赞数、折算后的整数值以及状态信息。
- 若指定了 `--output`，会在对应路径生成 CSV 文件，字段包含 `url`、`raw_like_count`、`normalized_like_count`、`status`。

## 5. 图形界面操作（可选）
如果更习惯图形化界面，可以运行：

```bash
python tiktok_like_scraper_gui.py
```

界面功能说明：
- 将 TikTok 链接逐行粘贴到顶部文本框。
- 根据需要选择浏览器、是否无界面运行、超时时间和链接间隔。
- 点击“开始采集”启动浏览器执行任务，结果会显示在下方表格。
- 点击“导出结果”可保存 CSV 文件，字段与命令行脚本一致。

### 5.1 小白快速上手步骤
1. **第一次准备**：确保已执行 `pip install -r requirements.txt` 和 `playwright install`。若对命令行不熟悉，可在文件夹空白处按 `Shift+右键`（Windows）或在 Finder 中打开“终端”（macOS），即可在当前目录启动命令行。
2. **填写链接**：打开 `tiktok_like_scraper_gui.py` 后，将需要采集的 TikTok 作品链接逐行粘贴到左上角的大文本框中；每行一个链接，支持粘贴几十甚至上百条。
3. **点击按钮**：直接点击“开始采集”。第一次运行时 Playwright 可能会自动打开浏览器窗口下载驱动，请耐心等待。界面底部会实时刷新结果表格，弹窗提示“采集完成”后即可查看完整数据。
4. **导出 CSV**：如果需要保存文件，点击“导出结果”，选择保存路径即可生成 `csv` 文件，可用 Excel 或 WPS 打开。
5. **常见问题处理**：
   - 浏览器打不开：再次运行 `playwright install`，确保网络可访问 TikTok。
   - 需要登录或滑块验证：取消“无界面模式”，在弹出的浏览器中手动完成验证后再继续。
   - 想要重新开始：清空文本框或替换为新的链接列表，再次点击“开始采集”即可。

## 6. 常见问题
- **浏览器无法打开或提示缺少驱动**：确认已执行 `playwright install`，必要时重新安装依赖。
- **TikTok 需要登录/验证**：尝试去掉 `--headless` 参数，在可见浏览器中手动完成验证后再继续。
- **网络访问异常**：检查本地网络、VPN 或代理设置，确保可以访问 TikTok。
- **结果为空或一直等待**：适当增大 `--timeout` 值，或在命令间增加 `--delay`。

## 7. 获取帮助
执行以下命令查看所有支持的参数：
```bash
python tiktok_like_scraper.py --help
```
如仍有疑问，可将运行命令与终端输出整理后反馈。这样可以更快定位问题。
