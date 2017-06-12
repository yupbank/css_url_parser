import tinycss2
from tinycss2.ast import URLToken, AtRule
from itertools import chain, ifilter, imap
import requests
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


def parse_url_to_tokens(url):
    # todo: figure out what are the url schemas supported
    try:
       tokens, _ = tinycss2.parse_stylesheet_bytes(urlopen('http:'+url).read())
    except Exception, e:
        print e
        tokens = []
    return tokens

def _import(token):
    if isinstance(token, URLToken):
        return token.value
    elif hasattr(token, 'prelude'):
        return ifilter(None, imap(_get_url, token.prelude or []))

def import_rule(token):
    if isinstance(token, AtRule):
        return _import(token)

def _get_url(token):
    if isinstance(token, URLToken):
        return token.value
    elif hasattr(token, 'content'):
        return ifilter(None, imap(_get_url, token.content or []))

def get_url(stylesheet_str):
    tokens = tinycss2.parse_stylesheet(stylesheet_str)
    imported_url = list(chain.from_iterable(ifilter(None, map(import_rule, tokens))))
    imported_tokens = list(chain.from_iterable(ifilter(None, map(parse_url_to_tokens, imported_url))))
    return imported_url+parse_tokens(tokens+imported_tokens)

def parse_tokens(tokens):
    return list(chain.from_iterable(ifilter(None, map(_get_url, tokens))))

file_name = 'data/css_6.css'
file_name = 'data/styles.css'
#file_name = sys.argv[1]
tokens = open(file_name).read()
print get_url(tokens)
print get_url("selector { width: 123px; backgound-image: url('xxx');}")
