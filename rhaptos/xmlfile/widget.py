from zope.interface import implementsOnly, implementer
from zope.component import adapter

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.browser.widget import addFieldClass
from z3c.form.widget import FieldWidget

from plone.app.textfield.widget import IRichTextWidget
from plone.app.textfield.widget import RichTextWidget

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
    

@adapter(IXMLText, IFormLayer)
@implementer(IFieldWidget)
def XMLTextFieldWidget(field, request):
    """IFieldWidget factory for XMLTextWidget."""
    return FieldWidget(field, XMLTextWidget(request))

