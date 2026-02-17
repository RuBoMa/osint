import requests

def http_get(url: str, headers: dict = None, timeout: int = 10) -> str:
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return ""
