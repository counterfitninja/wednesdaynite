import gc
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import template_rendered

from test_stats_goals import stats_app


class MatchupStatsTests(unittest.TestCase):
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

    def add_game(self, date, assignments, scores=(2, 1), abandoned=0):
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

    def get_stats(self, player_id=None, comparisons=(), expected_status=200):
        contexts = []

        def capture(sender, template, context, **extra):
            contexts.append(context)

        query = [('comparison_ids', str(pid)) for pid in comparisons]
        if player_id is not None:
            query.append(('player_id', str(player_id)))
        with template_rendered.connected_to(capture, stats_app.app):
            response = self.client.get('/stats/matchups', query_string=query)
        self.assertEqual(response.status_code, expected_status)
        return response, contexts[0]

    def test_individual_and_combination_counts_across_years_and_colours(self):
        alice = self.add_player('Alice')
        bob = self.add_player('Bob')
        charlie = self.add_player('Charlie')
        absent = self.add_player('Absent')
        extra = self.add_player('Extra')
        self.add_game('2023-01-04', [(alice, 1), (bob, 1), (charlie, 1), (extra, 2)])
        self.add_game('2024-01-03', [(alice, 2), (bob, 1), (charlie, 1), (extra, 2)])
        self.add_game('2025-01-01', [(alice, 1), (bob, 1), (charlie, 2)])
        self.add_game('2026-01-07', [(alice, 2), (bob, 2)])
        self.add_game('2026-01-14', [(alice, 2), (bob, 2), (charlie, 2)], scores=(0, 0))
        self.add_game('2026-01-21', [(alice, 1)])

        response, context = self.get_stats(alice, [bob, charlie])
        self.assertEqual(context['total_games'], 6)
        self.assertEqual(context['combination'], {
            'with_count': 2, 'against_count': 1, 'shared_count': 4, 'split_count': 1
        })
        rows = {row['player_id']: row for row in context['player_rows']}
        self.assertNotIn(alice, rows)
        self.assertEqual((rows[bob]['with_count'], rows[bob]['against_count']), (4, 1))
        self.assertEqual((rows[charlie]['with_count'], rows[charlie]['against_count']), (2, 2))
        self.assertEqual(rows[absent]['shared_count'], 0)
        self.assertEqual([row['player_id'] for row in context['player_rows']], [bob, charlie, extra, absent])
        self.assertIn(b'33.3% of games', response.data)
        self.assertIn(b'16.7% of games', response.data)
        for comparison_id in (bob, charlie):
            self.assertIn(f'value="{comparison_id}" checked'.encode(), response.data)
        self.assertIn(f'value="{alice}"  disabled'.encode(), response.data)

        _, single = self.get_stats(alice, [bob, bob])
        self.assertEqual(single['selected_ids'], {bob})
        self.assertEqual(single['combination'], {
            'with_count': 4, 'against_count': 1, 'shared_count': 5, 'split_count': 0
        })
        _, no_meetings = self.get_stats(alice, [bob, absent])
        self.assertEqual(no_meetings['combination']['shared_count'], 0)

    def test_excludes_abandoned_missing_scores_invalid_teams_and_attendance_only(self):
        alice = self.add_player('Alice')
        bob = self.add_player('Bob')
        self.add_game('2026-01-07', [(alice, 1), (bob, 2)], abandoned=None)
        self.add_game('2026-01-14', [(alice, 1), (bob, 1)], abandoned=1)
        for date, scores in [('2026-01-21', (2, None)), ('2026-01-28', (None, 2)),
                             ('2026-02-04', (None, None))]:
            self.add_game(date, [(alice, 1), (bob, 1)], scores=scores)
        self.add_game('2026-02-11', [(alice, 3), (bob, 1)])
        self.add_game('2026-02-18', [(alice, 2), (bob, 3)])
        game_id = self.add_game('2026-02-25', [(bob, 1)])
        with stats_app.get_db() as conn:
            conn.execute(
                "INSERT INTO attendance (game_id, player_id, status) VALUES (?, ?, 'playing')",
                (game_id, alice)
            )
        _, context = self.get_stats(alice, [bob])
        self.assertEqual(context['total_games'], 2)
        self.assertEqual(context['combination'], {
            'with_count': 0, 'against_count': 1, 'shared_count': 1, 'split_count': 0
        })

    def test_empty_initial_and_zero_game_states(self):
        response, context = self.get_stats()
        self.assertIn(b'No players yet.', response.data)
        self.assertIsNone(context['selected_player'])
        alice = self.add_player('Alice')
        response, context = self.get_stats()
        self.assertIn(b'Choose a main player', response.data)
        self.assertEqual(context['player_rows'], [])
        response, context = self.get_stats(alice)
        self.assertIn(b'No completed games', response.data)
        self.assertIn(b'Add another player', response.data)
        self.assertIsNone(context['combination'])
        bob = self.add_player('Bob')
        response, context = self.get_stats(alice, [bob])
        self.assertIn(b'0.0% of games', response.data)
        self.assertEqual(context['combination']['shared_count'], 0)
        self.assertNotIn(b'nan', response.data.lower())

    def test_invalid_selection_has_explicit_error_and_no_stats(self):
        alice = self.add_player('Alice')
        bob = self.add_player('Bob')
        for player_id, comparisons in [
            ('invalid', []), (99999, []), (alice, ['invalid']),
            (alice, [99999]), (alice, [alice]), (None, [bob])
        ]:
            with self.subTest(player_id=player_id, comparisons=comparisons):
                response, context = self.get_stats(player_id, comparisons, expected_status=400)
                self.assertIn(b'role="alert"', response.data)
                self.assertIsNotNone(context['error'])
                self.assertIsNone(context['combination'])
                self.assertEqual(context['player_rows'], [])

    def test_names_are_escaped_and_navigation_is_available(self):
        alice = self.add_player('<script>alert("Alice")</script>')
        response, _ = self.get_stats(alice)
        self.assertIn(b'&lt;script&gt;', response.data)
        self.assertNotIn(b'<script>alert', response.data)
        for path in ('/leaderboard', '/stats/guide'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'href="/stats/matchups"', response.data)
        with stats_app.app.test_request_context():
            html = stats_app.render_template(
                'player_stats.html', player={'id': alice, 'name': 'Alice'}, year=2026,
                games=[], stats={'games': 0, 'wins': 0, 'draws': 0, 'losses': 0}
            )
        self.assertIn(f'href="/stats/matchups?player_id={alice}"', html)


if __name__ == '__main__':
    unittest.main()
