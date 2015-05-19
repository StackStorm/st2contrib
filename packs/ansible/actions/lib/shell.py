from st2common.util.shell import quote_unix

__all__ = [
    'replace_args',
    'escape_args',
]


def replace_args(attribute=None):
    """
    Decorator to Apply replacements in a list of command line arguments.

    :param attribute: Class attribute name which stores replacement rules.
    :type attribute: ``str``
    :return:
    :rtype: ``callable``
    """
    def _replace_args(f):
        def _wrapper(self, *args):
            rules = getattr(self, attribute)
            if not rules:
                return f(self, *args)
            return map(lambda a: rules[a] if a in rules else a, f(self, *args))
        return _wrapper
    return _replace_args


def escape_args(attribute=None):
    """
    Decorator to Quote/Escape a list of command line arguments.
    Optionally exclude quoting for specified arguments.

    :param attribute: Optional class attribute name which stores arguments we shouldn't escape.
    :type attribute: ``str``
    :return:
    :rtype: ``callable``
    """
    def _escape_args(f):
        def _wrapper(self, *args):
            if not attribute:
                return map(quote_unix, f(self, *args))
            exclude = getattr(self, attribute)
            if not exclude:
                return map(quote_unix, f(self, *args))
            return map(lambda a: a if a.startswith(exclude) else quote_unix(a), f(self, *args))
        return _wrapper
    return _escape_args
