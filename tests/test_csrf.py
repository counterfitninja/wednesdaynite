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


def test_bulk_attendance_confirmation_accepts_csrf(client):
    token = login(client)
    response = client.post(
        '/games/999999/bulk-attendance-confirm',
        data={'_csrf_token': token},
    )
    assert response.status_code in (301, 302)
