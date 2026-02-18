import requests
import ssl
import socket
# import time
from tools.ip_address import domain_to_ip

COMMON_SUBDOMAINS = [
    "www", "mail", "api", "dev", "test",
    "staging", "admin", "portal", "blog",
    "shop", "beta", "secure", "cdn",
    "static", "app", "vpn"
]

def brute_force_subdomains(domain: str) -> list:
    found = []

    for sub in COMMON_SUBDOMAINS:
        full_domain = f"{sub}.{domain}"

        try:
            socket.gethostbyname(full_domain)
            found.append(full_domain)
        except socket.gaierror:
            # Domain does not exist
            continue

    return found

# gets SSL (Secure Sockets Layer) certificate by connecting to the server and performing a TLS handshake.
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

    except (ssl.SSLError, socket.error, ConnectionRefusedError, TimeoutError) as e:
        # SSL errors, connection failures, timeouts
        return None
    except Exception as e:
        # Catch any other unexpected errors
        return None
    
def check_takeover(subdomain: str) -> bool:
    try:
        response = requests.get(f"http://{subdomain}", timeout=5)
        # Check status code to ensure we got a response body
        if response.status_code >= 400:
            return False
        
        text = response.text.lower()

        takeover_signatures = [
            "no such bucket",
            "there isn't a github pages site here",
            "no such app",
            "heroku | no such app",
        ]

        return any(sig in text for sig in takeover_signatures)

    except requests.RequestException:
        # Network error, timeout, or connection failure
        return False
    except Exception:
        # Catch any other unexpected errors
        return False

def domain_enum(domain: str):
    domain = domain.replace("https://", "").replace("http://", "")
    domain = domain.replace("www.", "")

    results = []

    # Use brute force instead of crt.sh
    subs = brute_force_subdomains(domain)

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
