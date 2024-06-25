import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os

def getStories():
    # URL to get the top stories IDs from Hacker News
    top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    response = requests.get(top_stories_url)
    top_story_ids = response.json()

    # Function to get the details of a story by its ID
    def get_story_details(story_id):
        story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
        story_response = requests.get(story_url)
        return story_response.json()

    # Get the details of the top 5 stories
    top_5_stories = [get_story_details(story_id) for story_id in top_story_ids[:5]]

    def scrapeContent(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text().replace("\n", "")
                
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    top5stories = [] # collects top 5 stories
    titles = [] #titles of the stories
    for i, story in enumerate(top_5_stories, start=1):
        if 'url' in story:
            top5stories.append(scrapeContent(story['url']))
        else:
            top5stories.append(story['text'])

        titles.append(story["title"])
    # print(top5stories)
    return [top5stories, titles] # array of array of stories and array of titles

def summarize(content):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing "},
            {"role": "user", "content": "Summarize this text: {}".format(content)}
        ]
    )
    
    return completion.choices[0].message.content.strip()

def main():
    info = getStories() # array of the content of top 5 articles
    storyContent, storyTitles = info[0], info[1]

    summaries = []
    for i in storyContent:
        summaries.append(summarize(i))

    print(summaries)
    return summaries

if __name__ == "__main__":
    main()