from staticpages.views import fatpage
from django.http import Http404
from django.conf import settings
from coffin.shortcuts import render_to_response
from govexec.models import Page
from coffin.template import RequestContext



def page_404(request):

    view_vars = {
        "page":  Page({
        "category": None,
        "title": '404',
        }, request, ad_settings=settings.DART_AD_DEFAULTS)
    }

    if settings.SITE_NAME == "Nextgov":
        return render_to_response("nextgov/content/main/404.html", view_vars, context_instance=RequestContext(request))
    else:
        return render_to_response("content/main/404.html", view_vars, context_instance=RequestContext(request))


class FatpageFallbackMiddleware(object):
    def process_response(self, request, response):

        if response.status_code != 404:
            return response # No need to check for a fatpage for non-404 responses.
        try:
            return fatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return page_404(request)
        except:
            return page_404(request)
