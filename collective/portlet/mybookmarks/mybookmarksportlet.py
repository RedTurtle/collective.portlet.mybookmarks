from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.mybookmarks import MyBookmarksPortletMessageFactory as _
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implements

class IMyBookmarksPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """



class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMyBookmarksPortlet)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "My bookmarks portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('mybookmarksportlet.pt')
    
    @property
    @memoize
    def results(self):
        pc = getToolByName(self.context, 'portal_catalog')
        pm = getToolByName(self.context, 'portal_membership')
        
        user = pm.getAuthenticatedMember()
        fullname = user.getProperty('fullname', None)
        bookmarks = [x for x in user.getProperty('bookmarks', None)]
        external_bookmarks = [x for x in user.getProperty('external_bookmarks', None)]
        bookmarks_list = []
        for bookmark in bookmarks:
            try:
                res = pc.searchResults(UID = bookmark)
                for brain in res:
                    try:
                        obj = brain.getObject()
                    except:
                        pass

                bookmark_dict = {}
                bookmark_dict['Title'] = obj.Title()
                bookmark_dict['Description'] = obj.Description()
                bookmark_dict['url'] = obj.absolute_url
                bookmark_dict['removeValue'] = bookmark
                bookmark_dict['bookmark_type'] = 'bookmarks'
                bookmarks_list.append(bookmark_dict)
                
            except IndexError:
                self.context.plone_log("ERROR Bookmark '%s' for user %s" %(x,fullname))
                bookmarks.remove(x)
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
        return bookmarks_list


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    def create(self):
        assignment = Assignment()
        return assignment

