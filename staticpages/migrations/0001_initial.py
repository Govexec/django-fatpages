# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import sailthru_wrapper.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FatPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=100, verbose_name='URL', db_index=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('content', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('excerpt', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('enable_comments', models.BooleanField(default=False, verbose_name='enable comments')),
                ('template_name', models.CharField(default=False, help_text="Example: 'staticpages/contact_page.html'. If this isn't provided, the system will use 'the default.", max_length=70, verbose_name='template name', blank=True)),
                ('suppress_welcome_ad', models.BooleanField(default=False)),
                ('registration_required', models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='registration required')),
                ('custom_dart_zone', models.CharField(max_length=25, null=True, blank=True)),
                ('site', models.ForeignKey(default=1, to='sites.Site')),
            ],
            options={
                'ordering': ('url',),
                'db_table': 'django_flatpage',
                'verbose_name': 'static page',
                'verbose_name_plural': 'static pages',
            },
            bases=(models.Model, sailthru_wrapper.models.mixins.SailthruContentModelMixin),
        ),
    ]
