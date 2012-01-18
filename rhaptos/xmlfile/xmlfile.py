from cStringIO import StringIO
from lxml import etree

from zope import schema
from zope.interface import implements

from five import grok
from plone.directives import form
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichText
from plone.app.textfield.utils import getSiteEncoding

from rhaptos.xmlfile.value import IXMLTextValue, XMLTextValue
from rhaptos.xmlfile import MessageFactory as _

class IXMLText(IRichText):
    """ Marker interface for IXMLText
    """

class XMLText(RichText):
    """ Field that contains XML
    """

    implements(IXMLText)
    
    default_mime_type='text/xml',
    output_mime_type='text/html', 

    def __init__(self,
        default_mime_type='text/xml',
        output_mime_type='text/html', 
        allowed_mime_types=None,
        schema=IXMLTextValue,
        **kw):
        super(XMLText, self).__init__(
            default_mime_type=default_mime_type,
            output_mime_type=output_mime_type,
            allowed_mime_types=allowed_mime_types,
            schema=schema, **kw
            )

    def fromUnicode(self, str):
        return XMLTextValue(
                raw=str,
                mimeType=self.default_mime_type,
                outputMimeType=self.output_mime_type,
                encoding=getSiteEncoding(),
            )
        
    def _validate(self, value):
        # lxml will raise an exception if we have invalid xml
        parser = etree.XMLParser(resolve_entities=False)
        etree.parse(StringIO(value.raw_encoded), parser)

class IXMLFile(form.Schema):
    """
    XML File
    """

    form.primary('body')
    body = XMLText(
            title=_(u"Body"),
            required=False,
        )

class View(form.DisplayForm):
    grok.context(IXMLFile)
    grok.require('zope2.View')
