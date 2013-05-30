# -*- coding: utf-8 -*-

from Products.Five import BrowserView

# External Page

class ExternalPageView(BrowserView):
    """ External page view
    """
    #~ def __before_publishing_traverse__(self, self2, request):
        #~ request['pippo'] = 'ciao#####'

    def __call__(self):
        # Get external page content
        self.context._get_ext_content()

        return super(ExternalPageView, self).__call__()


# Web Service

class WebServiceView(BrowserView):
    """ Web service view
    """
    def __call__(self):
        # Call web service
        self.context._call_service()

        return super(WebServiceView, self).__call__()

# XML Document

class XMLDocumentView(BrowserView):
    """ XML document view
    """
    def __call__(self):
        # get document
        self.context._get_document()

        return super(XMLDocumentView, self).__call__()


