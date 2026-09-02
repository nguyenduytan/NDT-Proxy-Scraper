# NDT Proxy Scraper

[![Update proxy lists](https://github.com/nguyenduytan/NDT-Proxy-Scraper/actions/workflows/update-proxies.yml/badge.svg)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/actions/workflows/update-proxies.yml)
[![License](https://img.shields.io/github/license/nguyenduytan/NDT-Proxy-Scraper)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/nguyenduytan/NDT-Proxy-Scraper)](https://github.com/nguyenduytan/NDT-Proxy-Scraper/commits/main)

Automatically collects public HTTP/HTTPS proxies, removes duplicates, optionally checks availability, and publishes a plain-text list maintained by **Tony Nguyen**.

## Download

- [Live proxy list](NDT-ProxyList.txt)
- [Raw scraped list](NDT-ProxyList-raw.txt)

Direct raw URL:

`https://raw.githubusercontent.com/nguyenduytan/NDT-Proxy-Scraper/main/NDT-ProxyList.txt`

## Automation

GitHub Actions updates the files every 6 hours at 00:00, 06:00, 12:00 and 18:00 UTC. You can also run it manually from the **Actions** tab.

The live list uses a short timeout. If no proxy passes the check, the raw list is published as a fallback so a temporary test-service outage does not erase the list.

## Run locally

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python scripts/main.py --check-live
```

Use `python scripts/main.py` to scrape without live checking. Add or remove public source URLs in `sources/sources.txt`.

## Responsible use

Sources are public and proxy availability is not guaranteed. Public proxies may log, modify, or inspect traffic. Do not use them for credentials, sensitive data, abuse, evasion, or activity that violates applicable laws or a service's terms. Use this project only for lawful testing, research, and automation where you have permission.

## License

The project code is released under the [MIT License](LICENSE). Individual proxy sources may have their own terms.

