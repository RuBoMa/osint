from datetime import datetime, timezone

def human_readable_time(timestamp: str) -> str:
    """Convert ISO 8601 timestamp to human-readable 'X time ago'"""
    if not timestamp:
        return "No activity"
    
    dt = datetime.fromisoformat(timestamp.rstrip("Z")).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minutes ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hours ago"
    else:
        days = int(seconds // 86400)
        return f"{days} days ago"