# ⚽ Football Game Tracker - Azure Web App

Track attendance for your amateur football games. Import data from WhatsApp polls and maintain a register of who plays each week.

## Features

✅ **Web-based interface** - Access from any device  
✅ **Player management** - Track all your regular players  
✅ **Game tracking** - Record games with dates, locations, and notes  
✅ **Attendance recording** - Track who's playing, not playing, or maybe  
✅ **WhatsApp CSV import** - Upload poll results directly  
✅ **Statistics dashboard** - See attendance rates and participation  
✅ **SQLite database** - Simple, file-based storage

## Deploy to Azure Web App

### Option 1: Deploy from VS Code

1. **Install Azure App Service extension** in VS Code

2. **Sign in to Azure**
   - Click Azure icon in sidebar
   - Sign in to your account

3. **Deploy**
   - Right-click on the project folder
   - Select "Deploy to Web App..."
   - Choose "Create new Web App"
   - Enter a name (e.g., "football-tracker")
   - Select Python 3.11
   - Wait for deployment

### Option 2: Deploy via Azure Portal

1. **Create Web App**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create → Web App
   - Name: `football-tracker-yourname`
   - Runtime: Python 3.11
   - Region: Choose nearest
   - Plan: Free F1 or Basic B1

2. **Deploy Code**
   - In Web App → Deployment Center
   - Source: Local Git or GitHub
   - Push your code

### Option 3: Deploy via Azure CLI

```powershell
# Login to Azure
az login

# Create resource group
az group create --name FootballTrackerRG --location eastus

# Create App Service plan
az appservice plan create --name FootballTrackerPlan --resource-group FootballTrackerRG --sku F1 --is-linux

# Create web app
az webapp create --resource-group FootballTrackerRG --plan FootballTrackerPlan --name football-tracker-yourname --runtime "PYTHON:3.11"

# Deploy code
az webapp up --name football-tracker-yourname --resource-group FootballTrackerRG
```

## Local Development

### Run Locally

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:5000`

## Using the App

### Add Players

1. Click "Players" in navigation
2. Click "Add New Player"
3. Enter name (required), phone and email (optional)

### Create a Game

1. Click "Add New Game"
2. Enter date, location, and notes
3. Click "Add Game"

### Record Attendance

1. Click on a game to view details
2. Use the "Record Attendance" form
3. Select player and status (Playing/Maybe/Not Playing)
4. Submit

### Import WhatsApp Poll

1. Click "Import CSV"
2. Prepare your CSV file:
```csv
Player Name,Status
John Smith,Yes
Jane Doe,No
Mike Johnson,Yes
```
3. Upload file and select game date
4. Click Import

### View Statistics

- Click "Players" to see attendance rates
- Green badge = 75%+ attendance
- Yellow badge = 50-74% attendance
- Red badge = Below 50% attendance

## File Structure

```
football-tracker/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base layout
│   ├── index.html        # Games list
│   ├── players.html      # Players list
│   ├── add_game.html     # Add game form
│   ├── add_player.html   # Add player form
│   ├── game_detail.html  # Game attendance details
│   └── import.html       # CSV import
└── football.db           # SQLite database (created on first run)
```

## Database

The app uses SQLite with three tables:

**players**
- id, name, phone, email, created_at

**games**
- id, date, location, notes, created_at

**attendance**
- id, game_id, player_id, status, created_at

## Configuration

### Custom Domain

In Azure Portal → Your Web App → Custom domains

### Scale Up

In Azure Portal → Your Web App → Scale up (App Service plan)
- Free F1: Good for testing
- Basic B1: Better performance
- Standard S1: Production

### Backup Database

The SQLite database file is stored in the web app's file system. To backup:

```powershell
# Using Azure CLI
az webapp download --resource-group FootballTrackerRG --name football-tracker-yourname --file-path football.db
```

Or use FTP/FTPS from Azure Portal → Deployment Center

## Troubleshooting

### App won't start

Check logs in Azure Portal → Your Web App → Log stream

### Database not persisting

SQLite files in Azure Web Apps persist in `/home` directory. Make sure `football.db` is created there.

### Import not working

Check file format:
- Must be CSV with headers
- Headers: "Player Name" and "Status"
- UTF-8 encoding

## Tips

### Weekly Workflow

1. Create game for next week
2. Share WhatsApp poll: "Playing this Sunday?"
3. After voting, export results to CSV
4. Import CSV via web interface
5. Check attendance stats

### Mobile Access

The web app is mobile-friendly. Bookmark it on your phone for quick access.

### WhatsApp Integration

You can manually create the CSV from WhatsApp poll results, or copy-paste into Excel and save as CSV.

## Cost

**Azure Free Tier (F1)**
- Free forever
- 60 CPU minutes/day
- 1 GB RAM
- 1 GB storage
- Perfect for small groups

**Basic Tier (B1)**
- ~$13/month
- Unlimited CPU time
- 1.75 GB RAM
- 10 GB storage
- Better for active use

## Future Enhancements

- Email/SMS reminders
- Team balancing
- Score tracking
- Player ratings
- WhatsApp bot integration

---

Made for tracking amateur football games 🎯⚽
