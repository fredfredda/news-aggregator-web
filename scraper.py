import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

site_url = 'https://ground.news'

home_page = requests.get(f'{site_url}/').text
soup_home_page = BeautifulSoup(home_page, 'lxml')
div_elements = soup_home_page.find_all('div', class_='group')

def get_news():
    news = dict()
    for i, title in enumerate(div_elements):
        text = title.find('h4').text if title.find('h4') else 'Failed to fetch title'
        news[i] = text
    return news

def remove_duplicates(news):
    seen = set()
    unique_news = {}
    for index, title in news.items():
        if title not in seen:
            seen.add(title)
            unique_news[index] = title
    return unique_news

def analyze_sentiments(news):
    vader = SentimentIntensityAnalyzer()
    good, neutral, bad = {}, {}, {}
    for index, title in news.items():
        score = vader.polarity_scores(title)['compound']
        if score >= 0.05:
            good[index] = title
        elif score <= -0.05:
            bad[index] = title
        else:
            neutral[index] = title
    return good, neutral, bad

def get_article_content(index):
    article_route = div_elements[index].find('a')['href']
    article_link = f'{site_url}{article_route}'
    article_page = requests.get(article_link).text
    soup = BeautifulSoup(article_page, 'lxml')
    summary_items = soup.find_all('li', class_='mb-8px')
    summary = [item.text for item in summary_items]
    title = div_elements[index].find('h4').text
    return title, summary, article_link
