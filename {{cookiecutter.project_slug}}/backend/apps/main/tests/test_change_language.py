from unittest import mock

from django.urls import reverse
from django.utils.translation import LANGUAGE_SESSION_KEY

from ..views import change_language


@mock.patch('django.utils.translation.activate')
def test_change_language(activate_mock, client):
    url = reverse('change-language')
    response = client.post(url, {'language': 'es'})
    activate_mock.assert_called_with('es')
    assert response.client.session[LANGUAGE_SESSION_KEY] == 'es'
    assert response.status_code == 204


@mock.patch('django.utils.translation.activate')
def test_change_language_redirect(activate_mock, client):
    url = reverse('change-language')
    response = client.post(url, {'language': 'es', 'redirect_to': '/'}, follow=True)
    last_url, status_code = response.redirect_chain[0]
    assert last_url == '/'
    assert status_code == 302
