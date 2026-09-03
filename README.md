# NDT Proxy Scraper

[![Update proxy lists](https://github.com/nguyenduytan/NDT-Proxy-Scraper/actions/workflows/update-proxies.yml/badge.svg)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/actions/workflows/update-proxies.yml)
[![License](https://img.shields.io/github/license/nguyenduytan/NDT-Proxy-Scraper)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/nguyenduytan/NDT-Proxy-Scraper)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/commits/main)

Automatically collects public HTTP, SOCKS4 and SOCKS5 proxy endpoints, removes duplicates, filters invalid addresses, and publishes plain-text lists maintained by **Tony Nguyen**.

## Download lists

Each file contains one `ip:port` entry per line after the header:

- [HTTP proxies](http.txt)
- [SOCKS4 proxies](socks4.txt)
- [SOCKS5 proxies](socks5.txt)

Raw URLs:

```text
https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/http.txt
https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/socks4.txt
https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/socks5.txt
```

## Automation

GitHub Actions scrapes the configured sources every 6 hours at 00:00, 06:00, 12:00 and 18:00 UTC. It can also be started manually from the **Actions** tab.

This repository is intentionally **scrape-only**: live proxy checking is disabled. Availability, protocol support and safety are not guaranteed.

## Run locally

```bash
python scripts/main.py --timeout 15 \
  --source "http|https://example.com/http.txt" \
  --source "socks4|https://example.com/socks4.txt" \
  --source "socks5|https://example.com/socks5.txt"
```

The complete source configuration is kept inside the GitHub Actions workflow and is not published as a separate source file.

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
