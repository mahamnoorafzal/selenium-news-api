
from flask import Flask, request, jsonify

from scraper import scrape_dawn
from summarizer import summarize_article

app = Flask(__name__)

REGISTRATION = "FA23-BDS-020"
NEWS_SOURCE = "DAWN News Pakistan"


@app.route("/")
def home():
    return f"""
    <html>
        <head>
            <title>DAWN News Automation</title>
        </head>
        <body style="font-family: Arial; text-align: center;
                     margin-top: 100px;">
            <h1>DAWN News Automation API</h1>
            <h2>Registration: {REGISTRATION}</h2>
            <p>News Source: {NEWS_SOURCE}</p>
            <p>API Endpoint: /get?keyword=AI</p>
        </body>
    </html>
    """


@app.route("/get", methods=["GET"])
def get_news():

    keyword = request.args.get("keyword", "").strip()

    if not keyword:
        return jsonify({
            "error": "Please provide a keyword."
        }), 400

    try:
        article = scrape_dawn(keyword)

        summary = summarize_article(article["text"])

        response = {
            "registration": REGISTRATION,
            "newssource": NEWS_SOURCE,
            "keyword": keyword,
            "url": article["url"],
            "summary": summary
        }

        return jsonify(response)

    except Exception as e:
        app.logger.exception("News extraction failed")

        return jsonify({
            "error": "Unable to retrieve news article.",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=False
    )
