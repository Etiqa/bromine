from six.moves.urllib.parse import urlsplit, urlunsplit


def url_with_given_scheme(url, scheme=None):
    if scheme is None:
        return url
    else:
        parts = list(urlsplit(url))
        parts[0] = scheme
        return urlunsplit(parts)
