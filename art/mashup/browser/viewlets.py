# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile, BoundPageTemplate
from zope.component import getMultiAdapter
from plone.app.layout.viewlets import common
from cgi import escape
import os


# External Page

class ExternalPageTitleViewlet(common.TitleViewlet):

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request),
                                         name=u'plone_context_state')
        #page_title = escape(safe_unicode(context_state.object_title()))
        page_title = escape(safe_unicode(self.context.get_ext_title()))

        portal_title = escape(safe_unicode(portal_state.portal_title()))
        if page_title == portal_title:
            self.site_title = portal_title
        else:
            self.site_title = u"%s &mdash; %s" % (page_title, portal_title)

# Webservice Client

class WebServiceResultViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('web_service_result_viewlet.pt')

    def update(self):
        super(WebServiceResultViewlet, self).update()

    def render(self):
        alternate_template = self.context.getAlternate_template()
        if os.path.isfile(os.path.join(os.path.dirname(__file__), alternate_template)):
            template = ViewPageTemplateFile(alternate_template)
            template = BoundPageTemplate(template, self)
            return template()
        else:
            return self.index()

# XML Document

class XMLDocumentTitleViewlet(common.TitleViewlet):
    index = ViewPageTemplateFile('title.pt')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portal_title = escape(safe_unicode(portal_state.portal_title()))

        if callable(self.context.page_title) and self.context.page_title():
            page_title = escape(safe_unicode(self.context.page_title()))
        else:
            context_state = getMultiAdapter((self.context, self.request),
                             name=u'plone_context_state')
            page_title = escape(safe_unicode(context_state.object_title()))

        if page_title == portal_title:
            self.site_title = portal_title
        else:
            self.site_title = u"%s &mdash; %s" % (page_title, portal_title)


class XMLDocumentContentViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('xml_document_content_viewlet.pt')

    def update(self):
        super(XMLDocumentContentViewlet, self).update()

    def render(self):
        alternate_template = self.context.getAlternate_template()
        if os.path.isfile(os.path.join(os.path.dirname(__file__), alternate_template)):
            template = ViewPageTemplateFile(alternate_template)
            template = BoundPageTemplate(template, self)
            return template()
        else:
            return self.index()