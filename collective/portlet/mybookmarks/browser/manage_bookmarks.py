# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.mybookmarks import MyBookmarksPortletMessageFactory as _

class ManageBookmarksView(BrowserView):
    """
    A view to manage personal bookmarks
    """    
    def __call__(self):
        """
        If there is "remove_bookmark"  in the request, the passed bookmark will be removed.
        If nothing is passed, the current object will be added as a bookmark.
        If the external bookmark form is filled, the bookmark will be added in external_bookmarks property.
        """
        if self.request.form.has_key('remove_bookmark') and self.request.form.has_key('bookmark_type'):
            return self.removeBookmark(self.request.form.get('remove_bookmark',''),self.request.form.get('bookmark_type',''))
        if not self.request.form.has_key('form.button.Add'):
            return self.addBookmark(self.context.UID(),'bookmarks')
        elif self.request.form.has_key('form.submitted'):
            if not self.request.form.get('external_title') or not self.request.form.get('external_url'):
                return self.doReturn(_(u'External bookmarks: all the required fields must be filled.'), 'error')
            external_string="%s|%s"%(self.request.form.get('external_title'),self.request.form.get('external_url'))
            return self.addBookmark(external_string,'external_bookmarks')
    
    def removeBookmark(self,element,bookmark_type):
        """
        remove the bookmark from bookmark_type property
        """
        pm = getToolByName(self.context,'portal_membership')
        user = pm.getAuthenticatedMember()
        user_bookmarks = [x for x in user.getProperty(bookmark_type, None)]
        if element in user_bookmarks:
            user_bookmarks.remove(element)
            bookmarks=tuple(user_bookmarks)
            user.setMemberProperties({bookmark_type:bookmarks})
            return self.doReturn(_(u'Bookmark removed.'), 'info')
        return self.doReturn(_(u'Bookmark not present in list.'), 'error')
    
    def addBookmark(self,element,bookmark_type):
        """
        Add the bookmark to bookmark_type property
        """
        pm = getToolByName(self.context,'portal_membership')
        user = pm.getAuthenticatedMember()
        user_bookmarks = [x for x in user.getProperty(bookmark_type, None)]
        if not user_bookmarks:
            user.setMemberProperties({bookmark_type:(element,)})
            return self.doReturn(_(u'Bookmark added.'), 'info')
        
        if element in user_bookmarks:
            return self.doReturn(_(u'Bookmark already present.'), 'error')
        user_bookmarks.append(element)
        bookmarks=tuple(user_bookmarks)
        user.setMemberProperties({bookmark_type:bookmarks})
        return self.doReturn(_(u'Bookmark added.'), 'info')

    def doReturn(self,message,type):
        pu = getToolByName(self.context, "plone_utils")
        pu.addPortalMessage(message, type=type)
        self.request.RESPONSE.redirect(self.context.absolute_url())