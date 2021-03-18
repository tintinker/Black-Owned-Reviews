from flask import Flask
from flask import request
from blackownedreviews.scraping.urlscraper import get_business_urls
import blackownedreviews.scraping.reviewscraper

app = Flask(__name__)


@app.route('/urls')
def urls():
    get_business_urls(request.args.get("q"))
    return "Complete!"

@app.route('/reviews')
def reviews():
    return "Hello World!" + request.args.get("q")


if __name__ == '__main__':
    app.run(port=4949)