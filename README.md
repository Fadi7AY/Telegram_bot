# Telegram Bot with GitHub, Weather, and Jokes Integration

This project is a Python Telegram bot that integrates multiple external APIs:
- GitHub API (to fetch repositories, branches, issues, pull requests, and top starred repos)
- OpenWeatherMap API (to fetch current weather for a city)
- Official Joke API (to deliver random jokes)

---

## ✨ Features

✅ `/start` → Greet the user  
✅ `/repos <username>` → List all repositories of a GitHub user  
✅ `/toprepos` → Show the top 10 most starred public repositories on GitHub  
✅ `/branches <owner> <repo>` → Show all branches in a given GitHub repository  
✅ `/issues <owner> <repo>` → Show open issues in a given GitHub repository  
✅ `/pullreq <owner> <repo>` → Show open pull requests in a given GitHub repository  
✅ `/weather <city>` → Get current weather information (requires OpenWeatherMap API key)  
✅ `/joke` → Get a random joke  

---

## 🔧 Setup

### 1️⃣ Clone the project

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
