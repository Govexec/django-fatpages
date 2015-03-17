from django.conf import settings
from django.http import Http404, HttpResponseNotFound

from coffin.shortcuts import render_to_string
from coffin.template import RequestContext

from staticpages.views import fatpage
from websites.models import Page
from websites.route_fifty.views import NotFoundView as RFNotFoundView


def page_404(request):

    view_vars = {
        "page":  Page({
        "category": None,
        "title": '404',
        }, request, ad_settings=settings.DART_AD_DEFAULTS)
    }

    if settings.SITE_NAME == "Nextgov":
        return HttpResponseNotFound(render_to_string("nextgov/content/main/404.html", view_vars, context_instance=RequestContext(request)))
    elif settings.SITE_NAME == "Defense One":
        return HttpResponseNotFound(render_to_string("defenseone/content/main/404.html", view_vars, context_instance=RequestContext(request)))
    elif settings.SITE_NAME == "Route Fifty":
        return RFNotFoundView.as_view()(request)
    else:
        return HttpResponseNotFound(render_to_string("content/main/404.html", view_vars, context_instance=RequestContext(request)))


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
