import requests
import time
from getpass import getpass
from datetime import datetime, timedelta
import random

def get_github_token():
    """Get GitHub personal access token from user"""
    print("You need a GitHub personal access token with 'user' and 'follow' permissions.")
    print("Create one at: https://github.com/settings/tokens")
    return getpass("Enter your GitHub personal access token: ")

def get_following(token):
    """Get list of users you are currently following"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    following = set()
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/user/following?page={page}&per_page=100',
            headers=headers
        )
        if not response.json():
            break
        following.update(user['login'] for user in response.json())
        page += 1
    return following

def is_active_user(user_data):
    """Quick check if user has been active recently"""
    if not user_data.get('updated_at'):
        return False
    
    last_active = datetime.strptime(user_data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
    one_month_ago = datetime.now() - timedelta(days=30)
    return last_active > one_month_ago

def find_users_to_follow(token, max_users=200):
    """Find active users to follow based on relevant topics"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get current following list
    print("Getting your current following list...")
    current_following = get_following(token)
    print(f"You are currently following {len(current_following)} users")
    
    search_queries = [
        'data science followers:50..2000',
        'machine learning followers:50..2000',
        'web development followers:50..2000',
        'data analyst followers:50..2000',
        'python developer followers:50..2000',
        'javascript developer followers:50..2000',
        'full stack developer followers:50..2000',
        'backend developer followers:50..2000',
        'frontend developer followers:50..2000',
        'AI engineer followers:50..2000'
    ]
    
    users_to_follow = set()
    
    for query in search_queries:
        if len(users_to_follow) >= max_users:
            break
            
        print(f"\nSearching for users interested in {query}...")
        
        try:
            response = requests.get(
                f'https://api.github.com/search/users?q={query}+type:user&sort=followers&order=desc&per_page=100',
                headers=headers
            )
            
            if response.status_code == 403:
                print("Rate limit exceeded. Please wait a few minutes and try again.")
                break
            elif response.status_code != 200:
                print(f"Error searching users: {response.status_code}")
                continue
            
            for user in response.json().get('items', []):
                if len(users_to_follow) >= max_users:
                    break
                    
                username = user['login']
                if username in current_following or username in users_to_follow:
                    continue
                
                # Quick check of user profile
                user_response = requests.get(
                    f'https://api.github.com/users/{username}',
                    headers=headers
                )
                
                if user_response.status_code != 200:
                    continue
                    
                user_data = user_response.json()
                
                # Basic filtering with increased limits
                if (user_data.get('following', 0) <= 2000 and
                    user_data.get('followers', 0) <= 10000 and
                    is_active_user(user_data)):
                    users_to_follow.add(username)
                    print(f"Found user to follow: {username} (Followers: {user_data.get('followers', 0)})")
                
                time.sleep(0.25)  # Reduced delay
                
        except Exception as e:
            print(f"Error during search: {e}")
            continue
            
        time.sleep(0.5)  # Reduced delay
    
    return list(users_to_follow)

def follow_users_bulk(usernames, token):
    """Follow multiple users in bulk with minimal delay"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    success_count = 0
    
    for username in usernames:
        response = requests.put(
            f'https://api.github.com/user/following/{username}',
            headers=headers
        )
        
        if response.status_code == 204:
            success_count += 1
            print(f"Followed ({success_count}): {username}")
        else:
            print(f"Failed to follow: {username}")
        
        time.sleep(0.5)  # Minimal delay between follows
    
    return success_count

def main():
    token = get_github_token()
    max_users = int(input("Enter the maximum number of users to follow (recommended: 50-200): "))
    
    try:
        print("\nSearching for active users... This should be quick.")
        users_to_follow = find_users_to_follow(token, max_users)
        
        if not users_to_follow:
            print("\nNo suitable users found.")
            return
            
        print(f"\nFound {len(users_to_follow)} users to follow.")
        proceed = input("Do you want to follow these users? (y/n): ")
        
        if proceed.lower() == 'y':
            print("\nFollowing users in bulk...")
            success_count = follow_users_bulk(users_to_follow, token)
            print(f"\nDone! Successfully followed {success_count} users.")
        else:
            print("\nOperation cancelled.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main() 