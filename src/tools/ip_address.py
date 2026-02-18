import os
import requests
from dotenv import load_dotenv

load_dotenv()

IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")
ABUSE_KEY = os.getenv("ABUSEIPDB_API_KEY")

IPINFO_URL = "https://ipinfo.io/"
ABUSE_URL = "https://api.abuseipdb.com/api/v2/check"


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

    try:
        response = requests.get(ABUSE_URL, headers=headers, params=params, timeout=5)
        response.raise_for_status()  # raise error for 4xx/5xx status codes
        data = response.json().get("data", {})

        return {
            "abuse_score": data.get("abuseConfidenceScore"),
            "total_reports": data.get("totalReports"),
            "last_reported": data.get("lastReportedAt"),
        }
    except (requests.RequestException, ValueError) as e:
        # RequestException: network/timeout error
        # ValueError: JSON decode error
        return {"error": f"AbuseIPDB lookup failed: {str(e)}"}


def lookup_ip(ip: str) -> dict:
    try:
        result = {"ip": ip}
        result.update(lookup_ipinfo(ip))
        result.update(lookup_abuse(ip))
        return result
    except requests.RequestException as e:
        return {"error": str(e)}
