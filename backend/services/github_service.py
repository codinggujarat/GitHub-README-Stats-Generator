import requests
import os
import datetime

GITHUB_API_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_headers():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        # In production, this should probably error or use public API with strict limits
        print("Warning: GITHUB_TOKEN not found in environment.")
        return {}
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_user_data(username):
    """
    Fetches basic user data + repo stats via REST API.
    """
    headers = get_headers()
    # 1. Basic User Info
    user_url = f"{GITHUB_API_URL}/users/{username}"
    user_resp = requests.get(user_url, headers=headers)
    
    if user_resp.status_code != 200:
        return None, user_resp.status_code

    user_info = user_resp.json()
    
    # 2. Fetch Repos for language stats/stars (Handling pagination might be needed for large users, 
    # but for MVP we'll grab first 100 which is usually enough for 'top' languages)
    repos_url = f"{GITHUB_API_URL}/users/{username}/repos?per_page=100&type=owner"
    repos_resp = requests.get(repos_url, headers=headers)
    repos = repos_resp.json() if repos_resp.status_code == 200 else []

    stats = {
        "username": user_info.get("login"),
        "name": user_info.get("name"),
        "followers": user_info.get("followers"),
        "following": user_info.get("following"),
        "public_repos": user_info.get("public_repos"),
        "total_stars": sum(repo.get("stargazers_count", 0) for repo in repos),
        "total_forks": sum(repo.get("forks_count", 0) for repo in repos),
    }
    
    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
            
    # Sort languages by usage
    sorted_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))

    return {
        "stats": stats,
        "languages": sorted_languages
    }

def get_contribution_years(username):
    """
    Fetches contribution years using GraphQL (cheaper than iterating events).
    """
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    headers = get_headers()
    response = requests.post(
        GITHUB_GRAPHQL_URL, 
        json={'query': query, 'variables': {'username': username}}, 
        headers=headers
    )
    
    
    if response.status_code == 200:
        data = response.json()
        return calculate_streak_stats(data)
    return None

def calculate_streak_stats(data):
    """
    Parses GraphQL response to calculate streak stats.
    """
    try:
        weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        days = []
        for week in weeks:
            days.extend(week['contributionDays'])
            
        # Sort by date just in case
        days.sort(key=lambda x: x['date'])
        
        total_contributions = sum(d['contributionCount'] for d in days)
        
        current_streak = 0
        longest_streak = 0
        temp_streak = 0
        
        # Simple streak mech: iterate and count consecutive days > 0
        # This is a simplification; authentic streak calc needs to check "yesterday" relative to today.
        # For this demo, we'll scan the whole year or just rely on the data present.
        
        today = datetime.date.today().isoformat()
        
        for day in days:
            if day['contributionCount'] > 0:
                temp_streak += 1
            else:
                if temp_streak > longest_streak:
                    longest_streak = temp_streak
                temp_streak = 0
        
        # Check if last day (today/yesterday) has contrib for current streak
        # This is a rough approx
        if temp_streak > longest_streak:
            longest_streak = temp_streak
            
        current_streak = temp_streak if days and days[-1]['contributionCount'] > 0 else 0

        # Start/End dates (mocked for visual layout matching the image)
        start_date = days[0]['date'] if days else "Jan 1"
        end_date = days[-1]['date'] if days else "Dec 31"

        return {
            "total_contributions": total_contributions,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "start_date": start_date,
            "end_date": end_date,
            "mode": "daily" # vs weekly
        }
    except Exception as e:
        print(f"Error calculating streak: {e}")
        return {
            "total_contributions": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "start_date": "",
            "end_date": ""
        }
