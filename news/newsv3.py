from urllib.parse import quote_plus

import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# ===== Config Section =====
rss_feeds = {
    "Google News": "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en",
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    # "CNN Top Stories": "http://rss.cnn.com/rss/edition.rss",
    # "Reuters Top News": "http://feeds.reuters.com/reuters/topNews"
    # Bangladeshi News Portals (if available)
    # "Dhaka Post": "https://www.dhakapost.com/rss",  # Confirmed
    # "Sarabangla": "https://sarabangla.net/feed/",  # WordPress-based
    # "The Daily Star": "https://www.thedailystar.net/rss",  # Confirmed
    # "BD Pratidin": "https://www.bd-pratidin.com/feed",  # WordPress-based
    # "Jagonews24": "https://www.jagonews24.com/rss",  # Confirmed
    # "Samakal": "https://samakal.com/rss",  # Confirmed
    # "somoy": "https://news.google.com/rss/search?q=somoy+tv",
    "prothom-alo": "https://www.prothomalo.com/feed",
    "bdnews24":"https://bdnews24.com/?widgetName=rssfeed&widgetId=1150&getXmlFeed=true",
}

sender_email = 'devopsdeveloper99@gmail.com'
app_password = 'rbtm xedv tbni sqae'

receiver_emails = ['fmatiq@yahoo.com', 'nazmul.nrb87@gmail.com', 'rezaaub@yahoo.com']

csv_filename = 'news/news_resultsV3.csv'


# ===========================

def get_youtube_videos(keyword, api_key):
    all_youtube_articles = []
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'q': keyword,
        'part': 'snippet',
        'type': 'video',
        'maxResults': 5,
        'key': api_key
    }

    response = requests.get(url, params=params).json()
    for item in response.get('items', []):
        title = item['snippet']['title']
        video_id = item.get('id', {}).get('videoId')
        if not video_id:
            continue
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        all_youtube_articles.append({
            'source': "Youtube",
            'keyword': keyword,
            'title': title,
            'link': video_url,
            'summary': fetch_article_summary(video_url)
        })
    return all_youtube_articles


def get_facebook_news(keyword):
    all_facebook_articles=[]
    encoded_query = quote_plus(f"{keyword} site:facebook.com")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=bn&gl=BD&ceid=BD:bn"

    feed = feedparser.parse(rss_url)

    for entry in feed.entries[:5]:
        all_facebook_articles.append({
            'source': "Facebook",
            'keyword': keyword,
            'title': entry.title,
            'link': entry.link,
            'summary': fetch_article_summary(entry.link)
        })
    return all_facebook_articles


def search_news(keywords, max_results_per_feed=5):
    print("keywords "+keywords)
    all_articles = []
    keywords = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    for keyword in keywords:
        print("keyword " + keyword)
        print("youtube...")
        all_articles.extend(get_youtube_videos(keyword, "AIzaSyAwoV63VltPHMgh2LJRZat6M6-ay-wzlr8"))
        print("facebook...")
        all_articles.extend(get_facebook_news(keyword))

        for source, feed_url_template in rss_feeds.items():
            print(f"\n🌐 Fetching articles from {source}...")

            if "{query}" in feed_url_template:
                feed_url = feed_url_template.format(query=keyword.replace(' ', '+'))
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:max_results_per_feed]:
                    all_articles.append({
                        'source': source,
                        'keyword': keyword,
                        'title': entry.title,
                        'link': entry.link,
                        'summary': fetch_article_summary(entry.link)
                    })
            else:
                feed = feedparser.parse(feed_url_template)
                for entry in feed.entries[:max_results_per_feed]:
                    print("entry "+str(entry))
                    if keyword.lower() in entry.title.lower() or keyword.lower() in (entry.get('summary', '').lower()):
                        all_articles.append({
                            'source': source,
                            'keyword': keyword,
                            'title': entry.title,
                            'link': entry.link,
                            'summary': fetch_article_summary(entry.link)
                        })

    return all_articles


def fetch_article_summary(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']

        p_tag = soup.find('p')
        if p_tag:
            return p_tag.get_text()

        return "Summary not available."
    except Exception as e:
        print(f"Error fetching article summary: {e}")
        return "Summary not available."


def save_to_csv(articles):
    df = pd.DataFrame(articles)
    df.to_csv(csv_filename, index=False)
    print(f"\n✅ Saved {len(articles)} articles to {csv_filename}")


def generate_html_body(articles):
    html = """
    <html>
    <body>
    <h2>📰 Latest News Articles based on your keywords</h2>
    <table border="1" cellspacing="0" cellpadding="8" style="border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px;">
      <thead style="background-color: #f2f2f2;">
        <tr>
          <th>#</th>
          <th>Source</th>
          <th>Keyword</th>
          <th>Title</th>
          <th>Summary</th>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
    """

    for idx, article in enumerate(articles, start=1):
        html += f"""
        <tr>
          <td>{idx}</td>
          <td>{article['source']}</td>
          <td>{article['keyword']}</td>
          <td>{article['title']}</td>
          <td>{article['summary'][:150]}...</td>
          <td><a href="{article['link']}">View Article</a></td>
        </tr>
        """

    html += """
      </tbody>
    </table>
    <p style="margin-top:20px;">Generated automatically 📬</p>
    </body>
    </html>
    """
    return html


def send_email_with_attachment(sender, password, receivers, subject, html_body, attachment_path):
    try:
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ", ".join(receivers)
        message['Subject'] = subject

        message.attach(MIMEText(html_body, 'html'))

        # Attach the CSV file
        with open(attachment_path, "rb") as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            message.attach(part)

        # SMTP Connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receivers, message.as_string())
        server.quit()

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def main():
    keywords_input = input("Enter keywords separated by commas: ")
    keywords = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]

    all_articles = search_news(keywords)

    if all_articles:
        save_to_csv(all_articles, csv_filename)

        html_body = generate_html_body(all_articles)

        send_email_choice = input("\nDo you want to send the results by email? (yes/no): ").lower()
        if send_email_choice == 'yes':
            subject = "📰 Fancy News Digest - Based on Your Keywords"
            send_email_with_attachment(sender_email, app_password, receiver_emails, subject, html_body, csv_filename)
    else:
        print("❌ No articles found.")


if __name__ == "__main__":
    main()
