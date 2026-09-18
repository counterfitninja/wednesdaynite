from conftest import connect, csrf_token, login


def test_team_view_is_read_only_for_anonymous_client(client, app, db_path):
    with connect(db_path) as conn:
        game_id = conn.execute("INSERT INTO games (date, location) VALUES ('2026-09-23', 'Test')").lastrowid
        conn.commit()
    response = client.get(f'/games/{game_id}/teams')
    assert response.status_code == 200
    with connect(db_path) as conn:
        assert conn.execute('SELECT COUNT(*) FROM team_assignments').fetchone()[0] == 0


def test_team_generation_requires_csrf(client, db_path):
    login(client)
    with connect(db_path) as conn:
        game_id = conn.execute("INSERT INTO games (date) VALUES ('2026-09-23')").lastrowid
        conn.commit()
    response = client.post(f'/games/{game_id}/teams')
    assert response.status_code == 403


def test_invalid_attendance_status_is_rejected_without_write(client, db_path):
    token = login(client)
    with connect(db_path) as conn:
        game_id = conn.execute("INSERT INTO games (date) VALUES ('2026-09-23')").lastrowid
        player_id = conn.execute("INSERT INTO players (name) VALUES ('Test Player')").lastrowid
        conn.commit()
    response = client.post(f'/games/{game_id}/attendance', data={
        '_csrf_token': token, 'player_id': player_id, 'status': 'invalid-status'
    })
    assert response.status_code in (200, 302, 400)
    with connect(db_path) as conn:
        assert conn.execute('SELECT COUNT(*) FROM attendance').fetchone()[0] == 0
