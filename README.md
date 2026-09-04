# NDT Proxy Scraper

[![NDT Proxy Updater](https://github.com/nguyenduytan/NDT-Proxy-Scraper/actions/workflows/update-proxies.yml/badge.svg)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/actions/workflows/update-proxies.yml)
[![GitHub stars](https://img.shields.io/github/stars/nguyenduytan/NDT-Proxy-Scraper?style=social)](https://github.com/nguyenduytan/NDT-Proxy-Scraper)
[![GitHub forks](https://img.shields.io/github/forks/nguyenduytan/NDT-Proxy-Scraper?style=social)](https://github.com/nguyenduytan/NDT-Proxy-Scraper)
[![GitHub repo size](https://img.shields.io/github/repo-size/nguyenduytan/NDT-Proxy-Scraper)](https://github.com/nguyenduytan/NDT-Proxy-Scraper)
[![Commit activity](https://img.shields.io/github/commit-activity/m/nguyenduytan/NDT-Proxy-Scraper?logo=git)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/commits/main)
[![License](https://img.shields.io/github/license/nguyenduytan/NDT-Proxy-Scraper)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/nguyenduytan/NDT-Proxy-Scraper)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/commits/main)

Automatically collects public HTTP, SOCKS4 and SOCKS5 proxy endpoints, removes duplicates, filters invalid addresses, and publishes plain-text lists maintained by **Tony Nguyen**.

<!-- AUTO-STATS:START -->
- **Total proxy:** 19,261
- **HTTP:** 10,307
- **SOCKS4:** 7,429
- **SOCKS5:** 8,115
- **Last update:** Fri, 04 Sep 2026 23:21:43 ICT
<!-- AUTO-STATS:END -->

## Download lists

Each file contains one `ip:port` entry per line after the header:

- [HTTP proxies](http.txt)
- [SOCKS4 proxies](socks4.txt)
- [SOCKS5 proxies](socks5.txt)

<!-- AUTO-DOWNLOADS:START -->
### HTTP (10,307 proxies)

```bash
curl -fsSL https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/http.txt -o http.txt
```

### SOCKS4 (7,429 proxies)

```bash
curl -fsSL https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/socks4.txt -o socks4.txt
```

### SOCKS5 (8,115 proxies)

```bash
curl -fsSL https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/socks5.txt -o socks5.txt
```

<!-- AUTO-DOWNLOADS:END -->

## Automation

GitHub Actions scrapes the configured sources every hour at minute 17 (`17 */1 * * *`, UTC). It can also be started manually from the **Actions** tab.

This repository is intentionally **scrape-only**: live proxy checking is disabled. Availability, protocol support and safety are not guaranteed.

## Run locally

```bash
python scripts/main.py --timeout 15 \
  --source "http|https://example.com/http.txt" \
  --source "socks4|https://example.com/socks4.txt" \
  --source "socks5|https://example.com/socks5.txt"
```

The source configuration is kept inside the GitHub Actions workflow and is not published as a separate source file. Sources are fetched directly; no proxy list is mirrored from another aggregator repository.

Source argument format:

```text
http|https://example.com/http.txt
socks4|https://example.com/socks4.txt
socks5|https://example.com/socks5.txt
```

## Responsible use

Public proxies may log, modify or inspect traffic and may be unstable or malicious. Never use them for credentials, sensitive data, abuse, evasion, or activity that violates applicable laws or service terms. Use this project only for lawful testing, research and automation where you have permission.

## License

Project code is released under the [MIT License](LICENSE). Individual source projects may have their own licenses and terms.
