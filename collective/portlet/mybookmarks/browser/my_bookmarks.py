# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
import json
from collective.portlet.mybookmarks.controlpanel.interfaces import IMyBookmarksSettings
from plone.protect import PostOnly
from plone.protect.authenticator import createToken
from zExceptions import Forbidden
import logging
logger = logging.getLogger(__name__)


class BaseBookmarksView(BrowserView):
    def extract_user_bookmarks(self):
        """
        bookmarks are stored as json list
        """
        user = api.user.get_current()
        bookmarks = user.getProperty("internal_bookmarks")
        if not bookmarks:
            return []
        try:
            return json.loads(bookmarks)
        except ValueError as e:
            logger.error("Unable to retrieve %s bookmarks for user: " % (user.getId()))
            logger.exception(e)
            return []

    def update_user_bookmarks(self, bookmarks):
        """
        bookmarks are stored as json list
        """
        user = api.user.get_current()
        user.setMemberProperties({"internal_bookmarks": json.dumps(bookmarks)})

    def update_bookmark(self, index, name, value):
        bookmarks = self.extract_user_bookmarks()
        try:
            bookmark = bookmarks[index]
        except IndexError:
            logger.error('Invalid index "%s" for personal bookmarks.' % index)
            return False
        if name not in bookmark:
            logger.error('"%s": invalid key.' % name)
            return False
        bookmark[name] = value
        self.update_user_bookmarks(bookmarks)
        return True

    def remove_bookmark(self, index):
        bookmarks = self.extract_user_bookmarks()
        bookmarks.pop(index)
        self.update_user_bookmarks(bookmarks)
        return True

    def add_bookmark(self, title, url, type):
        bookmarks = self.extract_user_bookmarks()
        bookmarks.append({
            'title': title,
            'url': url,
            'type': type
        })
        self.update_user_bookmarks(bookmarks)
        return True


class MyBookmarksView(BaseBookmarksView):
    '''
    View for MyBookmarks
    '''

    def authenticator(self):
        return createToken()

    def get_bookmarks(self):
        """
        Return a list of saved bookmarks
        """
        bookmarks = self.extract_user_bookmarks()
        if not bookmarks:
            return []
        formatted_bookmarks = []
        for bookmark in bookmarks:
            bookmark_dict = self.parse_bookmark(bookmark)
            if bookmark_dict:
                formatted_bookmarks.append(bookmark_dict)
        return formatted_bookmarks

    def parse_bookmark(self, bookmark):
        """
        """
        if bookmark.get('type') == 'internal':
            return self.parse_internal_bookmark(bookmark)
        elif bookmark.get('type') == 'external':
            return self.parse_external_bookmark(bookmark)
        return {}

    def parse_external_bookmark(self, bookmark):
        """ """
        url = bookmark.get('url')
        if not url:
            return {}
        return {
            'title': bookmark.get('title', url),
            'url': url,
            'type': bookmark.get('type')
        }

    def parse_internal_bookmark(self, bookmark):
        """ """
        uid = bookmark.get('uid')
        item = api.content.get(UID=uid)
        if not item:
            return False
        return {
            'title': bookmark.get('title', item.Title()),
            'id': item.getId(),
            'url': item.absolute_url(),
            'description': item.Description(),
            'type': bookmark.get('type')
        }


class MyBookmarksEditView(MyBookmarksView):
    """ """


class ReorderView(BaseBookmarksView):
    """ """

    def __call__(self):
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            return json.dumps({'error': e.message})
        try:
            delta = int(self.request.form.get('delta', 0))
            original = int(self.request.form.get('original', 0))
        except ValueError:
            msg = "Unable to sort bookmarks. Invalid values: %s" % self.request.form
            logger.error(msg)
            return json.dumps({'error': msg})
        if not delta:
            return
        if delta == original:
            return
        bookmarks = self.extract_user_bookmarks()
        newIndex = original + delta
        bookmarks.insert(newIndex, bookmarks.pop(original))
        self.update_user_bookmarks(bookmarks)


class EditBookmarkView(BaseBookmarksView):
    """ """

    def __call__(self):
        res_dict = {
            'field': self.request.form.get('fieldName')
        }
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            res_dict['success'] = False
            res_dict['message'] = e.message
            return json.dumps(res_dict)
        index_str, name = self.request.form.get('fieldName').split('-')
        if not index_str or not name:
            logger.error("Unable to edit bookmark. index or name not provided.")
            res_dict['success'] = False
            res_dict['message'] = "Error on saving"
            return json.dumps(res_dict)
        try:
            index = int(index_str)
        except ValueError:
            msg = "Unable to edit bookmark. index is not a valid number."
            logger.error(msg)
            res_dict['success'] = False
            res_dict['message'] = msg
            return json.dumps(res_dict)
        res_dict['success'] = self.update_bookmark(
            index=index,
            name=name,
            value=self.request.form.get('value')
        )
        return json.dumps(res_dict)


class RemoveBookmarkView(BaseBookmarksView):
    """ """

    def __call__(self):
        res_dict = {
            'field': self.request.form.get('fieldName')
        }
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            res_dict['success'] = False
            res_dict['message'] = e.message
            return json.dumps(res_dict)
        index_str = self.request.form.get('index')
        try:
            index = int(index_str)
        except ValueError:
            msg = "Unable to edit bookmark. index is not a valid number."
            logger.error(msg)
            res_dict['success'] = False
            res_dict['message'] = msg
            return json.dumps(res_dict)
        res_dict['success'] = self.remove_bookmark(index=index)
        return json.dumps(res_dict)


class AddBookmarkView(BaseBookmarksView):
    """ """

    def __call__(self):
        res_dict = {}
        try:
            PostOnly(self.context.REQUEST)
        except Forbidden as e:
            logger.exception(e)
            res_dict['success'] = False
            res_dict['message'] = e.message
            return json.dumps(res_dict)
        title = self.request.form.get('title')
        url = self.request.form.get('url')
        type = self.request.form.get('type')
        res_dict['success'] = self.add_bookmark(
            title=title,
            url=url,
            type=type
        )
        return json.dumps(res_dict)
