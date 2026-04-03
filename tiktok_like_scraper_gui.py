"""Simple Tkinter interface for the TikTok like-count scraper."""
from __future__ import annotations

import asyncio
from pathlib import Path
from tkinter import (
    END,
    N,
    S,
    E,
    W,
    BooleanVar,
    IntVar,
    StringVar,
    Text,
    Tk,
    filedialog,
    messagebox,
)
from tkinter import ttk
from types import SimpleNamespace
from typing import List

from tiktok_like_scraper import ScrapeResult, scrape_urls, write_results_to_csv


class TikTokScraperGUI:
    """Tkinter front-end that exposes a button-driven workflow for the scraper."""

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("TikTok 点赞数采集工具")
        self.root.geometry("820x600")

        self.browser_var = StringVar(value="chromium")
        self.headless_var = BooleanVar(value=False)
        self.timeout_var = IntVar(value=20000)
        self.delay_var = StringVar(value="0")

        self.results: List[ScrapeResult] = []

        self._build_layout()

    def _build_layout(self) -> None:
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.grid(row=0, column=0, sticky=(N, S, E, W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # URL input section
        url_label = ttk.Label(main_frame, text="请输入 TikTok 作品链接（每行一个）:")
        url_label.grid(row=0, column=0, sticky=W)

        self.url_text = Text(main_frame, width=80, height=8)
        self.url_text.grid(row=1, column=0, columnspan=4, sticky=(N, S, E, W), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)

        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="运行设置", padding=10)
        options_frame.grid(row=2, column=0, columnspan=4, sticky=(E, W), pady=(0, 10))

        ttk.Label(options_frame, text="浏览器内核:").grid(row=0, column=0, sticky=W)
        browser_menu = ttk.Combobox(options_frame, textvariable=self.browser_var, state="readonly")
        browser_menu["values"] = ("chromium", "firefox", "webkit")
        browser_menu.grid(row=0, column=1, sticky=W, padx=(6, 20))

        headless_check = ttk.Checkbutton(options_frame, text="无界面模式", variable=self.headless_var)
        headless_check.grid(row=0, column=2, sticky=W)

        ttk.Label(options_frame, text="超时时间(ms):").grid(row=1, column=0, sticky=W, pady=(8, 0))
        timeout_entry = ttk.Entry(options_frame, textvariable=self.timeout_var, width=10)
        timeout_entry.grid(row=1, column=1, sticky=W, pady=(8, 0))

        ttk.Label(options_frame, text="链接间隔(秒):").grid(row=1, column=2, sticky=W, pady=(8, 0))
        delay_entry = ttk.Entry(options_frame, textvariable=self.delay_var, width=8)
        delay_entry.grid(row=1, column=3, sticky=W, pady=(8, 0))

        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, sticky=E, pady=(0, 10))

        run_button = ttk.Button(button_frame, text="开始采集", command=self.on_run_clicked)
        run_button.grid(row=0, column=0, padx=(0, 10))

        save_button = ttk.Button(button_frame, text="导出结果", command=self.on_save_clicked)
        save_button.grid(row=0, column=1)

        # Results table
        tips_frame = ttk.LabelFrame(main_frame, text="使用提示", padding=10)
        tips_frame.grid(row=4, column=0, columnspan=4, sticky=(E, W), pady=(0, 10))
        tips_text = (
            "1. 第一次使用请先在命令行执行 pip install -r requirements.txt 和 "
            "playwright install。\n"
            "2. 在上方文本框粘贴 TikTok 链接（每行一个），无需额外符号。\n"
            "3. 点击“开始采集”后请等待弹窗提示完成，期间可见浏览器自动访问。\n"
            "4. 采集结束后可点击“导出结果”保存 CSV 文件，方便用 Excel 打开。"
        )
        ttk.Label(
            tips_frame,
            text=tips_text,
            justify="left",
            wraplength=760,
        ).grid(row=0, column=0, sticky=W)

        results_frame = ttk.LabelFrame(main_frame, text="采集结果", padding=10)
        results_frame.grid(row=5, column=0, columnspan=4, sticky=(N, S, E, W))
        main_frame.rowconfigure(5, weight=1)

        columns = ("url", "raw", "normalized", "status")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
        self.results_tree.heading("url", text="URL")
        self.results_tree.heading("raw", text="原始点赞数")
        self.results_tree.heading("normalized", text="标准化数值")
        self.results_tree.heading("status", text="状态")

        self.results_tree.column("url", width=320, anchor=W)
        self.results_tree.column("raw", width=110, anchor=E)
        self.results_tree.column("normalized", width=120, anchor=E)
        self.results_tree.column("status", width=160, anchor=W)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        self.results_tree.grid(row=0, column=0, sticky=(N, S, E, W))
        scrollbar.grid(row=0, column=1, sticky=(N, S))
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)

    def run(self) -> None:
        self.root.mainloop()

    def on_run_clicked(self) -> None:
        urls = self._collect_urls()
        if not urls:
            messagebox.showwarning("提示", "请至少输入一个有效的 TikTok 链接。")
            return

        try:
            delay = float(self.delay_var.get() or 0)
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("参数错误", "链接间隔必须是大于等于 0 的数字。")
            return

        args = SimpleNamespace(
            browser=self.browser_var.get(),
            headless=self.headless_var.get(),
            timeout=self.timeout_var.get(),
            delay=delay,
        )

        try:
            self.root.config(cursor="wait")
            self.root.update_idletasks()
            results = asyncio.run(scrape_urls(urls, args))
        except FileNotFoundError as exc:
            messagebox.showerror("依赖缺失", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("执行失败", f"启动浏览器时发生错误：{exc}")
            return
        finally:
            self.root.config(cursor="")

        self.results = results
        self._populate_results()
        messagebox.showinfo("完成", "采集完成！结果已显示在下方表格中。")

    def on_save_clicked(self) -> None:
        if not self.results:
            messagebox.showwarning("提示", "暂无可导出的结果，请先执行采集。")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=(("CSV 文件", "*.csv"), ("所有文件", "*.*")),
            title="保存结果"
        )
        if not file_path:
            return

        try:
            write_results_to_csv(self.results, Path(file_path))
        except Exception as exc:
            messagebox.showerror("保存失败", f"写入 CSV 时发生错误：{exc}")
            return

        messagebox.showinfo("完成", "结果已成功保存。")

    def _collect_urls(self) -> List[str]:
        raw_text = self.url_text.get("1.0", END)
        urls = [line.strip() for line in raw_text.splitlines() if line.strip()]
        return urls

    def _populate_results(self) -> None:
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for result in self.results:
            normalized = (
                str(result.normalized_like_count)
                if result.normalized_like_count is not None
                else ""
            )
            self.results_tree.insert(
                "",
                END,
                values=(result.url, result.raw_like_count or "", normalized, result.status),
            )


def main() -> None:
    app = TikTokScraperGUI()
    app.run()


if __name__ == "__main__":
    main()
