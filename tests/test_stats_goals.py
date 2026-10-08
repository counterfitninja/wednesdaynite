import gc
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import template_rendered


repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
with tempfile.TemporaryDirectory() as import_dir:
    original_dir = os.getcwd()
    try:
        os.chdir(import_dir)
        import app as stats_app
    finally:
        os.chdir(original_dir)
        gc.collect()


class GoalStatsTests(unittest.TestCase):
    def setUp(self):
        self.db_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.cleanup_db)
        self.db_patch = patch.object(stats_app, 'DATABASE', str(Path(self.db_dir.name) / 'games.db'))
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        stats_app.init_db()
        self.client = stats_app.app.test_client()

    def cleanup_db(self):
        gc.collect()
        self.db_dir.cleanup()

    def add_player(self, name):
        with stats_app.get_db() as conn:
            return conn.execute('INSERT INTO players (name) VALUES (?)', (name,)).lastrowid

    def add_game(self, date, scores, assignments, abandoned=0):
        with stats_app.get_db() as conn:
            game_id = conn.execute(
                'INSERT INTO games (date, team1_score, team2_score, is_abandoned) VALUES (?, ?, ?, ?)',
                (date, *scores, abandoned)
            ).lastrowid
            conn.executemany(
                'INSERT INTO team_assignments (game_id, player_id, team_number) VALUES (?, ?, ?)',
                [(game_id, player_id, team) for player_id, team in assignments]
            )
            return game_id

    def get_stats(self):
        contexts = []

        def capture(sender, template, context, **extra):
            contexts.append(context)

        with template_rendered.connected_to(capture, stats_app.app):
            response = self.client.get('/stats/goals')
        self.assertEqual(response.status_code, 200)
        return response, [dict(row) for row in contexts[0]['player_rows']]

    def test_combines_both_teams_and_all_years_for_each_player(self):
        alice = self.add_player('Alice')
        bob = self.add_player('Bob')
        charlie = self.add_player('Charlie')
        self.add_game('2023-01-04', (5, 2), [(alice, 1), (bob, 2), (charlie, 1)])
        self.add_game('2024-01-03', (1, 4), [(alice, 2), (bob, 1)])
        self.add_game('2025-01-01', (3, 3), [(alice, 1)])
        self.add_game('2026-01-07', (0, 2), [(alice, 1), (bob, 2)])
        _, rows = self.get_stats()
        by_player = {row['player_id']: row for row in rows}
        self.assertEqual((by_player[alice]['goals_scored'], by_player[alice]['goals_conceded']), (12, 8))
        self.assertEqual((by_player[bob]['goals_scored'], by_player[bob]['goals_conceded']), (5, 9))
        self.assertEqual((by_player[charlie]['goals_scored'], by_player[charlie]['goals_conceded']), (5, 2))
        self.assertEqual([row['player_id'] for row in rows], [alice, bob, charlie])

    def test_excludes_abandoned_incomplete_unassigned_and_invalid_teams(self):
        alice = self.add_player('Alice')
        absent = self.add_player('Absent')
        self.add_game('2026-01-07', (2, 1), [(alice, 2)], abandoned=None)
        self.add_game('2026-01-14', (100, 200), [(alice, 1)], abandoned=1)
        self.add_game('2026-01-21', (7, None), [(alice, 1)])
        self.add_game('2026-01-28', (None, 9), [(alice, 2)])
        self.add_game('2026-02-04', (None, None), [(alice, 1)])
        self.add_game('2026-02-11', (0, 0), [(alice, 1)])
        game_id = self.add_game('2026-02-18', (50, 60), [])
        with stats_app.get_db() as conn:
            conn.execute(
                "INSERT INTO attendance (game_id, player_id, status) VALUES (?, ?, 'playing')",
                (game_id, alice)
            )
        self.add_game('2026-02-25', (80, 90), [(alice, 3)])
        response, rows = self.get_stats()
        by_player = {row['player_id']: row for row in rows}
        self.assertEqual((by_player[alice]['goals_scored'], by_player[alice]['goals_conceded']), (1, 2))
        self.assertEqual((by_player[absent]['goals_scored'], by_player[absent]['goals_conceded']), (0, 0))
        self.assertIn(b'Goals scored', response.data)
        self.assertIn(b'Goals conceded', response.data)
        self.assertIn(b'not goals scored individually', response.data)

    def test_zero_totals_and_empty_state(self):
        response, rows = self.get_stats()
        self.assertEqual(rows, [])
        self.assertIn(b'No players yet.', response.data)
        alice = self.add_player('Alice')
        response, rows = self.get_stats()
        self.assertEqual(rows, [{
            'player_id': alice, 'name': 'Alice', 'goals_scored': 0, 'goals_conceded': 0
        }])
        self.assertNotIn(b'No players yet.', response.data)

    def test_navigation_links_from_leaderboard_and_stats_guide(self):
        for path in ('/leaderboard', '/stats/guide', '/stats/margins', '/stats/balance'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'href="/stats/goals"', response.data)


if __name__ == '__main__':
    unittest.main()
