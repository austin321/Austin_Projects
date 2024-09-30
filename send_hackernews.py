import requests
import json
import smtplib
import logging

TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json?'
URL = 'https://hacker-news.firebaseio.com/v0/item/'

# Reference separate credentials file with our creds in json
with open('creds.json', "r") as f:
    creds = json.load(f)

# Establish our creds and assign to variables
EMAIL = creds['email']
PASSWORD = creds['password']
RECIPIENT = EMAIL

try:
    #we want to send our email using SMTP ! 
    def send_email(news):
        s = smtplib.SMTP('smtp.gmail.com', 587)  # Specific to Gmail
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.sendmail(EMAIL, RECIPIENT, f'\n{news}')
        s.quit()
        print("Email sent successfully")
except:
    #error handling
    logging.error("Error sending email")
    exit()

#define a function that will take the results from the top 10 stories of the day
def fetch_latest():
    response = requests.get(TOP_STORIES_URL)
    result = response.json()
    return result[0:10]

latest_articles = fetch_latest()

#make a new URL based on the ID codes previously defined
def get_hackernews(story_id):
    response = requests.get(f'{URL}{story_id}.json')
    result = response.json()
    return result

#make an empty list which populates with fills with each article
stories = []
for article_id in latest_articles:
    story = get_hackernews(article_id)
    
    # Extract fields from the story
    title = story.get('title', 'No title')
    url = story.get('url', 'No URL available')
    by = story.get('by', 'Unknown author')
    score = story.get('score', 'No score')
    text = story.get('text', 'No content available')  # Get the article text
    
    # Format the content including text
    story_content = (f"Title: {title}\n"
                     f"By: {by}\n"
                     f"Score: {score}\n"
                     f"URL: {url}\n"
                     f"Content: {text}\n\n")  # Include the text content
    stories.append(story_content)

# Combine all stories into a single string
all_stories = ''.join(stories)


# Send the email with the stories
send_email(all_stories)
