from lxml import etree

from zope.interface import implements

from Products.PortalTransforms.interfaces import ITransform

class xml_to_html:
    """ a generic html transform for xml files """
    implements(ITransform)

    __name__ = "xml_to_html"
    inputs = ("text/xml",)
    output = "text/html"

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        xmldoc = etree.fromstring(orig)
        html = "<pre>%s</pre>" % etree.tostring(xmldoc, pretty_print=True)

        data.setData(html)
        return data


def register():
    return xml_to_html()
