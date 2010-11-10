from zope.i18nmessageid import MessageFactory
MyBookmarksPortletMessageFactory = MessageFactory('collective.portlet.mybookmarks')

import config

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
