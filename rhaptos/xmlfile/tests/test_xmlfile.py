import os
import unittest2 as unittest

from zope.component import createObject

from Products.CMFCore.utils import getToolByName

from rhaptos.xmlfile.xmlfile import IXMLFile, IXMLText, XMLText
from rhaptos.xmlfile.value import XMLTextValue

from base import PROJECTNAME
from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)

class TestXMLFile(unittest.TestCase):
    """ Test xmlfile module """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_xmlfile(self):
        xmlfile = createObject('rhaptos.xmlfile.xmlfile', id='xmlfile')
        self.assertTrue(IXMLFile.providedBy(xmlfile))

    def test_xmltext(self):
        testfile = open(os.path.join(dirname, 'test.cnxml')).read()
        xmlfield = XMLText()
        value = xmlfield.fromUnicode(testfile)
        self.assertTrue(isinstance(value, XMLTextValue))
