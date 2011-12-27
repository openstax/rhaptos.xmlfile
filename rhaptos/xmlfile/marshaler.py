from plone.app.textfield.marshaler import HAVE_MARSHALER

if HAVE_MARSHALER:

    from plone.app.textfield.marshaler import RichTextFieldMarshaler

    from zope.interface import Interface
    from zope.component import adapts
    
    from rhaptos.xmlfile.xmlfile import IXMLText
    from rhaptos.xmlfile.value import XMLTextValue
    
    class XMLTextFieldMarshaler(RichTextFieldMarshaler):
        """Field marshaler for rhaptos.xmlfile.
        """
        
        adapts(Interface, IXMLText)
        
        def encode(self, value, charset='utf-8', primary=False):
            if value is None:
                return
            return value.raw.encode(charset)
        
        def decode(self, value, message=None, charset='utf-8',
                   contentType=None, primary=False):
            return XMLTextValue(
                    raw=value.decode('utf-8'),
                    mimeType=contentType or self.field.default_mime_type,
                    outputMimeType=self.field.output_mime_type,
                    encoding=charset
                )
