from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.mybookmarks import MyBookmarksPortletMessageFactory as _
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements

class IMyBookmarksPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    portletTitle = schema.TextLine(title=_(u"Title of the portlet"),
                                           description = _(u"Insert the title of the portlet."),
                                           default=_("Personal bookmark"),
                                           required = True)



class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMyBookmarksPortlet)
    
    def __init__(self, portletTitle=''):
        self.portletTitle=portletTitle
    
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.portletTitle:
            return self.portletTitle
        return _(u"Personal bookmark")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('mybookmarksportlet.pt')
    
    @property
    def available(self):
        
        pm = getToolByName(self.context, 'portal_membership')
        if pm.isAnonymousUser():
            return False
        return True
    
    @property
    @memoize
    def results(self):
        pc = getToolByName(self.context, 'portal_catalog')
        pm = getToolByName(self.context, 'portal_membership')
        
        user = pm.getAuthenticatedMember()
        fullname = user.getProperty('fullname', None)
        bookmarks = [x for x in user.getProperty('bookmarks', ())]
        external_bookmarks = [x for x in user.getProperty('external_bookmarks', ())]
        bookmarks_list = []
        if bookmarks:
            portal_types = getToolByName(self.context, 'portal_types')
            portal_properties = getToolByName(self.context, 'portal_properties')
            site_properties = getattr(portal_properties, 'site_properties')
            if site_properties.hasProperty('types_not_searched'):
                search_types=[x for x
                              in portal_types.keys()
                              if x not in site_properties.getProperty('types_not_searched')]
        for bookmark in bookmarks:
            res = pc.searchResults(UID = bookmark,portal_type=search_types)
            if res:
                bookmark_dict = {}
                bookmark_dict['Title'] = res[0].Title
                bookmark_dict['Description'] = res[0].Description
                bookmark_dict['url'] = res[0].getURL()
                bookmark_dict['removeValue'] = bookmark
                bookmark_dict['bookmark_type'] = 'bookmarks'
                bookmarks_list.append(bookmark_dict)
                
            else:
                self.context.plone_log("ERROR Bookmark '%s' for user %s" %(bookmark,fullname))
                bookmarks.remove(bookmark)
                bookmarks = tuple(bookmarks)
                user.setMemberProperties({'bookmarks':bookmarks})
                    
        for bookmark in external_bookmarks:
            bookmark_values=bookmark.split('|')
            bookmark_dict = {}
            bookmark_dict['Title'] = bookmark_values[0]
            bookmark_dict['url'] = bookmark_values[1]
            bookmark_dict['removeValue'] = bookmark
            bookmark_dict['bookmark_type'] = 'external_bookmarks'
            bookmarks_list.append(bookmark_dict)
        bookmarks_list.sort(lambda x,y:cmp(x['Title'].lower(),y['Title'].lower()))
        return bookmarks_list


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    
    form_fields = form.Fields(IMyBookmarksPortlet)
    def create(self, data):
        return Assignment(**data)
    
    
class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IMyBookmarksPortlet)
    