# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-10 19:13
from __future__ import unicode_literals

from django.db import migrations

from c3nav.mapdata.utils.geometry import assert_multipolygon


def assign_locations_area(apps, schema_editor):
    Space = apps.get_model('mapdata', 'Space')
    Area = apps.get_model('mapdata', 'Area')
    AreaLocation = apps.get_model('mapdata', 'AreaLocation')
    LocationSlug = apps.get_model('mapdata', 'LocationSlug')
    LocationGroup = apps.get_model('mapdata', 'LocationGroup')
    for obj in AreaLocation.objects.filter(location_type='area').order_by('slug'):
        spaces = [s for s in Space.objects.filter(section=obj.section, level='')
                  if s.geometry.intersection(obj.geometry).area / s.geometry.area > 0.10]

        if not spaces:
            obj.delete()
            continue

        total_spaces = [s for s in spaces
                        if s.geometry.intersection(obj.geometry).area / s.geometry.area > 0.95]
        partial_spaces = [s for s in spaces if s not in total_spaces]

        to_obj = LocationGroup()
        to_obj.locationslug_ptr = LocationSlug.objects.create(slug=obj.slug)
        to_obj.titles = obj.titles
        to_obj.can_search = obj.can_search
        to_obj.can_describe = obj.can_describe
        to_obj.color = obj.color
        to_obj.compiled_area = True
        to_obj.save()

        for space in total_spaces:
            space.groups.add(to_obj)

        for space in partial_spaces:
            for polygon in assert_multipolygon(space.geometry.intersection(obj.geometry)):
                area = Area()
                area.locationslug_ptr = LocationSlug.objects.create()
                area.geometry = polygon
                area.space = space
                area.can_search = False
                area.can_describe = False
                area.save()
                area.groups.add(to_obj)

        obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0088_locationgroup_compiled_area'),
    ]

    operations = [
        migrations.RunPython(assign_locations_area),
    ]
