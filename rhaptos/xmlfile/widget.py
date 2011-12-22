from xml.dom.minidom import parseString
from zope.interface import implementsOnly, implementer
from zope.component import adapts, adapter
from zope.app.component.hooks import getSite

from z3c.form.interfaces import IFormLayer, IFieldWidget, NOVALUE
from z3c.form.browser.widget import addFieldClass
from z3c.form.widget import FieldWidget

from plone.app.textfield.interfaces import ITransformer, TransformError
from plone.app.textfield.widget import IRichTextWidget
from plone.app.textfield.widget import RichTextWidget
from plone.app.textfield.widget import RichTextConverter
from plone.app.textfield.utils import getSiteEncoding

from rhaptos.xmlfile.xmlfile import IXMLText
from rhaptos.xmlfile.value import IXMLTextValue, XMLTextValue

class IXMLTextWidget(IRichTextWidget):
    """ Marker interface for XMLTextWidget
    """

class XMLTextWidget(RichTextWidget):
    implementsOnly(IXMLTextWidget)
    
    klass = u'xmlTextWidget'
    value = None

    def update(self):
        super(RichTextWidget, self).update()
        addFieldClass(self)

    def extract(self, default=NOVALUE):
        raw = self.request.get(self.name, default)
        
        if raw is default:
            return default
        
        mimeType = self.request.get("%s.mimeType" % self.name,
                                    self.field.default_mime_type)
        return XMLTextValue(raw=raw,
                            mimeType=mimeType,
                            outputMimeType=self.field.output_mime_type,
                            encoding=getSiteEncoding())

    def html(self):
        site = getSite()
        transformer = ITransformer(site, None)
        if transformer is None:
            return None
        return transformer(self.value, self.value.outputMimeType)


@adapter(IXMLText, IFormLayer)
@implementer(IFieldWidget)
def XMLTextFieldWidget(field, request):
    """IFieldWidget factory for XMLTextWidget."""
    return FieldWidget(field, XMLTextWidget(request))


class XMLTextConverter(RichTextConverter):
    """Data converter for the XMLTextWidget
    """
    
    adapts(IXMLText, IXMLTextWidget)
    
    def toWidgetValue(self, value):
        if IXMLTextValue.providedBy(value):
            return value
        elif isinstance(value, unicode):
            return self.field.fromUnicode(value)
        elif value is None:
            return None
        raise ValueError("Cannot convert %s to an IXMLTextValue" % repr(value))

    def toFieldValue(self, value):
        if IXMLTextValue.providedBy(value):
            if value.raw == u'':
                return self.field.missing_value
            return value
        elif isinstance(value, unicode):
            if value == u'':
                return self.field.missing_value
            return self.field.fromUnicode(value)
        raise ValueError("Cannot convert %s to an IXMLTextValue" % repr(value))
