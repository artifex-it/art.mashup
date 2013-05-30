# -*- coding: utf-8 -*-
"""Definition of the XML Document content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

# -*- Message Factory Imported Here -*-
from art.mashup import mashupMessageFactory as _

from art.mashup.interfaces import IXMLDocument
from art.mashup.config import PROJECTNAME

from art.mashup.artlib import XMLParser
import xml.dom
import urllib2
import urllib
import re


XMLDocumentSchema = document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name = 'document_url',
        required = True,
        searchable = False,
        widget = atapi.StringWidget(
            label = _('document_url_label', u'Document URL'),
            description = _('document_url_description', u'example: http://localhost:8000/default/index?lang=it'),

            size = 100,
        ),
        validators = ('isURL', ),
    ),
    atapi.StringField(
        name = 'document_encoding',
        required = True,
        default = 'utf-8',
        searchable = False,
        widget = atapi.StringWidget(
            label = _('document_encoding_label', u'Document encoding'),
            description = _('document_encoding_description', u'example values: utf-8, ascii, cp1252, iso-8859-1'),
            size = 100,
        ),
    ),
    atapi.StringField(
        name = 'page_title_tag',
        required = False,
        searchable = False,
        widget = atapi.StringWidget(
            label = _('page_title_tag_label', u'Page title tag'),
            description = _('page_title_tag_description', u'example: /elements/element/title'),
            size = 100,
        ),
    ),
    #~ atapi.StringField(
        #~ name = 'tags_to_extract',
        #~ required = False,
        #~ searchable = False,
        #~ widget = atapi.LinesWidget(
            #~ label = _('tags_to_extract_label', u'Tags to extract'),
            #~ description = _('tags_to_extract_description', u'one service parameter per line'),
            #~ size = 100,
        #~ ),
    #~ ),
    atapi.StringField(
        name = 'alternate_template',
        required = False,
        searchable = False,
        widget = atapi.StringWidget(
            label = _('alternate_template_label', u'Alternate Viewlet Template'),
            description = _('alternate_template_description', u'Relative path from directory containing  the definition of XMLDocumentContentViewlet (example ../../../../apt.visit/apt/visit/browser/templates/tpl_example.pt)'),
            size = 100,
        ),
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

XMLDocumentSchema['title'].storage = atapi.AnnotationStorage()
XMLDocumentSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(XMLDocumentSchema)

class XMLDocument(document.ATCTContent):
    """Viewing of a XML document"""
    implements(IXMLDocument)

    meta_type = "XMLDocument"
    schema = XMLDocumentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    security = ClassSecurityInfo()

    _v_doc_content = None
    _v_err = None

    security.declarePrivate('_get_document')
    def _get_document(self):
        queryString = self.REQUEST['QUERY_STRING']

        if queryString:
            if self.getDocument_encoding != '':
                queryString = urllib.unquote_plus(queryString)
                try:
                    queryString = queryString.decode('utf-8')
                    queryString = queryString.encode(self.getDocument_encoding())
                except UnicodeDecodeError:
                    pass
                queryString = urllib.quote_plus(queryString, '&=')
            queryString = re.sub('&set_language=..', '', queryString)

        # get external XML file
        if self.REQUEST.form:
            formData = urllib.urlencode(self.REQUEST.form)
        else:
            formData = urllib.urlencode('')
        try:
            docURL = self.getDocument_url()
            if queryString:
                if '?' in docURL:
                    docURL += '&' + queryString
                else:
                    docURL += '?' + queryString
            docFile = urllib2.urlopen(docURL, data=formData, timeout=30)
            #~ docFile = urllib2.urlopen(docURL, timeout=30)
            docContent = unicode(docFile.read(), self.getDocument_encoding())
            #~ docContent = docFile.read()
            docFile.close()

            self._v_doc_content = xml.dom.minidom.parseString(docContent.encode('utf-8'))
        except Exception as e:
            self._v_err = str(e)

    security.declarePrivate('getContent')
    def getContent(self):

        return self._v_doc_content

    security.declarePrivate('page_title')
    def page_title(self):

        if self.getPage_title_tag():
            tag_names = self.getPage_title_tag().split('/')
            for tag_name in tag_names:
                tag = self._v_doc_content.getElementsByTagName(tag_name)

            return tag[0].firstChild.nodeValue

        else:
            return None


atapi.registerType(XMLDocument, PROJECTNAME)






































































