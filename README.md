# 🤖 GitHub Smart Follow Manager

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![GitHub API](https://img.shields.io/badge/GitHub-API-green.svg)](https://docs.github.com/en/rest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚀 Automate your GitHub networking with smart follow/unfollow scripts!

This repository contains two powerful Python scripts to help you manage your GitHub following list:
- 🎯 `github_smart_follow.py`: Automatically find and follow relevant developers
- 🔄 `github_unfollow.py`: Unfollow users who don't follow you back

---

## 📋 Prerequisites

<details>
<summary>Click to expand</summary>

1. 🐍 Python 3.6 or higher
2. 📦 Required library:
```bash
pip install requests
```

3. 🔑 GitHub Personal Access Token:
   - Go to [GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)](https://github.com/settings/tokens)
   - Generate a new token with `user` and `follow` permissions
   - Save the token somewhere safe (you'll only see it once)

</details>

---

## 🎯 Smart Follow Script (`github_smart_follow.py`)

> Find and follow developers matching your interests!

### 🎨 Target Interests
- 📊 Data Science
- 🧠 Machine Learning
- 🌐 Web Development
- 📈 Data Analysis
- 🐍 Python Development
- 💻 JavaScript Development
- 🔧 Full Stack Development
- 🤖 AI Engineering

### ✨ Features
- 🔍 Finds active users (active in the last month)
- 🎯 Avoids following users you already follow
- ⚖️ Smart filtering based on follower/following ratios
- 🚀 Bulk following with optimal delays
- 🛡️ Respects GitHub API rate limits

### 📝 Usage
1. Run the script:
```bash
python github_smart_follow.py
```

2. 🔑 Enter your GitHub token when prompted
3. 📊 Specify how many users to follow (recommended: 50-200)
4. 📋 Review the list of users found
5. ✅ Confirm to start following them

---

## 🔄 Unfollow Script (`github_unfollow.py`)

> Clean up your following list by removing non-followers!

### ✨ Features
- 📊 Shows detailed following/followers statistics
- 📋 Lists all users who don't follow you back
- ✅ Confirmation before any action
- 📝 Real-time feedback for each unfollow
- 📚 Handles large following lists

### 📝 Usage
1. Run the script:
```bash
python github_unfollow.py
```
2. 🔑 Enter your GitHub token when prompted
3. 📋 Review the list of non-followers
4. ✅ Confirm to unfollow them

---

## ⚠️ Important Notes

- 🚦 **Rate Limits**: GitHub API has rate limits. If hit, wait a few minutes.
- 🔒 **Token Security**: Never share your GitHub token!
- ⚡ **Bulk Actions**: Avoid following/unfollowing too many users at once.
- ⏱️ **Delays**: Built-in delays prevent API blocking.

---

## 🐛 Error Handling

Both scripts include robust error handling for:
- 🌐 Network errors
- 🚦 Rate limit exceeded
- 🔑 Invalid tokens
- 🔄 API response errors

> All errors display clear, actionable messages.

---

## 🤝 Contributing

Feel free to:
- 🍴 Fork this repository
- 🌟 Star it if you find it useful
- 🔧 Submit pull requests with improvements

---

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is open source and available under the MIT License.

---

<p align="center">
Made with ❤️ for the GitHub community
</p>
