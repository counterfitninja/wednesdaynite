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
        import app as payment_app
    finally:
        os.chdir(original_dir)
        gc.collect()


class PlayerPaymentTests(unittest.TestCase):
    def setUp(self):
        self.db_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.db_dir.cleanup)
        self.db_patch = patch.object(
            payment_app, 'DATABASE', str(Path(self.db_dir.name) / 'payments.db')
        )
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        self.addCleanup(self.cleanup_db)
        payment_app.init_db()
        with payment_app.get_db() as conn:
            self.player_id = conn.execute(
                "INSERT INTO players (name) VALUES ('Alice')"
            ).lastrowid
            self.game_id = conn.execute(
                "INSERT INTO games (date, location) VALUES ('2026-11-18', 'Pitch')"
            ).lastrowid
            self.attendance_id = conn.execute(
                '''
                INSERT INTO attendance (game_id, player_id, status, paid)
                VALUES (?, ?, 'playing', 0)
                ''',
                (self.game_id, self.player_id),
            ).lastrowid

        self.client = payment_app.app.test_client()
        with self.client.session_transaction() as session:
            session['logged_in'] = True

    def cleanup_db(self):
        gc.collect()
        self.db_dir.cleanup()

    def test_ajax_payment_update_persists_checked_and_unchecked_values(self):
        endpoint = f'/players/{self.player_id}/payments'
        headers = {'X-Requested-With': 'XMLHttpRequest'}

        response = self.client.post(
            endpoint,
            data={'attendance_id': self.attendance_id, 'paid': '1'},
            headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['ok'])
        self.assertEqual(response.get_json()['paid_weeks'], 1)

        with payment_app.get_db() as conn:
            self.assertEqual(
                conn.execute(
                    'SELECT paid FROM attendance WHERE id = ?',
                    (self.attendance_id,),
                ).fetchone()['paid'],
                1,
            )

        response = self.client.post(
            endpoint,
            data={'attendance_id': self.attendance_id},
            headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['paid_weeks'], 0)

        with payment_app.get_db() as conn:
            self.assertEqual(
                conn.execute(
                    'SELECT paid FROM attendance WHERE id = ?',
                    (self.attendance_id,),
                ).fetchone()['paid'],
                0,
            )


if __name__ == '__main__':
    unittest.main()
