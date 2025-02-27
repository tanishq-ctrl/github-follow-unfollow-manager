import requests
import time

def get_following_and_followers(token):
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

def unfollow_users(users_to_unfollow, token, progress_callback=None):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    if progress_callback:
        progress_callback(f"Unfollowing {len(users_to_unfollow)} users...")
    for username in users_to_unfollow:
        response = requests.delete(
            f'https://api.github.com/user/following/{username}',
            headers=headers
        )
        if response.status_code == 204:
            if progress_callback:
                progress_callback(f"Unfollowed: {username}")
        else:
            if progress_callback:
                progress_callback(f"Failed to unfollow {username}")
        
        time.sleep(1)
