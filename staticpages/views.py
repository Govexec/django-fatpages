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
from websites.models import Page
from cachew.decorators import cache_page_function as cache_page
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
@cache_page(1800)
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

    page = Page({
        "type": "static",
        "category": None,
        "title": f.title,
        "section": None,
        "preview": False,
        "description": f.excerpt,
        "url": combine_root_url_and_path(settings.SITE_URL, f.get_absolute_url()),
        }, request=request)
    page.sailthru.update_from_static(f)

    view_vars = {
        'fatpage': f,
        'page': page,
    }

    ad_unit = "/{}/{}".format(settings.GPT_NETWORK_CODE, settings.GPT_BASE_AD_UNIT_PATH)
    try:
        custom_ad_unit = f.custom_ad_unit.strip()
        if custom_ad_unit:
            if custom_ad_unit.startswith("/"):
                ad_unit += custom_ad_unit
            else:
                ad_unit += "/" + custom_ad_unit
    except:
        pass

    view_vars['gpt'] = {
        'ad_unit': ad_unit,
    }

    c = RequestContext(request, view_vars)
    x = t.render(c)

    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FatPage, f.id)
    return response
