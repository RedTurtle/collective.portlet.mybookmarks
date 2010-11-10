## Script (Python) "delfromBookmark"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Cancella un bookmark dell'utente
##
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone import PloneMessageFactory as _

RESPONSE = context.REQUEST.RESPONSE
REQUEST=context.REQUEST

state = context.restrictedTraverse("@@plone_context_state")
view_url = '%s/%s' % (context.absolute_url(), state.view_template_id())

pm = context.portal_membership
user = pm.getAuthenticatedMember()

user_bookmarks = user.getProperty('internal_bookmarks', None)

UID = REQUEST.get('uid')

if user_bookmarks:
    lista = []
    for x in user_bookmarks:
        lista.append(x)
        
    if UID in lista:
        lista.remove(UID)
        msg = _(u'Il bookmark e\' stato correttamente rimosso.')
        
    user_bookmarks = tuple(lista)
    user.setProperties(internal_bookmarks=user_bookmarks)
    
context.plone_utils.addPortalMessage(msg)

return RESPONSE.redirect(view_url)