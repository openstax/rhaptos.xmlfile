from lxml import etree
from zope.interface import implements

from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue, RawValueHolder
from plone.app.textfield.interfaces import IRichText, IRichTextValue

class IXMLTextValue(IRichTextValue):
    """The value actually stored in a XMLText field.
    """

class XMLTextValue(RichTextValue):
    """ Extend RichTextValue with xpath functionality
    """

    implements(IXMLTextValue)

    def _updateFromTree(self, tree):
        tree = tree.getroottree()
        docinfo = tree.docinfo
        pi = '<?xml version="%s" encoding="%s"?>' % (docinfo.xml_version,
                                                     docinfo.encoding)
        raw = pi + '\n' + etree.tostring(tree)
        self._raw_holder = RawValueHolder(raw)

    def xpathUpdate(self, value, xpath, namespaces={}):
        if isinstance(value, basestring):
            value = etree.fromstring(value)
        tree = etree.fromstring(self.raw_encoded)
        for node in tree.xpath(xpath, namespaces=namespaces):
            node.getparent().replace(node, value)
        self._updateFromTree(tree)

    def xpathDelete(self, xpath, namespaces={}):
        tree = etree.fromstring(self.raw_encoded)
        for node in tree.xpath(xpath, namespaces=namespaces):
            node.getparent().remove(node)
        self._updateFromTree(tree)

    def xpathInsert(self, value, position, xpath, namespaces={}):
        if isinstance(value, basestring):
            value = etree.fromstring(value)
        tree = etree.fromstring(self.raw_encoded)
        for node in tree.xpath(xpath, namespaces=namespaces):
            if position == 'before':
                node.addprevious(value)
            else:
                node.addnext(value)
        self._updateFromTree(tree)

    @property
    def processingInstruction(self):
        tree = etree.fromstring(self.raw_encoded).getroottree()
        docinfo = tree.docinfo
        pi = '<?xml version="%s" encoding="%s"?>' % (docinfo.xml_version,
                                                     docinfo.encoding)
        return pi
        
        
    def __repr__(self):
        return u"XMLTextValue object. (Did you mean <attribute>.raw or <attribute>.output?)"

