from django.conf import settings

from c3nav.mapdata.inclusion import get_maybe_invisible_areas_names
from c3nav.mapdata.utils.cache import get_packages_cached


def get_public_packages():
    packages_cached = get_packages_cached()
    return [packages_cached[name] for name in settings.PUBLIC_PACKAGES]


def get_nonpublic_packages():
    packages_cached = get_packages_cached()
    return [package for name, package in packages_cached.items() if name not in settings.PUBLIC_PACKAGES]


def get_unlocked_packages(request, packages_cached=None):
    return tuple(get_packages_cached().values()) if request.c3nav_full_access else get_public_packages()


def get_unlocked_packages_names(request, packages_cached=None):
    if request.c3nav_full_access:
        return get_packages_cached().keys()
    return settings.PUBLIC_PACKAGES


def can_access_package(request, package):
    return request.c3nav_full_access or package.name in get_unlocked_packages_names(request)


def filter_queryset_by_access(request, queryset):
    return queryset if request.c3nav_full_access else queryset.filter(package__in=get_unlocked_packages(request))


def get_visible_areas(request):
    areas = [':full' if request.c3nav_full_access else ':base']
    areas += [name for name in get_maybe_invisible_areas_names() if name in request.c3nav_access_list]
    return areas