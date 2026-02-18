import requests

from utils.time_format import human_readable_time
from urllib.parse import quote

PLATFORMS = {
    "github": "https://api.github.com/users/{}",
    "twitter": "https://api.twitter.com/2/users/by/username/{}",
    "linkedin": "https://www.linkedin.com/in/{}",
    "facebook": "https://www.facebook.com/{}",
    "instagram": "https://www.instagram.com/{}",
    "reddit": "https://www.reddit.com/user/{}",
}

def normalize_username(username: str) -> str:
    return username.lstrip("@").lower()

def check_platform(url: str) -> bool:
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False
    

def github_lookup(username: str) -> dict:
    user_url = f"https://api.github.com/users/{username}"
    events_url = f"https://api.github.com/users/{username}/events/public"

    try: 
        user_response = requests.get(user_url, timeout=5)

        if user_response.status_code != 200:
            return {"exists": False}
    
        user_data = user_response.json()

        # get latest activity
        events_response = requests.get(events_url, timeout=5)
        events = events_response.json() if events_response.status_code == 200 else []

        last_activity = None
        if events:
            last_activity = events[0].get("created_at") if events else None

        return {
            "exists": True,
            "url": user_data.get("html_url"),
            "name": user_data.get("name"),
            "bio": user_data.get("bio"),
            "followers": user_data.get("followers"),
            "public_repos": user_data.get("public_repos"),
            "last_activity": last_activity,
        }
    except requests.RequestException:
        return {"exists": False}
    
def reddit_lookup(username: str) -> dict:
    username = normalize_username(username)
    url = f"https://www.reddit.com/user/{username}/about.json"
    headers = {"User-Agent": "osint-tool/1.0"}

    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code != 200:
            return {"exists": False}

        json_data = r.json()
        data = json_data.get("data", {})

        subreddit = data.get("subreddit", {})

        profile_url = f"https://www.reddit.com{data.get('url', f'/user/{username}')}"

        return {
            "exists": True,
            "profile_url": profile_url,
            "bio": subreddit.get("public_description") or "No bio",
            "karma": data.get("total_karma", 0),
            "followers": subreddit.get("subscribers", 0),
        }
    except requests.RequestException:
        return {"exists": False}
    
def stackoverflow_lookup(username: str) -> dict:
    username = username.lstrip("@").lower()
    username_encoded = quote(username)
    url = f"https://api.stackexchange.com/2.3/users"
    params = {
        "inname": username_encoded,
        "site": "stackoverflow"
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json().get("items", [])

        # Try to find exact match ignoring case
        user = next((u for u in data if u.get("display_name", "").lower() == username.lower()), None)
        if not user:
            return {"exists": False}

        return {
            "exists": True,
            "profile_url": user.get("link"),
            "name": user.get("display_name"),
            "reputation": user.get("reputation"),
            "badges": user.get("badge_counts"),
        }
    except requests.RequestException:
        return {"exists": False}

def gitlab_lookup(username: str) -> dict:
    username = username.lstrip("@")

    url = "https://gitlab.com/api/v4/users"
    params = {"username": username}  # exact lookup

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        users = r.json()

        if not users:
            return {"exists": False}

        user = users[0]  # exact match returns single-item list

        return {
            "exists": True,
            "profile_url": user.get("web_url"),
            "name": user.get("name") or "No name",
            "bio": user.get("bio") or "No bio",
        }

    except requests.RequestException:
        return {"exists": False}

def devto_lookup(username: str) -> dict:
    username = username.lstrip("@").strip()

    url = "https://dev.to/api/users/by_username"
    params = {"url": username}

    try:
        r = requests.get(url, params=params, timeout=5)

        if r.status_code == 404:
            return {"exists": False}

        r.raise_for_status()
        user = r.json()

        return {
            "exists": True,
            "profile_url": user.get("profile_image"),
            "name": user.get("name") or "No name",
            "bio": user.get("summary") or "No bio",
        }

    except requests.RequestException:
        return {"exists": False}

def search_username(username: str) -> dict:
    username = normalize_username(username)
    results = {}

    results["github"] = github_lookup(username)
    results["reddit"] = reddit_lookup(username)
    results["stackoverflow"] = stackoverflow_lookup(username)
    results["gitlab"] = gitlab_lookup(username)
    results["devto"] = devto_lookup(username)
    
    for platform, url in PLATFORMS.items():
        if platform in ["github", "reddit", "stackoverflow", "gitlab", "hackerrank", "devto"]:
            continue

        profile_url = url.format(username)
        exists = check_platform(profile_url)

        results[platform] = {
            "exists": exists, 
            "url": profile_url if exists else None}

    return results

def format_username_results(results: dict) -> str:
    output = []

    for platform, data in results.items():
        status = "Found" if data.get("exists") else "Not Found"
        output.append(f"{platform.capitalize()}: {status}")

        if platform == "github" and data.get("exists"):
            output.append(f"  Profile URL: {data.get('url')}")
            output.append(f"  Name: {data.get('name')}")
            output.append(f"  Bio: {data.get('bio')}")
            output.append(f"  Followers: {data.get('followers')}")
            output.append(f"  Public Repos: {data.get('public_repos')}")
            output.append(f"  Last Activity: {human_readable_time(data.get('last_activity'))}")
        elif platform == "reddit" and data.get("exists"):
            output.append(f"  Profile URL: {data.get('profile_url')}")
            output.append(f"  Bio: {data.get('bio')}")
            output.append(f"  Karma: {data.get('karma')}")
            output.append(f"  Followers: {data.get('followers')}")
        elif platform == "stackoverflow" and data.get("exists"):
            output.append(f"  Profile URL: {data.get('profile_url')}")
            output.append(f"  Name: {data.get('name')}")
            output.append(f"  Reputation: {data.get('reputation')}")
            badges = data.get("badges", {})
            output.append(f"  Badges: Gold {badges.get('gold', 0)}, Silver {badges.get('silver', 0)}, Bronze {badges.get('bronze', 0)}")
        elif platform == "gitlab" and data.get("exists"):
            output.append(f"  Profile URL: {data.get('profile_url')}")
            output.append(f"  Name: {data.get('name')}")
            output.append(f"  Bio: {data.get('bio')}")
            output.append(f"  Followers: {data.get('followers')}")
        elif platform == "devto" and data.get("exists"):
            output.append(f"  Profile URL: {data.get('profile_url')}")
            output.append(f"  Name: {data.get('name')}")
            output.append(f"  Bio: {data.get('bio')}")
    return "\n".join(output)

