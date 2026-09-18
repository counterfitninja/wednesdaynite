from pathlib import Path

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


def test_invalid_csrf_logs_safe_request_diagnostics(client, caplog):
    with caplog.at_level('INFO', logger='app'):
        response = client.post(
            '/login',
            data={'password': 'test-password', '_csrf_token': 'invalid'},
        )

    assert response.status_code == 403
    message = '\n'.join(record.getMessage() for record in caplog.records)
    assert 'CSRF request:' in message
    assert 'source=form' in message
    assert 'valid=False' in message
    assert 'supplied_fp=' in message
    assert 'invalid' not in message.split('supplied_fp=', 1)[1].split(' ', 1)[0]


def test_csrf_logger_is_enabled_for_info_diagnostics():
    import logging

    application_logger = logging.getLogger('app')
    assert application_logger.isEnabledFor(logging.INFO)


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


def test_bulk_attendance_confirmation_rejects_missing_csrf(client):
    login(client)
    response = client.post('/games/999999/bulk-attendance-confirm')
    assert response.status_code == 403


def test_signed_csrf_token_from_another_session_is_rejected(client):
    token = login(client)
    with client.session_transaction() as session:
        session['_csrf_token'] = 'rotated-session-token'
    response = client.post(
        '/games/999999/bulk-attendance-confirm',
        data={'_csrf_token': token},
    )
    assert response.status_code == 403


def test_game_detail_bulk_form_contains_csrf_token(client):
    login(client)
    template = Path(__file__).resolve().parents[1] / 'templates' / 'game_detail.html'
    source = template.read_text(encoding='utf-8')
    assert 'name="_csrf_token" value="{{ csrf_token() }}"' in source
    assert 'HTMLFormElement.prototype.submit.call(_bulkForm)' in source
