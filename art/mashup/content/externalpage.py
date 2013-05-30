# -*- coding: utf-8 -*-
"""Definition of the External Page content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

# -*- Message Factory Imported Here -*-
from art.mashup import mashupMessageFactory as _
from art.mashup import artlib

from art.mashup.interfaces import IExternalPage
from art.mashup.config import PROJECTNAME

import urllib
import urllib2
import re


ExternalPageSchema = document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name = 'external_urls',
        required = True,
        searchable = False,
        widget = atapi.LinesWidget(
            label = _('external_urls_label', u'External URLs'),
            description = _('external_urls_description', u'use URL parameter _art_ext_url_ind to select the external URL, 0 is default [one URL per line]'),
            rows = 3,
            cols = 100,
        ),
        validators = ('areURLs', ),
    ),
    atapi.StringField(
        name = 'external_encoding',
        required = True,
        default = 'utf-8',
        searchable = False,
        widget = atapi.StringWidget(
            label = _('external_encoding_label', u'External encoding'),
            description = _('external_encoding_description', u'example values: utf-8, ascii, cp1252, iso-8859-1'),
            size = 100,
        ),
    ),
    atapi.StringField(
        name = 'fragments_start_tags',
        required = False,
        searchable = False,
        widget = atapi.LinesWidget(
            label = _('fragments_start_tags_label', u'Start tags of fragments to extract'),
            description = _('fragments_starts_tags_description', u'one tag per line, in render order'),
            size = 100,
        ),
    ),
    atapi.LinesField(
        name = 'options',
        required = False,
        searchable = False,
        vocabulary = [
            ('c_to_xhtml',    _('c_to_xhtml_label', u'Convert HTML to XHTML')),
            ('use_ext_title', _('use_ext_title_label', u'Use external header title (<title>)')),
            ('hide_loc_title', _('hide_loc_title_label', u'Hide local content title (<h1>)')),
        ],
        widget = atapi.MultiSelectionWidget(
            label = _('option_label', u'Options'),
            format = 'checkbox',
        ),
    ),
    atapi.LinesField(
        name = 'substitutions',
        required = False,
        searchable = False,
        widget = atapi.LinesWidget(
            label = _('substitutions_label', u'String substitutions'),
            description = _('substitutions_description', u'one substitution per line: |search text|=>|replacement text|'),
            rows = 5,
            cols = 100,
        ),
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ExternalPageSchema['title'].storage = atapi.AnnotationStorage()
ExternalPageSchema['description'].storage = atapi.AnnotationStorage()
#~ ExternalPageSchema['text'].widget.condition = 'nothing'

schemata.finalizeATCTSchema(ExternalPageSchema)


class ExternalPage(document.ATCTContent):
    """Viewing of an external page"""
    implements(IExternalPage)

    meta_type = "ExternalPage"
    schema = ExternalPageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    security = ClassSecurityInfo()

    _v_errorPrefix = '<div class="error">'
    _v_errorSuffix = '</div>'

    # External page content
    _v_ext_content = ''

    security.declarePrivate('_get_ext_content')
    def _get_ext_content(self):
        queryString = self.REQUEST['QUERY_STRING']

        if queryString:
            if self.getExternal_encoding != '':
                queryString = urllib.unquote_plus(queryString)
                try:
                    queryString = queryString.decode('utf-8')
                    queryString = queryString.encode(self.getExternal_encoding())
                except UnicodeDecodeError:
                    pass
                queryString = urllib.quote_plus(queryString, '&=')
            queryString = re.sub('&set_language=..', '', queryString)

        # Get external page
        #~ if self.REQUEST.form:
            #~ formData = urllib.urlencode(self.REQUEST.form)
        #~ else:
            #~ formData = ''
        self.REQUEST.form['VISIT_REFERER'] = self.REQUEST['HTTP_REFERER']
        formData = urllib.urlencode(self.REQUEST.form)
        if hasattr(self.REQUEST, '_art_ext_url_ind'):
            extURL = self.getExternal_urls()[int(self.REQUEST['_art_ext_url_ind'])]
        else:
            extURL = self.getExternal_urls()[0]
        try:
            if queryString:
                if '?' in extURL:
                    extURL += '&' + queryString
                else:
                    extURL += '?' + queryString
            extFile = urllib2.urlopen(extURL, data=formData, timeout=90)
            #extContent = artlib.uniEncode(extFile.read())
            extContent = unicode(extFile.read(), self.getExternal_encoding())
            extFile.close()
        except:
            extContent = self._v_errorPrefix + _('connection_error', 'Failure connecting to server') + self._v_errorSuffix

        self._v_ext_content = extContent

    security.declarePrivate('get_ext_body')
    def get_ext_body(self):
        content = self._v_ext_content

        # Check that it is an html document
        if re.search('<(h|H)(t|T)(m|M)(l|L)', content):
            # find start and end of body contents
            bodyStartGroup = re.search('<(b|B)(o|O)(d|D)(y|Y)[^>]*>', content)
            if bodyStartGroup:
                bodyStart = bodyStartGroup.end()
                bodyEndGroup = re.search('</(b|B)(o|O)(d|D)(y|Y)', content)
                if bodyEndGroup:
                    bodyEnd = bodyEndGroup.start()
                    content = content[bodyStart:bodyEnd]
            else:
                content = ''

        # Extract fragments if field is set
        start_tags = self.getFragments_start_tags()
        if start_tags:
            #~ start_tags.append(self._v_errorPrefix)
            start_tags = start_tags + [self._v_errorPrefix]
            newContent = ''
            for s in start_tags:
                if s != '':
                    extractor = artlib.HTMLExtractor()
                    newContent += extractor.get(s, content)
            content = newContent

        # Convert HTML to XHTML if c_to_xhtml of options is checked
        if 'c_to_xhtml' in self.getOptions():
            converter = artlib.HTMLToXHTMLConverter()
            content = converter.get(content)

        # Apply substitutions
        for s in self.getSubstitutions():
            searchString, substitution = s[1:-1].split('|=>|')
            content = content.replace(searchString, substitution)

        return self.getText() + content

    security.declarePrivate('get_ext_title')
    def get_ext_title(self):
        content = self._v_ext_content

        matchs = re.search(r'<title>\s*(.*?)\s*</title>', content)

        if matchs and 'use_ext_title' in self.getOptions():
            return matchs.group(1)
        else:
            return self.title

    def hideLocalTitle(self):
        return 'hide_loc_title' in self.getOptions()


atapi.registerType(ExternalPage, PROJECTNAME)
