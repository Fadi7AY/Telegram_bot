from http.client import responses
from itertools import count

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TElEGRAM_TOKEN")
#api_url = f'https://api.github.com/users/{username}/repos'

def start(update, context):
    update.message.reply_text("Hi! I'm your bot.")

def echo(update, context):
    update.message.reply_text(f"You said: {update.message.text}")

# Exercise 1: Get the repositores of a user in github via api calls to github api
def get_repos(update, context):
    username = context.args[0]

    response = requests.get(f'https://api.github.com/users/{username}/repos')
    repos = response.json()
    repo_names=[]
    for repo in repos:
        repo_names.append(repo['name'])
        repo_list = "\n".join(repo_names)
        #update.message.reply_text(repo_list)

    reply_text = f"Repositories for {username}:\n\n {repo_list}"
    update.message.reply_text(reply_text)


    print(response.status_code)
#2. Add a command to get the top 10 repositores in github via api calls to github api
def get_top_10_repos(update,context):
    response = requests.get("https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc")
    repos = response.json()

    top_list=[]
    count=0
    for repo in repos['items']:
        top_list.append(f"{count+1}. {repo['full_name']}")
        count+=1
        if count == 11:
            break
        top_repos = f"\n".join(top_list)
    reply_text = f"Top 10 repos : \n\n  {top_repos}"
    update.message.reply_text(reply_text)



#3. Add a commad to get how many branches a repo has via api calls to github api
def get_branches(update, context):

    owner = context.args[0]
    repo_name=context.args[1]

    response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/branches")
    branches = response.json()

    branches_names = []
    for branch in branches:
        branches_names.append(branch['name'])
        branch_list = "\n".join(branches_names)
    if len(branches_names) > 1:
        reply_text = f"{repo_name} from {owner} has {len(branches_names)} branches :\n\n {branch_list}"
    else:
        reply_text = f"{repo_name} from {owner} has 1 branch :\n\n {branch_list}"

    update.message.reply_text(reply_text)



#4. Check if a GitHub repo has open issues and how many.
def get_open_issues(update, context):

    owner = context.args[0]
    repo_name = context.args[1]

    response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/issues?state=open")
    issues = response.json()

    issue_names = []
    for issue in issues:
        issue_names.append(issue['title'])
        issues_list = "\n".join(issue_names)
    if len(issue_names) >0 :
        reply_text = f"{repo_name} from {owner} has {len(issue_names)} open issues : \n\n {issues_list} "
        update.message.reply_text(reply_text)
    else :
        update.message.reply_text("No Open Issues\n")

#5. Check if a GitHub repo has open pull requests and how many.
def get_open_pull_requests(update, context):
    owner = context.args[0]
    repo_name = context.args[1]

    response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/pulls?state=open")
    prs = response.json()

    pr_names = []
    for pr in prs:
        pr_names.append(pr['title'])
        prs_list = "\n".join(pr_names)
    if len(pr_names) > 0:
        reply_text = f"{repo_name} from {owner} has {len(pr_names)} open PRs : \n\n {prs_list} "
        update.message.reply_text(reply_text)
    else:
        update.message.reply_text("No Open pull requests\n")

#6. Add a /weather <city> command→ Use OpenWeatherMap API to return current weather.
def get_weather(update, context):

        if not context.args:
            update.message.reply_text("Usage: /weather <city>")
            return

        city = context.args[0]
        API_KEY = os.getenv("OpenWeather")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            # Provide the API's error message if available
            error_message = data.get('message', 'Unknown error')
            update.message.reply_text(f"Failed to get weather for {city}: {error_message.capitalize()}")
            return

        weather_description = data['weather'][0]['description'].title()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']

        reply = (
            f" Weather in {city.title()}:\n"
            f"Description: {weather_description}\n"
            f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%"
        )

        update.message.reply_text(reply)


#7. Add a /joke command → Use https://official-joke-api.appspot.com/random_joke API to return a random joke.
def get_joke(update, context):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    jokes = response.json()

    full_joke = f"{jokes['setup']}\n\n{jokes['punchline']}"
    update.message.reply_text(full_joke)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("repos", get_repos))
    dp.add_handler(CommandHandler("toprepos", get_top_10_repos))
    dp.add_handler(CommandHandler("branches", get_branches))
    dp.add_handler(CommandHandler("issues", get_open_issues))
    dp.add_handler(CommandHandler("pullreq", get_open_pull_requests))
    dp.add_handler(CommandHandler("joke", get_joke))
    dp.add_handler(CommandHandler("weather", get_weather))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

