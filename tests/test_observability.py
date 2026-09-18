import sqlite3


def test_health_response_excludes_host_and_port(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert set(response.json) == {'status', 'build_version'}
    assert response.json['status'] == 'ok'


def test_health_failure_is_safe(client, monkeypatch):
    import app as application

    def unavailable_db():
        raise sqlite3.OperationalError('secret database path')

    monkeypatch.setattr(application, 'get_db', unavailable_db)
    response = client.get('/healthz')
    assert response.status_code == 503
    assert response.json['status'] == 'degraded'
    assert 'secret database path' not in response.get_data(as_text=True)
