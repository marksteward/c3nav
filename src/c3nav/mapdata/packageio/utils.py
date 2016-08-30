import json
import sys

from django.core.management.base import CommandError

from ..models import Level, Package, Source


class ObjectCollection:
    def __init__(self):
        self.packages = {}
        self.levels = {}
        self.sources = {}

    def add_package(self, package):
        self._add(self.packages, 'package', package)

    def add_level(self, level):
        self._add(self.levels, 'level', level)

    def add_source(self, source):
        self._add(self.sources, 'source', source)

    def add_packages(self, packages):
        for package in packages:
            self.add_package(package)

    def add_levels(self, levels):
        for level in levels:
            self.add_level(level)

    def add_sources(self, sources):
        for source in sources:
            self.add_source(source)

    def _add(self, container, name, item):
        if item['name'] in container:
            raise CommandError('Duplicate %s name: %s' % (name, item['name']))
        container[item['name']] = item

    def apply_to_db(self):
        for name, package in tuple(self.packages.items()):
            package, created = Package.objects.update_or_create(name=name, defaults=package)
            self.packages[name] = package
            if created:
                print('- Created package: '+name)

        for name, level in self.levels.items():
            level['package'] = self.packages[level['package']]
            level, created = Level.objects.update_or_create(name=name, defaults=level)
            self.levels[name] = level
            if created:
                print('- Created level: '+name)

        for name, source in self.sources.items():
            source['package'] = self.packages[source['package']]
            source, created = Source.objects.update_or_create(name=name, defaults=source)
            self.sources[name] = source
            if created:
                print('- Created source: '+name)

        for source in Source.objects.exclude(name__in=self.sources.keys()):
            print('- Deleted source: '+source.name)
            source.delete()

        for level in Level.objects.exclude(name__in=self.levels.keys()):
            print('- Deleted level: '+level.name)
            level.delete()

        for package in Package.objects.exclude(name__in=self.packages.keys()):
            print('- Deleted package: '+package.name)
            package.delete()


def _preencode(data, magic_marker):
    if isinstance(data, dict):
        data = data.copy()
        for name, value in tuple(data.items()):
            if name in ('bounds', ):
                data[name] = magic_marker+json.dumps(value)+magic_marker
            else:
                data[name] = _preencode(value, magic_marker)
        return data
    elif isinstance(data, (tuple, list)):
        return tuple(_preencode(value, magic_marker) for value in data)
    else:
        return data


def json_encode(data):
    magic_marker = '***JSON_MAGIC_MARKER***'
    test_encode = json.dumps(data)
    while magic_marker in test_encode:
        magic_marker += '*'
    result = json.dumps(_preencode(data, magic_marker), indent=4)
    return result.replace('"'+magic_marker, '').replace(magic_marker+'"', '')+'\n'
