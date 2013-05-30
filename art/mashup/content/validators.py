# -*- coding: utf-8 -*-

from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator

from zope.i18nmessageid import MessageFactory

import re

_ = MessageFactory('art.mashup')


class areURLsValidator:
    implements(IValidator)

    name = 'areURLs'

    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        for url in value:
            if not re.match(r'(http|https)://[^\s\r\n]+', url):
                return _('urls_validation_message', u'One of the URLs is not valid')
        return 1



