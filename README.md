# 58pic Utilities

This repository now includes a TikTok like-count scraping helper that leverages
Playwright to automate a locally installed browser. The tool lets you provide
multiple TikTok video URLs and records the visible like counts for each video.

## TikTok Like Count Scraper

### Requirements
- Python 3.8 or newer
- [Playwright](https://playwright.dev/python/) Python package
- Installed browser binaries for Playwright (`playwright install`)

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

### Usage
Run the scraper by passing either individual URLs or a text file containing one
URL per line:

```bash
python tiktok_like_scraper.py --urls https://www.tiktok.com/@user/video/1234567890
```

Or with an input file and CSV output:

```bash
python tiktok_like_scraper.py \
  --input-file urls.txt \
  --output results.csv \
  --browser chromium \
  --delay 1.0
```

Useful flags:
- `--browser`: choose between `chromium`, `firefox`, or `webkit`.
- `--headless`: run the browser without a visible window.
- `--timeout`: override the maximum wait (milliseconds) for the like count to appear.
- `--delay`: pause between URLs to reduce load or avoid rate limits.

The script prints a table summarizing the raw like counts, their normalized
integer representations (when possible), and whether the scraping succeeded.
When `--output` is supplied, the same information is saved as a CSV file.

### Button-friendly desktop helper
Prefer clicking a button instead of using the command line? Launch the optional
Tkinter interface:

```bash
python tiktok_like_scraper_gui.py
```

Paste one TikTok URL per line into the text box, adjust the optional browser and
timing settings, and click **开始采集** to collect like counts. The **导出结果**
button saves the table to a CSV file using the same format as the CLI script.

### Beginner-friendly GUI quick start (Windows & macOS)
If you prefer a step-by-step checklist, follow the sequence below:

1. **Install Python** – download Python 3.8+ from [python.org](https://www.python.org/downloads/) and make sure
   the “Add to PATH” option is enabled during installation (Windows).
2. **Download the project** – click the green “Code” button on GitHub and choose
   “Download ZIP”. Extract the archive to a folder such as `C:\tiktok-scraper`.
3. **Install dependencies** – open “Command Prompt” (Windows) or “Terminal”
   (macOS), change into the project folder, and run:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
4. **Start the GUI** – still in the terminal, launch:
   ```bash
   python tiktok_like_scraper_gui.py
   ```
   A browser window may open the first time while Playwright downloads the
   required engine.
5. **Collect results** – in the GUI window:
   - Paste one TikTok video link per line into the large text box.
   - Click **开始采集** and wait for the status pop-up confirming the run has
     finished.
   - (Optional) Click **导出结果** to save a CSV file containing the like counts.

If the browser fails to start, confirm that the Playwright installation in step
3 completed without errors and that your network allows access to TikTok.

### 使用指南（中文）
> 想快速上手？请阅读更详细的[中文使用手册](docs/usage_guide_zh.md)。

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
   如果首次运行 Playwright，请执行 `playwright install` 为三大浏览器下载驱动。

2. **准备地址**
   - 可以直接在命令行通过 `--urls` 参数传入一个或多个 TikTok 作品链接。
   - 也可以将多个链接逐行写入一个文本文件（例如 `urls.txt`），然后通过 `--input-file` 读取。

3. **运行脚本**
   ```bash
   python tiktok_like_scraper.py --input-file urls.txt --output result.csv
   ```
   常用参数：
   - `--browser`：选择浏览器内核（`chromium`、`firefox` 或 `webkit`）。
   - `--headless`：无界面运行浏览器，适合服务器环境。
   - `--delay`：在访问每个链接之间增加等待时间（秒）。
   - `--timeout`：等待点赞数元素出现的最长时间（毫秒）。

4. **查看结果**
   - 终端会输出一个表格，展示原始点赞数、标准化后的数值以及每条链接的状态。
   - 如果提供了 `--output`，同样的数据会保存到指定的 CSV 文件中，方便后续整理。

5. **图形界面**
   如果希望通过按钮操作，可以运行 `python tiktok_like_scraper_gui.py` 打开桌面界面。
   - 第一次运行前，请务必完成上方的依赖安装（`pip install -r requirements.txt` 与 `playwright install`）。
   - 将 TikTok 链接逐行粘贴到文本框中。
   - 点击“开始采集”即可启动浏览器执行批量抓取，弹窗提示“采集完成”即表示执行结束。
   - 采集完成后可以通过“导出结果”按钮保存 CSV 文件。
   - 如遇浏览器无法启动，请再次确认步骤 1 的依赖已成功安装，并检查本地网络是否可访问 TikTok。

6. **故障排查**
   - 若遇到 TikTok 要求登录或验证，请在非无头模式下运行并按提示完成。
   - 确认本地网络可以正常访问 TikTok，必要时配置代理或 VPN。
