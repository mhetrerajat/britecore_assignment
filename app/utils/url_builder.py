class URLBuilder(object):
    """This class implements url builder. It generates URL based on params and base url
    given in parameter
    """

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
        """This method builds url using all parameters
        
        :param base_url: Base URL
        :type base_url: str
        :param params: The key value pair of all the parameters that to be added in request, defaults to None
        :type params: dict, optional
        :param offset: Offset , defaults to None
        :type offset: int, optional
        :param limit: Limit the number of records to return, defaults to None
        :type limit: int, optional
        :return: URL
        :rtype: str
        """
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
