import os
import sys
from dotenv import load_dotenv

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.github_service import get_user_data

load_dotenv(os.path.join('backend', '.env'))

username = 'torvalds' # Use a known user
print(f"Fetching stats for {username}...")

print("\n--- Test 1: Default (include_private=True) ---")
try:
    data = get_user_data(username, include_private=True)
    if data:
        stats = data['stats']
        print(f"Total Commits (Private Included): {stats.get('total_commits')}")
    else:
        print("Failed to fetch data.")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Test 2: Public Only (include_private=False) ---")
try:
    data = get_user_data(username, include_private=False)
    if data:
        stats = data['stats']
        print(f"Total Commits (Public Only): {stats.get('total_commits')}")
    else:
        print("Failed to fetch data.")
except Exception as e:
    print(f"Error: {e}")
