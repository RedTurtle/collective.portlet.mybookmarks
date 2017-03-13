# -*- coding: utf-8 -*-
from collective.portlet.mybookmarks.browser.my_bookmarks import \
    BaseBookmarksView
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class AddView(BaseBookmarksView):

    """
    """

    def add_bookmark(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        bookmarks = self.extract_user_bookmarks()
        result = {'success': True}
        if self.already_bookmarked(bookmarks):
            result['success'] = False
            result['message'] = '"{}" is already bookmarked. Nothing done.'.format(
                self.context.Title())
            return result
        bookmarks.append(self.format_bookmark())
        self.update_user_bookmarks(bookmarks)
        return result

    def already_bookmarked(self, bookmarks):
        uid = api.content.get_uuid(obj=self.context)
        return [x for x in bookmarks if x.get('uid') == uid] > 0

    def format_bookmark(self):
        return {
            'uid': api.content.get_uuid(obj=self.context),
            'title': self.context.Title(),
            'type': 'internal'
        }
