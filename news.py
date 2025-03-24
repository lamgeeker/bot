from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Функція для отримання футбольних новин
def get_football_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "sports",
        "q": "football",
        "apiKey": "5396ff8daa0c49fa97e42c63b16f0712"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("articles"):
        articles = data["articles"][:5]
        news_list = [f"{article['title']} - {article['url']}" for article in articles]
        return "\n".join(news_list)
    else:
        return "На жаль, не вдалося знайти новини."

# Вебхук для Dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
    
    if intent == "Футбольні новини":
        news = get_football_news()
        return jsonify({"fulfillmentText": news})
    
    return jsonify({"fulfillmentText": "Не зрозумів запит."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)