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

def get_user_data(username, include_private=True):
    """
    Fetches basic user data + repo stats via GraphQL API.
    Includes total commit contributions.
    """
    headers = get_headers()
    if not headers:
        return None

    query = """
    query($username: String!) {
      user(login: $username) {
        name
        login
        followers {
          totalCount
        }
        following {
          totalCount
        }
        repositories(first: 50, ownerAffiliations: [OWNER], orderBy: {field: STARGAZERS, direction: DESC}) {
          totalCount
          nodes {
            name
            stargazers {
              totalCount
            }
            forks {
              totalCount
            }
            primaryLanguage {
              name
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
        issues {
          totalCount
        }
        pullRequests {
          totalCount
        }
        createdAt
        organizations {
          totalCount
        }
      }
    }
    """
    
    try:
        response = requests.post(
            GITHUB_GRAPHQL_URL, 
            json={'query': query, 'variables': {'username': username}}, 
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"GraphQL request failed: {response.status_code}")
            return {"error": f"GitHub API Status: {response.status_code}"}
            
        data = response.json()
        if 'errors' in data:
            print(f"GraphQL errors: {data['errors']}")
            return {"error": f"GraphQL Error: {data['errors'][0]['message']}"}
            
        user = data.get('data', {}).get('user')
        if not user:
            return {"error": "User not found in data"}

        # Process repos for stats
        repos = user['repositories']['nodes']
        total_stars = sum(repo['stargazers']['totalCount'] for repo in repos)
        total_forks = sum(repo['forks']['totalCount'] for repo in repos)
        
        languages = {}
        for repo in repos:
            if repo['primaryLanguage']:
                lang = repo['primaryLanguage']['name']
                languages[lang] = languages.get(lang, 0) + 1
                
        sorted_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))

        total_commits = user['contributionsCollection']['totalCommitContributions']
        if not include_private:
             # If private commits should be hidden, subtract restricted (private) contributions
             # Note: totalCommitContributions INCLUDES restricted/private commits if the token has access.
             restricted = user['contributionsCollection']['restrictedContributionsCount']
             total_commits = max(0, total_commits - restricted)

        stats = {
            "username": user['login'],
            "name": user['name'],
            "followers": user['followers']['totalCount'],
            "following": user['following']['totalCount'],
            "public_repos": user['repositories']['totalCount'], 
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_commits": total_commits,
            "total_issues": user['issues']['totalCount'],
            "total_prs": user['pullRequests']['totalCount'],
            "created_at": user['createdAt'],
            "total_orgs": user['organizations']['totalCount']
        }
        
        return {
            "stats": stats,
            "languages": sorted_languages
        }
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return {"error": f"Exception: {str(e)}"}

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
