from Products.CMFCore.utils import getToolByName
from collective.portlet.mybookmarks import logger


def import_various(context):
    if context.readDataFile('mybookmarksportlet-various.txt') is None:
        return
    # Define portal properties
    portal = context.getSite()
    insertProperties(context, portal)


def insertProperties(context, portal):
    """
    insert some properties
    """
    portal_properties = getToolByName(context, 'portal_properties')
    mybookmarks_properties = getattr(portal_properties, 'mybookmarks_properties', None)
    if not mybookmarks_properties:
        portal_properties.addPropertySheet(id='mybookmarks_properties', title="MyBookmarks properties")
        logger.info("Added mybookmarks_properties property-sheet")
        mybookmarks_properties = getattr(portal_properties, 'mybookmarks_properties', None)
    if not mybookmarks_properties.hasProperty('default_bookmarks'):
        mybookmarks_properties.manage_addProperty(id='default_bookmarks', value='', type='lines')
        logger.info("Added default_bookmarks property")
