from django.conf import settings
from staticpages.models import FatPage

try:
	from coffin.template import loader, RequestContext
except ImportError:
	print 'ImportError'
	from django.template import loader, RequestContext

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from content_utils.utils import combine_root_url_and_path
from govexec.models import Page
from cachecow.pagecache import cache_page
from django.views.decorators.cache import cache_control


if hasattr(settings, 'FATPAGES_DEFAULT_TEMPLATE'):
	DEFAULT_TEMPLATE = settings.FATPAGES_DEFAULT_TEMPLATE
else:
	DEFAULT_TEMPLATE = 'staticpages/default.html'

# This view is called from FatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching fatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.
def fatpage(request, url):
    """
    Public interface to the fat page view.

    Models: `staticpages.fatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `fatpages/default.html` if template_name is not defined.
    Context:
        fatpage
            `staticpages.fatpages` object
    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(FatPage, url__exact=url, site=settings.SITE_ID)
    return render_fatpage(request, f)

@csrf_protect
@cache_page
@cache_control(max_age=1800)
def render_fatpage(request, f):
    """
    Internal interface to the fat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in fatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    ad_settings = settings.DART_AD_DEFAULTS.copy()
    """ if the page has a custom dart zone, set the page dart zone to the custom dart zone """

    if f.custom_dart_zone:
        ad_settings['zone'] = f.custom_dart_zone

    page = Page({
        "type": "static",
        "category": None,
        "title": f.title,
        "section": None,
        "preview": False,
        "description": f.excerpt,
        "url": combine_root_url_and_path(settings.SITE_URL, f.get_absolute_url()),
        }, request=request, ad_settings=ad_settings)

    c = RequestContext(request, {
        'fatpage': f,
        'page': page,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FatPage, f.id)
    return response
