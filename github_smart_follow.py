import requests
import time
import random

def get_following(token):
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

def find_and_follow_users(token, max_users=200, progress_callback=None):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    if progress_callback:
        progress_callback("Getting your current following list...")
    current_following = get_following(token)
    if progress_callback:
        progress_callback(f"You are currently following {len(current_following)} users")
    
    success_count = 0
    visited_pages = set()
    max_pages = 30  # GitHub search API pagination limit
    
    search_queries = [
        'followers:5..5000',
        'followers:5..5000 location:india',
        'followers:5..5000 location:usa',
        'followers:5..5000 language:python',
        'followers:5..5000 language:javascript',
        'followers:5..5000 created:>2023-01-01',
    ]
    
    while success_count < max_users and len(visited_pages) < max_pages:
        available_pages = set(range(1, max_pages + 1)) - visited_pages
        if not available_pages:
            break
        page = random.choice(list(available_pages))
        visited_pages.add(page)
        
        query = random.choice(search_queries)
        if progress_callback:
            progress_callback(f"Searching for users on page {page} with query: {query}...")
        
        try:
            response = requests.get(
                f'https://api.github.com/search/users?q={query}+type:user&sort=joined&order=desc&page={page}&per_page=100',
                headers=headers
            )
            
            if response.status_code == 403:
                if progress_callback:
                    progress_callback("Rate limit exceeded. Please wait a few minutes and try again.")
                break
            elif response.status_code != 200:
                if progress_callback:
                    progress_callback(f"Error searching users: {response.status_code}")
                if response.status_code == 422:
                    continue
                break
            
            results = response.json().get('items', [])
            if not results:
                if progress_callback:
                    progress_callback("No more users found on this page.")
                continue
            
            random.shuffle(results)
            
            for user in results:
                if success_count >= max_users:
                    break
                username = user['login']
                if username in current_following:
                    continue
                
                user_response = requests.get(
                    f'https://api.github.com/users/{username}',
                    headers=headers
                )
                if user_response.status_code != 200:
                    continue
                    
                user_data = user_response.json()
                following_count = user_data.get('following', 0)
                followers_count = user_data.get('followers', 0)
                
                if (following_count > followers_count and following_count <= 5000):
                    follow_response = requests.put(
                        f'https://api.github.com/user/following/{username}',
                        headers=headers
                    )
                    if follow_response.status_code == 204:
                        success_count += 1
                        if progress_callback:
                            progress_callback(f"Followed ({success_count}): {username} (Following: {following_count}, Followers: {followers_count})")
                    else:
                        if progress_callback:
                            progress_callback(f"Failed to follow: {username}")
                    
                time.sleep(0.25)
            time.sleep(0.5)
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error during search: {e}")
            continue
    return success_count
