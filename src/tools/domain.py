import requests
import ssl
import socket
import time
from tools.ip_address import domain_to_ip


def enumerate_subdomains(domain: str) -> list:
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for attempt in range(3):  # retry up to 3 times
        try:
            r = requests.get(url, headers=headers, timeout=20)

            if r.status_code == 503:
                print("crt.sh rate limited. Retrying...")
                time.sleep(2)
                continue

            if r.status_code != 200:
                return []

            data = r.json()
            subdomains = set()

            for entry in data:
                name_value = entry.get("name_value")
                if not name_value:
                    continue

                for sub in name_value.split("\n"):
                    sub = sub.strip()

                    if sub.startswith("*."):
                        sub = sub[2:]

                    if sub.endswith(domain):
                        subdomains.add(sub)

            return sorted(subdomains)

        except Exception as e:
            print("Error:", e)
            time.sleep(2)

    return []

def get_ssl_info(hostname: str):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        return {
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "subject": dict(x[0] for x in cert.get("subject", [])),
            "notBefore": cert.get("notBefore"),
            "notAfter": cert.get("notAfter"),
        }

    except Exception:
        return None
    
def check_takeover(subdomain: str) -> bool:
    try:
        r = requests.get(f"http://{subdomain}", timeout=5)
        text = r.text.lower()

        takeover_signatures = [
            "no such bucket",
            "there isn't a github pages site here",
            "no such app",
            "heroku | no such app",
        ]

        return any(sig in text for sig in takeover_signatures)

    except requests.RequestException:
        return False

def domain_enum(domain: str):
    results = []
    subs = enumerate_subdomains(domain)

    for sub in subs:
        ip = domain_to_ip(sub)
        ssl_info = get_ssl_info(sub)
        takeover = check_takeover(sub)

        results.append({
            "subdomain": sub,
            "ip": ip,
            "ssl": ssl_info,
            "possible_takeover": takeover
        })

    return results