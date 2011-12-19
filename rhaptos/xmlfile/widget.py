from xml.dom.minidom import parseString
from zope.interface import implementsOnly, implementer
from zope.component import adapts, adapter
from zope.app.component.hooks import getSite

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.browser.widget import addFieldClass
from z3c.form.widget import FieldWidget

from plone.app.textfield.interfaces import ITransformer, TransformError
from plone.app.textfield.widget import IRichTextWidget
from plone.app.textfield.widget import RichTextWidget
from plone.app.textfield.widget import RichTextConverter

from rhaptos.xmlfile.xmlfile import IXMLText

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
