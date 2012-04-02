Introduction
============
A simple portlet that allow to manage some personal bookmarks that can be site objects or external links.
The bookmarks are stored in two member properties.

Settings
========
Managers can set some default bookmarks that all users should view by default.
These bookmarks can be set in a portal_property called "*mybookmarks_properties*".
These bookmarks should be putted in a list field one per line, with the following sintax:
*Title|url_or_path*.
For example:

``Common Page|/common_documents/common_page``

``google.com|http://www.google.com``

Usage
=====
If you want to add an object to bookmarks list, just click on the "bookmark" link in document_actions.
To add a new external link, you need to fill two fields of the form in the portlet.
To remove a bookmark from member properties, just click on delete icon.
