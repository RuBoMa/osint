"""Output formatting utilities."""


def format_ip(result: dict) -> str:
    """Format IP lookup results as human-readable text."""
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
