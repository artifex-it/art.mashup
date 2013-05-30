from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
# -*- Additional Imports Here -*-


class IXMLDocument(Interface):
    """Viewing of a XML document"""

class IXMLDocumentContent(IViewletManager):
    """Viewlet manager for document viewing"""

    # -*- schema definition goes here -*-
