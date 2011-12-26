import os
import unittest2 as unittest

from zope.component import createObject

from rhaptos.xmlfile.xmlfile import XMLText
from rhaptos.xmlfile.marshaler import XMLTextFieldMarshaler
from rhaptos.xmlfile.value import IXMLTextValue, XMLTextValue

from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)

class TestMarshaler(unittest.TestCase):
    """ Test marshaler module """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.raw = open(os.path.join(dirname, 'test.cnxml')).read()
        self.raw = self.raw.decode('utf-8')
        xmlfile = createObject('rhaptos.xmlfile.xmlfile', id='xmlfile')
        field = XMLText()
        self.xmltextvalue = field.fromUnicode(self.raw)
        self.marshaler = XMLTextFieldMarshaler(xmlfile, field)

    def test_encode(self):
        self.assertEqual(self.marshaler.encode(self.xmltextvalue),
                         self.raw.encode('utf-8'))
        with self.assertRaises(UnicodeEncodeError):
            self.marshaler.encode(self.xmltextvalue, charset='latin-1')

    def test_decode(self):
        value = self.marshaler.decode(self.xmltextvalue)
        self.assertTrue(IXMLTextValue.providedBy(value))

