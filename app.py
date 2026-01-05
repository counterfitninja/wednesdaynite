from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATABASE = 'football.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                phone TEXT,
                email TEXT,
                skill_rating INTEGER DEFAULT 5 CHECK(skill_rating >= 1 AND skill_rating <= 10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                location TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('playing', 'not_playing', 'maybe')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games(id),
                FOREIGN KEY (player_id) REFERENCES players(id),
                UNIQUE(game_id, player_id)
            )
        ''')
        
        conn.execute('CREATE INDEX IF NOT EXISTS idx_attendance_game ON attendance(game_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_attendance_player ON attendance(player_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_games_date ON games(date)')
        conn.commit()

@app.route('/')
def index():
    with get_db() as conn:
        games = conn.execute('SELECT * FROM games ORDER BY date DESC LIMIT 10').fetchall()
        
        game_data = []
        for game in games:
            attendance = conn.execute('''
                SELECT COUNT(*) as count 
                FROM attendance 
                WHERE game_id = ? AND status = 'playing'
            ''', (game['id'],)).fetchone()
            
            game_data.append({
                'id': game['id'],
                'date': game['date'],
                'location': game['location'],
                'notes': game['notes'],
                'players_count': attendance['count']
            })
    
    return render_template('index.html', games=game_data)

@app.route('/players')
def players():
    with get_db() as conn:
        players = conn.execute('''
            SELECT 
                p.*,
                COUNT(a.id) as total_games,
                SUM(CASE WHEN a.status = 'playing' THEN 1 ELSE 0 END) as games_played,
                CASE 
                    WHEN COUNT(a.id) > 0 
                    THEN CAST(SUM(CASE WHEN a.status = 'playing' THEN 1 ELSE 0 END) AS REAL) / COUNT(a.id) * 100
                    ELSE 0
                END as attendance_rate
            FROM players p
            LEFT JOIN attendance a ON p.id = a.player_id
            GROUP BY p.id
            ORDER BY attendance_rate DESC, p.name
        ''').fetchall()
    
    return render_template('players.html', players=players)
@app.route('/players/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        skill_rating = request.form.get('skill_rating', 5)
        
        try:
            with get_db() as conn:
                conn.execute('INSERT INTO players (name, phone, email, skill_rating) VALUES (?, ?, ?, ?)',
                           (name, phone, email, skill_rating))
                conn.commit()
            return redirect(url_for('players'))
        except sqlite3.IntegrityError:
            return render_template('add_player.html', error='Player already exists')
    
    return render_template('add_player.html')

@app.route('/players/<int:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    with get_db() as conn:
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form.get('phone', '')
            email = request.form.get('email', '')
            skill_rating = request.form.get('skill_rating', 5)
            
            conn.execute('UPDATE players SET name = ?, phone = ?, email = ?, skill_rating = ? WHERE id = ?',
                       (name, phone, email, skill_rating, player_id))
            conn.commit()
            return redirect(url_for('players'))
        
        player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
        if not player:
            return "Player not found", 404
        
        return render_template('edit_player.html', player=player)
    return render_template('add_player.html')

@app.route('/games/add', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        date = request.form['date']
        location = request.form.get('location', '')
        notes = request.form.get('notes', '')
        
        with get_db() as conn:
            conn.execute('INSERT INTO games (date, location, notes) VALUES (?, ?, ?)',
                       (date, location, notes))
            conn.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_game.html')

@app.route('/games/<int:game_id>')
def game_detail(game_id):
    with get_db() as conn:
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
        
        if not game:
            return "Game not found", 404
        
        attendance = conn.execute('''
            SELECT p.*, a.status
            FROM attendance a
            JOIN players p ON a.player_id = p.id
            WHERE a.game_id = ?
            ORDER BY a.status, p.name
        ''', (game_id,)).fetchall()
        
        all_players = conn.execute('SELECT * FROM players ORDER BY name').fetchall()
    
    playing = [a for a in attendance if a['status'] == 'playing']
    not_playing = [a for a in attendance if a['status'] == 'not_playing']
    maybe = [a for a in attendance if a['status'] == 'maybe']
    
    return render_template('game_detail.html', 
                         game=game, 
@app.route('/games/<int:game_id>/teams')
def generate_teams(game_id):
    import random
    
    with get_db() as conn:
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
        
        if not game:
            return "Game not found", 404
        
        # Get all players marked as playing
        playing = conn.execute('''
            SELECT p.*, a.status
            FROM attendance a
            JOIN players p ON a.player_id = p.id
            WHERE a.game_id = ? AND a.status = 'playing'
            ORDER BY p.name
        ''', (game_id,)).fetchall()
        
        if len(playing) < 2:
            return render_template('teams.html', game=game, error='Need at least 2 players to create teams')
        
        # Convert to list and shuffle
        players_list = list(playing)
        random.shuffle(players_list)
        
        # Sort by skill rating (descending) for balanced distribution
        players_list.sort(key=lambda p: p['skill_rating'] or 5, reverse=True)
        
        # Alternate assignment to balance teams
        team1 = []
        team2 = []
        team1_skill = 0
        team2_skill = 0
        
        for player in players_list:
            skill = player['skill_rating'] or 5
            if team1_skill <= team2_skill:
                team1.append(player)
                team1_skill += skill
            else:
                team2.append(player)
                team2_skill += skill
        
        # Calculate average skill
        team1_avg = team1_skill / len(team1) if team1 else 0
        team2_avg = team2_skill / len(team2) if team2 else 0
        
        return render_template('teams.html', 
                             game=game,
                             team1=team1,
                             team2=team2,
                             team1_skill=team1_skill,
                             team2_skill=team2_skill,
                             team1_avg=team1_avg,
                             team2_avg=team2_avg)

@app.route('/import', methods=['GET', 'POST'])
def import_csv():        not_playing=not_playing,
                         maybe=maybe,
                         all_players=all_players)

@app.route('/games/<int:game_id>/attendance', methods=['POST'])
def update_attendance(game_id):
    player_id = request.form['player_id']
    status = request.form['status']
    
    with get_db() as conn:
        conn.execute('''
            INSERT INTO attendance (game_id, player_id, status) 
            VALUES (?, ?, ?)
            ON CONFLICT(game_id, player_id) 
            DO UPDATE SET status = excluded.status
        ''', (game_id, player_id, status))
        conn.commit()
    
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/import', methods=['GET', 'POST'])
def import_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('import.html', error='No file selected')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('import.html', error='No file selected')
        
        date = request.form['date']
        location = request.form.get('location', 'Weekly Game')
        
        try:
            import csv
            import io
            
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            with get_db() as conn:
                # Create game
                cursor = conn.execute('INSERT INTO games (date, location, notes) VALUES (?, ?, ?)',
                                    (date, location, f'Imported from CSV on {datetime.now()}'))
                game_id = cursor.lastrowid
                
                imported = 0
                for row in csv_reader:
                    player_name = row.get('Player Name') or row.get('Name') or row.get('player')
                    status_raw = row.get('Status') or row.get('status') or row.get('Response')
                    
                    if not player_name:
                        continue
                    
                    # Normalize status
                    status_lower = status_raw.lower().strip()
                    if status_lower in ['yes', '✓', '✅', 'playing', 'in']:
                        status = 'playing'
                    elif status_lower in ['maybe', '?', '❓']:
                        status = 'maybe'
                    else:
                        status = 'not_playing'
                    
                    # Get or create player
                    player = conn.execute('SELECT id FROM players WHERE name = ?', (player_name,)).fetchone()
                    
                    if not player:
                        cursor = conn.execute('INSERT INTO players (name) VALUES (?)', (player_name,))
                        player_id = cursor.lastrowid
                    else:
                        player_id = player['id']
                    
                    # Record attendance
                    conn.execute('INSERT INTO attendance (game_id, player_id, status) VALUES (?, ?, ?)',
                               (game_id, player_id, status))
                    imported += 1
                
                conn.commit()
            
            return render_template('import.html', success=f'Imported {imported} records for game on {date}')
        
        except Exception as e:
            return render_template('import.html', error=f'Import failed: {str(e)}')
    
    return render_template('import.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
