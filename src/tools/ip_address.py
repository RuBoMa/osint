import os
import requests
import ipaddress
import socket
from dotenv import load_dotenv

load_dotenv()

IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")
ABUSE_KEY = os.getenv("ABUSEIPDB_API_KEY")

IPINFO_URL = "https://ipinfo.io/"
ABUSE_URL = "https://api.abuseipdb.com/api/v2/check"


def validate_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
def resolve_target(target: str) -> str:
    if validate_ip(target):
        return {"ip": target, "source": "ip"}
    else:
        ip = domain_to_ip(target)
        if ip:
            return {"ip": ip, "source": "domain", "domain": target}
        else:
            raise ValueError(f"Unable to resolve domain: {target}")
    
def domain_to_ip(domain: str) -> str:
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def lookup_ipinfo(ip: str) -> dict:
    response = requests.get(
        f"{IPINFO_URL}{ip}",
        params={"token": IPINFO_TOKEN},
        timeout=5,
    )

    response.raise_for_status()  # important
    data = response.json()

    # ipinfo returns "bogon" for invalid/private IPs
    if data.get("bogon"):
        return {"error": "Invalid or private IP"}

    return {
        "country": data.get("country"),
        "city": data.get("city"),
        "isp": data.get("isp"),
        "org": data.get("org"),
        "as": data.get("as"),
        "proxy": data.get("proxy"),
        "hosting": data.get("hosting"),
    }


def lookup_abuse(ip: str) -> dict:
    headers = {"Key": ABUSE_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}

    response = requests.get(ABUSE_URL, headers=headers, params=params, timeout=5)
    data = response.json().get("data", {})

    return {
        "abuse_score": data.get("abuseConfidenceScore"),
        "total_reports": data.get("totalReports"),
        "last_reported": data.get("lastReportedAt"),
    }


def lookup_ip(ip: str) -> dict:
    # if not validate_ip(ip):
    #     return {"error": f"Invalid IP address: {ip}"}

    try:
        result = {"ip": ip}
        result.update(lookup_ipinfo(ip))
        result.update(lookup_abuse(ip))
        return result
    except requests.RequestException as e:
        return {"error": str(e)}


def format_ip(result: dict) -> str:
    if "error" in result:
        return f"Error: {result['error']}"

    return (
        f"IP Address: {result.get('ip')}\n"
        f"Country: {result.get('country')}\n"
        f"City: {result.get('city')}\n"
        f"ISP: {result.get('isp')}\n"
        f"Organization: {result.get('org')}\n"
        f"AS: {result.get('as')}\n"
        f"Proxy: {'Yes' if result.get('proxy') else 'No'}\n"
        f"Hosting: {'Yes' if result.get('hosting') else 'No'}\n"
        f"Abuse Score: {result.get('abuse_score')}\n"
        f"Total Reports: {result.get('total_reports')}\n"
    )
