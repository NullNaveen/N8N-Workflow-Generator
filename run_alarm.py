"""
Run a simple SSL expiry alarm now, without n8n or external credentials.

Checks certificate validity for a domain and prints an alarm message if expired.
This mirrors the workflow logic in workflows/0045_Manual_Telegram_Import_Triggered.json
but avoids Telegram creds by logging to console.
"""

import ssl
import socket
from datetime import datetime
import sys


def get_cert_expiry(hostname: str, port: int = 443) -> datetime:
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=10) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            # 'notAfter' like 'Nov  6 12:00:00 2025 GMT'
            not_after = cert.get('notAfter')
            return datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")


def main() -> int:
    domain = sys.argv[1] if len(sys.argv) > 1 else "n8n.io"
    try:
        expiry = get_cert_expiry(domain)
    except Exception as e:
        print(f"[ERROR] Failed to fetch certificate for {domain}: {e}")
        return 2

    now = datetime.utcnow()
    if expiry <= now:
        print(f"[ALARM] The certificate of the domain {domain} has expired! (expired at {expiry} UTC)")
        return 1
    else:
        remaining = expiry - now
        days = remaining.days
        print(f"[OK] Certificate valid for {domain}. Expires on {expiry} UTC ({days} days left)")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
