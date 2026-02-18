import requests

from src.utils.time_format import human_readable_time

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
    


def search_username(username: str) -> dict:
    username = normalize_username(username)
    results = {}

    results["github"] = github_lookup(username)

    for platform, url in PLATFORMS.items():
        if platform == "github":
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
        
    return "\n".join(output)

