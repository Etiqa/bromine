from six.moves.urllib.parse import urlsplit, urlunsplit


def _url_with_scheme(url, scheme):
    parts = list(urlsplit(url))
    parts[0] = scheme
    return urlunsplit(parts)


def http(url):
    return _url_with_scheme(url, 'http')


def https(url):
    return _url_with_scheme(url, 'https')
