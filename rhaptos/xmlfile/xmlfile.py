from zope import schema

from plone.directives import form
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichText, IRichTextValue

from rhaptos.xmlfile import MessageFactory as _

class IXMLText(IRichText):
    """ Marker interface for IXMLText
    """

class XMLText(RichText):
    """ Field that contains XML
    """
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

class IXMLFile(form.Schema):
    """
    XML File
    """

    body = XMLText(
            title=_(u"Body"),
            required=False,
        )
    

