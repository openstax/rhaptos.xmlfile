from cgi import escape
import unittest2 as unittest

from zope.interface import Interface, implements
from z3c.form.interfaces import NOVALUE
from z3c.form.widget import FieldWidget

from Products.CMFCore.PortalContent import PortalContent
from rhaptos.xmlfile.widget import XMLTextWidget, XMLTextConverter
from rhaptos.xmlfile.xmlfile import XMLText
from rhaptos.xmlfile.value import IXMLTextValue, XMLTextValue

from base import INTEGRATION_TESTING

class TestXMLTextWidget(unittest.TestCase):
    """ Test XMLTextWidget """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request =self.layer['request']

    def test_extract(self):
        class IWithText(Interface):
            
            text = XMLText(title=u"Text")
        
        class Context(PortalContent):
            implements(IWithText)
            
            text = None
        
        widget = FieldWidget(IWithText['text'], XMLTextWidget(self.request))
        widget.update()
        
        value = widget.extract()
        self.assertEquals(NOVALUE, value)
        
        self.request.form['%s' % widget.name] = u"<html><body>test</body></html>"
        self.request.form['%s.mimeType' % widget.name] = 'text/xml'
        
        value = widget.extract()
        self.assertEquals(u"<html><body>test</body></html>", value.raw)

    def test_html(self):
        class IWithText(Interface):
            
            text = XMLText(title=u"Text")
        
        class Context(PortalContent):
            implements(IWithText)
            
            text = None
        
        widget = FieldWidget(IWithText['text'], XMLTextWidget(self.request))
        widget.update()
        
        value = widget.extract()
        self.assertEquals(NOVALUE, value)
        
        self.request.form['%s' % widget.name] = u"<html><body>test</body></html>"
        self.request.form['%s.mimeType' % widget.name] = 'text/xml'
        
        widget.update()
        self.assertEquals(widget.html(), '<pre>&lt;html&gt;\n  &lt;body&gt;test&lt;/body&gt;\n&lt;/html&gt;\n</pre>')

    def test_converter(self):
        _marker = object()

        class IWithText(Interface):
            
            text = XMLText(title=u"Text", missing_value = _marker)

        widget = FieldWidget(IWithText['text'], XMLTextWidget(self.request))
        widget.update()

        converter = XMLTextConverter(IWithText['text'], widget)
        self.assertTrue(converter.toFieldValue(u'') is _marker)
        self.assertTrue(converter.toFieldValue(XMLTextValue(u'')) is _marker)

        self.assertEquals(converter.toWidgetValue(None), None)
        self.assertTrue(IXMLTextValue.providedBy(
            converter.toWidgetValue(XMLTextValue(u''))))
        self.request.form['%s' % widget.name] = u"<html><body>test</body></html>"
        self.request.form['%s.mimeType' % widget.name] = 'text/xml'
        widget.update()
        self.assertTrue(IXMLTextValue.providedBy(
            converter.toWidgetValue(u"<html><body>test</body></html>")))
        with self.assertRaises(ValueError):
            converter.toWidgetValue(int)
