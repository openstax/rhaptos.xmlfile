from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

from zope import schema
from zope.interface import implements

from plone.directives import form
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichText, IRichTextValue

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
    output_mime_type='text/xml', 

    def __init__(self,
        default_mime_type='text/xml',
        output_mime_type='text/xml', 
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
        try:
            parseString(value.output)
        except ExpatError:
            raise InvalidXML(value.output)
        

class IXMLFile(form.Schema):
    """
    XML File
    """

    body = XMLText(
            title=_(u"Body"),
            required=False,
        )
    

