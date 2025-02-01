import requests
import time
from getpass import getpass

def get_github_token():
    """Get GitHub personal access token from user"""
    print("You need a GitHub personal access token with 'user' and 'follow' permissions.")
    print("Create one at: https://github.com/settings/tokens")
    return getpass("Enter your GitHub personal access token: ")

def get_following_and_followers(token):
    """Get lists of users you follow and users following you"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get users you follow
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

    # Get your followers
    followers = set()
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/user/followers?page={page}&per_page=100',
            headers=headers
        )
        if not response.json():
            break
        followers.update(user['login'] for user in response.json())
        page += 1
        
    return following, followers

def unfollow_users(users_to_unfollow, token):
    """Unfollow users who don't follow back"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    print(f"\nUnfollowing {len(users_to_unfollow)} users...")
    for username in users_to_unfollow:
        response = requests.delete(
            f'https://api.github.com/user/following/{username}',
            headers=headers
        )
        if response.status_code == 204:
            print(f"Unfollowed: {username}")
        else:
            print(f"Failed to unfollow {username}")
        
        # Sleep to avoid hitting rate limits
        time.sleep(1)

def main():
    token = get_github_token()
    
    try:
        following, followers = get_following_and_followers(token)
        
        # Find users who don't follow you back
        users_to_unfollow = following - followers
        
        if not users_to_unfollow:
            print("\nEveryone you follow is following you back!")
            return
            
        print(f"\nYou follow {len(following)} users")
        print(f"You have {len(followers)} followers")
        print(f"\nUsers who don't follow you back ({len(users_to_unfollow)}):")
        for username in users_to_unfollow:
            print(f"- {username}")
            
        proceed = input("\nDo you want to unfollow these users? (y/n): ")
        if proceed.lower() == 'y':
            unfollow_users(users_to_unfollow, token)
            print("\nDone!")
        else:
            print("\nOperation cancelled.")
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main() 