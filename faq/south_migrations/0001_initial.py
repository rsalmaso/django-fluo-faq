# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings

user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'faq_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('fluo.models.fields.StatusField')()),
            ('ordering', self.gf('fluo.models.fields.OrderField')(default=0, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'faq', ['Topic'])

        # Adding model 'Faq'
        db.create_table(u'faq_faq', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordering', self.gf('fluo.models.fields.OrderField')(default=0, blank=True)),
            ('created_at', self.gf('fluo.models.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_modified_at', self.gf('fluo.models.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('status', self.gf('fluo.models.fields.StatusField')(default='draft')),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'faq-faq-owned', null=True, to=orm[user_model])),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('pub_date_begin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('pub_date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'faq', ['Faq'])

        # Adding M2M table for field users on 'Faq'
        m2m_table_name = db.shorten_name(u'faq_faq_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faq', models.ForeignKey(orm[u'faq.faq'], null=False)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['faq_id', 'user_id'])

        # Adding M2M table for field topics on 'Faq'
        m2m_table_name = db.shorten_name(u'faq_faq_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faq', models.ForeignKey(orm[u'faq.faq'], null=False)),
            ('topic', models.ForeignKey(orm[u'faq.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['faq_id', 'topic_id'])

        # Adding model 'FaqTranslation'
        db.create_table(u'faq_faqtranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['faq.Faq'])),
        ))
        db.send_create_signal(u'faq', ['FaqTranslation'])

        # Adding unique constraint on 'FaqTranslation', fields ['parent', 'language']
        db.create_unique(u'faq_faqtranslation', ['parent_id', 'language'])

        # Adding unique constraint on 'FaqTranslation', fields ['title', 'slug']
        db.create_unique(u'faq_faqtranslation', ['title', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'FaqTranslation', fields ['title', 'slug']
        db.delete_unique(u'faq_faqtranslation', ['title', 'slug'])

        # Removing unique constraint on 'FaqTranslation', fields ['parent', 'language']
        db.delete_unique(u'faq_faqtranslation', ['parent_id', 'language'])

        # Deleting model 'Topic'
        db.delete_table(u'faq_topic')

        # Deleting model 'Faq'
        db.delete_table(u'faq_faq')

        # Removing M2M table for field users on 'Faq'
        db.delete_table(db.shorten_name(u'faq_faq_users'))

        # Removing M2M table for field topics on 'Faq'
        db.delete_table(db.shorten_name(u'faq_faq_topics'))

        # Deleting model 'FaqTranslation'
        db.delete_table(u'faq_faqtranslation')


    models = {
        user_model: {
            'Meta': {'object_name': user_model.split('.')[1]},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'faq.faq': {
            'Meta': {'object_name': 'Faq'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('fluo.models.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_at': ('fluo.models.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ordering': ('fluo.models.fields.OrderField', [], {'default': '0', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'faq-faq-owned'", 'null': 'True', 'to': u"orm[user_model]"}),
            'pub_date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('fluo.models.fields.StatusField', [], {'default': "'draft'"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['faq.Topic']", 'symmetrical': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'faq-faq-visible'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm[user_model]"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'})
        },
        u'faq.faqtranslation': {
            'Meta': {'unique_together': "(('parent', 'language'), ('title', 'slug'))", 'object_name': 'FaqTranslation'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['faq.Faq']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'faq.topic': {
            'Meta': {'object_name': 'Topic'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ordering': ('fluo.models.fields.OrderField', [], {'default': '0', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('fluo.models.fields.StatusField', [], {})
        },
        u'locations.administrativearea1': {
            'Meta': {'object_name': 'AdministrativeArea1'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.administrativearea2': {
            'Meta': {'object_name': 'AdministrativeArea2'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.administrativearea3': {
            'Meta': {'object_name': 'AdministrativeArea3'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.locality': {
            'Meta': {'object_name': 'Locality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'administrative_area_level_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'locations'", 'null': 'True', 'to': u"orm['locations.AdministrativeArea1']"}),
            'administrative_area_level_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'locations'", 'null': 'True', 'to': u"orm['locations.AdministrativeArea2']"}),
            'administrative_area_level_3': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'locations'", 'null': 'True', 'to': u"orm['locations.AdministrativeArea3']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'locations'", 'null': 'True', 'to': u"orm['locations.Country']"}),
            'dump': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'geo_lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'geo_lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'locations'", 'null': 'True', 'to': u"orm['locations.Locality']"}),
            'other_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'locations'", 'to': u"orm[user_model]"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'telephone_no': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['faq']
