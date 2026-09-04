"""Collect public proxy endpoints and publish protocol-specific text files."""

from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {"http": ROOT / "http.txt", "socks4": ROOT / "socks4.txt", "socks5": ROOT / "socks5.txt"}
PROXY_RE = re.compile(r"(?<![\w.])((?:\d{1,3}\.){3}\d{1,3}:\d{1,5})(?!\w)")


def header(protocol: str, updated: str) -> str:
    return f"""# ==================================================
# NDT {protocol.upper()} Proxy List
# Maintained by Tony Nguyen
# Repository: https://github.com/nguyenduytan/NDT-Proxy-Scraper
# Format: ip:port
# Mode: scrape-only (live checking disabled)
# Updated: {updated}
# Updated automatically by GitHub Actions
# ==================================================
"""


def parse_sources(values: list[str]) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = []
    for value in values:
        try:
            protocol, url = value.split("|", 1)
        except ValueError:
            print(f"WARN invalid source argument: {value}", file=sys.stderr)
            continue
        protocol = protocol.strip().lower()
        if protocol in OUTPUTS and url.strip():
            sources.append((protocol, url.strip()))
    return sources


def valid_proxy(value: str) -> bool:
    try:
        host, port = value.rsplit(":", 1)
        address = ipaddress.ip_address(host)
        return address.is_global and 1 <= int(port) <= 65535
    except (ValueError, ipaddress.AddressValueError):
        return False


def fetch_proxies(url: str, timeout: int) -> set[str]:
    request = Request(url, headers={"User-Agent": "NDT-Proxy-Scraper/1.0"})
    with urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
    return {match for match in PROXY_RE.findall(text) if valid_proxy(match)}


def write_list(protocol: str, proxies: set[str]) -> None:
    ordered = sorted(proxies, key=lambda item: tuple(map(int, item.replace(":", ".").split("."))))
    body = "\n".join(ordered)
    updated = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%a, %d %b %Y %H:%M:%S ICT")
    OUTPUTS[protocol].write_text(header(protocol, updated) + ("\n" if body else "") + body + "\n", encoding="utf-8")


def update_readme(grouped: dict[str, set[str]]) -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    total = len(set().union(*grouped.values()))
    updated = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%a, %d %b %Y %H:%M:%S ICT")
    rows = [
        "<!-- AUTO-STATS:START -->",
        f"- **Total proxy:** {total:,}",
        f"- **HTTP:** {len(grouped['http']):,}",
        f"- **SOCKS4:** {len(grouped['socks4']):,}",
        f"- **SOCKS5:** {len(grouped['socks5']):,}",
        f"- **Last update:** {updated}",
        "<!-- AUTO-STATS:END -->",
    ]
    block = "\n".join(rows)
    pattern = re.compile(r"<!-- AUTO-STATS:START -->.*?<!-- AUTO-STATS:END -->", re.DOTALL)
    text, replacements = pattern.subn(block, text, count=1)
    if replacements != 1:
        raise RuntimeError("README auto-stat markers are missing")
    downloads = ["<!-- AUTO-DOWNLOADS:START -->"]
    for protocol in OUTPUTS:
        filename = OUTPUTS[protocol].name
        downloads.extend([
            f"### {protocol.upper()} ({len(grouped[protocol]):,} proxies)",
            "",
            "```bash",
            f"curl -fsSL https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/{filename} -o {filename}",
            "```",
            "",
        ])
    downloads.append("<!-- AUTO-DOWNLOADS:END -->")
    download_block = "\n".join(downloads)
    download_pattern = re.compile(r"<!-- AUTO-DOWNLOADS:START -->.*?<!-- AUTO-DOWNLOADS:END -->", re.DOTALL)
    text, download_replacements = download_pattern.subn(download_block, text, count=1)
    if download_replacements != 1:
        raise RuntimeError("README auto-download markers are missing")
    readme.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape public proxies without live checking.")
    parser.add_argument("--timeout", type=int, default=15, help="Source download timeout in seconds")
    parser.add_argument("--source", action="append", default=[], metavar="PROTOCOL|URL")
    args = parser.parse_args()
    sources = parse_sources(args.source)
    if not sources:
        parser.error("at least one --source PROTOCOL|URL is required")

    grouped = {protocol: set() for protocol in OUTPUTS}
    failed = 0
    for protocol, source in sources:
        try:
            current = fetch_proxies(source, args.timeout)
            grouped[protocol].update(current)
            print(f"[{protocol}] {source}: {len(current)} proxies")
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failed += 1
            print(f"WARN source failed: {source} ({exc})", file=sys.stderr)
        except Exception as exc:
            failed += 1
            print(f"WARN unexpected source error: {source} ({exc})", file=sys.stderr)

    for protocol, proxies in grouped.items():
        write_list(protocol, proxies)
        print(f"Published {len(proxies)} {protocol} proxies to {OUTPUTS[protocol].name}")
    update_readme(grouped)
    print("Updated README statistics")
    return 0 if failed < len(sources) else 1


if __name__ == "__main__":
    raise SystemExit(main())
