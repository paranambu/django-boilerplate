from django.conf import settings
from django.template import Context, Template
from django.test.client import RequestFactory


def test_get_settings():
    template = Template('{% load utils %}{% get_settings "DEBUG" %}')
    rendered = template.render(Context())
    assert rendered == str(settings.DEBUG)


def test_build_absolute_url():
    template = Template('{% load utils %}{% build_absolute_url %}')
    request_factory = RequestFactory()
    request = request_factory.get('/test/')
    context = Context({'request': request})
    rendered = template.render(context)
    assert rendered == 'http://testserver/test/'


def test_build_absolute_url_with_location():
    template = Template('{% load utils %}{% build_absolute_url "/admin/" %}')
    request_factory = RequestFactory()
    request = request_factory.get('/test/')
    context = Context({'request': request})
    rendered = template.render(context)
    assert rendered == 'http://testserver/admin/'


def test_get_language_info():
    template = Template('{% load utils %}{% get_language_info "es" as language_info %}{{ language_info.code }}')
    rendered = template.render(Context())
    assert rendered == 'es'


def test_subtract():
    template = Template('{% load utils %}{{ 10|subtract:1 }}')
    rendered = template.render(Context())
    assert rendered == '9'
