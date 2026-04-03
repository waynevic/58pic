"""TikTok like count scraper.

This script launches a local Playwright-controlled browser to open one or more
TikTok video URLs and extracts their like counts. It is intended for users who
already have a locally installed browser (Chromium, Firefox, or WebKit) and the
Playwright Python bindings.

Usage example:
    python tiktok_like_scraper.py --urls <url1> <url2>

See the repository README for more detailed instructions.
"""
from __future__ import annotations

import argparse
import asyncio
import csv
from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Sequence, Tuple

from playwright.async_api import Browser, Page, async_playwright, TimeoutError as PlaywrightTimeoutError

LIKE_SELECTOR = "strong[data-e2e='like-count']"
DEFAULT_TIMEOUT_MS = 20_000


@dataclass
class ScrapeResult:
    """Container for a single TikTok scrape result."""

    url: str
    raw_like_count: Optional[str]
    normalized_like_count: Optional[int]
    error: Optional[str] = None

    @property
    def status(self) -> str:
        if self.error:
            return f"error: {self.error}"
        if self.raw_like_count is None:
            return "like count not found"
        return "ok"


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Open TikTok URLs in a local browser via Playwright and extract the "
            "reported like counts."
        )
    )
    parser.add_argument(
        "--urls",
        nargs="*",
        default=None,
        help="One or more TikTok video URLs to process.",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        help=(
            "Optional path to a text file containing one TikTok URL per line. "
            "Blank lines and lines starting with # are ignored."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional CSV file where the results will be written.",
    )
    parser.add_argument(
        "--browser",
        choices=("chromium", "firefox", "webkit"),
        default="chromium",
        help="Browser engine to launch via Playwright (default: chromium).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help=(
            "Run the browser in headless mode. By default the browser window is "
            "visible so you can observe the navigation."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_MS,
        help=(
            "Maximum time in milliseconds to wait for the like counter to "
            "appear (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Optional delay in seconds between processing consecutive URLs.",
    )
    return parser.parse_args(argv)


def read_urls(args: argparse.Namespace) -> List[str]:
    urls: List[str] = []
    if args.input_file:
        if not args.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {args.input_file}")
        for line in args.input_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            urls.append(stripped)
    if args.urls:
        urls.extend(args.urls)
    unique_urls = []
    seen = set()
    for url in urls:
        if url not in seen:
            unique_urls.append(url)
            seen.add(url)
    return unique_urls


def normalize_like_count(raw_value: str) -> Optional[int]:
    if not raw_value:
        return None
    value = raw_value.strip().upper().replace(",", "")
    if not value:
        return None
    multiplier_map = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}
    match = re.fullmatch(r"([0-9]*\.?[0-9]+)([KMB])", value)
    if match:
        number, suffix = match.groups()
        try:
            return int(float(number) * multiplier_map[suffix])
        except ValueError:
            return None
    # Fallback for plain integers or decimals.
    try:
        return int(float(value))
    except ValueError:
        return None


async def extract_like_count(page: Page, url: str, timeout_ms: int) -> Tuple[Optional[str], Optional[int]]:
    try:
        await page.goto(url, wait_until="networkidle")
        element = await page.wait_for_selector(LIKE_SELECTOR, timeout=timeout_ms)
        raw_value = (await element.inner_text()).strip()
        normalized = normalize_like_count(raw_value)
        return raw_value, normalized
    except PlaywrightTimeoutError:
        return None, None
    except Exception as exc:  # noqa: BLE001 - bubble up via result object
        raise RuntimeError(str(exc)) from exc


async def scrape_urls(urls: Sequence[str], args: argparse.Namespace) -> List[ScrapeResult]:
    results: List[ScrapeResult] = []
    async with async_playwright() as p:
        browser_launcher = getattr(p, args.browser)
        browser: Browser = await browser_launcher.launch(headless=args.headless)
        try:
            page = await browser.new_page()
            for index, url in enumerate(urls, start=1):
                try:
                    raw_value, normalized = await extract_like_count(page, url, args.timeout)
                    results.append(
                        ScrapeResult(
                            url=url,
                            raw_like_count=raw_value,
                            normalized_like_count=normalized,
                        )
                    )
                except Exception as exc:  # noqa: BLE001 - we want to capture the message
                    results.append(
                        ScrapeResult(
                            url=url,
                            raw_like_count=None,
                            normalized_like_count=None,
                            error=str(exc),
                        )
                    )
                if args.delay and index < len(urls):
                    await asyncio.sleep(args.delay)
        finally:
            await browser.close()
    return results


def write_results_to_csv(results: Sequence[ScrapeResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["url", "raw_like_count", "normalized_like_count", "status"])
        for result in results:
            writer.writerow([
                result.url,
                result.raw_like_count or "",
                result.normalized_like_count if result.normalized_like_count is not None else "",
                result.status,
            ])


def display_results(results: Sequence[ScrapeResult]) -> None:
    width = max((len(result.url) for result in results), default=10)
    header = f"{'URL'.ljust(width)} | Raw Like Count | Normalized Like Count | Status"
    print(header)
    print("-" * len(header))
    for result in results:
        normalized = (
            str(result.normalized_like_count) if result.normalized_like_count is not None else ""
        )
        raw_value = result.raw_like_count or ""
        print(f"{result.url.ljust(width)} | {raw_value:>15} | {normalized:>21} | {result.status}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_arguments(argv)
    urls = read_urls(args)
    if not urls:
        print("No TikTok URLs were provided. Use --urls or --input-file to supply URLs.")
        return 1

    try:
        results = asyncio.run(scrape_urls(urls, args))
    except FileNotFoundError as exc:
        print(exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to launch browser: {exc}")
        return 1

    display_results(results)
    if args.output:
        write_results_to_csv(results, args.output)
        print(f"Results written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
