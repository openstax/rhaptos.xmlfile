import logging
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem

log = logging.getLogger('rhaptos.xmlfile-setuphandlers')

def install_xml_to_html(portal):
    log.info('Installing xml_to_html transform')
    xml_to_html_id = 'xml_to_html'
    xml_to_html_module = "rhaptos.xmlfile.xml2html"
    pt = getToolByName(portal, 'portal_transforms')

    if xml_to_html_id not in pt.objectIds():
        pt.manage_addTransform(xml_to_html_id, xml_to_html_module)
    log.info('xml_to_html transform installed successfully')


def install(context):
    if context.readDataFile('rhaptos.xmlfile-marker.txt') is None:
        return
    site = context.getSite()
    install_xml_to_html(site)

