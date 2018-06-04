class Locator(object):

    def __call__(self, *element_finders):
        raise NotImplementedError

    def item(self, index):
        # TODO: DOC highlight different semantics than CSS Selectors' :nth-child pseudo-class
        return LocatorChain(self).item(index)


class LocatorBy(Locator):

    def __init__(self, value, by):
        self._value = value
        self._by = by

    def __call__(self, *element_finders):
        """element_finders may be either selenium WebDriver or selenium WebElement instances"""
        result = []
        for element_finder in element_finders:
            find_method = 'find_elements_by_{}'.format(self._by)
            find = getattr(element_finder, find_method)
            result.extend(find(self._value))
        return result


class XPath(LocatorBy):

    def __init__(self, value):
        super(XPath, self).__init__(value, 'xpath')

    def item(self, index):
        cls = type(self)
        value = '(%s)[%s]' % (self._value, index)
        return cls(value)


class _IndexLocator(Locator):

    def __init__(self, index):
        self._index = index

    def __call__(self, *element_finders):
        item = element_finders[self._index]
        return [item]

    def item(self, index):
        return NotImplementedError


class LocatorChain(Locator):

    def __init__(self, *locators):
        self._locators = locators

    def __call__(self, *element_finders):
        if not self._locators:
            return []
        result = element_finders
        for locator in self._locators:
            result = locator(result)
        return result

    def item(self, index):
        return self.add(_IndexLocator(index))

    def add(self, locator):
        locators = list(self._locators)
        locators.append(locator)
        cls = type(self)
        return cls(*locators)
