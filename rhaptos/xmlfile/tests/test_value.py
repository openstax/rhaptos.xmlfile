import os
import unittest2 as unittest
from lxml import etree

from rhaptos.xmlfile.value import XMLTextValue, IXMLTextValue

from base import PROJECTNAME
from base import INTEGRATION_TESTING

class TestXMLTextValue(unittest.TestCase):
    """ Test value module """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.value = XMLTextValue(
            raw='<html><body>test</body></html>',
            mimeType='text/xml',
            outputMimeType='text/html',
            encoding='utf-8'
        )

    def test_xmltextvalue(self):
        self.assertTrue(IXMLTextValue.providedBy(self.value))

    def test_updateFromTree(self):
        tree = etree.fromstring('<html><body><h1>heading</h1></body></html>')
        self.value._updateFromTree(tree)
        self.assertEqual(self.value.raw, '%s\n%s' % (
                                         self.value.processingInstruction,
                                         etree.tostring(tree)
                                         ))

    def test_xpathUpdate(self):
        self.value.xpathUpdate('<body><h2>Heading2</h2></body>', '/html/body')
        self.assertEqual(self.value.raw,
            '%s\n<html><body><h2>Heading2</h2></body></html>'
            % self.value.processingInstruction)

    def test_xpathDelete(self):
        self.value.xpathDelete('/html/body')
        self.assertEqual(self.value.raw, '%s\n<html/>'
            % self.value.processingInstruction)

    def test_xpathInsert(self):
        self.value.xpathInsert('<head>brain</head>', 'before', '/html/body')
        self.assertEqual(self.value.raw,
            '%s\n<html><head>brain</head><body>test</body></html>'
            % self.value.processingInstruction)

    def test_processingInstruction(self):
        self.assertEqual(self.value.processingInstruction,
            '<?xml version="1.0" encoding="UTF-8"?>')
