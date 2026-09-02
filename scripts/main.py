"""Fetch, normalize, optionally validate, and publish public proxy lists."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources" / "sources.txt"
LIVE_OUTPUT = ROOT / "NDT-ProxyList.txt"
RAW_OUTPUT = ROOT / "NDT-ProxyList-raw.txt"
HEADER = """# ==================================================
# NDT Proxy List
# Maintained by Tony Nguyen
# Repository: https://github.com/nguyenduytan/NDT-Proxy-Scraper
# Format: ip:port
# Updated automatically by GitHub Actions
# ==================================================
"""
PROXY_RE = re.compile(r"(?<![\w.])((?:\d{1,3}\.){3}\d{1,3}:\d{1,5})(?!\w)")


def read_sources() -> list[str]:
    return [
        line.strip()
        for line in SOURCES.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def valid_proxy(value: str) -> bool:
    try:
        host, port = value.rsplit(":", 1)
        ipaddress.ip_address(host)
        return 1 <= int(port) <= 65535
    except (ValueError, ipaddress.AddressValueError):
        return False


def fetch_proxies(url: str, timeout: int) -> set[str]:
    request = Request(
        url,
        headers={"User-Agent": "NDT-Proxy-Scraper/1.0 (+https://github.com/nguyenduytan/NDT-Proxy-Scraper)"},
    )
    with urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
    return {match for match in PROXY_RE.findall(text) if valid_proxy(match)}


def is_live(proxy: str, test_url: str, timeout: int) -> bool:
    try:
        opener = build_opener(
            ProxyHandler({"http": f"http://{proxy}", "https": f"http://{proxy}"})
        )
        request = Request(test_url, headers={"User-Agent": "NDT-Proxy-Scraper/1.0"})
        with opener.open(request, timeout=timeout) as response:
            return 200 <= response.status < 400
    except (HTTPError, URLError, TimeoutError, OSError):
        return False


def write_list(path: Path, proxies: set[str]) -> None:
    body = "\n".join(sorted(proxies, key=lambda item: tuple(map(int, item.replace(":", ".").split(".")))))
    path.write_text(HEADER + ("\n" if body else "") + body + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--test-url", default="http://httpbin.org/ip")
    args = parser.parse_args()

    found: set[str] = set()
    failed_sources = 0
    for source in read_sources():
        try:
            current = fetch_proxies(source, args.timeout)
            print(f"{source}: {len(current)} proxies")
            found.update(current)
        except requests.RequestException as exc:
            failed_sources += 1
            print(f"WARN source failed: {source} ({exc})", file=sys.stderr)

    write_list(RAW_OUTPUT, found)
    selected = found
    if args.check_live and found:
        with ThreadPoolExecutor(max_workers=64) as pool:
            results = pool.map(lambda item: is_live(item, args.test_url, args.timeout), found)
            live = {proxy for proxy, passed in zip(found, results) if passed}
        print(f"Live check: {len(live)}/{len(found)}")
        # Preserve a usable output if all checks fail because the test service is unavailable.
        if live:
            selected = live
        else:
            print("WARN no live proxy passed; publishing raw list as fallback", file=sys.stderr)

    write_list(LIVE_OUTPUT, selected)
    print(f"Published {len(selected)} proxies to {LIVE_OUTPUT.name}")
    return 0 if found or failed_sources == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
