from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
# -*- Additional Imports Here -*-


class IWebServiceClient(Interface):
    """Viewing of a web service result"""

class IWebServiceResult(IViewletManager):
    """Viewlet manager for result viewing"""

    # -*- schema definition goes here -*-

