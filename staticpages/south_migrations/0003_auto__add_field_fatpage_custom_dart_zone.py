# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'FatPage.custom_dart_zone'
        db.add_column('django_flatpage', 'custom_dart_zone', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'FatPage.custom_dart_zone'
        db.delete_column('django_flatpage', 'custom_dart_zone')


    models = {
        'staticpages.fatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FatPage', 'db_table': "'django_flatpage'"},
            'content': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'custom_dart_zone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'excerpt': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['staticpages']
