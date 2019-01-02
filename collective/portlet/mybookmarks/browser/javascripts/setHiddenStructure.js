$(document).ready(function() {
	var dd=$('#addExternalBlock');
	if (dd.length === 1) {
		var translated_label=dd.children('span#hiddenJsLabel').html();
		var translated_alt=dd.children('span#hiddenAltLabel').html();
		var href_title=$('#externalBookmarkFieldset legend').html();
		var form=dd.children('#externalBookmarkForm');
		html='<a id="addExternalLink"';
		html+='title="'+href_title+'"';
		html+='href="#">';
		html+='<img class="bookmarkIcon" src="'+$('body').attr('data-portal-url')+'/++resource++collective.portlet.mybookmarks.images/add.png" alt="' + translated_alt + '"/>';
		html+=translated_label;
		html+='</a>';
		form.before(html);
		$('a#addExternalLink').bind('click', function(event){
			event.preventDefault();
			form.toggle();
		});
	}
});

/*
 * Super-trick file... we apply (only with JS enabled) a special additioal CSS class that hide
 * our images, in this way we do not get bad effects on page load.
 * 
 * We use JS, so not js-able browsers will not see this class, and Javascript enabled ones
 * will remove this class from portlet when images are ready.
 */

document.write('<style type="text/css">#externalBookmarkForm {display:none}</style>');
