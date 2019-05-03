class URLBuilder(object):
    def __init__(self, **kwargs):
        pass

    def _add_param(self, base_url, key, value):
        if key and value:
            base_url += "{0}={1}&".format(key, value)
        return base_url

    def _clean(self, base_url):
        if base_url.endswith("&"):
            base_url = base_url[:-1]

        return base_url

    def build(self, base_url, params=None, offset=None, limit=None):
        if any([params, offset, limit]):
            base_url += "?"

        # Add params if given
        if params:
            for key, value in params.items():
                base_url = self._add_param(base_url, key, value)

        # Add offset if given
        base_url = self._add_param(base_url, 'offset', offset)

        # Add limit if given
        base_url = self._add_param(base_url, 'limit', limit)

        return self._clean(base_url)
