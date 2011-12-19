from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

from zope import schema
from zope.interface import implements
from zope.app.component.hooks import getSite

from plone.directives import form
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichText, IRichTextValue

from Products.CMFCore.utils import getToolByName

from rhaptos.xmlfile import MessageFactory as _

class IXMLText(IRichText):
    """ Marker interface for IXMLText
    """

class InvalidXML(schema.ValidationError):
    __doc__ = _("""Invalid XML.""")

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
        schema=IRichTextValue,
        **kw):
        super(XMLText, self).__init__(
            default_mime_type=default_mime_type,
            output_mime_type=output_mime_type,
            allowed_mime_types=allowed_mime_types,
            schema=schema, **kw
            )

    def _validate(self, value):
        site = getSite()
        properties = getToolByName(self, 'portal_properties', None)
        site_properties = getattr(properties, 'site_properties', None)
        charset = site_properties.getProperty('default_charset')
        try:
            parseString(value.raw.encode(charset))
        except ExpatError:
            raise InvalidXML(value.raw)
        

class IXMLFile(form.Schema):
    """
    XML File
    """

    body = XMLText(
            title=_(u"Body"),
            required=False,
        )

