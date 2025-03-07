# Instagram Real-Time Sentiment Analysis Pipeline

## 1. Install Required Libraries
```python
pip install selenium textblob pymongo pandas flask
```

## 2. Web Scraping (Instagram Comments)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.instagram.com/p/DGD6xE4v4iL/?igsh=Z3U3ZDJyem1jZTNp")
time.sleep(5)  # Allow time for page to load

# Scrape comments
comments = []
comment_elements = driver.find_elements(By.CLASS_NAME, "_a9zs")  # Adjust based on Instagram's class names
for comment in comment_elements:
    comments.append(comment.text)

driver.quit()
```

## 3. Sentiment Analysis (Using TextBlob)
```python
from textblob import TextBlob

def get_sentiment(comment):
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
comment_sentiments = [(comment, get_sentiment(comment)) for comment in comments]
```

## 4. Store Data in MongoDB
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["InstagramSentiment"]
collection = db["comments"]

data = [{"comment": c[0], "sentiment": c[1]} for c in comment_sentiments]
collection.insert_many(data)
```

## 5. Power BI Integration
- **Connect Power BI to MongoDB** using an ODBC driver or export data to CSV:
```python
import pandas as pd

data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)
df.to_csv("instagram_sentiment_data.csv", index=False)
```
- **Load CSV into Power BI** and create visuals (Pie Chart, Bar Graph, etc.).

## 6. Basic Web Interface (Flask App)
```python
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["InstagramSentiment"]
collection = db["comments"]

@app.route('/')
def index():
    comments = list(collection.find({}, {"_id": 0}))
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
```