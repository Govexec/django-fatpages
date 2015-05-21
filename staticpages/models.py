from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.conf import settings

from sailthru_wrapper.models.mixins import SailthruContentModelMixin

class FatPage(models.Model, SailthruContentModelMixin):
    site = models.ForeignKey(Site, default=1)
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = RichTextField(null=True, blank=True)
    excerpt = RichTextField(null=True, blank=True)
    enable_comments = models.BooleanField(_('enable comments'), default=False)

    template_name = models.CharField(
        _('template name'), default=False, max_length=70, blank=True,
        help_text=_("Example: 'staticpages/contact_page.html'. If this isn't provided, the system will use 'the default.")
    )

    suppress_welcome_ad = models.BooleanField(default=False)

    registration_required = models.BooleanField(
        _('registration required'), default=False,
        help_text=_("If this is checked, only logged-in users will be able to view the page.")
    )

    custom_dart_zone = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        db_table = 'django_flatpage'
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.site.name, self.title)

    def get_absolute_url(self):
        return self.url

    def get_full_absolute_url(self):
        return 'http://' + self.site.domain + self.url

    def is_published(self):
        return True

    def sailthru_data(self):
        data = super(FatPage, self).sailthru_data()
        data.update({
            'update-from': 'update_from_static',
        })
        return data

    def save(self, *args, **kwargs):
        self.update_sailthru_handle_delete_outdated()
        super(FatPage, self).save(*args, **kwargs)
        self.update_sailthru_handle_change()
