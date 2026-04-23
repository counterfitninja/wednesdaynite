from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from datetime import datetime, timedelta
import os
from functools import wraps
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-to-something-secure-in-production')
# Keep admin sessions alive longer by default; can be overridden via env var.
session_lifetime_days = int(os.environ.get('SESSION_LIFETIME_DAYS', '180'))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=session_lifetime_days)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# Build version - timestamp when app starts
BUILD_VERSION = datetime.now().strftime('%Y.%m.%d.%H%M')

# Network config
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', os.environ.get('SERVER_PORT', 5000)))

# Admin password - require environment variable in production
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
if not ADMIN_PASSWORD:
    # Only use default if not in Azure (no WEBSITE_INSTANCE_ID)
    if not os.environ.get('WEBSITE_INSTANCE_ID'):
        ADMIN_PASSWORD = 'football2026'
    else:
        raise ValueError('ADMIN_PASSWORD environment variable must be set in Azure')

@app.context_processor
def inject_build_version():
    final_score_game_id = None
    try:
        with get_db() as conn:
            latest_pending = conn.execute('''
                SELECT id FROM games
                WHERE date <= date('now')
                    AND (is_abandoned IS NULL OR is_abandoned = 0)
                    AND (team1_score IS NULL OR team2_score IS NULL)
                ORDER BY date DESC
                LIMIT 1
            ''').fetchone()

            latest_completed = conn.execute('''
                SELECT id FROM games
                WHERE date <= date('now')
                    AND (is_abandoned IS NULL OR is_abandoned = 0)
                ORDER BY date DESC
                LIMIT 1
            ''').fetchone()

            target = latest_pending if latest_pending else latest_completed
            if target:
                final_score_game_id = target['id']
    except Exception as exc:
        print(f"DEBUG - final score lookup failed: {exc}")

    return {
        'build_version': BUILD_VERSION,
        'is_admin': session.get('logged_in', False),
        'final_score_game_id': final_score_game_id
    }

@app.route('/team-balancer')
def team_balancer():
    return render_template('team_balancer.html')

# Simple health/version endpoints for smoke testing
@app.route('/healthz')
@app.route('/status')
def healthcheck():
    return {'status': 'ok', 'build_version': BUILD_VERSION, 'host': HOST, 'port': PORT}

@app.template_filter('ukdate')
def format_uk_date(date_string):
    """Convert YYYY-MM-DD to DD/MM/YYYY format"""
    if not date_string:
        return ''
    try:
        from datetime import datetime
        date_obj = datetime.strptime(str(date_string), '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except:
        return date_string

@app.template_filter('name_initial')
def format_name_with_initial(full_name):
    """Format name as 'FirstName S.' (first name + surname initial)"""
    if not full_name:
        return ''
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0]
    elif len(parts) >= 2:
        return f"{parts[0]} {parts[-1][0]}."
    return full_name

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Use /home directory in Azure Web Apps for persistent storage
if os.environ.get('WEBSITE_INSTANCE_ID'):
    # Running in Azure
    DATABASE = '/home/football.db'
else:
    # Running locally
    DATABASE = 'football.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


ALLOWED_FACE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
FACE_IMAGE_MAX_DIMENSION = 256
FACE_IMAGE_WEBP_QUALITY = 82


def _face_storage_dir():
    return os.path.join(app.static_folder, 'player_faces')


def allowed_face_file(filename):
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_FACE_EXTENSIONS


def get_player_face_url(player_id):
    base_dir = _face_storage_dir()
    for ext in ('png', 'jpg', 'jpeg', 'webp', 'gif'):
        path = os.path.join(base_dir, f'{player_id}.{ext}')
        if os.path.exists(path):
            return f'/static/player_faces/{player_id}.{ext}'
    return None


def save_player_face(player_id, upload_file):
    if not upload_file or upload_file.filename == '':
        return False, 'Please choose an image file.'

    if not allowed_face_file(upload_file.filename):
        return False, 'Invalid file type. Use png, jpg, jpeg, webp, or gif.'

    os.makedirs(_face_storage_dir(), exist_ok=True)

    for ext in ALLOWED_FACE_EXTENSIONS:
        old_path = os.path.join(_face_storage_dir(), f'{player_id}.{ext}')
        if os.path.exists(old_path):
            os.remove(old_path)

    save_path = os.path.join(_face_storage_dir(), f'{player_id}.webp')

    try:
        upload_file.stream.seek(0)
        with Image.open(upload_file.stream) as img:
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                processed = img.convert('RGBA')
            else:
                processed = img.convert('RGB')

            processed.thumbnail((FACE_IMAGE_MAX_DIMENSION, FACE_IMAGE_MAX_DIMENSION), Image.Resampling.LANCZOS)
            processed.save(save_path, format='WEBP', quality=FACE_IMAGE_WEBP_QUALITY, method=6)
    except UnidentifiedImageError:
        return False, 'Invalid image file. Please upload a valid image.'
    except Exception:
        return False, 'Could not process image. Please try a different file.'

    return True, 'Face image uploaded and optimized.'

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                alias TEXT,
                phone TEXT,
                email TEXT,
                skill_rating INTEGER DEFAULT 5,
                payment_exempt INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                location TEXT,
                notes TEXT,
                team1_score INTEGER,
                team2_score INTEGER,
                is_abandoned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games(id),
                FOREIGN KEY (player_id) REFERENCES players(id),
                UNIQUE(game_id, player_id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS team_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                team_number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games(id),
                FOREIGN KEY (player_id) REFERENCES players(id),
                UNIQUE(game_id, player_id)
            )
        ''')
        
        conn.execute('CREATE INDEX IF NOT EXISTS idx_attendance_game ON attendance(game_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_attendance_player ON attendance(player_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_games_date ON games(date)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_team_assignments_game ON team_assignments(game_id)')
        
        # Create settings table for app configuration
        conn.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # ============================================================
        # DATABASE MIGRATIONS
        # ============================================================
        # IMPORTANT: When adding new columns to existing tables, ALWAYS
        # add them here with ALTER TABLE wrapped in try/except blocks.
        # This ensures existing Azure databases get updated gracefully
        # without breaking the app or requiring manual SQL commands.
        # 
        # Template for adding new columns:
        # try:
        #     conn.execute('ALTER TABLE table_name ADD COLUMN column_name TYPE')
        # except sqlite3.OperationalError:
        #     pass  # Column already exists
        # ============================================================
        
        # Migration: Add score columns if they don't exist
        try:
            conn.execute('ALTER TABLE players ADD COLUMN alias TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists

        try:
            conn.execute('ALTER TABLE players ADD COLUMN payment_exempt INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Column already exists

        try:
            conn.execute('ALTER TABLE games ADD COLUMN team1_score INTEGER')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            conn.execute('ALTER TABLE games ADD COLUMN team2_score INTEGER')
        except sqlite3.OperationalError:
            pass  # Column already exists

        try:
            conn.execute('ALTER TABLE games ADD COLUMN is_abandoned INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Column already exists

        try:
            conn.execute('ALTER TABLE attendance ADD COLUMN paid INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Column already exists

        conn.execute('UPDATE games SET is_abandoned = 0 WHERE is_abandoned IS NULL')

        # Ensure default alias for known mapping
        conn.execute("UPDATE players SET alias = 'you' WHERE name = 'Dave Bird' AND (alias IS NULL OR alias = '')")

        conn.commit()

# Initialize database on module load (for Gunicorn/Azure)
init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        # Debug logging
        print(f"DEBUG - Entered password length: {len(password) if password else 0}")
        print(f"DEBUG - Expected password length: {len(ADMIN_PASSWORD) if ADMIN_PASSWORD else 0}")
        print(f"DEBUG - Password match: {password == ADMIN_PASSWORD}")
        
        if password == ADMIN_PASSWORD:
            session.permanent = True
            session['logged_in'] = True
            next_url = request.args.get('next', url_for('admin'))
            return redirect(next_url)
        else:
            return render_template('login.html', error='Incorrect password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    from datetime import datetime, timedelta
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1
    per_page = 10
    offset = (page - 1) * per_page
    
    with get_db() as conn:
        # Auto-create next Wednesday game if it doesn't exist
        today = datetime.now()
        days_until_wednesday = (2 - today.weekday()) % 7  # 2 = Wednesday (0=Monday)
        if days_until_wednesday == 0 and today.hour >= 21:  # After 9pm Wednesday, create next week
            days_until_wednesday = 7
        
        next_wednesday = today + timedelta(days=days_until_wednesday)
        next_wednesday_str = next_wednesday.strftime('%Y-%m-%d')
        
        # Check if game already exists for this Wednesday
        existing = conn.execute('SELECT id FROM games WHERE date = ?', (next_wednesday_str,)).fetchone()
        
        if not existing:
            conn.execute(
                'INSERT INTO games (date, location, notes) VALUES (?, ?, ?)',
                (next_wednesday_str, 'Selwood School', 'Weekly Wednesday 9pm game - Auto-created')
            )
            conn.commit()
        
        total_games = conn.execute('SELECT COUNT(*) as count FROM games').fetchone()['count']
        games = conn.execute(
            'SELECT * FROM games ORDER BY date DESC LIMIT ? OFFSET ?',
            (per_page, offset)
        ).fetchall()
        
        game_data = []
        for game in games:
            attendance = conn.execute('''
                SELECT COUNT(*) as count 
                FROM attendance 
                WHERE game_id = ? AND status = 'playing'
            ''', (game['id'],)).fetchone()
            
            # Safely get score fields (may not exist in older databases)
            try:
                team1_score = game['team1_score']
                team2_score = game['team2_score']
            except (KeyError, IndexError):
                team1_score = None
                team2_score = None
            
            game_data.append({
                'id': game['id'],
                'date': game['date'],
                'location': game['location'],
                'notes': game['notes'],
                'players_count': attendance['count'] if attendance else 0,
                'team1_score': team1_score,
                'team2_score': team2_score,
                'is_abandoned': game['is_abandoned'] if 'is_abandoned' in game.keys() else 0
            })
    
    has_prev = page > 1
    has_next = (offset + len(game_data)) < total_games

    return render_template(
        'index.html',
        games=game_data,
        is_admin=session.get('logged_in'),
        page=page,
        has_prev=has_prev,
        has_next=has_next
    )

@app.route('/admin')
@login_required
def admin():
    return redirect(url_for('admin_games'))

@app.route('/admin/games')
@login_required
def admin_games():
    status_filter = request.args.get('status', 'all')
    if status_filter not in ('all', 'active', 'abandoned'):
        status_filter = 'all'
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1
    per_page = 20
    offset = (page - 1) * per_page

    with get_db() as conn:
        if status_filter == 'active':
            total_games = conn.execute('''
                SELECT COUNT(*) as count
                FROM games
                WHERE is_abandoned = 0 OR is_abandoned IS NULL
            ''').fetchone()['count']
            games = conn.execute('''
                SELECT * FROM games
                WHERE is_abandoned = 0 OR is_abandoned IS NULL
                ORDER BY date DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset)).fetchall()
        elif status_filter == 'abandoned':
            total_games = conn.execute('''
                SELECT COUNT(*) as count
                FROM games
                WHERE is_abandoned = 1
            ''').fetchone()['count']
            games = conn.execute('''
                SELECT * FROM games
                WHERE is_abandoned = 1
                ORDER BY date DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset)).fetchall()
        else:
            total_games = conn.execute('SELECT COUNT(*) as count FROM games').fetchone()['count']
            games = conn.execute(
                'SELECT * FROM games ORDER BY date DESC LIMIT ? OFFSET ?',
                (per_page, offset)
            ).fetchall()
        
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
                'players_count': attendance['count'] if attendance else 0,
                'is_abandoned': game['is_abandoned'] if 'is_abandoned' in game.keys() else 0
            })
    
    has_prev = page > 1
    has_next = (offset + len(game_data)) < total_games

    return render_template(
        'admin_games.html',
        games=game_data,
        status_filter=status_filter,
        page=page,
        has_prev=has_prev,
        has_next=has_next
    )

@app.route('/admin/players')
@login_required
def admin_players():
    with get_db() as conn:
        total_games_count = conn.execute("""
            SELECT COUNT(*) as count
            FROM games
            WHERE date <= date('now')
                AND (is_abandoned IS NULL OR is_abandoned = 0)
        """).fetchone()['count']
        payment_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'weekly_payment_amount'"
        ).fetchone()
        try:
            weekly_payment_amount = float(payment_setting['value']) if payment_setting and payment_setting['value'] is not None else 0.0
        except (TypeError, ValueError):
            weekly_payment_amount = 0.0

        # Attendance denominator is all non-abandoned past games.
        players = conn.execute('''
            SELECT 
                p.id,
                p.name,
                p.alias,
                p.phone,
                p.email,
                p.skill_rating,
                COALESCE(p.payment_exempt, 0) as payment_exempt,
                COUNT(DISTINCT CASE
                    WHEN a.status = 'playing'
                        AND g.date <= date('now')
                        AND (g.is_abandoned IS NULL OR g.is_abandoned = 0)
                    THEN a.game_id END) as games_played,
                COUNT(DISTINCT CASE
                    WHEN a.status = 'playing'
                        AND COALESCE(a.paid, 0) = 1
                        AND g.date <= date('now')
                        AND (g.is_abandoned IS NULL OR g.is_abandoned = 0)
                    THEN a.game_id END) as paid_games,
                ? as total_games,
                CASE 
                    WHEN ? > 0 
                    THEN ROUND((COUNT(DISTINCT CASE
                        WHEN a.status = 'playing'
                            AND g.date <= date('now')
                            AND (g.is_abandoned IS NULL OR g.is_abandoned = 0)
                        THEN a.game_id END) * 100.0 / ?), 1)
                    ELSE 0 
                END as attendance_rate
            FROM players p
            LEFT JOIN attendance a ON p.id = a.player_id
            LEFT JOIN games g ON a.game_id = g.id
            GROUP BY p.id, p.name, p.alias, p.phone, p.email, p.skill_rating, p.payment_exempt
            ORDER BY p.name
        ''', (total_games_count, total_games_count, total_games_count)).fetchall()

    return render_template(
        'admin_players.html',
        players=players,
        weekly_payment_amount=weekly_payment_amount
    )


@app.route('/admin/player-faces', methods=['GET', 'POST'])
@login_required
def admin_player_faces():
    if request.method == 'POST':
        player_id = request.form.get('player_id', type=int)
        file = request.files.get('face_image')

        if not player_id:
            return redirect(url_for('admin_player_faces', error='Please choose a player and an image file.'))

        ok, message = save_player_face(player_id, file)
        if ok:
            return redirect(url_for('admin_player_faces', success=message))
        return redirect(url_for('admin_player_faces', error=message))

    with get_db() as conn:
        players = conn.execute('SELECT id, name FROM players ORDER BY name').fetchall()

    player_faces = {player['id']: get_player_face_url(player['id']) for player in players}
    return render_template(
        'admin_player_faces.html',
        players=players,
        player_faces=player_faces,
        error=request.args.get('error'),
        success=request.args.get('success')
    )


@app.route('/players/<int:player_id>/face', methods=['POST'])
@login_required
def upload_player_face(player_id):
    file = request.files.get('face_image')
    ok, _ = save_player_face(player_id, file)
    return redirect(url_for('edit_player', player_id=player_id))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    with get_db() as conn:
        if request.method == 'POST':
            notifications_enabled = request.form.get('notifications_enabled') == 'on'
            weekly_payment_amount_raw = request.form.get('weekly_payment_amount', '').strip()
            rankings_face_size_raw = request.form.get('rankings_face_size', '').strip()

            try:
                weekly_payment_amount = float(weekly_payment_amount_raw) if weekly_payment_amount_raw else 0.0
            except ValueError:
                weekly_payment_amount = 0.0
            weekly_payment_amount = max(0.0, weekly_payment_amount)

            try:
                rankings_face_size = int(rankings_face_size_raw) if rankings_face_size_raw else 16
            except ValueError:
                rankings_face_size = 16
            rankings_face_size = max(8, min(36, rankings_face_size))
            
            # Update or insert setting
            conn.execute('''
                INSERT OR REPLACE INTO settings (key, value) 
                VALUES ('notifications_enabled', ?)
            ''', ('true' if notifications_enabled else 'false',))
            conn.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES ('weekly_payment_amount', ?)
            ''', (str(weekly_payment_amount),))
            conn.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES ('rankings_face_size', ?)
            ''', (str(rankings_face_size),))
            conn.commit()
            
            return redirect(url_for('admin_settings'))
        
        # GET request - fetch current setting
        setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'notifications_enabled'"
        ).fetchone()
        payment_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'weekly_payment_amount'"
        ).fetchone()
        face_size_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'rankings_face_size'"
        ).fetchone()
        
        notifications_enabled = setting['value'] == 'true' if setting else False
        try:
            weekly_payment_amount = float(payment_setting['value']) if payment_setting and payment_setting['value'] is not None else 0.0
        except (TypeError, ValueError):
            weekly_payment_amount = 0.0
        try:
            rankings_face_size = int(face_size_setting['value']) if face_size_setting and face_size_setting['value'] is not None else 16
        except (TypeError, ValueError):
            rankings_face_size = 16
        rankings_face_size = max(8, min(36, rankings_face_size))
    
    return render_template(
        'admin_settings.html',
        notifications_enabled=notifications_enabled,
        weekly_payment_amount=weekly_payment_amount,
        rankings_face_size=rankings_face_size
    )

@app.route('/api/settings/notifications')
def get_notification_setting():
    """API endpoint for JavaScript to check if notifications are enabled"""
    with get_db() as conn:
        setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'notifications_enabled'"
        ).fetchone()
        
        enabled = setting['value'] == 'true' if setting else False
    
    return jsonify({'enabled': enabled})
    with get_db() as conn:
        players = conn.execute('''
            SELECT p.*,
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
    
    return render_template('admin_players.html', players=players)

@app.route('/players')
def players():
    # Check if user is logged in
    if session.get('logged_in'):
        return redirect(url_for('admin_players'))
    else:
        # Public view - only show player names
        with get_db() as conn:
            players = conn.execute('SELECT id, name FROM players ORDER BY name').fetchall()
        return render_template('players_public.html', players=players)

@app.route('/leaderboard')
def leaderboard():
    from datetime import datetime
    current_year = datetime.now().year
    
    with get_db() as conn:
        latest_pending = conn.execute('''
            SELECT id, date FROM games
            WHERE date <= date('now')
                AND (is_abandoned IS NULL OR is_abandoned = 0)
                AND (team1_score IS NULL OR team2_score IS NULL)
            ORDER BY date DESC
            LIMIT 1
        ''').fetchone()

        latest_completed = conn.execute('''
            SELECT id, date FROM games
            WHERE date <= date('now')
                AND (is_abandoned IS NULL OR is_abandoned = 0)
            ORDER BY date DESC
            LIMIT 1
        ''').fetchone()

        final_score_target = latest_pending if latest_pending else latest_completed

        # Get all games with scores from this year
        leaderboard_data = conn.execute('''
            SELECT 
                p.id,
                p.name,
                SUM(CASE 
                    WHEN (ta.team_number = 1 AND g.team1_score > g.team2_score) OR
                         (ta.team_number = 2 AND g.team2_score > g.team1_score)
                    THEN 1 ELSE 0 
                END) as wins,
                SUM(CASE 
                    WHEN (ta.team_number = 1 AND g.team1_score < g.team2_score) OR
                         (ta.team_number = 2 AND g.team2_score < g.team1_score)
                    THEN 1 ELSE 0 
                END) as losses,
                SUM(CASE 
                    WHEN g.team1_score = g.team2_score
                    THEN 1 ELSE 0
                END) as draws,
                COUNT(*) as total_games
            FROM players p
            JOIN team_assignments ta ON p.id = ta.player_id
            JOIN games g ON ta.game_id = g.id
            WHERE g.team1_score IS NOT NULL 
                AND g.team2_score IS NOT NULL
                AND (g.is_abandoned IS NULL OR g.is_abandoned = 0)
                AND strftime('%Y', g.date) = ?
            GROUP BY p.id, p.name
            HAVING total_games > 0
            ORDER BY wins DESC, total_games DESC, p.name
        ''', (str(current_year),)).fetchall()
        
        # Calculate win percentages
        leaderboard = []
        for row in leaderboard_data:
            win_pct = round((row['wins'] / row['total_games'] * 100) if row['total_games'] > 0 else 0, 1)
            loss_pct = round((row['losses'] / row['total_games'] * 100) if row['total_games'] > 0 else 0, 1)
            non_loss_pct = round(((row['wins'] + row['draws']) / row['total_games'] * 100) if row['total_games'] > 0 else 0, 1)
            leaderboard.append({
                'id': row['id'],
                'name': row['name'],
                'wins': row['wins'],
                'draws': row['draws'],
                'losses': row['losses'],
                'total_games': row['total_games'],
                'win_percentage': win_pct,
                'loss_percentage': loss_pct,
                'non_loss_percentage': non_loss_pct
            })
        
        # Get total games with scores
        total_games = conn.execute('''
            SELECT COUNT(*) as count 
            FROM games 
            WHERE team1_score IS NOT NULL 
                AND team2_score IS NOT NULL
                AND (is_abandoned IS NULL OR is_abandoned = 0)
                AND strftime('%Y', date) = ?
        ''', (str(current_year),)).fetchone()['count']
        
        total_games_year = conn.execute('''
            SELECT COUNT(*) as count
            FROM games
            WHERE date <= date('now')
                AND (is_abandoned IS NULL OR is_abandoned = 0)
                AND strftime('%Y', date) = ?
        ''', (str(current_year),)).fetchone()['count']

        # Attendance leaderboard for current year.
        # Denominator is all non-abandoned games in the year.
        # Explicitly filter out abandoned games to ensure they're never included.
        attendance_data = conn.execute('''
            SELECT 
                p.id,
                p.name,
                COUNT(DISTINCT CASE
                    WHEN a.status = 'playing'
                        AND g.date <= date('now')
                        AND g.is_abandoned = 0
                        AND strftime('%Y', g.date) = ?
                    THEN a.game_id END) as games_played,
                ? as total_games,
                CASE 
                    WHEN ? > 0 
                    THEN ROUND(COUNT(DISTINCT CASE
                        WHEN a.status = 'playing'
                            AND g.date <= date('now')
                            AND g.is_abandoned = 0
                            AND strftime('%Y', g.date) = ?
                        THEN a.game_id END) * 100.0 / ?, 1)
                    ELSE 0 
                END as attendance_rate
            FROM players p
            LEFT JOIN attendance a ON p.id = a.player_id
            LEFT JOIN games g ON a.game_id = g.id
            WHERE g.id IS NULL OR g.is_abandoned = 0
            GROUP BY p.id, p.name
            ORDER BY attendance_rate DESC, games_played DESC, p.name
        ''', (str(current_year), total_games_year, total_games_year, str(current_year), total_games_year)).fetchall()
    
    return render_template('leaderboard.html', 
                         leaderboard=leaderboard,
                         attendance_leaderboard=attendance_data,
                         total_games=total_games,
                         total_players=len(leaderboard),
                         year=current_year,
                         final_score_game_id=final_score_target['id'] if final_score_target else None)

@app.route('/players/<int:player_id>/stats')
def player_stats(player_id):
    from datetime import datetime
    current_year = datetime.now().year

    with get_db() as conn:
        player = conn.execute('SELECT id, name FROM players WHERE id = ?', (player_id,)).fetchone()
        if not player:
            return "Player not found", 404

        games = conn.execute('''
            SELECT
                g.id,
                g.date,
                g.team1_score,
                g.team2_score,
                ta.team_number,
                CASE
                    WHEN (ta.team_number = 1 AND g.team1_score > g.team2_score) OR
                         (ta.team_number = 2 AND g.team2_score > g.team1_score)
                    THEN 'win'
                    WHEN g.team1_score = g.team2_score
                    THEN 'draw'
                    ELSE 'loss'
                END as result,
                CASE WHEN ta.team_number = 1 THEN g.team1_score ELSE g.team2_score END as player_score,
                CASE WHEN ta.team_number = 1 THEN g.team2_score ELSE g.team1_score END as opponent_score
            FROM games g
            JOIN team_assignments ta ON g.id = ta.game_id AND ta.player_id = ?
            WHERE g.team1_score IS NOT NULL
                AND g.team2_score IS NOT NULL
                AND (g.is_abandoned IS NULL OR g.is_abandoned = 0)
                AND strftime('%Y', g.date) = ?
            ORDER BY g.date DESC
        ''', (player_id, str(current_year))).fetchall()

    return render_template('player_stats.html',
                           player=player,
                           games=games,
                           year=current_year)

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/players/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        alias = request.form.get('alias', '').strip() or None
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        skill_rating = request.form.get('skill_rating', 5, type=int)
        payment_exempt = 1 if request.form.get('payment_exempt') == 'on' else 0
        
        # Validate skill rating is between 1-5
        if skill_rating < 1 or skill_rating > 5:
            return render_template('add_player.html', error='Skill rating must be between 1 and 5')
        
        try:
            with get_db() as conn:
                conn.execute('INSERT INTO players (name, alias, phone, email, skill_rating, payment_exempt) VALUES (?, ?, ?, ?, ?, ?)',
                           (name, alias, phone, email, skill_rating, payment_exempt))
                conn.commit()
            return redirect(url_for('admin_players'))
        except sqlite3.IntegrityError:
            return render_template('add_player.html', error='Player already exists')
    
    return render_template('add_player.html')

@app.route('/players/<int:player_id>/edit', methods=['GET', 'POST'])
def edit_player(player_id):
    with get_db() as conn:
        if request.method == 'POST':
            name = request.form['name']
            alias = request.form.get('alias', '').strip() or None
            phone = request.form.get('phone', '')
            email = request.form.get('email', '')
            skill_rating = request.form.get('skill_rating', 5, type=int)
            payment_exempt = 1 if request.form.get('payment_exempt') == 'on' else 0
            
            # Validate skill rating is between 1-5
            if skill_rating < 1 or skill_rating > 5:
                player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
                return render_template(
                    'edit_player.html',
                    player=player,
                    face_url=get_player_face_url(player_id),
                    error='Skill rating must be between 1 and 5'
                )
            
            conn.execute('UPDATE players SET name = ?, alias = ?, phone = ?, email = ?, skill_rating = ?, payment_exempt = ? WHERE id = ?',
                       (name, alias, phone, email, skill_rating, payment_exempt, player_id))
            conn.commit()
            return redirect(url_for('admin_players'))
        
        player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
        if not player:
            return "Player not found", 404
        
        return render_template('edit_player.html', player=player, face_url=get_player_face_url(player_id))
    return render_template('add_player.html')

@app.route('/players/<int:player_id>/payments', methods=['GET', 'POST'])
@login_required
def player_payments(player_id):
    with get_db() as conn:
        player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
        if not player:
            return "Player not found", 404

        if request.method == 'POST':
            attendance_id = request.form.get('attendance_id', type=int)
            paid = 1 if request.form.get('paid') == '1' else 0

            if attendance_id:
                conn.execute('''
                    UPDATE attendance
                    SET paid = ?
                    WHERE id = ? AND player_id = ? AND status = 'playing'
                ''', (paid, attendance_id, player_id))
                conn.commit()

            return redirect(url_for('player_payments', player_id=player_id))

        payment_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'weekly_payment_amount'"
        ).fetchone()
        try:
            weekly_payment_amount = float(payment_setting['value']) if payment_setting and payment_setting['value'] is not None else 0.0
        except (TypeError, ValueError):
            weekly_payment_amount = 0.0

        weeks = conn.execute('''
            SELECT
                a.id as attendance_id,
                a.game_id,
                COALESCE(a.paid, 0) as paid,
                g.date,
                g.location
            FROM attendance a
            JOIN games g ON a.game_id = g.id
            WHERE a.player_id = ?
              AND a.status = 'playing'
              AND (g.is_abandoned IS NULL OR g.is_abandoned = 0)
            ORDER BY g.date DESC
        ''', (player_id,)).fetchall()

    total_weeks = len(weeks)
    paid_weeks = sum(1 for week in weeks if week['paid'])
    total_paid_amount = round(paid_weeks * weekly_payment_amount, 2)

    return render_template(
        'player_payments.html',
        player=player,
        weeks=weeks,
        total_weeks=total_weeks,
        paid_weeks=paid_weeks,
        weekly_payment_amount=weekly_payment_amount,
        total_paid_amount=total_paid_amount
    )

@app.route('/players/<int:player_id>/delete', methods=['POST'])
@login_required
def delete_player(player_id):
    with get_db() as conn:
        # Delete attendance records first (foreign key constraint)
        conn.execute('DELETE FROM attendance WHERE player_id = ?', (player_id,))
        # Delete the player
        conn.execute('DELETE FROM players WHERE id = ?', (player_id,))
        conn.commit()
    
    return redirect(url_for('admin_players'))

@app.route('/players/merge', methods=['POST'])
@login_required
def merge_players():
    source_player_id = request.form.get('source_player_id', type=int)
    target_player_id = request.form.get('target_player_id', type=int)
    
    if not source_player_id or not target_player_id:
        return redirect(url_for('admin_players'))
    
    if source_player_id == target_player_id:
        return redirect(url_for('admin_players'))
    
    with get_db() as conn:
        # Update all attendance records from source to target
        # First, delete any duplicate attendance records (same game)
        conn.execute('''
            DELETE FROM attendance 
            WHERE id IN (
                SELECT a1.id 
                FROM attendance a1
                INNER JOIN attendance a2 ON a1.game_id = a2.game_id
                WHERE a1.player_id = ? AND a2.player_id = ?
            )
        ''', (source_player_id, target_player_id))
        
        # Update remaining attendance records
        conn.execute('''
            UPDATE attendance 
            SET player_id = ? 
            WHERE player_id = ?
        ''', (target_player_id, source_player_id))
        
        # Update team assignments if they exist
        conn.execute('''
            UPDATE team_assignments 
            SET player_id = ? 
            WHERE player_id = ?
        ''', (target_player_id, source_player_id))
        
        # Delete the source player
        conn.execute('DELETE FROM players WHERE id = ?', (source_player_id,))
        
        conn.commit()
    
    return redirect(url_for('admin_players'))

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
        
        return redirect(url_for('admin_games'))
    
    return render_template('add_game.html')

@app.route('/games/<int:game_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    with get_db() as conn:
        if request.method == 'POST':
            date = request.form['date']
            location = request.form['location']
            notes = request.form.get('notes', '')
            team1_score = request.form.get('team1_score', None)
            team2_score = request.form.get('team2_score', None)
            is_abandoned = 1 if request.form.get('is_abandoned') == 'on' else 0
            
            # Convert empty strings to None for database
            team1_score = int(team1_score) if team1_score else None
            team2_score = int(team2_score) if team2_score else None

            # Abandoned matches do not carry final scores
            if is_abandoned:
                team1_score = None
                team2_score = None
            
            conn.execute('''
                UPDATE games 
                SET date = ?, location = ?, notes = ?, team1_score = ?, team2_score = ?, is_abandoned = ?
                WHERE id = ?
            ''', (date, location, notes, team1_score, team2_score, is_abandoned, game_id))
            conn.commit()
            
            return redirect(url_for('admin_games'))
        
        # GET request - show form
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
        
        if not game:
            return "Game not found", 404
        
        return render_template('edit_game.html', game=game)

@app.route('/games/<int:game_id>/abandoned', methods=['POST'])
@login_required
def toggle_game_abandoned(game_id):
    abandoned = 1 if request.form.get('abandoned') == '1' else 0

    with get_db() as conn:
        if abandoned:
            conn.execute('''
                UPDATE games
                SET is_abandoned = 1,
                    team1_score = NULL,
                    team2_score = NULL
                WHERE id = ?
            ''', (game_id,))
        else:
            conn.execute('UPDATE games SET is_abandoned = 0 WHERE id = ?', (game_id,))
        conn.commit()

    return redirect(url_for('admin_games'))

@app.route('/games/<int:game_id>/delete', methods=['POST'])
@login_required
def delete_game(game_id):
    with get_db() as conn:
        # Delete attendance records first (foreign key constraint)
        conn.execute('DELETE FROM attendance WHERE game_id = ?', (game_id,))
        # Delete the game
        conn.execute('DELETE FROM games WHERE id = ?', (game_id,))
        conn.commit()
    
    return redirect(url_for('admin_games'))

@app.route('/games/<int:game_id>')
@login_required
def game_detail(game_id):
    with get_db() as conn:
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
        
        if not game:
            return "Game not found", 404
        
        attendance = conn.execute('''
            SELECT p.*, a.status, COALESCE(a.paid, 0) as paid
            FROM attendance a
            JOIN players p ON a.player_id = p.id
            WHERE a.game_id = ?
            ORDER BY a.status, p.name
        ''', (game_id,)).fetchall()
        
        all_players = [dict(r) for r in conn.execute('SELECT * FROM players ORDER BY name').fetchall()]

        payment_amount_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'weekly_payment_amount'"
        ).fetchone()
        try:
            weekly_payment_amount = float(payment_amount_setting['value']) if payment_amount_setting and payment_amount_setting['value'] is not None else 0.0
        except (TypeError, ValueError):
            weekly_payment_amount = 0.0
    
    playing = [a for a in attendance if a['status'] == 'playing']
    not_playing = [a for a in attendance if a['status'] == 'not_playing']
    maybe = [a for a in attendance if a['status'] == 'maybe']
    
    return render_template('game_detail.html', 
                         game=game, 
                         playing=playing,
                         not_playing=not_playing,
                         maybe=maybe,
                         all_players=all_players,
                         weekly_payment_amount=weekly_payment_amount)

@app.route('/games/<int:game_id>/teams')
def generate_teams(game_id):
    import random

    with get_db() as conn:
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()

        if not game:
            return "Game not found", 404

        # Check if team_assignments table exists, if not create it
        try:
            conn.execute('SELECT 1 FROM team_assignments LIMIT 1')
        except:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS team_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    player_id INTEGER NOT NULL,
                    team_number INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES games(id),
                    FOREIGN KEY (player_id) REFERENCES players(id),
                    UNIQUE(game_id, player_id)
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_team_assignments_game ON team_assignments(game_id)')
            conn.commit()

        # Check if teams have already been generated for this game
        existing_teams = conn.execute('''
            SELECT p.*, ta.team_number
            FROM team_assignments ta
            JOIN players p ON ta.player_id = p.id
            WHERE ta.game_id = ?
            ORDER BY ta.team_number, p.name
        ''', (game_id,)).fetchall()

        if existing_teams:
            team1 = [dict(p) for p in existing_teams if p['team_number'] == 1]
            team2 = [dict(p) for p in existing_teams if p['team_number'] == 2]

            return render_template('teams.html',
                                 game=game,
                                 team1=team1,
                                 team2=team2,
                                 teams_generated=True,
                                 is_admin=session.get('logged_in'))

        if not session.get('logged_in'):
            return render_template('teams.html',
                                 game=game,
                                 teams_generated=False,
                                 is_admin=False)

        # Admin user - generate teams
        playing = conn.execute('''
            SELECT p.*, a.status
            FROM attendance a
            JOIN players p ON a.player_id = p.id
            WHERE a.game_id = ? AND a.status = 'playing'
            ORDER BY p.name
        ''', (game_id,)).fetchall()

        if len(playing) < 2:
            return render_template('teams.html', game=game, error='Need at least 2 players to create teams', is_admin=True, teams_generated=False)

        players_list = [dict(player) for player in playing]
        players_list.sort(key=lambda x: x.get('skill_rating', 5), reverse=True)

        from itertools import groupby
        shuffled_list = []
        for _, group in groupby(players_list, key=lambda x: x.get('skill_rating', 5)):
            group_list = list(group)
            random.shuffle(group_list)
            shuffled_list.extend(group_list)

        team1 = []
        team2 = []

        for i, player in enumerate(shuffled_list):
            if i % 4 == 0 or i % 4 == 3:
                team1.append(player)
            else:
                team2.append(player)

        for player in team1:
            conn.execute('''
                INSERT INTO team_assignments (game_id, player_id, team_number)
                VALUES (?, ?, 1)
                ON CONFLICT(game_id, player_id) DO UPDATE SET team_number = 1
            ''', (game_id, player['id']))

        for player in team2:
            conn.execute('''
                INSERT INTO team_assignments (game_id, player_id, team_number)
                VALUES (?, ?, 2)
                ON CONFLICT(game_id, player_id) DO UPDATE SET team_number = 2
            ''', (game_id, player['id']))

        conn.commit()

        return render_template('teams.html',
                             game=game,
                             team1=team1,
                             team2=team2,
                             teams_generated=True,
                             is_admin=session.get('logged_in'))


@app.route('/games/<int:game_id>/teams/regenerate', methods=['POST'])
@login_required
def regenerate_teams(game_id):
    with get_db() as conn:
        conn.execute('DELETE FROM team_assignments WHERE game_id = ?', (game_id,))
        conn.commit()

    return redirect(url_for('generate_teams', game_id=game_id))


@app.route('/games/<int:game_id>/teams/manual', methods=['GET', 'POST'])
@login_required
def manual_teams(game_id):
    with get_db() as conn:
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()

        if not game:
            return "Game not found", 404

        try:
            conn.execute('SELECT 1 FROM team_assignments LIMIT 1')
        except:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS team_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER NOT NULL,
                    player_id INTEGER NOT NULL,
                    team_number INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES games(id),
                    FOREIGN KEY (player_id) REFERENCES players(id),
                    UNIQUE(game_id, player_id)
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_team_assignments_game ON team_assignments(game_id)')
            conn.commit()

        if request.method == 'POST':
            team1_ids = request.form.getlist('team1_players')
            team2_ids = request.form.getlist('team2_players')

            conn.execute('DELETE FROM team_assignments WHERE game_id = ?', (game_id,))

            for player_id in team1_ids:
                conn.execute('''
                    INSERT INTO team_assignments (game_id, player_id, team_number)
                    VALUES (?, ?, 1)
                ''', (game_id, player_id))

            for player_id in team2_ids:
                conn.execute('''
                    INSERT INTO team_assignments (game_id, player_id, team_number)
                    VALUES (?, ?, 2)
                ''', (game_id, player_id))

            conn.commit()

            return redirect(url_for('generate_teams', game_id=game_id))

        playing = conn.execute('''
            SELECT p.*
            FROM attendance a
            JOIN players p ON a.player_id = p.id
            WHERE a.game_id = ? AND a.status = 'playing'
            ORDER BY p.name
        ''', (game_id,)).fetchall()

        existing_teams = conn.execute('''
            SELECT p.*, ta.team_number
            FROM team_assignments ta
            JOIN players p ON ta.player_id = p.id
            WHERE ta.game_id = ?
            ORDER BY ta.team_number, p.name
        ''', (game_id,)).fetchall()

        if existing_teams:
            team1 = [dict(p) for p in existing_teams if p['team_number'] == 1]
            team2 = [dict(p) for p in existing_teams if p['team_number'] == 2]
            assigned_ids = {p['id'] for p in existing_teams}
            unassigned = [dict(p) for p in playing if p['id'] not in assigned_ids]
        else:
            team1 = []
            team2 = []
            unassigned = [dict(p) for p in playing]

        return render_template('teams_manual.html',
                             game=game,
                             team1=team1,
                             team2=team2,
                             unassigned=unassigned)


@app.route('/games/<int:game_id>/teams/watch')
def teams_watch_view(game_id):
    with get_db() as conn:
        game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()

        if not game:
            return "Game not found", 404

        try:
            existing_teams = conn.execute('''
                SELECT p.*, ta.team_number
                FROM team_assignments ta
                JOIN players p ON ta.player_id = p.id
                WHERE ta.game_id = ?
                ORDER BY ta.team_number, p.name
            ''', (game_id,)).fetchall()

            if not existing_teams:
                return "No teams generated yet", 404

            team1 = [dict(p) for p in existing_teams if p['team_number'] == 1]
            team2 = [dict(p) for p in existing_teams if p['team_number'] == 2]

            return render_template('teams_watch.html',
                                 game=game,
                                 team1=team1,
                                 team2=team2)
        except:
            return "No teams generated yet", 404


@app.route('/games/<int:game_id>/attendance', methods=['POST'])
@login_required
def update_attendance(game_id):
    player_id = request.form['player_id']
    status = request.form['status']
    paid = 1 if request.form.get('paid') == 'on' else 0
    
    with get_db() as conn:
        conn.execute('''
            INSERT INTO attendance (game_id, player_id, status, paid)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(game_id, player_id) 
            DO UPDATE SET status = excluded.status, paid = excluded.paid
        ''', (game_id, player_id, status, paid))
        conn.commit()
    
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/games/<int:game_id>/payment', methods=['POST'])
@login_required
def update_payment(game_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    player_id = request.form.get('player_id', type=int)
    paid = 1 if request.form.get('paid') == '1' else 0

    if not player_id:
        if is_ajax:
            return jsonify({'ok': False, 'error': 'Missing player_id'}), 400
        return redirect(url_for('game_detail', game_id=game_id))

    with get_db() as conn:
        conn.execute('''
            UPDATE attendance
            SET paid = ?
            WHERE game_id = ? AND player_id = ?
        ''', (paid, game_id, player_id))

        totals = conn.execute('''
            SELECT
                COUNT(*) as total_playing,
                SUM(CASE WHEN COALESCE(paid, 0) = 1 THEN 1 ELSE 0 END) as paid_count
            FROM attendance a
            JOIN players p ON p.id = a.player_id
            WHERE a.game_id = ?
              AND a.status = 'playing'
              AND COALESCE(p.payment_exempt, 0) = 0
        ''', (game_id,)).fetchone()

        payment_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'weekly_payment_amount'"
        ).fetchone()
        try:
            weekly_payment_amount = float(payment_setting['value']) if payment_setting and payment_setting['value'] is not None else 0.0
        except (TypeError, ValueError):
            weekly_payment_amount = 0.0

        conn.commit()

    if is_ajax:
        total_playing = totals['total_playing'] if totals and totals['total_playing'] is not None else 0
        paid_count = totals['paid_count'] if totals and totals['paid_count'] is not None else 0
        return jsonify({
            'ok': True,
            'paid': paid,
            'total_playing': total_playing,
            'paid_count': paid_count,
            'unpaid_count': max(total_playing - paid_count, 0),
            'total_paid_amount': round(paid_count * weekly_payment_amount, 2)
        })

    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/games/<int:game_id>/bulk-remove', methods=['POST'])
@login_required
def bulk_remove_attendance(game_id):
    player_ids = request.form.getlist('player_ids')
    
    if not player_ids:
        return redirect(url_for('game_detail', game_id=game_id))
    
    with get_db() as conn:
        # Delete attendance records for selected players
        placeholders = ','.join('?' * len(player_ids))
        conn.execute(f'DELETE FROM attendance WHERE game_id = ? AND player_id IN ({placeholders})',
                    [game_id] + player_ids)
        conn.commit()
    
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/games/<int:game_id>/bulk-attendance', methods=['POST'])
@login_required
def bulk_attendance(game_id):
    players_text = request.form.get('players_text', '')
    
    if not players_text.strip():
        return redirect(url_for('game_detail', game_id=game_id))
    
    # Split by newlines and clean up
    playing_names = [name.strip().replace('-', '').strip() for name in players_text.split('\n') if name.strip()]
    
    with get_db() as conn:
        # Get all players
        all_players = conn.execute('SELECT id, name FROM players').fetchall()
        playing_ids = []
        
        # Process players who are playing
        for name in playing_names:
            # Get or create player
            player = conn.execute('SELECT id FROM players WHERE name = ? OR alias = ?', (name, name)).fetchone()
            
            if not player:
                try:
                    cursor = conn.execute('INSERT INTO players (name, skill_rating) VALUES (?, ?)', (name, 3))
                    player_id = cursor.lastrowid
                    playing_ids.append(player_id)
                except:
                    continue
            else:
                player_id = player['id']
                playing_ids.append(player_id)
            
            # Mark as playing
            try:
                conn.execute('''
                    INSERT INTO attendance (game_id, player_id, status) 
                    VALUES (?, ?, 'playing')
                    ON CONFLICT(game_id, player_id) 
                    DO UPDATE SET status = 'playing'
                ''', (game_id, player_id))
            except:
                continue
        
        # Don't mark others as not playing - only update the ones listed
        conn.commit()
    
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/games/<int:game_id>/bulk-attendance-confirm', methods=['POST'])
@login_required
def bulk_attendance_confirm(game_id):
    player_ids = request.form.getlist('player_ids')
    new_names = request.form.getlist('new_names')

    with get_db() as conn:
        for pid in player_ids:
            try:
                conn.execute('''
                    INSERT INTO attendance (game_id, player_id, status)
                    VALUES (?, ?, 'playing')
                    ON CONFLICT(game_id, player_id)
                    DO UPDATE SET status = 'playing'
                ''', (game_id, int(pid)))
            except Exception:
                continue

        for name in new_names:
            name = name.strip()
            if not name:
                continue
            try:
                cursor = conn.execute('INSERT INTO players (name, skill_rating) VALUES (?, ?)', (name, 3))
                new_id = cursor.lastrowid
                conn.execute('''
                    INSERT INTO attendance (game_id, player_id, status)
                    VALUES (?, ?, 'playing')
                    ON CONFLICT(game_id, player_id)
                    DO UPDATE SET status = 'playing'
                ''', (game_id, new_id))
            except Exception:
                continue

        conn.commit()

    return redirect(url_for('game_detail', game_id=game_id))


@app.route('/import', methods=['GET', 'POST'])
@login_required
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

                    # Normalize alias: CSVs with "you" should map to the real name
                    if player_name.strip().lower() == 'you':
                        player_name = 'Dave Bird'
                    
                    # Normalize status
                    status_lower = status_raw.lower().strip()
                    if status_lower in ['yes', '✓', '✅', 'playing', 'in']:
                        status = 'playing'
                    elif status_lower in ['maybe', '?', '❓']:
                        status = 'maybe'
                    else:
                        status = 'not_playing'
                    
                    # Get or create player
                    player = conn.execute('SELECT id FROM players WHERE name = ? OR alias = ?', (player_name, player_name)).fetchone()
                    
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

@app.route('/service-worker.js')
def service_worker():
    from flask import send_from_directory, make_response
    response = make_response(send_from_directory('static', 'service-worker.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response


@app.route('/stats/rankings')
def rankings_timeline():
    import json
    current_year = datetime.now().year
    player_limit_raw = request.args.get('player_limit', '10').strip().lower()
    player_limit_options = [5, 10, 15, 20]
    selected_player_limit = None

    if player_limit_raw and player_limit_raw != 'all':
        try:
            parsed_limit = int(player_limit_raw)
            if parsed_limit > 0:
                selected_player_limit = parsed_limit
        except ValueError:
            selected_player_limit = None

    def name_initial(full_name):
        if not full_name:
            return ''
        parts = full_name.strip().split()
        if len(parts) == 1:
            return parts[0]
        return f"{parts[0]} {parts[-1][0]}."

    with get_db() as conn:
        face_size_setting = conn.execute(
            "SELECT value FROM settings WHERE key = 'rankings_face_size'"
        ).fetchone()
        try:
            face_point_size = int(face_size_setting['value']) if face_size_setting and face_size_setting['value'] is not None else 16
        except (TypeError, ValueError):
            face_point_size = 16
        face_point_size = max(8, min(36, face_point_size))

        games = conn.execute('''
            SELECT id, date, team1_score, team2_score
            FROM games
            WHERE team1_score IS NOT NULL
                AND team2_score IS NOT NULL
                AND (is_abandoned IS NULL OR is_abandoned = 0)
                AND strftime('%Y', date) = ?
            ORDER BY date ASC
        ''', (str(current_year),)).fetchall()

        if not games:
            return render_template(
                'stats_rankings.html',
                chart_data=None,
                year=current_year,
                face_point_size=face_point_size,
                selected_player_limit=selected_player_limit,
                player_limit_options=player_limit_options,
                total_players=0,
                shown_players=0
            )

        game_ids = [g['id'] for g in games]
        placeholders = ','.join('?' * len(game_ids))
        assignments = conn.execute(f'''
            SELECT ta.game_id, ta.player_id, ta.team_number, p.name
            FROM team_assignments ta
            JOIN players p ON ta.player_id = p.id
            WHERE ta.game_id IN ({placeholders})
        ''', game_ids).fetchall()

    # Build per-game team lookup
    game_teams = {}
    player_names = {}
    for a in assignments:
        game_teams.setdefault(a['game_id'], {})[a['player_id']] = a['team_number']
        player_names[a['player_id']] = a['name']

    # Walk through games in order, accumulating stats and recording rank snapshots
    cumulative = {}  # player_id -> {wins, draws, losses, total}
    timeline = []

    for game in games:
        gid = game['id']
        t1 = game['team1_score']
        t2 = game['team2_score']
        teams = game_teams.get(gid, {})

        for player_id, team_number in teams.items():
            if player_id not in cumulative:
                cumulative[player_id] = {'wins': 0, 'draws': 0, 'losses': 0, 'total': 0}
            stats = cumulative[player_id]
            stats['total'] += 1
            if t1 == t2:
                stats['draws'] += 1
            elif (team_number == 1 and t1 > t2) or (team_number == 2 and t2 > t1):
                stats['wins'] += 1
            else:
                stats['losses'] += 1

        # Rank all players who have played at least one game
        snapshot = sorted(
            [(pid, s) for pid, s in cumulative.items() if s['total'] > 0],
            key=lambda x: (-x[1]['wins'], -(x[1]['wins'] + x[1]['draws']), -x[1]['total'])
        )
        ranks = {pid: rank + 1 for rank, (pid, _) in enumerate(snapshot)}
        timeline.append({'date': game['date'], 'ranks': ranks})

    if not timeline:
        return render_template(
            'stats_rankings.html',
            chart_data=None,
            year=current_year,
            face_point_size=face_point_size,
            selected_player_limit=selected_player_limit,
            player_limit_options=player_limit_options,
            total_players=0,
            shown_players=0
        )

    labels = [t['date'] for t in timeline]
    all_player_ids = list(player_names.keys())

    # Sort players by their final rank
    final_ranks = timeline[-1]['ranks']
    all_player_ids.sort(key=lambda pid: final_ranks.get(pid, 9999))

    datasets = []
    for pid in all_player_ids:
        data = [t['ranks'].get(pid) for t in timeline]
        if any(d is not None for d in data):
            datasets.append({
                'player_id': pid,
                'name': name_initial(player_names[pid]),
                'data': data,
                'final_rank': final_ranks.get(pid, 9999),
                'face_url': get_player_face_url(pid)
            })

    total_players = len(datasets)
    if selected_player_limit:
        datasets = datasets[:selected_player_limit]

    shown_players = len(datasets)

    chart_data = json.dumps({'labels': labels, 'datasets': datasets})
    return render_template(
        'stats_rankings.html',
        chart_data=chart_data,
        year=current_year,
        face_point_size=face_point_size,
        selected_player_limit=selected_player_limit,
        player_limit_options=player_limit_options,
        total_players=total_players,
        shown_players=shown_players
    )


# Initialize database on module load (for Gunicorn/Azure)
init_db()

if __name__ == '__main__':
    print(f"Starting Flask server on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=True)
