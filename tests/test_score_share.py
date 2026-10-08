import gc
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
with tempfile.TemporaryDirectory() as import_dir:
    original_dir = os.getcwd()
    try:
        os.chdir(import_dir)
        import app as score_app
    finally:
        os.chdir(original_dir)
        gc.collect()


class GameScoreShareTests(unittest.TestCase):
    def setUp(self):
        self.db_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.cleanup_db)
        self.db_patch = patch.object(score_app, 'DATABASE', str(Path(self.db_dir.name) / 'games.db'))
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        score_app.init_db()
        with score_app.get_db() as conn:
            self.game_id = conn.execute(
                "INSERT INTO games (date, location) VALUES ('2026-10-01', 'Pitch')"
            ).lastrowid
            self.other_game_id = conn.execute(
                "INSERT INTO games (date, location) VALUES ('2026-10-08', 'Other pitch')"
            ).lastrowid
        self.client = score_app.app.test_client()

    def cleanup_db(self):
        gc.collect()
        self.db_dir.cleanup()

    def create_link(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.post(f'/games/{self.game_id}/score-share')
        self.assertEqual(response.status_code, 302)
        with score_app.get_db() as conn:
            token = conn.execute(
                'SELECT token FROM game_score_share_tokens WHERE game_id = ?', (self.game_id,)
            ).fetchone()['token']
        return f'/games/score/shared/{token}'

    def test_only_admin_can_create_and_link_is_private_until_created(self):
        self.assertEqual(self.client.post(f'/games/{self.game_id}/score-share').status_code, 302)
        self.assertEqual(self.client.get(f'/games/{self.game_id}/edit').status_code, 302)
        with score_app.get_db() as conn:
            self.assertIsNone(conn.execute(
                'SELECT token FROM game_score_share_tokens WHERE game_id = ?', (self.game_id,)
            ).fetchone())
        url = self.create_link()
        self.assertIn(url.encode(), self.client.get(f'/games/{self.game_id}/edit').data)
        self.assertEqual(self.client.get('/games/score/shared/not-a-token').status_code, 404)

    def test_anonymous_submission_only_changes_target_game_scores(self):
        url = self.create_link()
        with self.client.session_transaction() as session:
            session.clear()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Referrer-Policy'], 'no-referrer')
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        response = self.client.post(url, data={'team1_score': '0', 'team2_score': '3'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Final score saved.', self.client.get(response.headers['Location']).data)
        self.assertIn(b'value="0"', self.client.get(url).data)
        with score_app.get_db() as conn:
            game = conn.execute('SELECT * FROM games WHERE id = ?', (self.game_id,)).fetchone()
            other = conn.execute('SELECT * FROM games WHERE id = ?', (self.other_game_id,)).fetchone()
            self.assertEqual((game['team1_score'], game['team2_score']), (0, 3))
            self.assertIsNone(other['team1_score'])
            self.assertEqual(game['location'], 'Pitch')

        for scores in (
            {'team1_score': '', 'team2_score': '1'},
            {'team1_score': '-1', 'team2_score': '2'},
            {'team1_score': '1000', 'team2_score': '2'},
            {'team1_score': 'abc', 'team2_score': '2'},
        ):
            self.assertEqual(self.client.post(url, data=scores).status_code, 400)
        with score_app.get_db() as conn:
            game = conn.execute('SELECT * FROM games WHERE id = ?', (self.game_id,)).fetchone()
            self.assertEqual((game['team1_score'], game['team2_score']), (0, 3))

    def test_regeneration_revokes_old_link_and_abandoned_games_cannot_update(self):
        old_url = self.create_link()
        new_url = self.create_link()
        self.assertNotEqual(old_url, new_url)
        self.assertEqual(self.client.post(old_url, data={
            'team1_score': '1', 'team2_score': '2'
        }).status_code, 404)
        with score_app.get_db() as conn:
            conn.execute('UPDATE games SET is_abandoned = 1 WHERE id = ?', (self.game_id,))
        self.assertEqual(self.client.get(new_url).status_code, 409)
        self.assertEqual(self.client.post(new_url, data={
            'team1_score': '1', 'team2_score': '2'
        }).status_code, 409)
        self.assertEqual(self.client.post(f'/games/{self.game_id}/score-share').status_code, 409)
        with score_app.get_db() as conn:
            game = conn.execute('SELECT * FROM games WHERE id = ?', (self.game_id,)).fetchone()
            self.assertIsNone(game['team1_score'])

    def test_deleting_game_removes_its_share_link(self):
        url = self.create_link()
        self.assertEqual(self.client.post(f'/games/{self.game_id}/delete').status_code, 302)
        self.assertEqual(self.client.get(url).status_code, 404)
        with score_app.get_db() as conn:
            self.assertIsNone(conn.execute(
                'SELECT token FROM game_score_share_tokens WHERE game_id = ?', (self.game_id,)
            ).fetchone())


if __name__ == '__main__':
    unittest.main()
