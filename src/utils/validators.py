import ipaddress
import socket


def validate_ip(ip: str) -> bool:
    """Check if a string is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def domain_to_ip(domain: str) -> str:
    """Resolve a domain name to an IPv4 address via DNS lookup.
    
    Returns None if resolution fails.
    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def resolve_target(target: str) -> dict:
    """Resolve target to IP address.
    
    Accepts both IP addresses and domain names.
    Returns a dict with 'ip' key and metadata ('source', 'domain').
    Returns error dict if resolution fails.
    """
    if validate_ip(target):
        return {"ip": target, "source": "ip"}
    
    ip = domain_to_ip(target)
    if ip:
        return {"ip": ip, "source": "domain", "domain": target}
    
    return {"error": f"Unable to resolve: {target}"}
