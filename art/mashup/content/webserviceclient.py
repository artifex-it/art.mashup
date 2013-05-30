# -*- coding: utf-8 -*-
"""Definition of the Web Service Client content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from AccessControl import ClassSecurityInfo

# -*- Message Factory Imported Here -*-
from art.mashup import mashupMessageFactory as _

from art.mashup.interfaces import IWebServiceClient
from art.mashup.config import PROJECTNAME

from suds.client import Client
import json
import time

WebServiceClientSchema = document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name = 'service_url',
        required = True,
        searchable = False,
        widget = atapi.StringWidget(
            label = _('service_url_label', u'Service URL'),
            size = 100,
        ),
        validators = ('isURL', ),
    ),
    atapi.StringField(
        name = 'service_name',
        required = True,
        searchable = False,
        widget = atapi.StringWidget(
            label = _('service_name_label', u'Service name'),
            size = 100,
        ),
    ),
    atapi.StringField(
        name = 'service_pars',
        required = False,
        searchable = False,
        widget = atapi.LinesWidget(
            label = _('service_pars_label', u'Service parameters'),
            description = _('service_pars_description', u'one service parameter per line (example self.REQUEST.get("par_name", "par_default_value"))'),
            size = 100,
        ),
    ),
    atapi.StringField(
        name = 'alternate_template',
        required = False,
        searchable = False,
        widget = atapi.StringWidget(
            label = _('alternate_template_label', u'Alternate Viewlet Template'),
            description = _('alternate_template_description', u'Relative path from directory containg the definition of WebserviceResultViewlet class (example ../../../../apt.visit/apt/visit/browser/templates/tpl_example.pt)'),
            size = 100,
        ),
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

WebServiceClientSchema['title'].storage = atapi.AnnotationStorage()
WebServiceClientSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(WebServiceClientSchema)


class WebServiceClient(document.ATCTContent):
    """Viewing of a web service result"""
    implements(IWebServiceClient)

    meta_type = "WebServiceClient"
    schema = WebServiceClientSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    security = ClassSecurityInfo()

    # Web service result
    _v_result = ''

    security.declarePrivate('_call_service')
    def _call_service(self):
        try:
            client = Client(self.getService_url())

            s = getattr(client.service, self.getService_name())
        except:
            return

        pars = []
        for p in self.getService_pars():
            pars.append(eval(p, {"__builtins__": None}, {'self': self}))

        self._v_result = s(*pars)

    security.declarePrivate('getResult')
    def getResult(self):
        return self._v_result


atapi.registerType(WebServiceClient, PROJECTNAME)
