import requests
import ipaddress

def lookup_ip(ip: str) -> dict:
    try:
        # Validate the IP address
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"[ERROR] Invalid IP address: {ip}")
        return {}
    
    # Use HTTP instead of HTTPS for free tier
    url = f"http://ip-api.com/json/{ip}"
    params = {
        "fields": "status,country,city,isp,org,as,proxy,hosting"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "success":
            return {"error": data.get("message", "Unknown error")}
        
        return {
            "ip": ip,
            "country": data.get("country"),
            "city": data.get("city"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "as": data.get("as"),
            "proxy": data.get("proxy"),
            "hosting": data.get("hosting")
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to lookup IP: {str(e)}"}

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
    )