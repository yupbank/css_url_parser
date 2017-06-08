from tinycss2.ast import URLToken
from tinycss2.parser import parse_stylesheet
from itertools import chain, ifilter, imap

def _get_url(token):
    if isinstance(token, URLToken):
        return token.value
    elif hasattr(token, 'content'):
        return ifilter(None, imap(_get_url, token.content))

def get_url(stylesheet_str):
    return list(chain.from_iterable(ifilter(None, imap(_get_url, parse_stylesheet(stylesheet_str)))))

file_name = 'data/css_6.css'
#file_name = sys.argv[1]
tokens = open(file_name).read()
print get_url(tokens)
