import urllib.request, json
from .models import Quote


base_url = None

def configure_request(app):

    global base_url    
    base_url = app.config['QUOTES_API_BASE_URL']


def get_quote():

    get_quote_url = base_url

    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)

        author = get_quote_response.get('author')
        quote = get_quote_response.get('quote')

        quote_object = Quote(author,quote)

    return quote_object
