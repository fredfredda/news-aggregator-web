from flask import Flask, render_template, request, redirect, url_for
from scraper import get_news, remove_duplicates, analyze_sentiments, get_article_content

app = Flask(__name__)

news_data = get_news()
news_data = remove_duplicates(news_data)
sentiment_data = analyze_sentiments(news_data)

@app.route('/')
def index():
    mood = request.args.get('mood', 'all')
    if mood == 'good':
        news = sentiment_data[0]
    elif mood == 'neutral':
        news = sentiment_data[1]
    elif mood == 'bad':
        news = sentiment_data[2]
    else:
        news = news_data
    return render_template('index.html', news=news, mood=mood)

@app.route('/article/<int:index>')
def article(index):
    title, summary, link = get_article_content(index)
    return render_template('article.html', title=title, summary=summary, link=link)

if __name__ == '__main__':
    app.run(debug=True)
