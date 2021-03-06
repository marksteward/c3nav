# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-08 14:04
from __future__ import unicode_literals

import c3nav.mapdata.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0062_auto_20170508_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arealocation',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
        migrations.AlterField(
            model_name='building',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
        migrations.AlterField(
            model_name='door',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
        migrations.AlterField(
            model_name='hole',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
        migrations.AlterField(
            model_name='lineobstacle',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polyline'),
        ),
        migrations.AlterField(
            model_name='obstacle',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
        migrations.AlterField(
            model_name='space',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
        migrations.AlterField(
            model_name='stair',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polyline'),
        ),
        migrations.AlterField(
            model_name='stuffedarea',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(geomtype='polygon'),
        ),
    ]
