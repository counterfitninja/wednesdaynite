from conftest import csrf_token, login


def test_admin_route_redirects_anonymous(client):
    response = client.get('/admin')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_login_accepts_credentials_and_rejects_external_redirect(client):
    token = csrf_token(client)
    response = client.post(
        '/login?next=https://example.com',
        data={'password': 'test-password', '_csrf_token': token},
    )
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/admin')


def test_logout_requires_csrf_and_clears_session(client):
    login(client)
    denied = client.post('/logout')
    assert denied.status_code == 403
    token = csrf_token(client)
    response = client.post('/logout', data={'_csrf_token': token})
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert not session.get('logged_in')
