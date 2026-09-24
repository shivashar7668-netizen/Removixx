"""
Removix 24/7 Keep-Alive Script
-------------------------------
Sends a lightweight HTTP request to Removix every 9 minutes to keep
the server awake 24/7 and prevent Render from going to sleep after 15 minutes.

Usage:
    python keep_alive.py
"""

import logging
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("RemovixKeepAlive")

TARGET_URL = "https://removix.sanvox.in/api/health"
PING_INTERVAL_SECONDS = 540  # 9 minutes (Render sleeps after 15 minutes of inactivity)


def ping():
    req = urllib.request.Request(
        TARGET_URL,
        headers={
            "User-Agent": "Removix-24-7-Pinger/1.0",
            "Accept": "application/json",
        },
    )
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            status = response.status
            elapsed = time.time() - start_time
            logger.info("Ping success -> Status: %d OK (%.2fs) | Removix is AWAKE & ACTIVE!", status, elapsed)
            return True
    except urllib.error.HTTPError as e:
        logger.warning("HTTP notice %d: %s", e.code, e.reason)
        return True
    except Exception as e:
        logger.error("Ping error: %s", e)
        return False


def main():
    print("=" * 60)
    print("  REMOVIX 24/7 KEEP-ALIVE DAEMON")
    print(f"  Target:   {TARGET_URL}")
    print(f"  Interval: Every {PING_INTERVAL_SECONDS}s ({PING_INTERVAL_SECONDS // 60} minutes)")
    print("  Press Ctrl+C to stop.")
    print("=" * 60)

    # Initial ping on start
    ping()

    count = 1
    while True:
        try:
            time.sleep(PING_INTERVAL_SECONDS)
            count += 1
            logger.info("[Check #%d] Sending keep-alive signal...", count)
            ping()
        except KeyboardInterrupt:
            print("\nKeep-alive daemon stopped.")
            sys.exit(0)


if __name__ == "__main__":
    main()
