from six.moves.urllib.parse import urlsplit, urlunsplit


def _url_with_scheme(url, scheme):
    return urlunsplit(
        urlsplit(url)._replace(scheme=scheme)
    )


def http(url):
    return _url_with_scheme(url, 'http')


def https(url):
    return _url_with_scheme(url, 'https')
