## Script (Python) "addtoBookmark"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Aggiunge un bookmark per l'utente
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
lista = []

UID = context.UID()

if user_bookmarks:    
    
    for x in user_bookmarks:
        lista.append(x)
        
    if UID not in lista:
        lista.append(UID)
        msg = _(u'${title} e\' stato aggiunto ai tuoi bookmarks.',
            mapping={u'title' : context.title_or_id()})
    else:
        msg = _(u'${title} e\' gia\' presente nei tuoi bookmarks.',
            mapping={u'title' : context.title_or_id()})
           
    user_bookmarks = tuple(lista)
    user.setProperties(internal_bookmarks=user_bookmarks)
    
else:
    user.setProperties(internal_bookmarks=(UID,))
    msg = _(u'${title} e\' stato aggiunto ai tuoi bookmarks.',
            mapping={u'title' : context.title_or_id()})
    
context.plone_utils.addPortalMessage(msg)

return RESPONSE.redirect(view_url)
