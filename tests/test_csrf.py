from conftest import csrf_token, login


def test_state_change_without_csrf_is_rejected(client):
    response = client.post('/login', data={'password': 'test-password'})
    assert response.status_code == 403


def test_state_change_with_invalid_csrf_is_rejected(client):
    response = client.post(
        '/login',
        data={'password': 'test-password', '_csrf_token': 'invalid'},
    )
    assert response.status_code == 403


def test_authenticated_mutation_requires_csrf(client):
    login(client)
    response = client.post('/logout')
    assert response.status_code == 403
