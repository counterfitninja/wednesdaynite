import gc
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse


repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
with tempfile.TemporaryDirectory() as import_dir:
    original_dir = os.getcwd()
    try:
        os.chdir(import_dir)
        import app as weather_app
    finally:
        os.chdir(original_dir)
        gc.collect()


class HistoricalWeatherTests(unittest.TestCase):
    def test_fetches_only_the_9pm_weather_code_and_temperature(self):
        payload = {
            'hourly': {
                'time': ['2025-06-18T20:00', '2025-06-18T21:00', '2025-06-18T22:00'],
                'weather_code': [3, 61, 0],
                'temperature_2m': [8.1, 7.4, 6.9],
            },
        }
        response = BytesIO(json.dumps(payload).encode('utf-8'))

        with patch.object(weather_app.urllib.request, 'urlopen', return_value=response) as urlopen:
            result = weather_app.get_historical_weather_symbols(['2025-06-18', '2999-01-01'])

        self.assertEqual(result['2025-06-18'], {
            'symbol': '🌧️',
            'description': 'Light rain',
            'temperature': 7.4,
        })
        params = parse_qs(urlparse(urlopen.call_args.args[0]).query)
        self.assertEqual(params['hourly'], ['weather_code,temperature_2m'])
        self.assertEqual(params['temperature_unit'], ['celsius'])
        self.assertEqual(params['timezone'], ['Europe/London'])

    def test_main_games_page_shows_symbol_and_temperature_without_forecast(self):
        connection = sqlite3.connect(':memory:')
        connection.row_factory = sqlite3.Row
        self.addCleanup(connection.close)
        database_patch = patch.object(weather_app, 'get_db', return_value=connection)
        database_patch.start()
        self.addCleanup(database_patch.stop)
        weather_app.init_db()
        with connection:
            connection.execute(
                "INSERT INTO games (date, location) VALUES ('2025-06-18', 'Selwood School')"
            )
        client = weather_app.app.test_client()

        with patch.object(weather_app, 'get_historical_weather_symbols', return_value={
            '2025-06-18': {
                'symbol': '🌧️',
                'description': 'Light rain',
                'temperature': 7.4,
            },
        }):
            response = client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('🌧️ 7°C'.encode('utf-8'), response.data)
        self.assertNotIn('forecast'.encode('utf-8'), response.data.lower())


if __name__ == '__main__':
    unittest.main()
