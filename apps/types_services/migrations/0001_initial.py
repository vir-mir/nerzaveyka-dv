# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'types_services_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'types_services', ['Item'])

        # Adding M2M table for field portfolios on 'Item'
        db.create_table(u'types_services_item_portfolios', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_item', models.ForeignKey(orm[u'types_services.item'], null=False)),
            ('to_item', models.ForeignKey(orm[u'portfolio.item'], null=False))
        ))
        db.create_unique(u'types_services_item_portfolios', ['from_item_id', 'to_item_id'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'types_services_item')

        # Removing M2M table for field portfolios on 'Item'
        db.delete_table('types_services_item_portfolios')


    models = {
        u'portfolio.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'active': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'height_prev': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['portfolio.Image']"}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_image'", 'null': 'True', 'to': u"orm['portfolio.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ratio': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'width_prev': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        },
        u'portfolio.image': {
            'Meta': {'object_name': 'Image'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'src_small': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'portfolio.item': {
            'Meta': {'object_name': 'Item'},
            'active': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'count_views': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'blank': 'True'}),
            'dd_creation': ('django.db.models.fields.DateTimeField', [], {}),
            'gallery': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['portfolio.Gallery']", 'null': 'True', 'blank': 'True'}),
            'gallery_is_item': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'blank': 'True'}),
            'seo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['portfolio.Seo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'portfolio.seo': {
            'Meta': {'object_name': 'Seo'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'types_services.item': {
            'Meta': {'object_name': 'Item'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'portfolios': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['portfolio.Item']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['types_services']