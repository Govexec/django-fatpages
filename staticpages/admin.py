from django import forms
from django.contrib import admin
from staticpages.models import FatPage
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class FatpageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = FatPage
        fields = (
            'site', 'url', 'title', 'content', 'enable_comments', 'excerpt',
            'template_name', 'custom_dart_zone', 'suppress_welcome_ad',
        )


class FatPageAdmin(admin.ModelAdmin):
    form = FatpageForm
    fieldsets = (
        (None, {'fields': ('site', 'url', 'title', 'content', 'enable_comments', 'excerpt', 'template_name', 'custom_dart_zone', 'suppress_welcome_ad',)}),
    )
    ordering = ['site']
    list_display = ('__unicode__', 'url')
    search_fields = ('title', 'url')

    class Media:
        js = (
            '/static/js/jquery-1.8.1.min.js',
            settings.NON_CDN_STATIC_URL + 'js/responsive_embed.js',
        )

admin.site.register(FatPage, FatPageAdmin)
