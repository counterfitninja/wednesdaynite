import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('football.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("="*80)
print("GAMES BREAKDOWN")
print("="*80)

games = cur.execute('''
    SELECT id, date, location, is_abandoned,
           (SELECT COUNT(*) FROM attendance WHERE game_id = g.id AND status='playing') as playing_count
    FROM games g
    ORDER BY date
''').fetchall()

today = datetime.now().strftime('%Y-%m-%d')
print(f"Today's date: {today}\n")

total_past = 0
total_past_non_abandoned = 0

for g in games:
    past = g['date'] <= today
    abandoned = g['is_abandoned'] == 1
    counts_label = ""
    
    if past:
        total_past += 1
        if not abandoned:
            total_past_non_abandoned += 1
            counts_label = " ✓ COUNTS for attendance denominator"
        else:
            counts_label = " ✗ ABANDONED - excluded from denominator"
    else:
        counts_label = " (future game)"
    
    print(f"Game #{g['id']:2} | {g['date']} | {g['location'] or 'N/A':20} | abandoned={abandoned} | {g['playing_count']} playing{counts_label}")

print(f"\n{'─'*80}")
print(f"Total past games: {total_past}")
print(f"Total past NON-ABANDONED games (denominator): {total_past_non_abandoned}")
print(f"{'─'*80}\n")

print("="*80)
print("PLAYER ATTENDANCE BREAKDOWN")
print("="*80)

players = cur.execute('''
    SELECT p.id, p.name
    FROM players p
    ORDER BY p.name
''').fetchall()

for player in players[:15]:  # Limit to first 15 for readability
    print(f"\n{player['name']}:")
    
    # Get all attendance records for this player
    records = cur.execute('''
        SELECT g.id, g.date, g.is_abandoned, a.status
        FROM attendance a
        JOIN games g ON a.game_id = g.id
        WHERE a.player_id = ?
        ORDER BY g.date
    ''', (player['id'],)).fetchall()
    
    played_count = 0
    responded_count = 0
    
    for r in records:
        past = r['date'] <= today
        abandoned = r['is_abandoned'] == 1
        
        if past and not abandoned:
            responded_count += 1
            if r['status'] == 'playing':
                played_count += 1
                print(f"  Game #{r['id']} {r['date']}: {r['status']:12} ✓ COUNTS as playing")
            else:
                print(f"  Game #{r['id']} {r['date']}: {r['status']:12} (responded but not playing)")
        elif past and abandoned:
            print(f"  Game #{r['id']} {r['date']}: {r['status']:12} ✗ ABANDONED - excluded")
        else:
            print(f"  Game #{r['id']} {r['date']}: {r['status']:12} (future)")
    
    if total_past_non_abandoned > 0:
        percentage = round((played_count * 100.0 / total_past_non_abandoned), 1)
    else:
        percentage = 0.0
    
    print(f"  ► PLAYED: {played_count} / DENOMINATOR: {total_past_non_abandoned} = {percentage}%")

conn.close()

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Attendance % formula: (games_played / total_non_abandoned_past_games) * 100")
print(f"Current denominator: {total_past_non_abandoned}")
print(f"\nFor 100% attendance, a player must have 'playing' status for all {total_past_non_abandoned} non-abandoned past games.")
