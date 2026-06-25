"""
SSAT Study App - Flask
Editable single-file Flask application for SSAT Verbal & Quantitative practice.
Mobile-friendly version with all fixes applied.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, render_template, jsonify
import random
from fractions import Fraction
import math
from datetime import datetime
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)

# Server-side session configuration (solves cookie size issue)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['SESSION_FILE_THRESHOLD'] = 500
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize server-side session
Session(app)

# Create session directory
os.makedirs('./flask_session', exist_ok=True)




# === User Info ===


USERS_FILE = 'users.csv'


# === Database Functions ===


# ============================================================
# DETECT IF RUNNING ON RENDER
# ============================================================
ON_RENDER = os.environ.get('RENDER') == 'true'
ON_RENDER = ON_RENDER or os.environ.get('DATABASE_URL') is not None

# ============================================================
# DATABASE/CSV FUNCTIONS - CONDITIONAL
# ============================================================

if ON_RENDER:
    pass
    #import pg8000
    #import urllib.parse
    
##    def get_db_connection():
##        """Get database connection using Render's DATABASE_URL"""
##        database_url = os.environ.get('DATABASE_URL')
##        if not database_url:
##            raise Exception("DATABASE_URL environment variable not set!")
##        
##        result = urllib.parse.urlparse(database_url)
##        
##        conn = pg8000.connect(
##            user=result.username,
##            password=result.password,
##            host=result.hostname,
##            port=result.port or 5432,
##            database=result.path[1:]
##        )
##        return conn
##    
##    def init_storage():
##        """Create all tables if they don't exist"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        
##        cursor.execute('''
##            CREATE TABLE IF NOT EXISTS users (
##                username TEXT PRIMARY KEY,
##                password_hash TEXT NOT NULL,
##                is_admin BOOLEAN DEFAULT FALSE,
##                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
##            )
##        ''')
##        
##        cursor.execute('''
##            CREATE TABLE IF NOT EXISTS attempts (
##                id SERIAL PRIMARY KEY,
##                username TEXT REFERENCES users(username),
##                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
##                reading_type TEXT,
##                total_score INTEGER,
##                reading_score INTEGER,
##                verbal_score INTEGER,
##                math_score INTEGER
##            )
##        ''')
##        
##        # Check for admin user
##        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
##        admin_exists = cursor.fetchone()
##        
##        if not admin_exists:
##            admin_hash = generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123'))
##            cursor.execute(
##                "INSERT INTO users (username, password_hash, is_admin) VALUES (%s, %s, %s)",
##                ('admin', admin_hash, True)
##            )
##        
##        conn.commit()
##        cursor.close()
##        conn.close()
##        print("PostgreSQL database initialized successfully with pg8000")
##    
##    def verify_user(username, password):
##        """Verify user credentials"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
##        user = cursor.fetchone()
##        cursor.close()
##        conn.close()
##        
##        # user is a tuple: (username, password_hash, is_admin, created_at)
##        if user and check_password_hash(user[1], password):
##            return True
##        return False
##    
##    def is_admin(username):
##        """Check if user is admin"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute("SELECT is_admin FROM users WHERE username = %s", (username,))
##        user = cursor.fetchone()
##        cursor.close()
##        conn.close()
##        # user[0] is the is_admin value
##        return user[0] if user else False
##    
##    def create_user(username, password, is_admin=True):
##        """Create a new user"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        
##        # Check if user exists
##        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
##        existing = cursor.fetchone()
##        
##        if existing:
##            cursor.close()
##            conn.close()
##            return False
##        
##        password_hash = generate_password_hash(password)
##        cursor.execute(
##            "INSERT INTO users (username, password_hash, is_admin) VALUES (%s, %s, %s)",
##            (username, password_hash, is_admin)
##        )
##        conn.commit()
##        cursor.close()
##        conn.close()
##        return True
##    
##    def delete_user(username):
##        """Delete a user and all their data"""
##        if username == 'admin':
##            return False
##        
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute("DELETE FROM attempts WHERE username = %s", (username,))
##        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
##        conn.commit()
##        cursor.close()
##        conn.close()
##        return True
##    
##    def get_all_users():
##        """Get list of all users"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute("SELECT username, is_admin, created_at FROM users ORDER BY created_at")
##        users = cursor.fetchall()
##        cursor.close()
##        conn.close()
##        
##        result = []
##        for user in users:
##            # user is a tuple: (username, is_admin, created_at)
##            result.append({
##                'username': user[0],
##                'is_admin': user[1],
##                'created_at': user[2]
##            })
##        return result
##    
##    def save_user_attempt(username, reading_type, total_score, reading_score, verbal_score, math_score):
##        """Save an attempt to PostgreSQL"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute('''
##            INSERT INTO attempts (username, reading_type, total_score, reading_score, verbal_score, math_score)
##            VALUES (%s, %s, %s, %s, %s, %s)
##        ''', (username, reading_type, total_score, reading_score, verbal_score, math_score))
##        conn.commit()
##        cursor.close()
##        conn.close()
##        print(f"Saved attempt for {username}: {total_score}%")  # Debug
##    
##    def get_user_attempts(username):
##        """Get all attempts for a user from PostgreSQL"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute('''
##            SELECT * FROM attempts 
##            WHERE username = %s 
##            ORDER BY timestamp
##        ''', (username,))
##        attempts = cursor.fetchall()
##        cursor.close()
##        conn.close()
##        
##        result = []
##        for a in attempts:
##            # a is a tuple: (id, username, timestamp, reading_type, total_score, reading_score, verbal_score, math_score)
##            result.append({
##                'id': a[0],
##                'username': a[1],
##                'timestamp': a[2].strftime('%Y-%m-%d %H:%M:%S') if hasattr(a[2], 'strftime') else str(a[2]),
##                'reading_type': a[3],
##                'total_score': a[4],
##                'reading_score': a[5],
##                'verbal_score': a[6],
##                'math_score': a[7]
##            })
##        return result
##    
##    def reset_user_data(username):
##        """Delete all attempts for a user"""
##        conn = get_db_connection()
##        cursor = conn.cursor()
##        cursor.execute('DELETE FROM attempts WHERE username = %s', (username,))
##        conn.commit()
##        cursor.close()
##        conn.close()
##        return True


else:
    # ============================================================
    # CSV MODE (for local testing)
    # ============================================================
    
    USERS_FILE = 'users.csv'
    ATTEMPTS_FILE = 'sample_test_data.csv'
    
    def init_storage():
        """Initialize CSV files if they don't exist"""
        # Initialize users.csv
        if not os.path.isfile(USERS_FILE):
            with open(USERS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password_hash', 'is_admin'])
            
            # Create default admin user
            admin_hash = generate_password_hash('admin123')
            with open(USERS_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['admin', admin_hash, 'True'])
        
        # Initialize attempts.csv
        if not os.path.isfile(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'username', 'reading_type', 'total_score', 'reading_score', 'verbal_score', 'math_score'])
        
        print("CSV files initialized successfully")
    
    def verify_user(username, password):
        """Verify user credentials from CSV"""
        if not os.path.isfile(USERS_FILE):
            return False
        
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    return check_password_hash(row['password_hash'], password)
        return False
    
    def is_admin(username):
        """Check if user is admin from CSV"""
        if not os.path.isfile(USERS_FILE):
            return False
        
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    return row['is_admin'] == 'True'
        return False
    
    def create_user(username, password, is_admin=False):
        """Create a new user in CSV"""
        # Check if user exists
        if os.path.isfile(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['username'] == username:
                        return False
        
        password_hash = generate_password_hash(password)
        
        with open(USERS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password_hash, 'True' if is_admin else 'False'])
        
        return True
    
    def delete_user(username):
        """Delete a user from CSV"""
        if username == 'admin':
            return False
        
        users = []
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['username'] != username:
                    users.append(row)
        
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        
        return True
    
    def get_all_users():
        """Get list of all users from CSV"""
        users = []
        if os.path.isfile(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users.append({
                        'username': row['username'],
                        'is_admin': row['is_admin'] == 'True'
                    })
        return users
    
    def save_user_attempt(username, reading_type, total_score, reading_score, verbal_score, math_score):
        """Save an attempt to CSV"""
        with open(ATTEMPTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                username,
                reading_type,
                total_score,
                reading_score,
                verbal_score,
                math_score
            ])
    
    def get_user_attempts(username):
        """Get all attempts for a user from CSV"""
        attempts = []
        if os.path.isfile(ATTEMPTS_FILE):
            with open(ATTEMPTS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['username'] == username:
                        attempts.append(row)
        return attempts
    
    def reset_user_data(username):
        """Delete all attempts for a user from CSV"""
        if not os.path.isfile(ATTEMPTS_FILE):
            return False
        
        rows = []
        with open(ATTEMPTS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['username'] != username:
                    rows.append(row)
        
        with open(ATTEMPTS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        return True

    init_storage()

# ============================================================
# INITIALIZE STORAGE (works for both modes)
# ============================================================





# === GENERATORS ===

_vocab_index = 0
_shuffled_vocab = None

def gen_synonyms(n=5):
    global _vocab_index, _shuffled_vocab

    vocab = [
        ("abolish", "end"),
        ("absurd", "ridiculous"),
        ("abundant", "plentiful"),
        ("accessible", "reachable"),
        ("achieve", "accomplish"),
        ("acute", "severe"),
        ("adapt", "adjust"),
        ("adversary", "enemy"),
        ("adversity", "hardship"),
        ("agile", "nimble"),
        ("alert", "watchful"),
        ("alternate", "switch"),
        ("ambiguous", "unclear"),
        ("ample", "sufficient"),
        ("ancient", "old"),
        ("anxious", "worried"),
        ("apparent", "obvious"),
        ("arid", "dry"),
        ("awkward", "clumsy"),
        ("barren", "empty"),
        ("benevolent", "kind"),
        ("brisk", "quick"),
        ("capable", "able"),
        ("cautious", "careful"),
        ("cherish", "value"),
        ("civil", "polite"),
        ("colossal", "huge"),
        ("compact", "dense"),
        ("condemn", "criticize"),
        ("conform", "obey"),
        ("contrast", "difference"),
        ("contribute", "donate"),
        ("convenient", "handy"),
        ("crucial", "vital"),
        ("curious", "inquisitive"),
        ("decay", "rot"),
        ("defer", "delay"),
        ("degrade", "humiliate"),
        ("delight", "joy"),
        ("dense", "thick"),
        ("detect", "discover"),
        ("diminish", "reduce"),
        ("distract", "divert"),
        ("eager", "keen"),
        ("efficient", "productive"),
        ("elevate", "raise"),
        ("essential", "necessary"),
        ("expand", "enlarge"),
        ("extinct", "gone"),
        ("fluent", "smooth"),
        ("fragile", "delicate"),
        ("frequent", "common"),
        ("genuine", "real"),
        ("glare", "stare"),
        ("gloom", "darkness"),
        ("graceful", "elegant"),
        ("grim", "stern"),
        ("hesitant", "uncertain"),
        ("host", "owner"),
        ("idle", "inactive"),
        ("identical", "same"),
        ("illegal", "unlawful"),
        ("immune", "protected"),
        ("immense", "huge"),
        ("influence", "impact"),
        ("inspect", "examine"),
        ("intense", "strong"),
        ("interrupt", "stop"),
        ("justify", "prove"),
        ("keen", "eager"),
        ("lethal", "deadly"),
        ("linger", "remain"),
        ("lofty", "high"),
        ("meddle", "interfere"),
        ("methodical", "orderly"),
        ("modest", "humble"),
        ("mortal", "human"),
        ("motivate", "inspire"),
        ("numerous", "many"),
        ("obstacle", "barrier"),
        ("oblivious", "unaware"),
        ("obtain", "gain"),
        ("obvious", "clear"),
        ("occupy", "fill"),
        ("originate", "start"),
        ("ordinary", "common"),
        ("pardon", "forgive"),
        ("peculiar", "strange"),
        ("permit", "allow"),
        ("persuade", "convince"),
        ("plentiful", "abundant"),
        ("precise", "exact"),
        ("postpone", "delay"),
        ("proud", "pleased"),
        ("qualify", "certify"),
        ("reluctant", "hesitant"),
        ("refine", "improve"),
        ("scarce", "rare"),
        ("sincere", "honest"),
        ("substantial", "large"),
        ("abrupt", "sudden"),
        ("accurate", "correct"),
        ("adaptable", "flexible"),
        ("adequate", "enough"),
        ("alertness", "awareness"),
        ("analyze", "examine"),
        ("anticipate", "expect"),
        ("approve", "accept"),
        ("assist", "help"),
        ("assume", "suppose"),
        ("benefit", "advantage"),
        ("brief", "short"),
        ("calculate", "compute"),
        ("candidate", "applicant"),
        ("clarify", "explain"),
        ("combine", "merge"),
        ("commend", "praise"),
        ("compare", "evaluate"),
        ("conclude", "finish"),
        ("confident", "certain"),
        ("consequence", "result"),
        ("consider", "think about"),
        ("constant", "unchanging"),
        ("consume", "eat"),
        ("contemporary", "modern"),
        ("convict", "declare guilty"),
        ("cooperate", "work together"),
        ("decline", "refuse"),
        ("definite", "certain"),
        ("demonstrate", "show"),
        ("dependable", "reliable"),
        ("desperate", "urgent"),
        ("determine", "decide"),
        ("distinct", "separate"),
        ("dominate", "control"),
        ("eliminate", "remove"),
        ("emphasize", "highlight"),
        ("encounter", "meet"),
        ("essentially", "basically"),
        ("eventual", "final"),
        ("exaggerate", "overstate"),
        ("exclude", "leave out"),
        ("flexible", "adaptable"),
        ("fortunate", "lucky"),
        ("frustrate", "annoy"),
        ("generous", "giving"),
        ("gradual", "slow"),
        ("illustrate", "explain"),
        ("immediate", "instant")
    ]

    synonym_distractors = [  # Renamed to avoid conflict
        "easy", "boring", "short", "lightweight", "slow",
        "funny", "careless", "weak", "fake", "noisy",
        "cold", "tiny", "secret", "hidden", "expensive",
        "lazy", "thick", "generous", "silly", "timid",
        "rare", "visible", "useless", "heavy", "rough",
        "strange", "unfair", "rapid", "beautiful", "confusing",
        "deep", "tall", "shallow", "odd", "harsh",
        "difficult", "old", "ancient", "wet", "dry",
        "colorless", "quiet", "fragile", "broken", "severe",
        "accurate", "active", "awkward", "basic", "brief",
        "calm", "clumsy", "common", "complex", "dangerous", "dark",
        "delayed", "dull", "empty", "familiar",
        "fancy", "fast", "firm", "formal", "friendly", "gentle",
        "happy", "harmless", "impossible", "informal",
        "interesting", "large", "loose", "minor", "modern",
        "narrow", "normal", "ordinary", "plain", "powerful",
        "public", "random", "safe", "simple", "soft", "strict",
        "sudden", "thin", "tidy", "useful", "warm", "wide", "young"
    ]

    # Initialize shuffled vocab ONCE
    if _shuffled_vocab is None:
        _shuffled_vocab = vocab[:]
        random.shuffle(_shuffled_vocab)

    questions = []

    for _ in range(n):
        # Reset after full cycle
        if _vocab_index >= len(_shuffled_vocab):
            random.shuffle(_shuffled_vocab)
            _vocab_index = 0

        word, correct_def = _shuffled_vocab[_vocab_index]
        _vocab_index += 1

        wrong_choices = random.sample(
            [d for d in synonym_distractors if d != correct_def],
            4
        )

        choices = wrong_choices + [correct_def]
        random.shuffle(choices)

        question_text = f"What does <b>{word}</b> most nearly mean?"
        questions.append((question_text, choices, choices.index(correct_def)))

    return questions



# analogy_templates: (A, B, C, correct D, category)
analogy_templates = [
    #miscelanious
    ("Deer", "Forest", "Gazelle", "Africa", "misc"),
    ("Pianist", "Hands", "Ballerina", "Feet", "misc"),
    ("Pound", "Weight", "Mile", "Distance", "misc"),
    ("Pencil", "Writing", "Mop", "Cleaning", "misc"),
    ("Faucet", "Water", "Outlet", "Electricity", "misc"),
    ("Arboretum", "Garden", "Orchard", "Farm", "misc"),
    ("Kitten", "Cat", "Puppy", "Dog", "misc"),
    ("Solitary", "Hermit", "Greedy", "Miser", "misc"),
    ("Abdicate", "Monarch", "Resign", "Governor", "misc"),
    ("Sculpture", "Art", "Tango", "Dance", "misc"),
    ("Trustworthy", "Friend", "Caring", "Parent", "misc"),
    ("Novel", "Poem", "Marathon", "Sprint", "misc"),
    ("Pious", "Belief", "Athletic", "Strength", "misc"),
    ("Mammal", "Human", "Relationship", "Friendship", "misc"),
    ("Wisdom", "Fools", "Folly", "Sages", "misc"),
    ("Telephone", "Communication", "Stove", "Cooking", "misc"),
    ("Physics", "Science", "Calculus", "Mathematics", "misc"),
    ("Jousting", "Lance", "Fencing", "Sword", "misc"),
    ("Tallow", "Fat", "Leather", "Skin", "misc"),
    ("Mitigate", "Harm", "Alleviate", "Suffering", "misc"),
    ("Yawn", "Sleepy", "Fidget", "Restless", "misc"),
    ("Website", "Internet", "Book", "Library", "misc"),
    ("Drought", "Water", "Famine", "Food", "misc"),
    ("Persuasive", "Argument", "Compelling", "Evidence", "misc"),
    ("Remorseful", "Unrepentant", "Slender", "Stout", "misc"),
    ("High School", "College", "Apprenticeship", "Job", "misc"),
    ("Dilate", "Contract", "Expand", "Narrow", "misc"),
    ("Collusion", "Cooperation", "Smuggling", "Importing", "misc"),
    ("Plausible", "Incredible", "Possible", "Unlikely", "misc"),
    ("Annoyed", "Furious", "Thin", "Gaunt", "misc"),
    ("Navigate", "Destination", "Strive", "Goal", "misc"),
     ("Fish", "Water", "Lion", "Land", "misc"),            
    ("Sick", "Healthy", "Jailed", "Free", "misc"),      
    ("Dancer", "Feet", "Drummer", "Drums", "misc"),     
    ("Bystander", "Event", "Spectator", "Game", "misc"), 
    ("Baker", "Bread", "Butcher", "Livestock", "misc"),  
    ("Igneous", "Rock", "Watercolor", "Painting", "misc"), 
    ("Delicious", "Taste", "Melodious", "Sound", "misc"), 
    ("Cube", "Square", "Sphere", "Circle", "misc"),      
    ("Jam", "Fruit", "Butter", "Milk", "misc"),         
    ("Mile", "Quart", "Length", "Volume", "misc"),      
    ("Biologist", "Scientist", "Surgeon", "Doctor", "misc"), 
    ("Clay", "Potter", "Marble", "Sculptor", "misc"),   
    ("Clip", "Movie", "Excerpt", "Novel", "misc"),      
    ("Glacier", "Ice", "Ocean", "Water", "misc"),       
    ("Sneer", "Disdain", "Cringe", "Fear", "misc"),       
    ("Famine", "Food", "Drought", "Water", "misc"),     
    ("Teacher", "Student", "Coach", "Player", "misc"),  
    ("Muffle", "Noise", "Dam", "Flood", "misc"),        
    ("Rest", "Exhaustion", "Water", "Thirst", "misc"), 
    ("Playwright", "Script", "Choreographer", "Dance", "misc"),
    ("Single-handed", "Assistance", "Anonymous", "Authorship", "misc"), 
    ("Stable", "Horse", "Kennel", "Dog", "misc"),       
    ("Tree", "Knee", "Forest", "Body", "misc"),
    
    # animals
    ("Puppy", "Dog", "Calf", "Cow", "animals"),
    ("Kitten", "Cat", "Fawn", "Deer", "animals"),
    ("Cub", "Bear", "Chick", "Bird", "animals"),
    ("Duck", "Water", "Camel", "Desert", "animals"),
    ("Bee", "Hive", "Ant", "Colony", "animals"),
    ("Lion", "Pride", "Wolf", "Pack", "animals"),
    ("Eagle", "Wing", "Shark", "Fin", "animals"),
    ("Snake", "Slither", "Bird", "Fly", "animals"),
    ("Frog", "Hop", "Fish", "Swim", "animals"),

    # plants
    ("Leaf", "Tree", "Petal", "Flower", "plants"),
    ("Root", "Plant", "Foundation", "Building", "plants"),
    ("Seed", "Soil", "Egg", "Nest", "plants"),
    ("Branch", "Tree", "Stem", "Flower", "plants"),
    ("Thorn", "Rose", "Spike", "Cactus", "plants"),
    ("Bark", "Tree", "Skin", "Animal", "plants"),
    ("Bud", "Flower", "Sprout", "Plant", "plants"),
    ("Fruit", "Tree", "Vegetable", "Plant", "plants"),
    ("Moss", "Rock", "Algae", "Water", "plants"),

    # places
    ("Student", "School", "Doctor", "Hospital", "places"),
    ("Chef", "Kitchen", "Teacher", "Classroom", "places"),
    ("Lifeguard", "Pool", "Pilot", "Cockpit", "places"),
    ("Actor", "Theater", "Artist", "Studio", "places"),
    ("Banker", "Bank", "Librarian", "Library", "places"),
    ("Farmer", "Farm", "Mechanic", "Garage", "places"),
    ("Scientist", "Lab", "Athlete", "Stadium", "places"),
    ("Judge", "Court", "Mayor", "City Hall", "places"),
    ("Firefighter", "Station", "Soldier", "Base", "places"),
    ("Waiter", "Restaurant", "Clerk", "Store", "places"),

    # materials / tools
    ("Brush", "Paint", "Pen", "Ink", "materials"),
    ("Hammer", "Nail", "Saw", "Wood", "materials"),
    ("Shovel", "Dig", "Knife", "Cut", "materials"),
    ("Wrench", "Bolt", "Scissors", "Paper", "materials"),
    ("Needle", "Thread", "Glue", "Paper", "materials"),
    ("Drill", "Hole", "Saw", "Cut", "materials"),
    ("Chisel", "Sculpture", "Pen", "Story", "materials"),
    ("Rope", "Tie", "Tape", "Stick", "materials"),
    ("Glass", "Window", "Metal", "Car", "materials"),
    ("Brick", "Wall", "Board", "Floor", "materials"),

    # measurements
    ("Clock", "Time", "Scale", "Weight", "measurements"),
    ("Thermometer", "Temperature", "Ruler", "Length", "measurements"),
    ("Odometer", "Miles", "Compass", "Direction", "measurements"),
    ("Protractor", "Angle", "Barometer", "Pressure", "measurements"),
    ("Speedometer", "Speed", "Watch", "Seconds", "measurements"),
    ("Calendar", "Days", "Meter", "Distance", "measurements"),
    ("Map", "Location", "Timer", "Seconds", "measurements"),
    ("Measuring Cup", "Volume", "Scale", "Mass", "measurements"),
    ("Gauge", "Pressure", "Meter", "Length", "measurements"),
    ("Telescope", "Stars", "Microscope", "Cells", "measurements"),

    # properties
    ("Rain", "Wet", "Ice", "Cold", "properties"),
    ("Fire", "Hot", "Snow", "Cold", "properties"),
    ("Feather", "Light", "Rock", "Heavy", "properties"),
    ("Glass", "Fragile", "Steel", "Strong", "properties"),
    ("Night", "Dark", "Day", "Bright", "properties"),
    ("Sponge", "Soft", "Brick", "Hard", "properties"),
    ("Cheetah", "Fast", "Turtle", "Slow", "properties"),
    ("Metal", "Shiny", "Wood", "Dull", "properties"),
    ("Rain", "Cloudy", "Sun", "Bright", "properties"),
    ("Fog", "Thick", "Wind", "Thin", "properties"),

    # creations
    ("Author", "Book", "Baker", "Bread", "creations"),
    ("Composer", "Music", "Chef", "Meal", "creations"),
    ("Painter", "Canvas", "Sculptor", "Stone", "creations"),
    ("Carpenter", "Furniture", "Tailor", "Clothes", "creations"),
    ("Chef", "Recipe", "Artist", "Design", "creations"),
    ("Engineer", "Bridge", "Architect", "Building", "creations"),
    ("Director", "Movie", "Musician", "Song", "creations"),
    ("Gardener", "Garden", "Builder", "House", "creations"),
    ("Writer", "Story", "Poet", "Poem", "creations"),
    ("Inventor", "Machine", "Designer", "Model", "creations"),

    # locations (nature / geography)
    ("Nest", "Bird", "Den", "Wolf", "locations"),
    ("Burrow", "Rabbit", "Hive", "Bee", "locations"),
    ("Lake", "Water", "Desert", "Sand", "locations"),
    ("Mountain", "High", "Valley", "Low", "locations"),
    ("River", "Flow", "Road", "Drive", "locations"),
    ("Cave", "Bat", "Ocean", "Fish", "locations"),
    ("Forest", "Trees", "Ocean", "Waves", "locations"),
    ("Island", "Ocean", "Oasis", "Desert", "locations"),
    ("Harbor", "Boat", "Garage", "Car", "locations"),
    ("Farm", "Animals", "Garden", "Plants", "locations"),

    # clothing
    ("Hand", "Glove", "Foot", "Sock", "clothing"),
    ("Head", "Hat", "Neck", "Scarf", "clothing"),
    ("Leg", "Pants", "Torso", "Shirt", "clothing"),
    ("Rain", "Coat", "Snow", "Boots", "clothing"),
    ("Sun", "Shade", "Rain", "Umbrella", "clothing"),
    ("Finger", "Ring", "Wrist", "Bracelet", "clothing"),
    ("Swimmer", "Goggles", "Biker", "Helmet", "clothing"),
    ("Chef", "Apron", "Doctor", "Gloves", "clothing"),
    ("Hiker", "Boots", "Runner", "Sneakers", "clothing"),

    # vehicles
    ("Wheel", "Car", "Propeller", "Airplane", "vehicles"),
    ("Sail", "Boat", "Wing", "Bird", "vehicles"),
    ("Engine", "Train", "Motor", "Boat", "vehicles"),
    ("Pedal", "Bike", "Oar", "Rowboat", "vehicles"),
    ("Pilot", "Plane", "Driver", "Car", "vehicles"),
    ("Anchor", "Ship", "Brake", "Bike", "vehicles"),
    ("Tractor", "Farm", "Bus", "City", "vehicles"),
    ("Light", "Car", "Horn", "Truck", "vehicles"),
    ("Paddle", "Canoe", "Wheel", "Skateboard", "vehicles"),
    ("Lift", "Helicopter", "Thrust", "Rocket", "vehicles"),

    # shapes
    ("Circle", "Sphere", "Square", "Cube", "shapes"),
    ("Triangle", "Pyramid", "Rectangle", "Box", "shapes"),
    ("Oval", "Egg", "Rectangle", "Book", "shapes"),
    ("Hexagon", "Beehive", "Circle", "Wheel", "shapes"),
    ("Square", "Tile", "Circle", "Coin", "shapes"),
    ("Line", "Segment", "Angle", "Corner", "shapes"),
    ("Star", "Sky", "Heart", "Body", "shapes"),

    # opposites
    ("Hot", "Cold", "Wet", "Dry", "opposites"),
    ("Up", "Down", "Left", "Right", "opposites"),
    ("Fast", "Slow", "Light", "Dark", "opposites"),
    ("Day", "Night", "Summer", "Winter", "opposites"),
    ("Happy", "Sad", "Brave", "Scared", "opposites"),
    ("Win", "Lose", "Give", "Take", "opposites"),
    ("Short", "Tall", "Weak", "Strong", "opposites"),
    ("Young", "Old", "Near", "Far", "opposites"),
    ("Full", "Empty", "Open", "Closed", "opposites"),
    ("Push", "Pull", "Rise", "Fall", "opposites"),
]

# ======================
# EXPANDED DISTRACTOR BANK (Renamed to avoid conflict)
# ======================

analogy_distractor_bank = {
    "animals": ["Horse","Goat","Rabbit","Fox","Sheep","Cow","Pig","Dog","Cat","Bird","Lion","Tiger","Snake","Elephant","Wolf","Bear","Frog","Fish"],
    "plants": ["Stem","Root","Seed","Branch","Bark","Leaf","Flower","Trunk","Petal","Sprout","Vine","Grass","Bush","Moss","Cactus","Fern"],
    "places": ["Library","Office","Gym","Restaurant","Store","Park","Hospital","School","Kitchen","Market","Zoo","Museum","Bank","Theater","Beach","Cafe","Station","Arena"],
    "materials": ["Paper","Wood","Clay","Glass","Plastic","Metal","Ink","Paint","Pen","Brush","Knife","Shovel","Hammer","String","Fabric","Wire","Stone","Brick"],
    "measurements": ["Speed","Distance","Weight","Height","Length","Temperature","Time","Volume","Pressure"],
    "properties": ["Cold","Soft","Bright","Loud","Dry","Hard","Hot","Wet","Heavy","Light","Fast","Slow"],
    "creations": ["Poem","Drawing","Song","Book","Bread","Dish","Painting","Sculpture","Essay","Melody","Craft","Cake"],
    "locations": ["Burrow","Cave","Tree","Water","Grassland","Log","Nest","Hive","Lake","Ocean","River","Garden","Barn","Den","Attic","Basement","Yard","Field"],
    "clothing": ["Hat","Belt","Sock","Scarf","Boot","Coat","Glove","Shoe","Shirt","Pants","Dress","Cap","Jacket","Sweater","Mitten","Hood","Sandal"],
    "vehicles": ["Car","Bicycle","Airplane","Boat","Helicopter","Train","Bus","Truck","Scooter","Ship","Submarine","Motorcycle","Tram","Cart","Van"],
    "shapes": ["Circle","Sphere","Square","Cube","Triangle","Pyramid","Rectangle","Cylinder","Oval","Cone","Hexagon","Pentagon","Rhombus","Trapezoid"],
    "opposites": ["Hot","Cold","Wet","Dry","Up","Down","Left","Right","Fast","Slow","Light","Dark","Tall","Short","Near","Far"]
}




# ======================
# READING COMPREHENSION DATA
# ======================

reading_passages = {

    "nonfiction": [
        # Original nf1 (kept as is)
        {
        "id": "nf1",
        "title": "The Great Pacific Garbage Patch",
        "passage": """The Great Pacific Garbage Patch is a massive collection of marine debris located in the North Pacific Ocean. Discovered in 1997, this floating dump is twice the size of Texas and consists primarily of microplastics—tiny plastic particles less than five millimeters in size. Unlike the popular image of a floating trash island, the patch is more like a cloudy soup of plastic particles suspended throughout the water column. These microplastics come from broken-down consumer products, fishing gear, and industrial waste. Marine animals often mistake these particles for food, leading to starvation and toxicity. Scientists estimate that by 2050, there will be more plastic than fish in the world's oceans by weight.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Great Pacific Garbage Patch forms a solid island where boats can easily land", "The Great Pacific Garbage Patch contains microplastics that endanger marine animals", "The Great Pacific Garbage Patch was found in 1997 and will vanish completely by 2050", "Ocean plastics decompose into safe particles that fish can consume without harm"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone in this passage?", "choices": ["Celebratory", "Indifferent", "Concerned", "Humorous"], "correct": 2},
            {"type": "vocab", "text": "The word 'microplastics' most nearly means", "choices": ["Nets", "Particles", "Gases", "Germs"], "correct": 1},
            {"type": "inference", "text": "Based on the passage, what can be inferred about the future of ocean ecosystems?", "choices": ["They will thrive due to increased nutrients from plastic waste", "They will remain unchanged because plastics are harmless to animals", "They will face serious challenges from ongoing plastic pollution", "They will naturally filter out all plastic contamination within ten years"], "correct": 2},
            {"type": "detail", "text": "According to the passage, when was the Great Pacific Garbage Patch discovered?", "choices": ["1985", "1997", "2003", "2010"], "correct": 1},
            {"type": "purpose", "text": "What is the author's primary purpose in writing this passage?", "choices": ["To entertain readers with a fictional ocean adventure story", "To inform readers about a serious environmental problem", "To persuade readers to stop using all plastic products immediately", "To describe a step-by-step plan for cleaning ocean garbage"], "correct": 1}
        ]
    },
    # nf2 - Short, kept as single paragraph
    {
        "id": "nf2",
        "title": "The Invention of the Printing Press",
        "passage": """Before Johannes Gutenberg invented the printing press around 1440, books were copied by hand, usually by monks in monasteries. This process was extremely slow and expensive, making books rare treasures that only the wealthy could afford. Gutenberg's revolutionary machine used movable metal type that could be arranged and rearranged to print pages quickly. His most famous printed work was the Gutenberg Bible, of which about 180 copies were produced. The printing press sparked an information revolution, allowing knowledge to spread rapidly across Europe. Within fifty years, millions of books were printed, literacy rates began to rise, and ideas about science, religion, and politics spread faster than ever before.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Monks worked very hard copying books in European monasteries before 1440", "Gutenberg's printing press revolutionized how information spread across Europe", "The Gutenberg Bible was the single most important book ever printed in history", "Books remained too expensive for most people to afford before Gutenberg's invention"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward Gutenberg's invention?", "choices": ["Dismissive", "Angry", "Admiring", "Confused"], "correct": 2},
            {"type": "vocab", "text": "The word 'revolutionary' most nearly means", "choices": ["Dangerous", "Costly", "Complex", "Innovative"], "correct": 3},
            {"type": "inference", "text": "What can be inferred about European society before the printing press?", "choices": ["Most people were able to read and write fluently at a young age", "Information and new ideas spread very slowly from place to place", "Books were available to everyone at a low and affordable cost", "Monks were the only people in Europe who knew how to read"], "correct": 1},
            {"type": "detail", "text": "According to the passage, approximately how many copies of the Gutenberg Bible were produced?", "choices": ["90", "120", "150", "180"], "correct": 3},
            {"type": "purpose", "text": "Why did the author include the fact that literacy rates began to rise after the printing press?", "choices": ["To show that printed books became much cheaper than hand-copied manuscripts", "To demonstrate the positive impact of making books more available to people", "To criticize people who remained unable to read even after books became common", "To prove that Gutenberg was a successful businessman who made a large profit"], "correct": 1}
        ]
    },
    # nf3 - Short, kept as single paragraph
    {
        "id": "nf3",
        "title": "The Migration of Monarch Butterflies",
        "passage": """Each year, millions of monarch butterflies embark on an extraordinary journey of up to 3,000 miles from Canada and the northern United States to central Mexico. What makes this migration truly remarkable is that no single butterfly completes the round trip. Instead, it takes three to four generations to complete the annual cycle. The butterflies that return to Mexico in the fall are known as the 'super generation'—they live eight times longer than their parents and possess unique navigational abilities. Scientists believe monarchs use a combination of the sun's position and Earth's magnetic field to find their way. Unfortunately, habitat loss and climate change have reduced monarch populations by 90% in recent decades.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Monarch butterflies migrate each year to escape cold winter weather in the north", "Monarch butterflies have a complex multi-generational migration that faces serious threats", "Scientists have fully explained how monarch butterflies navigate across long distances", "Monarch butterflies are widely considered the most beautiful of all insect species"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone when discussing the monarch population decline?", "choices": ["Optimistic", "Unconcerned", "Alarmed", "Confused"], "correct": 2},
            {"type": "vocab", "text": "The word 'embark' most nearly means", "choices": ["Finish", "Begin", "Cancel", "Delay"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the 'super generation' of monarch butterflies?", "choices": ["They are identical to all other generations of monarch butterflies", "They have special abilities that other generations of monarchs lack", "They cannot fly as far as other generations due to their longer lifespan", "They live in Mexico year-round and do not participate in migration"], "correct": 1},
            {"type": "detail", "text": "According to the passage, how far do monarch butterflies migrate?", "choices": ["1,000 miles", "2,000 miles", "3,000 miles", "4,000 miles"], "correct": 2},
            {"type": "purpose", "text": "Why did the author include information about the 90% population decline?", "choices": ["To celebrate the butterflies' successful adaptation to changing environments", "To raise concern about threats to monarch butterfly survival and habitats", "To prove that butterflies are unimportant to broader natural ecosystems", "To explain why monarchs no longer need to migrate across long distances"], "correct": 1}
        ]
    },
    # nf4 - Short, kept as single paragraph
    {
        "id": "nf4",
        "title": "The Underground Railroad",
        "passage": """The Underground Railroad was not a real railroad but a secret network of routes and safe houses used by enslaved African Americans to escape to free states and Canada. Operating primarily in the decades before the Civil War, this network included brave individuals known as 'conductors,' the most famous being Harriet Tubman, who made 13 missions and rescued over 70 people. Travelers moved at night, guided by the North Star and coded messages in songs and quilts. Safe houses, called 'stations,' were often located in homes, barns, and churches. It is estimated that over 100,000 enslaved people escaped using the Underground Railroad between 1810 and 1850.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Harriet Tubman was the only person who helped enslaved people escape to freedom", "The Underground Railroad was a secret network that helped enslaved people reach freedom", "The Underground Railroad was an actual train system that operated in northern states", "Enslaved people escaped by following real railroad tracks north toward Canada"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's attitude toward the Underground Railroad participants?", "choices": ["Critical", "Respectful", "Confused", "Bored"], "correct": 1},
            {"type": "vocab", "text": "The word 'conductors' most nearly means", "choices": ["Drivers", "Guides", "Singers", "Carpenters"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why escapees traveled at night?", "choices": ["Night air was cooler and more comfortable for walking long distances", "Darkness provided cover to avoid being caught by slave catchers", "The North Star was only visible in the sky during nighttime hours", "All safe houses only welcomed escapees after the sun had set"], "correct": 1},
            {"type": "detail", "text": "According to the passage, approximately how many people did Harriet Tubman rescue?", "choices": ["40", "55", "70", "85"], "correct": 2},
            {"type": "purpose", "text": "What is the author's primary purpose in writing this passage?", "choices": ["To entertain readers with fictional adventure stories about the Civil War era", "To inform readers about an important part of American history and resistance", "To persuade readers to build a new Underground Railroad for modern refugees", "To criticize the individuals who helped enslaved people escape to freedom"], "correct": 1}
        ]
    },
    # nf5 - Short, kept as single paragraph
    {
        "id": "nf5",
        "title": "The Water Cycle",
        "passage": """Earth's water is constantly moving in a process called the water cycle. This cycle has four main stages: evaporation, condensation, precipitation, and collection. When the sun heats water in oceans, lakes, and rivers, it turns into vapor and rises into the air—this is evaporation. As the vapor rises, it cools and turns back into tiny water droplets, forming clouds in a process called condensation. When these droplets become heavy enough, they fall as rain, snow, or hail—precipitation. Finally, the water collects in bodies of water or soaks into the ground, where the cycle begins again. This continuous process has been happening for billions of years and provides fresh water for all life on Earth.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The water cycle has several stages including evaporation and condensation", "The water cycle is a continuous process that provides fresh water for living things", "Rain is the most important part of the water cycle for human survival", "The water cycle only takes place in oceans and large bodies of salt water"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone in this passage?", "choices": ["Excited", "Neutral", "Skeptical", "Humorous"], "correct": 1},
            {"type": "vocab", "text": "The word 'precipitation' most nearly means", "choices": ["Soaking", "Evaporation", "Rainfall", "Condensation"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about what would happen if the sun stopped heating Earth's water?", "choices": ["The water cycle would continue exactly as it has for billions of years", "Evaporation would stop and the water cycle would be severely disrupted", "More rain would fall than ever before due to cooler temperatures", "All water on Earth would instantly freeze into solid ice"], "correct": 1},
            {"type": "detail", "text": "According to the passage, how many main stages does the water cycle have?", "choices": ["Two", "Three", "Four", "Five"], "correct": 2},
            {"type": "purpose", "text": "Why did the author write this passage?", "choices": ["To explain a natural process that sustains life on planet Earth", "To persuade readers to conserve water in their daily lives", "To entertain with a fictional story about a traveling raindrop", "To criticize how humans currently use and waste water resources"], "correct": 0}
        ]
    },
    # nf6 - Long, split into 2 paragraphs
    {
        "id": "nf6",
        "title": "The Discovery of Penicillin",
        "passage": """In September 1928, Scottish bacteriologist Alexander Fleming returned to his laboratory at St. Mary's Hospital in London after a month-long vacation. Before leaving, he had stacked several petri dishes containing Staphylococcus bacteria on a bench near an open window. When Fleming sorted through the dishes to discard contaminated ones, he noticed something unusual: on one dish, a mold called Penicillium notatum had grown, and the bacteria surrounding the mold had been destroyed. Rather than throwing the dish away, Fleming became curious. He cultured the mold and discovered that it produced a substance that killed several disease-causing bacteria. He named this substance 'penicillin.' However, Fleming struggled to purify penicillin in large quantities, and his work was largely forgotten for a decade.

In 1939, Australian scientist Howard Florey and German-born biochemist Ernst Chain rediscovered Fleming's research and developed methods to mass-produce penicillin. By 1945, penicillin was being widely used to treat infected wounds in soldiers during World War II, saving countless lives. That same year, Fleming, Florey, and Chain shared the Nobel Prize in Medicine. Penicillin became the first antibiotic, revolutionizing medicine and proving that even accidental discoveries can change the world.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Alexander Fleming discovered penicillin by accident, and later scientists developed it into a life-saving antibiotic", "Penicillin was the only antibiotic ever discovered in the 20th century by medical researchers", "World War II soldiers were the first people to benefit from any form of medical treatment", "Alexander Fleming won a Nobel Prize for his careful planning and laboratory organization skills"], "correct": 0},
            {"type": "tone", "text": "Which word best describes the author's tone toward Fleming's discovery?", "choices": ["Dismissive", "Celebratory", "Sarcastic", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The word 'bacteriologist' most nearly means", "choices": ["Doctor", "Scientist", "Chemist", "Researcher"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why Fleming's work was 'largely forgotten for a decade'?", "choices": ["He intentionally hid his research from other scientists to maintain secrecy", "He could not produce penicillin in large enough quantities to be practical", "Other scientists had already discovered better antibiotics that worked faster", "The Nobel Prize committee deliberately ignored his work for many years"], "correct": 1},
            {"type": "detail", "text": "According to the passage, who helped mass-produce penicillin?", "choices": ["Fleming alone", "Florey and Chain", "Hospital staff", "Army doctors"], "correct": 1},
            {"type": "purpose", "text": "Why did the author include the detail about the open window?", "choices": ["To criticize Fleming's poor laboratory safety practices and habits", "To explain how the mold likely entered the petri dish by accident", "To prove that Fleming was a careless scientist who made many errors", "To suggest that fresh air from outside is what kills bacteria"], "correct": 1}
        ]
    },
    # nf7 - Long, split into 2 paragraphs
    {
        "id": "nf7",
        "title": "The Great Wall of China",
        "passage": """Stretching over 13,000 miles, the Great Wall of China is the longest structure ever built by humans. Contrary to popular belief, the wall cannot be seen from space with the naked eye, but its historical significance remains immense. Construction began as early as the 7th century BCE, when various Chinese states built walls to protect against northern invaders. In 221 BCE, Emperor Qin Shi Huang connected and extended these walls into a unified defensive system. Most of the existing wall today was built during the Ming Dynasty (1368–1644), using stone, brick, and rammed earth. The wall includes watchtowers, barracks, and beacon towers for signaling.

Over 1 million workers—including soldiers, peasants, and prisoners—died building it, leading some to call it 'the longest cemetery on Earth.' Despite its massive scale, the wall was never completely effective at preventing invasions; nomadic armies repeatedly breached it. Today, the Great Wall is a UNESCO World Heritage Site and one of the most visited tourist attractions globally, though large sections have crumbled due to erosion and human activity.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Great Wall of China was a perfect defensive structure that never failed to stop invaders", "The Great Wall is a massive, historically significant structure built over centuries, though it was not completely effective", "Emperor Qin Shi Huang single-handedly built the entire Great Wall without any help from workers", "The Great Wall is clearly visible from outer space without using any special equipment"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone when discussing the wall's effectiveness?", "choices": ["Exaggerated", "Balanced", "Dismissive", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'breached' most nearly means", "choices": ["Built", "Repaired", "Entered", "Admired"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about why the wall is called 'the longest cemetery on Earth'?", "choices": ["Many workers died during its long and difficult construction", "It was built directly on top of ancient graves and burial grounds", "It contains the tombs of several Chinese emperors and their families", "Tourists frequently die there due to dangerous climbing conditions"], "correct": 0},
            {"type": "detail", "text": "During which dynasty was most of the existing wall built?", "choices": ["Qin Dynasty", "Ming Dynasty", "Han Dynasty", "Song Dynasty"], "correct": 1},
            {"type": "purpose", "text": "Why did the author mention that the wall cannot be seen from space?", "choices": ["To correct a common misconception about the wall's visibility", "To prove that the wall is not as impressive as people believe", "To argue against spending money on space exploration programs", "To show that astronauts have poor vision without telescopes"], "correct": 0}
        ]
    },
    # nf8 - Long, split into 2 paragraphs
    {
        "id": "nf8",
        "title": "Coral Bleaching: The Oceans' Warning Sign",
        "passage": """Coral reefs, often called the 'rainforests of the sea,' support about 25% of all marine species despite covering less than 1% of the ocean floor. These vibrant ecosystems depend on a symbiotic relationship between coral polyps and microscopic algae called zooxanthellae. The algae live inside the coral tissue, providing up to 90% of the coral's energy through photosynthesis, while the coral gives the algae a protected home. When ocean temperatures rise even 1–2 degrees Celsius above normal, the coral becomes stressed and expels the algae. Without the algae, the coral loses its main food source and turns white—a process called coral bleaching. Bleached corals are not dead immediately, but they are starving and vulnerable to disease. If temperatures return to normal quickly, corals can recover. However, prolonged warming leads to mass die-offs.

Major bleaching events have increased dramatically since the 1980s, driven by climate change. The 2016 bleaching event on Australia's Great Barrier Reef killed nearly 30% of shallow-water corals. Scientists warn that without urgent action to reduce carbon emissions, most of the world's coral reefs could disappear by 2050, devastating marine biodiversity and the millions of people who depend on reefs for food and tourism income.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Coral reefs are beautiful but ultimately unimportant to overall ocean health", "Rising ocean temperatures cause coral bleaching, threatening marine ecosystems and human communities", "Zooxanthellae are harmful parasites that damage coral reefs and should be removed", "The Great Barrier Reef has fully recovered from all bleaching events and is now healthy"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone in this passage?", "choices": ["Playful", "Urgent", "Angry", "Neutral"], "correct": 1},
            {"type": "vocab", "text": "The word 'symbiotic' most nearly means", "choices": ["Harmful", "Helpful", "Competitive", "Independent"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why bleached corals are described as 'starving'?", "choices": ["They refuse to eat any other food sources available in the water", "They have lost the algae that provided most of their energy", "Ocean warming destroys all food particles in the surrounding water", "Other fish and animals steal all available food from the corals"], "correct": 1},
            {"type": "detail", "text": "According to the passage, what percentage of shallow-water corals died on the Great Barrier Reef in 2016?", "choices": ["10%", "20%", "30%", "40%"], "correct": 2},
            {"type": "purpose", "text": "Why did the author call coral reefs the 'rainforests of the sea'?", "choices": ["To emphasize their biodiversity and ecological importance to the ocean", "To suggest that coral grows on underwater trees like leaves on branches", "To confuse readers with a misleading metaphor about forest ecosystems", "To argue that coral reefs should be protected just like rainforests"], "correct": 0}
        ]
    },
    # nf9 - Long, split into 2 paragraphs
    {
        "id": "nf9",
        "title": "The Rosetta Stone: Cracking Ancient Egyptian Code",
        "passage": """In July 1799, French soldiers digging the foundations of a fort near the town of Rosetta (modern-day Rashid), Egypt, uncovered a large black granite slab inscribed with text. The stone, now known as the Rosetta Stone, contained three distinct scripts: ancient Greek, Demotic (a later Egyptian script), and hieroglyphics. Scholars could already read Greek, so they realized the stone held the key to deciphering Egyptian hieroglyphics—a script that had been unreadable for nearly 1,400 years. The stone dated back to 196 BCE and recorded a decree issued by Egyptian priests honoring Pharaoh Ptolemy V. After Napoleon's defeat, the British seized the stone and transported it to the British Museum in London, where it remains today.

Deciphering the stone proved extremely difficult. English scientist Thomas Young made initial progress by identifying proper names. However, it was French scholar Jean-François Champollion who cracked the code in 1822. By comparing the Greek names with the hieroglyphic versions, Champollion realized that hieroglyphics represented sounds, not just ideas or objects. He identified phonetic characters and essentially created an Egyptian alphabet. His breakthrough unlocked thousands of years of Egyptian history, allowing modern readers to understand temple inscriptions, tomb writings, and papyrus scrolls that had been silent for centuries.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Rosetta Stone was carved by French soldiers in 1799 as a military monument", "The Rosetta Stone contained three identical scripts that were all easy to read", "The Rosetta Stone enabled scholars to decipher Egyptian hieroglyphics, unlocking ancient history", "Champollion discovered the Rosetta Stone in Egypt and kept it in France for study"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the author's attitude toward Champollion's achievement?", "choices": ["Dismissive", "Admiring", "Jealous", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'deciphering' most nearly means", "choices": ["Destroying", "Copying", "Decoding", "Hiding"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about why hieroglyphics had been unreadable for 1,400 years?", "choices": ["No one had found any surviving examples of hieroglyphic writing anywhere", "The knowledge of how to read and understand them had been lost over time", "Hieroglyphics were intentionally erased from all Egyptian monuments", "Scholars were not interested in ancient Egypt until the 1800s"], "correct": 1},
            {"type": "detail", "text": "What year did Champollion decipher the hieroglyphics?", "choices": ["1799", "1822", "1850", "1901"], "correct": 1},
            {"type": "purpose", "text": "Why did the author include the information about Young and Champollion?", "choices": ["To show that multiple scholars contributed to deciphering the stone's code", "To prove that English scientists were smarter than French scientists", "To argue that the Rosetta Stone should have stayed in Egypt permanently", "To criticize how slowly scholars worked without modern technology"], "correct": 0}
        ]
    },
    # nf10 - Long, split into 3 paragraphs
    {
        "id": "nf10",
        "title": "The Science of Sleep: Why We Need Rest",
        "passage": """Every living creature with a nervous system sleeps, yet scientists are still discovering exactly why. Sleep is not simply a period of rest; it is an active, essential biological process. During sleep, the brain cycles through several stages every 90 minutes, alternating between non-REM (rapid eye movement) and REM sleep. Non-REM sleep includes deep sleep, during which the body repairs tissues, strengthens the immune system, and releases growth hormones. REM sleep, when most vivid dreaming occurs, plays a critical role in memory consolidation and emotional regulation.

The consequences of insufficient sleep are severe. Adults who regularly sleep less than seven hours per night face higher risks of obesity, heart disease, diabetes, and depression. In children and teenagers, chronic sleep loss impairs learning, attention, and emotional stability. The body's internal clock, or circadian rhythm, regulates sleep-wake cycles based on light exposure. Exposure to blue light from phones and computers at night disrupts this rhythm by suppressing melatonin, the hormone that induces sleepiness.

Scientists recommend maintaining consistent sleep schedules, avoiding caffeine late in the day, and creating a dark, cool bedroom environment. Despite these known benefits, modern society often treats sleep as optional or even wasteful. However, accumulating research shows that sacrificing sleep for productivity ultimately backfires: well-rested people think more clearly, react faster, and perform better on nearly every cognitive task.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Sleep is a waste of time that productive people should try to minimize", "Sleep is an essential biological process with specific stages that support health and cognition", "Only humans and other large mammals need to sleep for proper brain function", "REM sleep is the only important stage of the sleep cycle for memory"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward people who sacrifice sleep?", "choices": ["Supportive", "Warning", "Amused", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The word 'circadian' most nearly means", "choices": ["Daily", "Weekly", "Monthly", "Yearly"], "correct": 0},
            {"type": "inference", "text": "What can be inferred about blue light from phones and computers?", "choices": ["It helps people fall asleep faster by calming the brain", "It disrupts melatonin production, making it harder to sleep", "It has no measurable effect on the human sleep cycle", "It only affects children's sleep patterns, not adults"], "correct": 1},
            {"type": "detail", "text": "According to the passage, what health risks increase with less than seven hours of sleep?", "choices": ["Only depression and anxiety disorders", "Obesity, heart disease, diabetes, and depression", "Broken bones and muscle pain from fatigue", "Hair loss and poor vision over time"], "correct": 1},
            {"type": "purpose", "text": "Why did the author state that 'sacrificing sleep for productivity ultimately backfires'?", "choices": ["To convince readers that sleep is actually important for good performance", "To encourage people to work more hours and sleep less each night", "To argue that sleep has no proven benefits for cognitive abilities", "To prove that all successful people sleep very few hours nightly"], "correct": 0}
        ]
    },
    # nf11 - Long, split into 2 paragraphs
    {
        "id": "nf11",
        "title": "The Eruption of Mount Vesuvius, 79 CE",
        "passage": """On August 24, 79 CE, the Roman cities of Pompeii and Herculaneum were thriving commercial centers near the Bay of Naples. Few residents knew that the mountain looming above them, Mount Vesuvius, was a volcano—volcanoes were not yet understood in the ancient world. At approximately 1:00 PM, Vesuvius erupted violently, sending a mushroom cloud of ash, pumice, and toxic gases over 20 miles into the sky. The eruption lasted over 24 hours. Pompeii, located about 6 miles from the volcano, was buried under 13 to 20 feet of volcanic ash and pumice. Herculaneum, even closer, was destroyed by pyroclastic flows—superheated waves of gas and debris moving at over 50 miles per hour. The pyroclastic flows reached temperatures of about 500°C (930°F), instantly killing anyone in their path. An estimated 2,000 people died in Pompeii alone, though many had already fled.

The cities were completely lost for nearly 1,700 years until their rediscovery in the 18th century. Excavations revealed remarkably preserved buildings, artifacts, and even plaster casts of human bodies frozen in their final moments. These discoveries provide an unparalleled snapshot of daily Roman life—from food in market stalls to graffiti on walls. Today, Vesuvius remains an active volcano, and nearly 3 million people live within dangerous proximity. Geologists warn that another major eruption is inevitable, though not immediately imminent.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Mount Vesuvius erupted in 79 CE, destroying Pompeii and Herculaneum but preserving a unique record of Roman life", "All Roman cities located near the Bay of Naples were destroyed by volcanoes in 79 CE", "The residents of Pompeii were foolish not to evacuate before the volcanic eruption occurred", "Mount Vesuvius has been completely dormant since 79 CE and will never erupt again"], "correct": 0},
            {"type": "tone", "text": "Which word best describes the author's tone when describing the destruction?", "choices": ["Humorous", "Factual", "Celebratory", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'pyroclastic' most nearly means", "choices": ["Slow", "Hot", "Wet", "Solid"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the cities were so well preserved?", "choices": ["People intentionally buried them to protect them from invaders", "The volcanic ash and debris covered and sealed them quickly", "The Romans built the cities to survive volcanic eruptions", "The cities were made entirely of metal and stone materials"], "correct": 1},
            {"type": "detail", "text": "Approximately how many people died in Pompeii according to the passage?", "choices": ["500", "1,000", "2,000", "5,000"], "correct": 2},
            {"type": "purpose", "text": "Why did the author mention the plaster casts of human bodies?", "choices": ["To shock readers with overly gruesome and disturbing details", "To show how the eruption preserved evidence of ancient life", "To prove that no single person survived the volcanic eruption", "To argue that the bodies should not be displayed in museums"], "correct": 1}
        ]
    },
    # nf12 - Long, split into 3 paragraphs
    {
        "id": "nf12",
        "title": "The Amazon Rainforest: Lungs of the Planet",
        "passage": """Spanning over 2.7 million square miles across nine South American countries, the Amazon rainforest is the largest tropical rainforest on Earth. It produces approximately 20% of the world's oxygen, earning its nickname 'the lungs of the planet.' However, recent scientific research suggests that the Amazon actually consumes nearly as much oxygen as it produces through respiration, making the 'lungs' label somewhat misleading. More accurately, the Amazon is an enormous carbon sink: its trees store about 100 billion metric tons of carbon, equivalent to roughly 10 years of global fossil fuel emissions.

The forest supports extraordinary biodiversity. One in ten known species on Earth lives in the Amazon, including over 40,000 plant species, 1,300 bird species, 3,000 fish species, and 2.5 million insect species. Indigenous peoples have lived in the Amazon for at least 11,000 years, with over 400 tribes currently residing there, some completely uncontacted by modern society.

Deforestation poses the greatest threat to the Amazon. Since 1978, over 289,000 square miles—an area larger than Texas—have been cleared primarily for cattle ranching and soybean farming. Deforestation releases stored carbon into the atmosphere, accelerates climate change, and destroys habitats. Scientists warn that the Amazon is approaching a 'tipping point' where it could transition from rainforest to dry savanna, a shift that would have catastrophic global consequences.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Amazon rainforest is a small forest with very few plant and animal species", "The Amazon is a massive, biodiverse ecosystem that stores carbon and faces serious deforestation threats", "Deforestation in the Amazon only affects local animals, not the global climate", "The Amazon produces all of the world's oxygen and has no environmental problems"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone regarding deforestation?", "choices": ["Optimistic", "Alarmed", "Celebratory", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The word 'sink' most nearly means", "choices": ["Hole", "Store", "Drain", "Source"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the 'lungs of the planet' nickname is somewhat misleading?", "choices": ["The Amazon produces no oxygen at all despite what people believe", "The Amazon consumes nearly as much oxygen as it produces through respiration", "Only scientists are allowed to use that nickname in published research", "The nickname was invented by a child and has no scientific basis"], "correct": 1},
            {"type": "detail", "text": "According to the passage, how many indigenous tribes currently live in the Amazon?", "choices": ["40", "200", "400", "800"], "correct": 2},
            {"type": "purpose", "text": "Why did the author mention the 'tipping point' where the Amazon could become savanna?", "choices": ["To warn readers that deforestation could cause irreversible damage to the ecosystem", "To suggest that savannas are better ecosystems than rainforests for biodiversity", "To claim that climate change is a hoax and not something to worry about", "To argue that the Amazon should be cut down intentionally for farmland"], "correct": 0}
        ]
    },
    # nf13 - Long, split into 3 paragraphs
    {
        "id": "nf13",
        "title": "The Cold War: A Half-Century of Tension",
        "passage": """Following World War II, the United States and the Soviet Union emerged as the world's two superpowers, but their political and economic systems could not have been more different. The United States promoted democracy and capitalism, while the Soviet Union enforced communist rule and a command economy. This ideological clash sparked the Cold War, a period of intense geopolitical tension from roughly 1947 to 1991. The term 'cold' war was used because the two superpowers never directly fought each other in a conventional war. Instead, they engaged in proxy wars—supporting opposing sides in conflicts in Korea, Vietnam, Afghanistan, and elsewhere.

Both nations amassed enormous nuclear arsenals, creating a doctrine called 'Mutually Assured Destruction' (MAD): if either side launched a nuclear attack, the other would retaliate, ensuring total destruction for both. Paradoxically, this terrifying balance prevented direct war. The Cold War also included the Space Race, as each nation sought to demonstrate technological superiority. The Soviets launched Sputnik, the first satellite, in 1957; the Americans landed astronauts on the moon in 1969. The arms race and proxy conflicts cost trillions of dollars and millions of lives.

The Cold War finally ended when the Soviet Union collapsed in 1991, largely due to economic stagnation and political reforms led by Mikhail Gorbachev. The end of the Cold War reshaped global politics, but its legacy—including leftover nuclear weapons and regional instability—persists today.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The United States won the Cold War easily without any major problems or costs", "The Cold War was a long period of tension between the US and Soviet Union, fought through proxies and nuclear threats", "The Soviet Union was always more powerful than the United States during the Cold War period", "The Cold War only involved space exploration, not military conflict or politics"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward the doctrine of Mutually Assured Destruction?", "choices": ["Celebratory", "Terrified", "Confused", "Humorous"], "correct": 1},
            {"type": "vocab", "text": "The word 'proxy' most nearly means", "choices": ["Direct", "Substitute", "Nuclear", "Peaceful"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the Cold War never became a direct war between the US and USSR?", "choices": ["Both countries were close allies and close friends after World War II", "The doctrine of Mutually Assured Destruction made direct war too dangerous", "The United Nations banned both countries from fighting each other", "Neither country had any weapons after World War II ended"], "correct": 1},
            {"type": "detail", "text": "In what year did the Soviet Union collapse?", "choices": ["1947", "1969", "1991", "2001"], "correct": 2},
            {"type": "purpose", "text": "Why did the author include the Space Race in this passage?", "choices": ["To show that the Cold War included competition beyond just military conflict", "To argue that space exploration was the main cause of the Cold War", "To prove that the Soviet Union won the Cold War due to space achievements", "To suggest that space exploration was irrelevant to Cold War tensions"], "correct": 0}
        ]
    },
    # nf14 - Long, split into 2 paragraphs
    {
        "id": "nf14",
        "title": "Photosynthesis: The Basis of Life on Earth",
        "passage": """Nearly all life on Earth depends on a single chemical process: photosynthesis. This process, performed by plants, algae, and some bacteria, converts light energy from the sun into chemical energy stored in sugars. The overall equation appears simple: six molecules of carbon dioxide plus six molecules of water, in the presence of sunlight and chlorophyll, produce one molecule of glucose and six molecules of oxygen. However, the actual process involves two complex stages: the light-dependent reactions and the Calvin cycle (light-independent reactions). In the light-dependent reactions, chlorophyll absorbs sunlight and uses that energy to split water molecules, releasing oxygen as a byproduct and generating energy-carrying molecules called ATP and NADPH. The Calvin cycle then uses ATP and NADPH to convert carbon dioxide from the atmosphere into glucose, which plants use for growth and energy.

Photosynthesis not only feeds plants but also produces the oxygen that animals—including humans—breathe. It also removes carbon dioxide from the atmosphere, helping regulate Earth's climate. Scientists estimate that photosynthetic organisms produce about 170 billion tons of organic matter annually. Without photosynthesis, Earth's atmosphere would contain almost no oxygen, and complex life would not exist. Understanding photosynthesis has allowed humans to improve crop yields, develop biofuels, and even inspire technologies like solar cells that mimic natural energy capture.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Photosynthesis is a simple process that only happens in science laboratories", "Photosynthesis is a complex, two-stage process that converts sunlight into chemical energy and produces oxygen", "Plants do not need sunlight to survive and can perform photosynthesis in darkness", "Photosynthesis only produces oxygen for animals, not food for the plants themselves"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward photosynthesis?", "choices": ["Dismissive", "Admiring", "Angry", "Humorous"], "correct": 1},
            {"type": "vocab", "text": "The word 'chlorophyll' most nearly means", "choices": ["Sugar", "Pigment", "Waste", "Gas"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about what would happen if photosynthesis stopped?", "choices": ["Nothing on Earth would change in any noticeable way", "Oxygen levels would drop and most life would eventually die", "Plants would grow faster without having to produce energy", "Animals would learn to perform photosynthesis instead of plants"], "correct": 1},
            {"type": "detail", "text": "According to the passage, what two stages make up photosynthesis?", "choices": ["Daytime and nighttime reactions", "Light-dependent reactions and the Calvin cycle", "Oxygen production and carbon destruction", "Glucose splitting and water combining"], "correct": 1},
            {"type": "purpose", "text": "Why did the author mention that scientists have developed solar cells inspired by photosynthesis?", "choices": ["To show that understanding natural processes can lead to useful technologies", "To argue that solar cells are better than plants at capturing energy", "To prove that photosynthesis is an outdated and inefficient process", "To confuse readers with irrelevant information about technology"], "correct": 0}
        ]
    },
    # nf15 - Long, split into 3 paragraphs
    {
        "id": "nf15",
        "title": "The Harlem Renaissance: A Cultural Explosion",
        "passage": """In the 1920s and early 1930s, the Harlem neighborhood of New York City became the epicenter of a remarkable cultural movement known as the Harlem Renaissance. This period saw an unprecedented flowering of African American literature, music, art, and intellectual thought. The Great Migration had brought hundreds of thousands of African Americans from the rural South to northern cities like New York, Chicago, and Detroit, seeking better economic opportunities and fleeing racial violence. Harlem, in particular, became a magnet for Black artists and thinkers.

Writers such as Langston Hughes, Zora Neale Hurston, and Claude McKay produced poetry, novels, and essays that celebrated Black identity and explored the African American experience. Hughes's poems, including 'The Negro Speaks of Rivers,' used jazz and blues rhythms to create a distinctive literary voice. Musicians like Duke Ellington, Louis Armstrong, and Bessie Smith transformed American music, developing jazz into a sophisticated art form that gained international acclaim. Visual artists including Aaron Douglas created paintings and murals inspired by African art and modernism.

The movement was not just artistic; it was intellectual. Scholars like W.E.B. Du Bois and Alain Locke argued for racial pride and full citizenship rights. While the Harlem Renaissance faded after the Great Depression, its influence endured. It challenged racist stereotypes, established African American culture as central to American identity, and paved the way for the Civil Rights Movement decades later.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Harlem Renaissance was a small, unimportant art movement in New York City", "The Harlem Renaissance was a major cultural movement of African American arts and ideas that reshaped American culture", "Only writers participated in the Harlem Renaissance; musicians and artists were not involved", "The Harlem Renaissance occurred in the 1950s during the Civil Rights Movement"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's attitude toward the Harlem Renaissance?", "choices": ["Dismissive", "Celebratory", "Confused", "Critical"], "correct": 1},
            {"type": "vocab", "text": "The word 'unprecedented' most nearly means", "choices": ["Minor", "New", "Boring", "Accidental"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why Harlem became a center for Black artists?", "choices": ["The government forced all Black artists to move to Harlem against their will", "The Great Migration brought many African Americans north, and Harlem became a cultural hub", "No other American cities allowed Black artists to work or perform publicly", "Harlem was chosen randomly by a group of artists who met by chance"], "correct": 1},
            {"type": "detail", "text": "According to the passage, which poet used jazz and blues rhythms in his work?", "choices": ["Hurston", "McKay", "Hughes", "Du Bois"], "correct": 2},
            {"type": "purpose", "text": "Why did the author include the effects of the Harlem Renaissance on the Civil Rights Movement?", "choices": ["To show that the movement had lasting historical importance beyond the 1920s", "To argue that art has no impact on politics or social change", "To prove that the Civil Rights Movement failed to achieve its goals", "To criticize the Harlem Renaissance for not doing enough for equality"], "correct": 0}
        ]
    },
    # nf16 - Long, split into 2 paragraphs
    {
        "id": "nf16",
        "title": "The Theory of Plate Tectonics",
        "passage": """Earth's surface is not a solid, unbroken shell. Instead, it consists of about 15 major tectonic plates—massive slabs of solid rock that float on the partially molten layer beneath them called the asthenosphere. The theory of plate tectonics, which became widely accepted by geologists in the 1960s, describes how these plates move, interact, and reshape Earth's surface. Plates move incredibly slowly, typically 1 to 10 centimeters per year—about the speed at which fingernails grow. However, over millions of years, this creeping movement produces dramatic results. Where plates diverge (move apart), magma rises to create new crust, forming mid-ocean ridges and rift valleys. Where plates converge (collide), one plate may subduct (sink beneath) the other, creating deep ocean trenches and volcanic mountain ranges like the Andes. When two continental plates collide, neither subducts easily; instead, they crumple to form massive mountain ranges like the Himalayas, which are still rising today as India pushes into Asia.

Where plates slide past each other horizontally, they create transform faults—the San Andreas Fault in California is a famous example. These sliding movements often trigger earthquakes. Plate tectonics explains not only earthquakes and volcanoes but also the distribution of fossils, the matching shapes of continents (like South America and Africa), and the locations of mineral deposits. Without plate motion, Earth would likely lack its protective magnetic field and might resemble the geologically dead planet Mars.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Earth's surface is completely solid and never changes over time", "Plate tectonics explains how slow-moving plates cause earthquakes, volcanoes, and mountain formation", "Only geologists care about tectonic plates and their movements", "Earthquakes are random events with no scientific explanation"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone in this passage?", "choices": ["Humorous", "Educational", "Angry", "Bored"], "correct": 1},
            {"type": "vocab", "text": "The word 'subduct' most nearly means", "choices": ["Rise", "Sink", "Split", "Freeze"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the Himalayas are still rising?", "choices": ["The Indian plate continues to push into the Asian plate over time", "The mountains are made of inflatable rock that expands when heated", "Volcanoes are constantly adding new lava to the mountain tops", "Humans are building them higher with construction equipment"], "correct": 0},
            {"type": "detail", "text": "According to the passage, how fast do tectonic plates typically move?", "choices": ["1-10 cm per year", "1-10 m per year", "1-10 km per year", "They do not move"], "correct": 0},
            {"type": "purpose", "text": "Why did the author compare Earth to Mars?", "choices": ["To suggest that humans should move to Mars for better living conditions", "To emphasize that plate tectonics may be essential for a planet to remain geologically active", "To prove that Mars once had life but lost it due to volcanic activity", "To show that Earth is completely different from all other planets"], "correct": 1}
        ]
    },
    # nf17 - Long, split into 3 paragraphs
    {
        "id": "nf17",
        "title": "The Industrial Revolution: Transforming Society",
        "passage": """Beginning in Great Britain around 1760 and spreading across Europe and North America by the mid-19th century, the Industrial Revolution fundamentally changed how humans produced goods, worked, and lived. Before industrialization, most people lived in rural agricultural communities, making goods by hand at home or in small workshops. The revolution introduced several key innovations: the steam engine (improved by James Watt), mechanical textile machines (spinning jenny, power loom), iron production techniques, and eventually electricity and the internal combustion engine. These technologies enabled factories to produce goods faster, cheaper, and in larger quantities than ever before.

The effects were profound and contradictory. On the positive side, industrialization created new jobs, increased overall wealth, improved transportation (railroads and steamships), and eventually raised living standards. Many consumer goods became affordable to ordinary people for the first time. However, the early Industrial Revolution also brought severe problems. Factory workers—including young children—labored 12 to 16 hours daily in dangerous conditions for low wages. Cities grew explosively but lacked sanitation or adequate housing, leading to disease outbreaks. Air and water pollution reached unprecedented levels.

Social reformers like Charles Dickens highlighted these injustices, and gradually labor laws, unions, and public health measures emerged. By the late 19th century, a growing middle class formed, but vast economic inequality persisted. The Industrial Revolution set the stage for modern capitalism, urbanization, and environmental challenges that the world still grapples with today.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Industrial Revolution only had negative effects on human society", "The Industrial Revolution brought both positive advances and serious problems that reshaped society", "Industrialization began in the United States in 1900, not in Great Britain", "The Industrial Revolution had no effect on how people lived or worked"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's treatment of the Industrial Revolution?", "choices": ["One-sided", "Balanced", "Critical", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'unprecedented' most nearly means", "choices": ["Minor", "Record", "Solvable", "Intentional"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why children worked in factories during the early Industrial Revolution?", "choices": ["Children preferred working to going to school at that time", "There were few labor laws, and factory owners wanted cheap labor", "No adults were available to work in the factories", "Children were stronger than adults for factory work"], "correct": 1},
            {"type": "detail", "text": "According to the passage, who improved the steam engine?", "choices": ["Dickens", "Watt", "Marx", "Bell"], "correct": 1},
            {"type": "purpose", "text": "Why did the author mention Charles Dickens?", "choices": ["To show that some writers criticized the negative effects of industrialization", "To argue that Charles Dickens supported child labor in factories", "To prove that all writers ignored industrial problems at that time", "To suggest that Charles Dickens invented the steam engine"], "correct": 0}
        ]
    },
    # nf18 - Long, split into 3 paragraphs
    {
        "id": "nf18",
        "title": "Vaccines: How They Work and Why They Matter",
        "passage": """Before the development of vaccines, infectious diseases like smallpox, polio, measles, and whooping cough killed or disabled millions of people annually. Vaccines have since saved more lives than any medical intervention except clean drinking water. The basic principle of vaccination is remarkably simple and elegant. When a pathogen—a virus or bacterium—enters the body, the immune system typically takes several days to recognize and mount a response. During that delay, the pathogen can multiply and cause severe illness. Vaccines work by exposing the immune system to a harmless version of a pathogen (or pieces of it) so that the immune system learns to recognize and destroy the real pathogen quickly. This creates immunological memory.

The first true vaccine was developed by Edward Jenner in 1796. Jenner observed that milkmaids who caught cowpox, a mild disease, did not catch deadly smallpox. He deliberately infected a boy with cowpox, then exposed him to smallpox—the boy remained healthy. The word 'vaccine' comes from 'vacca,' Latin for cow, referring to cowpox. In the 20th century, scientists like Jonas Salk and Albert Sabin developed polio vaccines, nearly eradicating polio worldwide.

Vaccination relies on herd immunity: when enough people are vaccinated, the disease cannot spread easily, protecting even those who cannot be vaccinated (infants, allergic individuals). Despite overwhelming scientific evidence, vaccine hesitancy—often based on a debunked 1998 study falsely linking vaccines to autism—has led to outbreaks of previously controlled diseases. The World Health Organization now considers vaccine hesitancy a top global health threat.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Vaccines are unnecessary because most infectious diseases are completely harmless", "Vaccines train the immune system to recognize pathogens, have saved millions of lives, and face modern hesitancy", "Edward Jenner invented vaccines in the year 2020, not in the 18th century", "Vaccines only work for smallpox and cannot prevent other diseases"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward vaccine hesitancy?", "choices": ["Supportive", "Alarmed", "Celebratory", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The word 'pathogen' most nearly means", "choices": ["Vaccine", "Germ", "Antibody", "Toxin"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about what happened to smallpox due to vaccination?", "choices": ["It was completely eradicated (eliminated worldwide)", "It became more dangerous and deadly over time", "It still kills millions of people every single year", "Vaccines had no effect on smallpox transmission"], "correct": 0},
            {"type": "detail", "text": "What year did Edward Jenner develop the first vaccine?", "choices": ["1696", "1796", "1896", "1996"], "correct": 1},
            {"type": "purpose", "text": "Why did the author mention the debunked 1998 study on vaccines and autism?", "choices": ["To argue that the study was correct and vaccines are dangerous", "To explain the origin of modern vaccine hesitancy", "To prove that scientists never make mistakes in research", "To suggest that autism is caused by something else entirely"], "correct": 1}
        ]
    },
    # nf19 - Long, split into 3 paragraphs
    {
        "id": "nf19",
        "title": "The Search for Exoplanets",
        "passage": """For most of human history, astronomers could only speculate whether planets existed beyond our solar system. The first confirmed detection of an exoplanet—a planet orbiting another star—came in 1992, when astronomers discovered two planets orbiting a pulsar. In 1995, Swiss astronomers Michel Mayor and Didier Queloz found 51 Pegasi b, the first exoplanet orbiting a sun-like star. This discovery earned them a Nobel Prize. Since then, exoplanet research has exploded. NASA's Kepler Space Telescope (launched 2009) and Transiting Exoplanet Survey Satellite (TESS, launched 2018) have identified over 5,000 confirmed exoplanets, with thousands more candidates awaiting confirmation.

Most exoplanets are detected using two primary methods: the transit method and the radial velocity method. The transit method observes a star's brightness; if a planet passes in front of the star, it dims slightly and periodically. The radial velocity method detects tiny wobbles in a star's motion caused by an orbiting planet's gravitational pull. The ultimate goal of exoplanet research is to find potentially habitable worlds—planets with conditions that might support life.

Scientists focus on the 'habitable zone' (or 'Goldilocks zone'), the region around a star where temperatures could allow liquid water to exist. Some promising candidates include the TRAPPIST-1 system (seven Earth-sized planets, three in the habitable zone) and Proxima Centauri b (orbiting the nearest star to our Sun). Future telescopes, including the James Webb Space Telescope and the planned Habitable Worlds Observatory, will analyze exoplanet atmospheres for biosignature gases like oxygen and methane that could indicate life.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Exoplanets are impossible to detect with current telescope technology", "Astronomers have discovered over 5,000 exoplanets using methods like transit and radial velocity, and are now searching for habitable worlds", "Only one exoplanet has ever been found, and it orbits our own Sun", "Exoplanets are all exactly like Earth with similar atmospheres"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward exoplanet discoveries?", "choices": ["Bored", "Excited", "Skeptical", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'exoplanet' most nearly means", "choices": ["Moon", "Star", "World", "Comet"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about why the 'habitable zone' is also called the 'Goldilocks zone'?", "choices": ["Because it is too hot, too cold, or just right for liquid water", "Because a famous astronomer named Goldilocks discovered it", "Because it contains bowls of porridge floating in space", "Because only bears and other large mammals can live there"], "correct": 0},
            {"type": "detail", "text": "In what year was the first exoplanet orbiting a sun-like star discovered?", "choices": ["1992", "1995", "2009", "2018"], "correct": 1},
            {"type": "purpose", "text": "Why did the author mention the James Webb Space Telescope?", "choices": ["To show that future telescopes will help search for signs of life on exoplanets", "To argue that current telescopes are completely useless for finding planets", "To prove that exoplanets do not exist and never have existed", "To suggest that telescopes are only for looking at Earth's moon"], "correct": 0}
        ]
    },
    # nf20 - Long, split into 3 paragraphs
    {
        "id": "nf20",
        "title": "The Psychology of Decision-Making",
        "passage": """Every day, humans make thousands of decisions, from trivial choices like what to eat for breakfast to life-altering ones like career changes or medical treatments. For decades, economists assumed that humans were rational actors who made decisions by carefully weighing costs and benefits. However, psychologists Daniel Kahneman and Amos Tversky revolutionized this understanding, showing that human decision-making is systematically flawed in predictable ways. Their work earned Kahneman a Nobel Prize (Tversky had died by then). They identified numerous cognitive biases—mental shortcuts or heuristics that lead to errors.

For example, the availability heuristic causes people to overestimate the likelihood of dramatic but rare events (like plane crashes) because they come easily to mind, while underestimating common but mundane risks (like car accidents). The anchoring effect occurs when an irrelevant number influences a judgment; for instance, seeing a high initial price makes subsequent prices seem reasonable even if still expensive. Loss aversion suggests people feel the pain of losing something twice as intensely as the pleasure of gaining the same thing. This explains why people often stick with bad investments or unhappy relationships—they fear loss more than they value potential gain.

Framing effects demonstrate that how a choice is presented changes people's answers: a surgery described as '90% survival rate' is chosen more often than the same surgery described as '10% mortality rate,' even though they are identical. Understanding these biases can help people make better decisions by slowing down, seeking diverse perspectives, and questioning initial instincts. Organizations now use this research to design better choice architectures, such as default enrollment in retirement savings plans, which dramatically increases participation without restricting freedom.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Humans make perfect, rational decisions every time without any errors", "Psychologists have shown that human decision-making is often biased and flawed in predictable ways, including loss aversion and framing effects", "Only economists should study decision-making because others lack expertise", "Decisions have no effect on people's lives or long-term outcomes"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the author's tone toward cognitive biases?", "choices": ["Dismissive", "Practical", "Celebratory", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'heuristics' most nearly means", "choices": ["Formulas", "Shortcuts", "Proofs", "Guesses"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why people fear plane crashes more than car accidents despite cars being more dangerous?", "choices": ["Plane crashes are rare and dramatic, making them more memorable (availability heuristic)", "People never drive cars, so they only fear plane travel", "Planes are actually safer than the passage suggests", "Car accidents never happen, so there is nothing to fear"], "correct": 0},
            {"type": "detail", "text": "According to the passage, loss aversion means people feel loss about how many times more intensely than gain?", "choices": ["Twice", "Three", "Four", "Five"], "correct": 0},
            {"type": "purpose", "text": "Why did the author include the '90% survival rate' vs '10% mortality rate' example?", "choices": ["To prove that doctors are bad at communicating with their patients", "To demonstrate framing effects—how presentation changes decisions", "To argue that surgery is always dangerous regardless of survival rates", "To suggest that survival rates are meaningless numbers"], "correct": 1}
        ]
    }
    ],

    
    "fiction": [
    # Original f1
    {
        "id": "f1",
        "title": "The Tortoise and the Hare",
        "passage": """Once upon a time, a hare was boasting about how fast he could run. He laughed at the tortoise for being so slow. The tortoise, tired of the hare's arrogance, challenged him to a race. The hare thought this was a ridiculous joke and agreed immediately. When the race began, the hare shot ahead and soon had such a large lead that he decided to take a nap under a tree. 'I can rest for a while,' he thought. 'That slow tortoise will never catch up.' Meanwhile, the tortoise continued plodding along, slowly but steadily. When the hare woke up, he saw the tortoise approaching the finish line. He ran as fast as he could, but it was too late. The tortoise had won.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Fast runners always win races", "Slow and steady wins the race", "Napping helps you run faster", "Tortoises are faster than hares"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the hare's attitude toward the tortoise before the race?", "choices": ["Respectful", "Arrogant", "Fearful", "Jealous"], "correct": 1},
            {"type": "vocab", "text": "The word 'arrogance' most nearly means", "choices": ["Kindness", "Pride", "Sorrow", "Shame"], "correct": 1},
            {"type": "inference", "text": "Why did the hare decide to nap during the race?", "choices": ["He was very tired", "He was overconfident", "He wanted to be fair", "He disliked running"], "correct": 1},
            {"type": "detail", "text": "What did the hare do after taking the lead?", "choices": ["Ran faster", "Took a nap", "Talked to the tortoise", "Went home"], "correct": 1},
            {"type": "purpose", "text": "What is the author's purpose in writing this fable?", "choices": ["To teach a lesson about humility and persistence", "To tell a funny joke about animals", "To describe how hares behave", "To persuade readers to race tortoises"], "correct": 0}
        ]
    },
    # f2 - Short (single paragraph)
    {
        "id": "f2",
        "title": "The Boy Who Cried Wolf",
        "passage": """A young shepherd boy tended his family's sheep near a dark forest. Bored with his work, he decided to play a trick on the villagers. 'Wolf! Wolf!' he shouted. The villagers came running with sticks and axes, only to find no wolf at all. The boy laughed at their worried faces. A few days later, he did it again, and again the villagers rushed to help, only to be fooled once more. Then one evening, a real wolf appeared and began attacking the sheep. The boy cried out desperately, 'Wolf! Wolf! Please help!' But this time, the villagers thought he was lying again. They didn't come, and the wolf ate many sheep.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this story?", "choices": ["Sheep are valuable", "Liars lose trust", "Wolves are dangerous", "Villagers are helpful"], "correct": 1},
            {"type": "tone", "text": "How did the villagers likely feel after being tricked twice?", "choices": ["Happy", "Frustrated", "Excited", "Proud"], "correct": 1},
            {"type": "vocab", "text": "The word 'desperately' most nearly means", "choices": ["Calmly", "Urgently", "Quietly", "Slowly"], "correct": 1},
            {"type": "inference", "text": "Why didn't the villagers come the third time?", "choices": ["They were busy", "They thought he was lying", "They didn't hear him", "They wanted the wolf to come"], "correct": 1},
            {"type": "detail", "text": "What happened when the real wolf appeared?", "choices": ["Villagers chased the wolf", "The wolf ate many sheep", "The boy fought the wolf", "The sheep ran away"], "correct": 1},
            {"type": "purpose", "text": "Why did the author write this story?", "choices": ["To teach why lying is harmful", "To tell an exciting wolf story", "To describe shepherd life", "To explain wolf behavior"], "correct": 0}
        ]
    },
    # f3 - Short (single paragraph)
    {
        "id": "f3",
        "title": "The Lion and the Mouse",
        "passage": """A lion lay sleeping in the forest when a tiny mouse ran across his nose. The lion woke up and caught the mouse under his huge paw. 'Please let me go!' squeaked the mouse. 'If you spare my life, I will repay your kindness someday.' The lion laughed at the idea that a small mouse could ever help him, but he decided to release the mouse anyway. A few days later, the lion became trapped in a hunter's net. He roared in frustration, unable to escape. The mouse heard the lion's roars and rushed to help. The tiny mouse gnawed through the ropes with his sharp teeth until the lion was free. 'You laughed at me once,' said the mouse, 'but now you see that even a small friend can be a great help.'""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Mice are very smart", "Small friends can help greatly", "Lions are always kind", "Hunters are dangerous"], "correct": 1},
            {"type": "tone", "text": "How did the lion feel when the mouse offered to help him?", "choices": ["Grateful", "Amused", "Frightened", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'gnawed' most nearly means", "choices": ["Chewed", "Ignored", "Pushed", "Tied"], "correct": 0},
            {"type": "inference", "text": "Why did the lion release the mouse?", "choices": ["He was afraid", "He was moved but skeptical", "He wanted to eat him later", "The mouse paid him"], "correct": 1},
            {"type": "detail", "text": "How did the mouse help the lion escape?", "choices": ["He distracted the hunter", "He chewed through the ropes", "He showed a secret path", "He called other animals"], "correct": 1},
            {"type": "purpose", "text": "What message does this fable convey?", "choices": ["Never trust a mouse", "Help can come from unexpected places", "Lions are dangerous predators", "Always hunt with nets"], "correct": 1}
        ]
    },
    # f4 - Short (single paragraph)
    {
        "id": "f4",
        "title": "The Fox and the Grapes",
        "passage": """A hungry fox was walking through a vineyard when he spotted a bunch of ripe, purple grapes hanging from a high vine. His mouth watered at the sight. He wanted those grapes more than anything. The fox jumped and jumped, trying to reach the grapes, but they were too high. Again and again, he leaped into the air, each time falling short. Finally, exhausted and frustrated, the fox stopped trying. As he walked away, he said to himself, 'Those grapes are probably sour anyway. I didn't really want them.' And he continued on his way, pretending not to care about what he could not have.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Grapes are delicious", "People pretend not to want what they cannot have", "Foxes are clever animals", "Vineyards have good food"], "correct": 1},
            {"type": "tone", "text": "How did the fox feel when he gave up?", "choices": ["Proud", "Bitter", "Joyful", "Relieved"], "correct": 1},
            {"type": "vocab", "text": "The word 'vineyard' most nearly means", "choices": ["Forest", "Farm", "River", "Mountain"], "correct": 1},
            {"type": "inference", "text": "Why did the fox claim the grapes were sour?", "choices": ["He tasted them", "He made an excuse", "Someone told him", "All grapes are sour"], "correct": 1},
            {"type": "detail", "text": "What did the fox do when he couldn't reach the grapes?", "choices": ["Asked for help", "Walked away pretending not to care", "Climbed the vine", "Waited for them to fall"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Being too persistent", "Making excuses after failure", "Sharing food with others", "Eating too many grapes"], "correct": 1}
        ]
    },
    # f5 - Short (single paragraph)
    {
        "id": "f5",
        "title": "The Wind and the Sun",
        "passage": """The North Wind and the Sun argued about which was stronger. They decided to settle their dispute with a challenge. Seeing a traveler walking down the road, they agreed that whoever could make the traveler remove his coat would be declared the winner. The North Wind went first. He blew with all his might, sending powerful gusts that rattled windows and bent trees. But the harder the wind blew, the tighter the traveler wrapped his coat around himself. Finally, the wind gave up. Then the Sun began to shine. He sent gentle, warm rays down upon the traveler. Soon the traveler, feeling the pleasant heat, unbuttoned his coat and then took it off completely. The Sun had won—not with force, but with warmth and gentleness.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Wind is very strong", "Gentleness beats force", "Travelers wear coats", "The sun is hot"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the North Wind's approach?", "choices": ["Gentle", "Aggressive", "Patient", "Sneaky"], "correct": 1},
            {"type": "vocab", "text": "The word 'dispute' most nearly means", "choices": ["Game", "Argument", "Race", "Song"], "correct": 1},
            {"type": "inference", "text": "Why did the traveler hold his coat tighter when the wind blew?", "choices": ["He was cold", "He wanted to win for the sun", "His coat was stuck", "He was afraid"], "correct": 0},
            {"type": "detail", "text": "What made the traveler remove his coat?", "choices": ["The strong wind", "The sun's warmth", "A sudden rainstorm", "He reached his destination"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Force is effective", "Gentleness works better than aggression", "The sun is powerful", "Never argue with the wind"], "correct": 1}
        ]
    },
    # f6 - Longer, split into 2 paragraphs
    {
        "id": "f6",
        "title": "The Ant and the Grasshopper",
        "passage": """On a bright summer day, a grasshopper hopped through a field, singing and playing his fiddle. He saw an ant carrying a heavy kernel of corn back to his nest. 'Why work so hard on such a beautiful day?' asked the grasshopper. 'Come sing and dance with me instead.' The ant paused and wiped his brow. 'I am storing food for the winter,' he replied. 'When cold weather comes, you will wish you had done the same.' The grasshopper laughed. 'Winter is far away! There is plenty of food everywhere.'

All summer, the ant continued gathering grain, while the grasshopper played. When autumn arrived, the ant worked even harder. The grasshopper grew tired of playing and began to feel hungry, but he still did not prepare. Then winter came with bitter winds and snow. The ground froze, and no food could be found. The grasshopper, weak and starving, stumbled to the ant's underground nest. 'Please, friend ant,' he begged, 'give me some food and shelter. I have nothing.' The ant looked at him sadly. 'What were you doing all summer while I labored?' 'I sang and played,' confessed the grasshopper. 'Then,' said the ant, 'since you sang all summer, you may dance all winter.' But the ant was not cruel. He shared his food, and the grasshopper learned an important lesson: there is a time for work and a time for play, but those who refuse to prepare for hard times will suffer.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Singing is fun", "Prepare for hard times", "Ants are selfish", "Summer is short"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the grasshopper's attitude in summer?", "choices": ["Worried", "Carefree", "Angry", "Jealous"], "correct": 1},
            {"type": "vocab", "text": "The word 'kernel' most nearly means", "choices": ["Seed", "Insect", "Tool", "Rock"], "correct": 0},
            {"type": "inference", "text": "Why did the grasshopper beg for food in winter?", "choices": ["He was lazy", "He had stored nothing", "The ant stole his food", "He was testing the ant"], "correct": 1},
            {"type": "detail", "text": "What did the grasshopper do all summer?", "choices": ["Worked hard", "Sang and played", "Built a nest", "Slept all day"], "correct": 1},
            {"type": "purpose", "text": "Why did the ant mention dancing all winter?", "choices": ["To be cruel", "To teach a lesson", "To make fun of him", "To send him away"], "correct": 1}
        ]
    },
    # f7 - Longer, split into 2 paragraphs
    {
        "id": "f7",
        "title": "The City Mouse and the Country Mouse",
        "passage": """A country mouse lived in a simple hole beneath a farmer's barn. He ate plain wheat and corn, drank water from a puddle, and lived quietly. One day, his cousin from the city came to visit. The city mouse looked around the barn with disdain. 'How can you live like this?' he said. 'In the city, I dine on fine cheeses, meats, and pastries. You must come stay with me.' The country mouse agreed.

That night, they arrived at a grand house in the city. The city mouse led his cousin to the dining room, where leftover food from a banquet sat on the table. 'See?' said the city mouse. 'Eat anything you like.' The country mouse had never seen such food. He nibbled a piece of cheese, then a bit of cake. But just as he began to enjoy himself, the kitchen door burst open. A huge cat leaped onto the table, growling. The mice ran for their lives, hiding behind a heavy cabinet. Then a cook entered with a broom, swinging wildly. 'This happens often,' whispered the city mouse, shaking. The country mouse grabbed his cousin's paw. 'Thank you for your kindness,' he said, 'but I would rather eat plain corn in safety than fine food in fear. I am going home tonight.' And he returned to his quiet barn, where no cats or brooms could find him.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this story?", "choices": ["City life is better", "Safety matters more than luxury", "Cats are dangerous", "Country food is healthy"], "correct": 1},
            {"type": "tone", "text": "How did the city mouse view the country mouse's home?", "choices": ["With envy", "With scorn", "With fear", "With joy"], "correct": 1},
            {"type": "vocab", "text": "The word 'disdain' most nearly means", "choices": ["Excitement", "Scorn", "Curiosity", "Kindness"], "correct": 1},
            {"type": "inference", "text": "Why did the country mouse return home?", "choices": ["He hated cheese", "He valued safety over luxury", "He was kicked out", "He got lost"], "correct": 1},
            {"type": "detail", "text": "What danger did the mice face in the city?", "choices": ["A snake", "A cat and a cook", "Poisoned food", "A trap"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Never visit relatives", "Choose what you value most", "All mice should live in cities", "Luxury is always best"], "correct": 1}
        ]
    },
    # f8 - Longer, split into 2 paragraphs
    {
        "id": "f8",
        "title": "The Oak and the Reed",
        "passage": """A mighty oak tree stood at the edge of a river. Beside it grew a slender reed that bent in every breeze. The oak often mocked the reed. 'How weak you are,' boomed the oak. 'A gentle wind makes you bow and tremble. Look at me: I stand firm against any storm. No wind can move me.' The reed replied softly, 'You are strong indeed, but do not mock what you do not understand. I bend so that I do not break.' The oak laughed.

One autumn night, a terrible hurricane swept across the land. The wind howled and screamed, tearing at everything in its path. The oak planted its roots deep and refused to yield. The harder the wind blew, the more the oak resisted. But the wind grew stronger and stronger, until with a tremendous crack, the oak was ripped from the ground. Its great roots tore free, and the oak crashed into the river. The reed, meanwhile, bent low—almost to the water—and let the storm pass over it. When dawn came, the reed stood up again, unharmed. And it whispered to the fallen oak, 'There is more than one kind of strength. Sometimes, flexibility is the greatest strength of all.'""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Oak trees are strongest", "Flexibility beats rigid strength", "Reeds are useless", "Hurricanes are powerful"], "correct": 1},
            {"type": "tone", "text": "How did the oak treat the reed?", "choices": ["Respectfully", "Mockingly", "Kindly", "Fearfully"], "correct": 1},
            {"type": "vocab", "text": "The word 'yield' most nearly means", "choices": ["Grow", "Surrender", "Attack", "Stand"], "correct": 1},
            {"type": "inference", "text": "Why did the reed survive the hurricane?", "choices": ["It was hidden", "It bent instead of resisting", "It had deep roots", "The wind missed it"], "correct": 1},
            {"type": "detail", "text": "What happened to the oak at the end?", "choices": ["It survived", "It fell into the river", "It became a reed", "It apologized"], "correct": 1},
            {"type": "purpose", "text": "Why did the author write this fable?", "choices": ["To teach about trees", "To show pride leads to downfall", "To describe hurricanes", "To promote planting oaks"], "correct": 1}
        ]
    },
    # f9 - Longer, split into 2 paragraphs
    {
        "id": "f9",
        "title": "The Crow and the Pitcher",
        "passage": """A thirsty crow searched for water on a hot, dry day. She had flown for miles without finding a single drop. Finally, she spotted a pitcher in a farmer's yard. She flew to it eagerly, hoping for a drink. But when she looked inside, she saw that the water was very low—too low for her beak to reach. She tried tipping the pitcher over, but it was too heavy. She tried pushing her head in farther, but her beak still could not touch the water.

The crow was about to give up when she had an idea. Around the yard lay many small pebbles. The crow picked up one pebble in her beak and dropped it into the pitcher. The water rose slightly. She dropped another pebble, and the water rose a little more. Pebble by pebble, the crow continued. The water crept higher and higher until, at last, it reached the brim. The crow drank deeply and flew away satisfied. The moral is that necessity is the mother of invention—and that patience and cleverness can solve problems that strength cannot.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Crows are smart", "Cleverness solves problems", "Thirst is painful", "Pebbles are useful"], "correct": 1},
            {"type": "tone", "text": "How did the crow approach her problem?", "choices": ["Panicked", "Cleverly", "Violently", "Lazily"], "correct": 1},
            {"type": "vocab", "text": "The word 'pitcher' most nearly means", "choices": ["Bird", "Container", "Player", "Tree"], "correct": 1},
            {"type": "inference", "text": "Why did pebbles raise the water level?", "choices": ["They melted", "They took up space", "They absorbed water", "They scared the water"], "correct": 1},
            {"type": "detail", "text": "Why couldn't the crow drink at first?", "choices": ["Water was frozen", "Water was too low", "Water was poisoned", "She wasn't thirsty"], "correct": 1},
            {"type": "purpose", "text": "What does 'necessity is the mother of invention' mean?", "choices": ["Inventions need mothers", "Need inspires creativity", "Crows are inventors", "Water is necessary"], "correct": 1}
        ]
    },
    # f10 - Longer, split into 2 paragraphs
    {
        "id": "f10",
        "title": "The Bundle of Sticks",
        "passage": """An old farmer had several sons who constantly argued and fought with one another. No matter what their father said, they would not stop quarreling. One day, the farmer called all his sons together. He handed each son a single stick. 'Break it,' he said. Each son easily snapped his stick in two. Then the farmer took a bundle of many sticks tied tightly together. 'Now break this,' he said.

The oldest son tried first. He strained and twisted, but the bundle would not break. One by one, the other sons tried. Not one of them could break the bundle. The farmer untied the sticks and let them fall to the ground. 'My sons,' he said, 'you see that alone, you are weak and easily broken. But if you stand together and support one another, no enemy can break you. Your arguments weaken you. Your unity will make you strong.' The sons understood at last. From that day forward, they worked together, and their farm prospered as never before.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this story?", "choices": ["Sticks are strong", "Unity makes strength", "Farmers are wise", "Sons should obey"], "correct": 1},
            {"type": "tone", "text": "How did the farmer teach his sons?", "choices": ["Cruelly", "Wisely", "Hastily", "Confusingly"], "correct": 1},
            {"type": "vocab", "text": "The word 'prospered' most nearly means", "choices": ["Failed", "Thrived", "Stayed", "Shrank"], "correct": 1},
            {"type": "inference", "text": "Why couldn't the sons break the bundle?", "choices": ["It was glued", "Sticks supported each other", "They were weak", "The farmer tied it tightly"], "correct": 1},
            {"type": "detail", "text": "What did the farmer give each son first?", "choices": ["A bundle", "A single stick", "A rope", "A field"], "correct": 1},
            {"type": "purpose", "text": "Why did the author write this fable?", "choices": ["To explain farming", "To teach unity and teamwork", "To criticize arguing", "To describe wood types"], "correct": 1}
        ]
    },
    # f11 - Longer, split into 2 paragraphs
    {
        "id": "f11",
        "title": "The Milkmaid and Her Pail",
        "passage": """A milkmaid named Patty carried a pail of milk on her head, walking to the market to sell it. As she walked, she began to daydream. 'With the money from this milk,' she thought, 'I will buy a hundred eggs. Those eggs will hatch into chickens. The chickens will grow fat and lay more eggs. I will sell the eggs and buy a new dress—a beautiful blue one with lace. When I wear that dress to the fair, all the young men will admire me. They will ask me to dance. But I will toss my head and refuse them all.'

At that moment, Patty tossed her head—just as she had imagined. The pail of milk fell from her head, crashed to the ground, and spilled everywhere. All the milk was lost. Patty sat down and wept. 'Do not count your chickens before they are hatched,' an old woman told her. Patty had planned for a future that never came, and she had nothing left but tears.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Milk is valuable", "Don't count on future rewards before securing the present", "Dancing is dangerous", "Old women are wise"], "correct": 1},
            {"type": "tone", "text": "How did the milkmaid daydream?", "choices": ["Practically", "Overconfidently", "Fearfully", "Sadly"], "correct": 1},
            {"type": "vocab", "text": "The phrase 'count your chickens before they hatch' means", "choices": ["Count eggs carefully", "Don't assume future success", "Chickens are unreliable", "Farmers are wise"], "correct": 1},
            {"type": "inference", "text": "Why did the milk spill?", "choices": ["Someone pushed her", "She tossed her head while dreaming", "The pail had a hole", "A chicken stole it"], "correct": 1},
            {"type": "detail", "text": "What did Patty plan to buy with her egg money?", "choices": ["A cow", "A blue dress", "More milk", "A house"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable warning against?", "choices": ["Working too hard", "Assuming future success too early", "Selling milk", "Buying dresses"], "correct": 1}
        ]
    },
    # f12 - Longer, split into 2 paragraphs
    {
        "id": "f12",
        "title": "The Goose That Laid the Golden Eggs",
        "passage": """A poor farmer and his wife owned a remarkable goose. Every morning, the goose laid a single egg made of solid gold. The farmer would sell the golden egg at the market and live comfortably. But soon, the farmer grew greedy. 'This goose lays only one egg per day,' he complained. 'If I cut her open, I will find all the gold inside her at once. Then I will be rich immediately!' His wife warned him, 'Do not destroy the goose that feeds you.' But the farmer would not listen.

One morning, he took a knife and killed the goose. When he cut her open, he found no gold inside at all—only ordinary goose organs. He had killed the goose, and now there would be no more golden eggs. The farmer wept, but it was too late. He had traded steady, patient wealth for a single moment of greedy foolishness.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Geese are valuable", "Greed destroys good things", "Farmers are foolish", "Gold is worthless"], "correct": 1},
            {"type": "tone", "text": "How did the farmer act?", "choices": ["Wisely", "Greedily", "Patiently", "Kindly"], "correct": 1},
            {"type": "vocab", "text": "The word 'remarkable' most nearly means", "choices": ["Ordinary", "Extraordinary", "Ugly", "Slow"], "correct": 1},
            {"type": "inference", "text": "Why did the farmer kill the goose?", "choices": ["He was hungry", "He wanted all the gold at once", "The goose stopped laying", "His wife told him to"], "correct": 1},
            {"type": "detail", "text": "What did the farmer find inside the goose?", "choices": ["Golden eggs", "Ordinary organs", "Treasure", "Nothing"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Trust geese", "Patience beats greed", "Listen to your wife", "Gold is common"], "correct": 1}
        ]
    },
    # f13 - Longer, split into 2 paragraphs
    {
        "id": "f13",
        "title": "The Dog and His Reflection",
        "passage": """A dog had stolen a large, juicy piece of meat from a butcher's shop. He held it firmly in his mouth and ran to a quiet stream to eat it alone. As he crossed a wooden bridge over the water, he looked down and saw his own reflection. But the dog did not know it was himself. He saw another dog with another piece of meat—and that piece looked twice as large as his own.

'I want that meat too!' thought the greedy dog. He opened his mouth to snatch the other dog's meat. But when he opened his mouth, his own piece of meat fell from his jaws, splashed into the water, and disappeared. The reflection vanished as well. The dog stood on the bridge, hungry and ashamed, with nothing left at all. He had lost everything because he wanted more than he already had.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Dogs can't swim", "Greed makes you lose what you have", "Reflections are tricky", "Meat is valuable"], "correct": 1},
            {"type": "tone", "text": "How did the dog act?", "choices": ["Generously", "Greedily", "Cautiously", "Helpfully"], "correct": 1},
            {"type": "vocab", "text": "The word 'reflection' most nearly means", "choices": ["Sound", "Image", "Shadow", "Smell"], "correct": 1},
            {"type": "inference", "text": "Why did the dog think there was another dog?", "choices": ["He never saw his reflection before", "Another dog was there", "He was dreaming", "The water was magic"], "correct": 0},
            {"type": "detail", "text": "What happened when the dog opened his mouth?", "choices": ["He bit the other dog", "His meat fell in the water", "He got more meat", "He swallowed both"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Sharing food", "Being greedy", "Crossing bridges", "Stealing meat"], "correct": 1}
        ]
    },
    # f14 - Longer, split into 2 paragraphs
    {
        "id": "f14",
        "title": "The North Wind and the Sun (Extended)",
        "passage": """One day, the North Wind and the Sun argued about who was the strongest among all the forces of nature. The North Wind boasted of his power to uproot trees and drive ships onto rocks. The Sun spoke calmly of his ability to warm the earth and make flowers bloom. Neither would yield. Finally, they saw a traveler walking along a winding road, wearing a heavy woolen cloak. 'Whoever can make that traveler remove his cloak is the stronger,' said the Sun. The North Wind agreed eagerly.

The North Wind went first. He blew with all his fury. He sent icy blasts that rattled shutters and bent the trees nearly to the ground. Snow flew sideways, and the air turned bitter cold. But the traveler, instead of removing his cloak, wrapped it tighter around himself and buttoned it to his chin. The harder the wind blew, the tighter the traveler held his cloak. Exhausted, the North Wind gave up. Then the Sun began. He sent gentle, warm rays down upon the traveler. The traveler relaxed his grip. The Sun shone brighter, and the traveler unbuttoned his cloak. The Sun shone warmer still, and the traveler removed his cloak entirely, draping it over his arm. The Sun had won—not with violence, but with patience and kindness. And that is how the Sun proved that gentleness is stronger than fury.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["The North Wind is strong", "Gentleness beats force", "Travelers wear cloaks", "The Sun is hot"], "correct": 1},
            {"type": "tone", "text": "How did the North Wind try to win?", "choices": ["Gently", "Aggressively", "Patiently", "Sneakily"], "correct": 1},
            {"type": "vocab", "text": "The word 'fury' most nearly means", "choices": ["Joy", "Rage", "Breeze", "Calm"], "correct": 1},
            {"type": "inference", "text": "Why did the traveler hold his cloak tighter when the wind blew?", "choices": ["He was cold", "He wanted to help the Sun", "His cloak was stuck", "He was afraid of losing it"], "correct": 0},
            {"type": "detail", "text": "What made the traveler remove his cloak?", "choices": ["The strong wind", "The Sun's warmth", "A rainstorm", "He arrived home"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Force is effective", "Gentleness works better than aggression", "The Sun is powerful", "Never argue with the wind"], "correct": 1}
        ]
    },
    # f15 - Longer, split into 2 paragraphs
    {
        "id": "f15",
        "title": "The Fox and the Stork",
        "passage": """A fox invited a stork to dinner, intending to play a mean trick. The fox served soup in a very shallow dish. The fox lapped up his soup easily with his tongue. But the stork, with her long, slender beak, could not get a single drop. She only wet the tip of her beak. 'I am sorry you do not like my soup,' said the fox, smiling. The stork said nothing, but she remembered.

A few days later, the stork invited the fox to dinner. She served food in a tall, narrow jar with a long, thin neck. The stork slipped her long beak into the jar and ate her fill easily. But the fox could not fit his nose into the narrow opening. He sniffed the delicious smells but could not reach the food. He went home hungry. As he left, the stork said, 'Do not give what you cannot take yourself.' The fox learned that tricks can backfire, and that those who are unkind to others may find themselves treated the same way.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Foxes are hungry", "Cruel tricks often backfire", "Storks have good manners", "Soup is best shallow"], "correct": 1},
            {"type": "tone", "text": "How did the fox treat the stork at first?", "choices": ["Kindly", "Deceitfully", "Generously", "Accidentally"], "correct": 1},
            {"type": "vocab", "text": "The word 'backfire' most nearly means", "choices": ["Explode", "Opposite effect", "Succeed", "Forget"], "correct": 1},
            {"type": "inference", "text": "Why did the stork choose a tall narrow jar?", "choices": ["It was the only dish", "She chose it to be easy for her but hard for the fox", "She didn't know the fox was coming", "It was an accident"], "correct": 1},
            {"type": "detail", "text": "Why couldn't the stork eat from the shallow dish?", "choices": ["She wasn't hungry", "Her beak was too long", "The soup was poisoned", "The fox ate it all"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Never accept dinner invitations", "Treat others as you wish to be treated", "Storks cook better than foxes", "Soup is bad for foxes"], "correct": 1}
        ]
    },
    # f16 - Longer, split into 2 paragraphs
    {
        "id": "f16",
        "title": "The Donkey in Lion's Skin",
        "passage": """A donkey found a lion's skin left behind by a hunter. The donkey draped the skin over his body and admired himself in a pond. 'Now I look like the king of beasts,' he thought. 'No one will dare touch me.' The donkey walked through the forest wearing the lion's skin. All the animals—rabbits, deer, and even wolves—ran away in terror. The donkey laughed to himself, feeling very clever.

He decided to visit a nearby farm. The farmer's sheep scattered when they saw the lion approaching. But just as the donkey was about to enjoy his victory, he opened his mouth and let out a loud, unmistakable 'Hee-Haw!' The farmer heard the bray. 'A donkey in a lion's skin!' he shouted. The farmer ran after the donkey with a stick and chased him out of the farm. The moral of the story is that fine clothes may disguise someone for a while, but a fool will eventually reveal himself by his words or actions.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Donkeys are strong", "Pretending will be exposed", "Lions are scary", "Farmers are clever"], "correct": 1},
            {"type": "tone", "text": "How did the donkey see himself?", "choices": ["Humbly", "Delusionally", "Fearfully", "Kindly"], "correct": 1},
            {"type": "vocab", "text": "The word 'bray' most nearly means", "choices": ["Roar", "Donkey sound", "Shout", "Whisper"], "correct": 1},
            {"type": "inference", "text": "Why was the donkey exposed?", "choices": ["The skin fell off", "His bray gave him away", "The farmer knew him", "Animals told the farmer"], "correct": 1},
            {"type": "detail", "text": "What did the donkey find in the forest?", "choices": ["A lion", "A lion's skin", "A hunter", "A pond"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Helping others", "Pretending to be something you're not", "Wearing animal skins", "Walking in forests"], "correct": 1}
        ]
    },
    # f17 - Longer, split into 2 paragraphs
    {
        "id": "f17",
        "title": "The Two Travelers and the Bear",
        "passage": """Two men were walking through a forest when suddenly a large bear appeared on the path ahead. One man immediately climbed a tall tree and hid among the branches. The other man knew he could not outrun the bear. He fell to the ground and lay perfectly still, holding his breath. The bear approached the man on the ground. It sniffed his ear, then his nose. The man did not move a muscle. Bears are known to avoid touching dead things. After a few minutes, the bear decided the man was dead and wandered away.

When the bear was gone, the first man climbed down from the tree. 'What did the bear whisper in your ear?' he asked with a nervous laugh. The second man stood up and brushed off his clothes. 'He told me,' he said, 'never travel with a friend who abandons you in danger.' And he walked away alone, leaving the first man ashamed.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Bears are dangerous", "True friends don't abandon you", "Climbing trees is smart", "Playing dead works"], "correct": 1},
            {"type": "tone", "text": "How did the first traveler act?", "choices": ["Brave", "Selfish", "Helpful", "Kind"], "correct": 1},
            {"type": "vocab", "text": "The word 'abandons' most nearly means", "choices": ["Helps", "Leaves", "Follows", "Saves"], "correct": 1},
            {"type": "inference", "text": "Why didn't the bear attack the man on the ground?", "choices": ["The bear wasn't hungry", "The bear thought he was dead", "The first man scared the bear", "The man was a bear trainer"], "correct": 1},
            {"type": "detail", "text": "What did the first traveler do when he saw the bear?", "choices": ["Played dead", "Climbed a tree", "Fought the bear", "Ran away"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach about friendship?", "choices": ["All friends are unreliable", "A friend who saves only himself is no true friend", "Bears make better friends", "Never travel in forests"], "correct": 1}
        ]
    },
    # f18 - Longer, split into 2 paragraphs
    {
        "id": "f18",
        "title": "The Farmer and the Snake",
        "passage": """On a freezing winter morning, a farmer found a snake lying stiff and frozen by the side of the road. The snake was nearly dead from the cold. 'Please, kind farmer,' the snake whispered weakly, 'take me inside and warm me by your fire. I will not hurt you.' The farmer hesitated. He knew snakes could be dangerous. But his heart softened, and he picked up the snake and carried it home. He placed the snake near the hearth.

The warmth slowly revived the snake. Its muscles loosened, and its eyes grew bright. The farmer's young son came close to see the snake. As soon as the snake had fully warmed, it reared up and bit the farmer's hand. 'But I saved your life!' cried the farmer, falling to his knees. 'Why did you bite me?' The snake hissed, 'You knew what I was when you picked me up.' And the farmer died. The moral is that kindness to evil does not change its nature.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Snakes are helpful", "Evil nature doesn't change", "Kindness is always rewarded", "Farmers are foolish"], "correct": 1},
            {"type": "tone", "text": "How did the farmer act initially?", "choices": ["Wisely", "Naively", "Cruelly", "Selfishly"], "correct": 1},
            {"type": "vocab", "text": "The word 'revived' most nearly means", "choices": ["Killed", "Restored", "Froze", "Weakened"], "correct": 1},
            {"type": "inference", "text": "Why did the snake bite the farmer?", "choices": ["It was grateful", "It acted on its nature", "The farmer stepped on it", "The snake was playing"], "correct": 1},
            {"type": "detail", "text": "What happened to the farmer at the end?", "choices": ["He killed the snake", "He died from the bite", "He recovered", "He became friends with the snake"], "correct": 1},
            {"type": "purpose", "text": "What warning does this fable give?", "choices": ["Never go outside in winter", "Be cautious about helping those known to be dangerous", "All farmers should carry anti-venom", "Snakes make good pets"], "correct": 1}
        ]
    },
    # f19 - Longer, split into 2 paragraphs
    {
        "id": "f19",
        "title": "The Peacock and the Crane",
        "passage": """A peacock spread his magnificent tail feathers in the sun. The iridescent blues and greens shimmered like jewels. A plain gray crane walked by, searching for food in the mud. The peacock laughed. 'Look at you,' he said. 'Your feathers are dull as dust. No one ever admires you. See how everyone stops to look at my beauty.' The crane stopped and looked at the peacock calmly. 'You are beautiful indeed,' said the crane. 'But while you strut on the ground showing off your tail, I can soar among the clouds. When danger comes, your fine feathers will not save you. But I can fly away to safety. Beauty is not the only measure of worth.'

Just then, a fox appeared in the clearing. The peacock screamed and ran awkwardly, his long tail feathers slowing him down. The crane spread his broad gray wings and rose gracefully into the sky. The fox caught the peacock easily. And the crane flew on, free and alive.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Peacocks are beautiful", "Vanity ignores practical strengths", "Cranes are jealous", "Foxes are dangerous"], "correct": 1},
            {"type": "tone", "text": "How did the peacock treat the crane?", "choices": ["Humbly", "Arrogantly", "Kindly", "Fearfully"], "correct": 1},
            {"type": "vocab", "text": "The word 'iridescent' most nearly means", "choices": ["Dull", "Shimmering", "Invisible", "Heavy"], "correct": 1},
            {"type": "inference", "text": "Why did the crane survive while the peacock did not?", "choices": ["The crane could fly away", "The crane was stronger", "The peacock was old", "The fox preferred peacock meat"], "correct": 0},
            {"type": "detail", "text": "What happened when the fox appeared?", "choices": ["Both birds flew away", "The peacock was caught; the crane flew to safety", "The crane was caught", "The fox admired the peacock's feathers"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Flying", "Vanity and mocking others", "Being humble", "Eating"], "correct": 1}
        ]
    },
    # f20 - Longer, split into 2 paragraphs
    {
        "id": "f20",
        "title": "The Old Lion and the Fox",
        "passage": """A lion too old and weak to hunt anymore lay in his cave, pretending to be ill. When other animals came to visit the 'sick' king, the lion would pounce and eat them. Many animals—a sheep, a goat, a young deer—entered the cave and never came out. One day, a clever fox approached the cave. He stood outside the entrance and called in, 'How are you feeling today, Your Majesty?' The lion put on his most pitiful voice. 'Oh, I am so weak, dear friend. Please come in and keep me company.'

The fox did not move. 'I would love to,' said the fox, 'but I notice that many footprints lead into your cave—but no footprints lead out.' The fox turned and walked away, leaving the hungry lion alone. The lion learned that cleverness can defeat brute strength, and that noticing details others ignore can save your life.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Lions are dangerous", "Observation protects from danger", "It's rude to refuse a king", "Old lions should be pitied"], "correct": 1},
            {"type": "tone", "text": "How did the fox behave?", "choices": ["Foolishly", "Cleverly", "Rudely", "Fearfully"], "correct": 1},
            {"type": "vocab", "text": "The word 'pounce' most nearly means", "choices": ["Welcome", "Attack", "Retreat", "Sleep"], "correct": 1},
            {"type": "inference", "text": "Why didn't the fox enter the cave?", "choices": ["He wasn't curious", "He noticed footprints going in but not coming out", "He was afraid of the dark", "He had met the lion before"], "correct": 1},
            {"type": "detail", "text": "What did the fox notice at the cave entrance?", "choices": ["The lion was sleeping", "Footprints in but none out", "A hidden escape route", "The cave was empty"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach about safety?", "choices": ["Never visit sick animals", "Pay attention to evidence to avoid danger", "Always trust what you're told", "Lions make good kings"], "correct": 1}
        ]
    }
],
    
    "poetry": [
    # Original p1
    {
        "id": "p1",
        "title": "The Road Not Taken (excerpt)",
        "passage": """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.
— Robert Frost""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker regrets his life choices", "Choices shape who we become", "Easy paths are always better", "Forest paths look identical"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood of this poem?", "choices": ["Joyful", "Angry", "Reflective", "Panicked"], "correct": 2},
            {"type": "vocab", "text": "The word 'diverged' most nearly means", "choices": ["Met", "Split", "Vanished", "Darkened"], "correct": 1},
            {"type": "inference", "text": "Why will the speaker tell this story 'with a sigh'?", "choices": ["He will feel nostalgic", "He will be out of breath", "He will be angry", "He won't remember"], "correct": 0},
            {"type": "detail", "text": "Which road did the speaker ultimately take?", "choices": ["The first road", "The worn road", "The less traveled road", "Neither road"], "correct": 2},
            {"type": "purpose", "text": "What is the poet's likely purpose?", "choices": ["To give directions", "To explore how choices affect identity", "To complain about options", "To describe autumn"], "correct": 1}
        ]
    },
    # p2
    {
        "id": "p2",
        "title": "The Eagle",
        "passage": """He clasps the crag with crooked hands;
Close to the sun in lonely lands,
Ring'd with the azure world, he stands.

The wrinkled sea beneath him crawls;
He watches from his mountain walls,
And like a thunderbolt he falls.
— Alfred, Lord Tennyson""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Oceans are dangerous", "Eagles fear heights", "The eagle is powerful and majestic", "Mountain walls protect eagles"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Humorous", "Majestic", "Mournful", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'azure' most nearly means", "choices": ["Red", "Green", "Blue", "Black"], "correct": 2},
            {"type": "inference", "text": "How fast does the eagle fall 'like a thunderbolt'?", "choices": ["Very slowly", "Extremely fast", "At a walking pace", "It doesn't fall"], "correct": 1},
            {"type": "detail", "text": "What is the eagle doing at the beginning?", "choices": ["Flying", "Perched on a cliff", "Building a nest", "Fighting"], "correct": 1},
            {"type": "purpose", "text": "Why compare the eagle's fall to a 'thunderbolt'?", "choices": ["To show speed and power", "To suggest fear", "To indicate bad weather", "To show weakness"], "correct": 0}
        ]
    },
    # p3
    {
        "id": "p3",
        "title": "Fog",
        "passage": """The fog comes
on little cat feet.

It sits looking
over harbor and city
on silent haunches
and then moves on.
— Carl Sandburg""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Fog is dangerous for ships", "Fog is compared to a silent cat", "Cats like foggy weather", "Fog never moves once it arrives"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood?", "choices": ["Loud", "Calm", "Angry", "Fast"], "correct": 1},
            {"type": "vocab", "text": "The word 'haunches' most nearly means", "choices": ["Eyes", "Paws", "Rear legs", "Whiskers"], "correct": 2},
            {"type": "inference", "text": "How does the poet view fog?", "choices": ["As a violent storm", "As a gentle visitor", "As dangerous", "As permanent"], "correct": 1},
            {"type": "detail", "text": "What does the fog do 'on little cat feet'?", "choices": ["Runs away", "Comes into the city", "Makes noise", "Disappears"], "correct": 1},
            {"type": "purpose", "text": "Why compare fog to a cat?", "choices": ["To show fog is scary", "To show fog moves silently and sits quietly", "To prove fog is an animal", "To describe cats"], "correct": 1}
        ]
    },
    # p4
    {
        "id": "p4",
        "title": "Hope is the thing with feathers",
        "passage": """Hope is the thing with feathers
That perches in the soul,
And sings the tune without the words,
And never stops at all,

And sweetest in the Gale is heard;
And sore must be the storm
That could abash the little Bird
That kept so many warm.

I've heard it in the chillest land,
And on the strangest Sea;
Yet, never, in Extremity,
It asked a crumb of me.
— Emily Dickinson""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Birds make good pets", "Hope is like a bird that never stops singing", "Storms harm small birds", "The speaker dislikes hope"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Desperate", "Hopeful", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'abash' most nearly means", "choices": ["Encourage", "Silence", "Celebrate", "Feed"], "correct": 1},
            {"type": "inference", "text": "How does the speaker view hope?", "choices": ["As a waste of time", "As always present and asking nothing", "As something she never felt", "As only for good times"], "correct": 1},
            {"type": "detail", "text": "Where does hope perch?", "choices": ["In a tree", "In the soul", "On the sea", "In a cage"], "correct": 1},
            {"type": "purpose", "text": "What is Dickinson's primary purpose?", "choices": ["To describe bird species", "To explain that hope is valuable and enduring", "To complain about hard times", "To sell pet birds"], "correct": 1}
        ]
    },
    # p5
    {
        "id": "p5",
        "title": "A Poison Tree",
        "passage": """I was angry with my friend:
I told my wrath, my wrath did end.
I was angry with my foe:
I told it not, my wrath did grow.

And I watered it in fears,
Night and morning with my tears;
And I sunned it with smiles,
And with soft deceitful wiles.

And it grew both day and night,
Till it bore an apple bright;
And my foe beheld it shine,
And he knew that it was mine,

And into my garden stole
When the night had veiled the pole;
In the morning, glad, I see
My foe outstretched beneath the tree.
— William Blake""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Apples are dangerous", "Unexpressed anger becomes destructive", "Friends should always agree", "Gardening helps with anger"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Joyful", "Dark and vengeful", "Confused", "Romantic"], "correct": 1},
            {"type": "vocab", "text": "The word 'wrath' most nearly means", "choices": ["Joy", "Rage", "Confusion", "Fear"], "correct": 1},
            {"type": "inference", "text": "What happened to the speaker's foe?", "choices": ["He ate the apple and died", "He became friends", "He ran away", "He apologized"], "correct": 0},
            {"type": "detail", "text": "What happened when the speaker told his friend about his anger?", "choices": ["They fought", "The anger ended", "The friend got angrier", "The anger grew"], "correct": 1},
            {"type": "purpose", "text": "What is Blake's purpose?", "choices": ["To teach gardening", "To warn that unexpressed anger becomes dangerous", "To describe a garden", "To promote apple trees"], "correct": 1}
        ]
    },
    # p6
    {
        "id": "p6",
        "title": "The Tyger",
        "passage": """Tyger Tyger, burning bright,
In the forests of the night;
What immortal hand or eye,
Could frame thy fearful symmetry?

In what distant deeps or skies.
Burnt the fire of thine eyes?
On what wings dare he aspire?
What the hand, dare seize the fire?

And what shoulder, & what art,
Could twist the sinews of thy heart?
And when thy heart began to beat,
What dread hand? & what dread feet?

What the hammer? what the chain,
In what furnace was thy brain?
What the anvil? what dread grasp,
Dare its deadly terrors clasp!

When the stars threw down their spears
And water'd heaven with their tears:
Did he smile his work to see?
Did he who made the Lamb make thee?

Tyger Tyger burning bright,
In the forests of the night:
What immortal hand or eye,
Dare frame thy fearful symmetry?
— William Blake""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Tigers are dangerous", "The poet marvels at the tiger's terrifying beauty and its creator", "Tigers should be protected", "The tiger fears the lamb"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Humorous", "Awed and fearful", "Bored", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'symmetry' most nearly means", "choices": ["Color", "Balance", "Speed", "Loudness"], "correct": 1},
            {"type": "inference", "text": "What other animal does the speaker mention?", "choices": ["Lion", "Lamb", "Eagle", "Snake"], "correct": 1},
            {"type": "detail", "text": "What does the speaker question about the tiger?", "choices": ["Its diet", "Its creator", "Its habitat", "Its age"], "correct": 1},
            {"type": "purpose", "text": "Why repeat the first stanza at the end?", "choices": ["The poet forgot", "To emphasize the central question", "To fill space", "To change the subject"], "correct": 1}
        ]
    },
    # p7
    {
        "id": "p7",
        "title": "I Wandered Lonely as a Cloud",
        "passage": """I wandered lonely as a cloud
That floats on high o'er vales and hills,
When all at once I saw a crowd,
A host, of golden daffodils;
Beside the lake, beneath the trees,
Fluttering and dancing in the breeze.

Continuous as the stars that shine
And twinkle on the milky way,
They stretched in never-ending line
Along the margin of a bay:
Ten thousand saw I at a glance,
Tossing their heads in sprightly dance.

The waves beside them danced; but they
Out-did the sparkling waves in glee:
A poet could not but be gay,
In such a jocund company:
I gazed—and gazed—but little thought
What wealth the show to me had brought:

For oft, when on my couch I lie
In vacant or in pensive mood,
They flash upon that inward eye
Which is the bliss of solitude;
And then my heart with pleasure fills,
And dances with the daffodils.
— William Wordsworth""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Clouds are lonely", "The memory of daffodils brings joy during lonely moments", "Daffodils are the prettiest flowers", "The speaker prefers sitting on his couch"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood?", "choices": ["Angry", "Joyful and reflective", "Frightened", "Bored"], "correct": 1},
            {"type": "vocab", "text": "The word 'jocund' most nearly means", "choices": ["Sad", "Cheerful", "Silent", "Angry"], "correct": 1},
            {"type": "inference", "text": "What is the 'inward eye'?", "choices": ["A physical eye", "Memory and imagination", "A telescope", "A window"], "correct": 1},
            {"type": "detail", "text": "Where does the speaker see the daffodils?", "choices": ["In a garden", "Beside a lake", "On a mountain", "In a dream"], "correct": 1},
            {"type": "purpose", "text": "Why include the final stanza about being on his couch?", "choices": ["To show that nature's memory brings lasting happiness", "To complain about being tired", "To prove couches are better", "To change the subject"], "correct": 0}
        ]
    },
    # p8
    {
        "id": "p8",
        "title": "If (excerpt)",
        "passage": """If you can keep your head when all about you
Are losing theirs and blaming it on you,
If you can trust yourself when all men doubt you,
But make allowance for their doubting too;
If you can wait and not be tired by waiting,
Or being lied about, don't deal in lies,
Or being hated, don't give way to hating,
And yet don't look too good, nor talk too wise:

If you can dream—and not make dreams your master;
If you can think—and not make thoughts your aim;
If you can meet with Triumph and Disaster
And treat those two impostors just the same;
If you can bear to hear the truth you've spoken
Twisted by knaves to make a trap for fools,
Or watch the things you gave your life to, broken,
And stoop and build 'em up with worn-out tools:

If you can fill the unforgiving minute
With sixty seconds' worth of distance run,
Yours is the Earth and everything that's in it,
And—which is more—you'll be a Man, my son!
— Rudyard Kipling""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Winning is most important", "The poem describes qualities of a virtuous person: patience, self-trust, resilience", "Dreams should be avoided", "Only fathers give good advice"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Sarcastic", "Wise and encouraging", "Angry", "Childish"], "correct": 1},
            {"type": "vocab", "text": "The word 'impostors' most nearly means", "choices": ["Kings", "Fakes", "Friends", "Children"], "correct": 1},
            {"type": "inference", "text": "How does the speaker view Triumph and Disaster?", "choices": ["As permanent", "As equally temporary", "Triumph is better", "Disaster is worse"], "correct": 1},
            {"type": "detail", "text": "What should you do when people lie about you?", "choices": ["Lie back", "Not deal in lies", "Get angry", "Ignore everyone"], "correct": 1},
            {"type": "purpose", "text": "Who is the speaker addressing in the final line?", "choices": ["Himself", "His son", "The reader's father", "A teacher"], "correct": 1}
        ]
    },
    # p9
    {
        "id": "p9",
        "title": "O Captain! My Captain!",
        "passage": """O Captain! my Captain! our fearful trip is done,
The ship has weather'd every rack, the prize we sought is won,
The port is near, the bells I hear, the people all exulting,
While follow eyes the steady keel, the vessel grim and daring;
But O heart! heart! heart!
O the bleeding drops of red,
Where on the deck my Captain lies,
Fallen cold and dead.

O Captain! my Captain! rise up and hear the bells;
Rise up—for you the flag is flung—for you the bugle trills,
For you bouquets and ribbon'd wreaths—for you the shores a-crowding,
For you they call, the swaying mass, their eager faces turning;
Here Captain! dear father!
This arm beneath your head!
It is some dream that on the deck,
You've fallen cold and dead.

My Captain does not answer, his lips are pale and still,
My father does not feel my arm, he has no pulse nor will,
The ship is anchor'd safe and sound, its voyage closed and done,
From fearful trip the victor ship comes in with object won;
Exult O shores, and ring O bells!
But I with mournful tread,
Walk the deck my Captain lies,
Fallen cold and dead.
— Walt Whitman""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["A captain celebrates a voyage", "The poem mourns a captain who died just as victory was achieved", "Ships are dangerous", "The speaker is angry at the captain"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's emotion?", "choices": ["Joyful", "Grieving", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'exulting' most nearly means", "choices": ["Crying", "Rejoicing", "Sleeping", "Working"], "correct": 1},
            {"type": "inference", "text": "What is the relationship between speaker and captain?", "choices": ["Strangers", "Close (he calls him father)", "Enemies", "The captain doesn't know him"], "correct": 1},
            {"type": "detail", "text": "What happened to the captain?", "choices": ["He retired", "He is celebrating", "He died", "He left the ship"], "correct": 2},
            {"type": "purpose", "text": "Why is this poem an elegy?", "choices": ["It celebrates a wedding", "It mourns a death", "It describes a ship", "It is a love poem"], "correct": 1}
        ]
    },
    # p10
    {
        "id": "p10",
        "title": "Fire and Ice",
        "passage": """Some say the world will end in fire,
Some say in ice.
From what I've tasted of desire
I hold with those who favor fire.
But if it had to perish twice,
I think I know enough of hate
To say that for destruction ice
Is also great
And would suffice.
— Robert Frost""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The world will end in fire", "The world will end in ice", "Desire and hate are both powerful destructive forces", "The poet doesn't care how the world ends"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Cheerful", "Darkly contemplative", "Angry", "Long-winded"], "correct": 1},
            {"type": "vocab", "text": "The word 'suffice' most nearly means", "choices": ["Fail", "Be enough", "Destroy", "Burn"], "correct": 1},
            {"type": "inference", "text": "What do 'fire' and 'ice' represent metaphorically?", "choices": ["Summer and winter", "Desire and hate", "Sun and moon", "Good and evil"], "correct": 1},
            {"type": "detail", "text": "Which destruction does the speaker favor based on desire?", "choices": ["Ice", "Fire", "Neither", "Both"], "correct": 1},
            {"type": "purpose", "text": "Why is the poem so short?", "choices": ["The poet was in a hurry", "To pack powerful ideas into a compact form", "He couldn't think of more lines", "He doesn't believe the world will end"], "correct": 1}
        ]
    },
    # p11
    {
        "id": "p11",
        "title": "Still I Rise (excerpt)",
        "passage": """You may write me down in history
With your bitter, twisted lies,
You may trod me in the very dirt
But still, like dust, I'll rise.

Does my sassiness upset you?
Why are you beset with gloom?
‘Cause I walk like I've got oil wells
Pumping in my living room.

Just like moons and like suns,
With the certainty of tides,
Just like hopes springing high,
Still I'll rise.

Did you want to see me broken?
Bowed head and lowered eyes?
Shoulders falling down like teardrops,
Weakened by my soulful cries?

Out of the huts of history's shame
I rise
Up from a past that's rooted in pain
I rise
I'm a black ocean, leaping and wide,
Welling and swelling I bear in the tide.

Leaving behind nights of terror and fear
I rise
Into a daybreak that's wondrously clear
I rise
Bringing the gifts that my ancestors gave,
I am the dream and the hope of the slave.
I rise
I rise
I rise.
— Maya Angelou""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker is sad", "The speaker celebrates her resilience and rises above oppression", "Rising is physically difficult", "History is always accurate"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Defeated", "Defiant and proud", "Angry", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The word 'beset' most nearly means", "choices": ["Confused", "Troubled", "Happy", "Sleepy"], "correct": 1},
            {"type": "inference", "text": "Who is the speaker addressing?", "choices": ["A friend", "Someone who tried to oppress her", "A child", "Herself only"], "correct": 1},
            {"type": "detail", "text": "What natural phenomena does she compare her rising to?", "choices": ["Earthquakes", "Moons, suns, and tides", "Rainstorms", "Volcanoes"], "correct": 1},
            {"type": "purpose", "text": "Why repeat 'I rise' multiple times at the end?", "choices": ["She forgot", "To emphasize resilience and create a powerful conclusion", "To fill space", "To show she is tired"], "correct": 1}
        ]
    },
    # p12
    {
        "id": "p12",
        "title": "Sonnet 18",
        "passage": """Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date;
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature's changing course untrimm'd;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow'st;
Nor shall death brag thou wander'st in his shade,
When in eternal lines to time thou grow'st:
So long as men can breathe or eyes can see,
So long lives this, and this gives life to thee.
— William Shakespeare""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this sonnet?", "choices": ["Summer is the best season", "The beloved is more beautiful than summer, and the poem grants immortality", "All beautiful things fade forever", "Shakespeare disliked summer"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Admiring", "Jealous", "Angry", "Bored"], "correct": 0},
            {"type": "vocab", "text": "The word 'temperate' most nearly means", "choices": ["Hot", "Cold", "Mild", "Windy"], "correct": 2},
            {"type": "inference", "text": "How can the beloved achieve immortality?", "choices": ["Through children", "Through fame", "Through this poem", "By living forever"], "correct": 2},
            {"type": "detail", "text": "What does the speaker say about summer's duration?", "choices": ["It lasts forever", "It's too short", "It's too hot", "It never arrives"], "correct": 1},
            {"type": "purpose", "text": "What is the function of the final couplet?", "choices": ["To change the subject", "To conclude that the poem gives life to the beloved", "To criticize summer", "To ask a question"], "correct": 1}
        ]
    },
    # p13
    {
        "id": "p13",
        "title": "Because I could not stop for Death",
        "passage": """Because I could not stop for Death –
He kindly stopped for me –
The Carriage held but just Ourselves –
And Immortality.

We slowly drove – He knew no haste
And I had put away
My labor and my leisure too,
For His Civility –

We passed the School, where Children strove
At Recess – in the Ring –
We passed the Fields of Gazing Grain –
We passed the Setting Sun –

Or rather – He passed Us –
The Dews drew quivering and Chill –
For only Gossamer, my Gown –
My Tippet – only Tulle –

We paused before a House that seemed
A Swelling of the Ground –
The Roof was scarcely visible –
The Cornice – in the Ground –

Since then – 'tis Centuries – and yet
Feels shorter than the Day
I first surmised the Horses' Heads
Were toward Eternity –
— Emily Dickinson""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker describes a car accident", "Death is personified as a gentleman taking the speaker toward eternity", "The speaker fears death", "The speaker outruns death"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone toward death?", "choices": ["Terrified", "Calm and accepting", "Angry", "Humorous"], "correct": 1},
            {"type": "vocab", "text": "The word 'surmised' most nearly means", "choices": ["Guessed", "Saw", "Heard", "Forgot"], "correct": 0},
            {"type": "inference", "text": "What is the 'House' in stanza 5?", "choices": ["A real house", "A grave", "A school", "A church"], "correct": 1},
            {"type": "detail", "text": "What season or time is suggested in stanza 4?", "choices": ["Midnight", "Sunset and cool evening", "Morning", "Noon"], "correct": 1},
            {"type": "purpose", "text": "Why personify Death as 'kindly'?", "choices": ["To make death less frightening", "To argue death is a person", "To prove death is evil", "To describe a funeral"], "correct": 0}
        ]
    },
    # p14
    {
        "id": "p14",
        "title": "The Raven (excerpt)",
        "passage": """Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore—
While I nodded, nearly napping, suddenly there came a tapping,
As of some one gently rapping, rapping at my chamber door.
“’Tis some visitor,” I muttered, “tapping at my chamber door—
            Only this and nothing more.”

Ah, distinctly I remember it was in the bleak December;
And each separate dying ember wrought its ghost upon the floor.
Eagerly I wished the morrow;—vainly I had sought to borrow
From my books surcease of sorrow—sorrow for the lost Lenore—
For the rare and radiant maiden whom the angels name Lenore—
            Nameless here for evermore.

And the silken, sad, uncertain rustling of each purple curtain
Thrilled me—filled me with fantastic terrors never felt before;
So that now, to still the beating of my heart, I stood repeating
“’Tis some visitor entreating entrance at my chamber door—
Some late visitor entreating entrance at my chamber door;—
            This it is and nothing more.”

Open here I flung the shutter, when, with many a flirt and flutter,
In there stepped a stately Raven of the saintly days of yore;
Not the least obeisance made he; not a minute stopped or stayed he;
But, with mien of lord or lady, perched above my chamber door—
Perched upon a bust of Pallas just above my chamber door—
            Perched, and sat, and nothing more.

Then this ebony bird beguiling my sad fancy into smiling,
By the grave and stern decorum of the countenance it wore,
“Though thy crest be shorn and shaven, thou,” I said, “art sure no craven,
Ghastly grim and ancient Raven wandering from the Nightly shore—
Tell me what thy lordly name is on the Night's Plutonian shore!”
            Quoth the Raven “Nevermore.”""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this excerpt?", "choices": ["A student meets a talking bird that says 'Nevermore,' deepening his grief", "The raven can say many words", "The speaker is happy", "The poem is about summer"], "correct": 0},
            {"type": "tone", "text": "Which word best describes the mood?", "choices": ["Joyful", "Melancholy and eerie", "Excited", "Boring"], "correct": 1},
            {"type": "vocab", "text": "The word 'surcease' most nearly means", "choices": ["Increase", "Relief", "Celebration", "Beginning"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about Lenore?", "choices": ["She is a lost loved one who died", "She is a bird", "She is the speaker's enemy", "She is the raven's name"], "correct": 0},
            {"type": "detail", "text": "What word does the raven repeatedly say?", "choices": ["Lenore", "Nevermore", "Forever", "Chamber"], "correct": 1},
            {"type": "purpose", "text": "Why use a raven instead of another bird?", "choices": ["Ravens are colorful", "Ravens symbolize ill omen and death", "Ravens are the only talking birds", "He saw one that morning"], "correct": 1}
        ]
    },
    # p15
    {
        "id": "p15",
        "title": "Invictus",
        "passage": """Out of the night that covers me,
      Black as the pit from pole to pole,
I thank whatever gods may be
      For my unconquerable soul.

In the fell clutch of circumstance
      I have not winced nor cried aloud.
Under the bludgeonings of chance
      My head is bloody, but unbowed.

Beyond this place of wrath and tears
      Looms but the Horror of the shade,
And yet the menace of the years
      Finds and shall find me unafraid.

It matters not how strait the gate,
      How charged with punishments the scroll,
I am the master of my fate,
      I am the captain of my soul.
— William Ernest Henley""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker is sad", "The speaker declares control over his own spirit despite suffering", "Fate controls everything", "The speaker prays for help"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's attitude?", "choices": ["Defeated", "Defiant and strong", "Carefree", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'fell' most nearly means", "choices": ["Friendly", "Cruel", "Fallen", "Soft"], "correct": 1},
            {"type": "inference", "text": "What does 'My head is bloody, but unbowed' suggest?", "choices": ["He is injured but refuses to submit", "He is completely healthy", "He is dead", "He is angry at a barber"], "correct": 0},
            {"type": "detail", "text": "What does the speaker call his soul in the first stanza?", "choices": ["Broken", "Unconquerable", "Afraid", "Lost"], "correct": 1},
            {"type": "purpose", "text": "Why did Henley write this poem?", "choices": ["To complain", "To inspire inner strength and self-mastery", "To describe night", "To pray"], "correct": 1}
        ]
    },
    # p16
    {
        "id": "p16",
        "title": "The New Colossus",
        "passage": """Not like the brazen giant of Greek fame,
With conquering limbs astride from land to land;
Here at our sea-washed, sunset gates shall stand
A mighty woman with a torch, whose flame
Is the imprisoned lightning, and her name
Mother of Exiles. From her beacon-hand
Glows world-wide welcome; her mild eyes command
The air-bridged harbor that twin cities frame.

“Keep, ancient lands, your storied pomp!” cries she
With silent lips. “Give me your tired, your poor,
Your huddled masses yearning to breathe free,
The wretched refuse of your teeming shore.
Send these, the homeless, tempest-tost to me,
I lift my lamp beside the golden door!”
— Emma Lazarus (inscribed on the Statue of Liberty)""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this sonnet?", "choices": ["The Statue of Liberty is a weapon", "The statue welcomes immigrants as symbols of refuge and freedom", "Ancient Greece was better", "The statue is made of brazen giant"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the statue's speech?", "choices": ["Harsh", "Welcoming", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'teeming' most nearly means", "choices": ["Empty", "Crowded", "Quiet", "Distant"], "correct": 1},
            {"type": "inference", "text": "What is the 'brazen giant of Greek fame'?", "choices": ["The Colossus of Rhodes (symbol of conquest)", "A famous American statue", "A bird", "A war ship"], "correct": 0},
            {"type": "detail", "text": "Whom does the statue call to come to America?", "choices": ["Only the wealthy", "Only scientists", "The tired, poor, huddled masses", "Only citizens"], "correct": 2},
            {"type": "purpose", "text": "Why is this poem inscribed on the Statue of Liberty?", "choices": ["To advertise tourism", "To define America as a nation of immigrants and refuge", "To scare immigrants", "To describe construction"], "correct": 1}
        ]
    },
    # p17
    {
        "id": "p17",
        "title": "Do Not Go Gentle into That Good Night",
        "passage": """Do not go gentle into that good night,
Old age should burn and rave at close of day;
Rage, rage against the dying of the light.

Though wise men at their end know dark is right,
Because their words had forked no lightning they
Do not go gentle into that good night.

Good men, the last wave by, crying how bright
Their frail deeds might have danced in a green bay,
Rage, rage against the dying of the light.

Wild men who caught and sang the sun in flight,
And learn, too late, they grieved it on its way,
Do not go gentle into that good night.

Grave men, near death, who see with blinding sight
Blind eyes could blaze like meteors and be gay,
Rage, rage against the dying of the light.

And you, my father, there on the sad height,
Curse, bless, me now with your fierce tears, I pray.
Do not go gentle into that good night.
Rage, rage against the dying of the light.
— Dylan Thomas""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this poem?", "choices": ["Death should be accepted peacefully", "The speaker urges his father to fight fiercely against death", "Old age is boring", "Light is better than night"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the poem's tone?", "choices": ["Calm", "Fierce and urgent", "Humorous", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The phrase 'that good night' is a metaphor for", "choices": ["Sleep", "Death", "Evening", "Darkness"], "correct": 1},
            {"type": "inference", "text": "What is the speaker's relationship with his father?", "choices": ["Strangers", "He loves him and pleads with him to fight death", "He hates him", "The father is already dead"], "correct": 1},
            {"type": "detail", "text": "What should men do against 'the dying of the light'?", "choices": ["Sleep", "Rage", "Sing", "Cry"], "correct": 1},
            {"type": "purpose", "text": "Why repeat the two lines throughout?", "choices": ["He forgot", "The villanelle form requires repetition for emphasis", "To fill space", "To make it easier to memorize"], "correct": 1}
        ]
    },
    # p18
    {
        "id": "p18",
        "title": "Phenomenal Woman (excerpt)",
        "passage": """Pretty women wonder where my secret lies.
I'm not cute or built to suit a fashion model's size
But when I start to tell them,
They think I'm telling lies.
I say,
It's in the reach of my arms,
The span of my hips,
The stride of my step,
The curl of my lips.
I'm a woman
Phenomenally.
Phenomenal woman,
That's me.

I walk into a room
Just as cool as you please,
And to a man,
The fellows stand or
Fall down on their knees.
Then they swarm around me,
A hive of honey bees.
I say,
It's the fire in my eyes,
And the flash of my teeth,
The swing in my waist,
And the joy in my feet.
I'm a woman
Phenomenally.
Phenomenal woman,
That's me.

Now you understand
Just why my head's not bowed.
I don't shout or jump about
Or have to talk real loud.
When you see me passing,
It ought to make you proud.
I say,
It's in the click of my heels,
The bend of my hair,
the palm of my hand,
The need for my care.
'Cause I'm a woman
Phenomenally.
Phenomenal woman,
That's me.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker is arrogant", "The speaker celebrates her confidence and inner beauty", "All women should be models", "Men are foolish"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Insecure", "Confident and proud", "Angry", "Sad"], "correct": 1},
            {"type": "vocab", "text": "The word 'phenomenally' most nearly means", "choices": ["Boringly", "Remarkably", "Quietly", "Sadly"], "correct": 1},
            {"type": "inference", "text": "Why do 'pretty women' wonder where her secret lies?", "choices": ["They are jealous of her confidence", "They want to be her friend", "They hate her", "They don't notice her"], "correct": 0},
            {"type": "detail", "text": "Where does the speaker's power come from?", "choices": ["Her money", "Her physical features and inner confidence", "Her fame", "Her clothes"], "correct": 1},
            {"type": "purpose", "text": "Why did Angelou write this poem?", "choices": ["To criticize models", "To celebrate women's confidence and redefine beauty", "To make men feel bad", "To describe a party"], "correct": 1}
        ]
    },
    # p19
    {
        "id": "p19",
        "title": "The Cremation of Sam McGee (excerpt)",
        "passage": """There are strange things done in the midnight sun
By the men who moil for gold;
The Arctic trails have their secret tales
That would make your blood run cold;
The Northern Lights have seen queer sights,
But the queerest they ever did see
Was that night on the marge of Lake Lebarge
I cremated Sam McGee.

Now Sam McGee was from Tennessee, where the cotton blooms and blows.
Why he left his home in the South to roam 'round the Pole, God only knows.
He was always cold, but the land of gold seemed to hold him like a spell;
Though he'd often say in his homely way that "he'd sooner live in hell."
On a Christmas Day we were mushing our way over the Dawson trail.
Talk of your cold! through the parka's fold it stabbed like a driven nail.
If our eyes we'd close, then the lashes froze till sometimes we couldn't see;
It wasn't much fun, but the only one to whimper was Sam McGee.

And that very night, as we lay packed tight in our robes beneath the snow,
And the dogs were fed, and the stars o'erhead were dancing heel and toe,
He turned to me, and "Cap," says he, "I'll cash in this trip, I guess;
And if I do, I'm asking that you won't refuse my last request."
Well, he seemed so low that I couldn't say no; then he says with a sort of moan:
"It's the cursèd cold, and it's got right hold till I'm chilled clean through to the bone.
Yet 'tain't being dead—it's my awful dread of the icy grave that pains;
So I want you to swear that, foul or fair, you'll cremate my last remains."

A pal's last need is a thing to heed, so I swore I would not fail;
And we started on at the streak of dawn; but God! he looked ghastly pale.
He crouched on the sleigh, and he raved all day of his home in Tennessee;
And before nightfall a corpse was all that was left of Sam McGee.
— Robert W. Service""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this excerpt?", "choices": ["Gold mining is easy", "The speaker promises to cremate Sam McGee, who dies from extreme cold", "Sam McGee returns home", "Cremation is illegal"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood?", "choices": ["Cheerful", "Eerie and grim", "Romantic", "Boring"], "correct": 1},
            {"type": "vocab", "text": "The word 'moil' most nearly means", "choices": ["Rest", "Work hard", "Sing", "Travel"], "correct": 1},
            {"type": "inference", "text": "Why is Sam McGee afraid of an 'icy grave'?", "choices": ["He hates cold", "He is claustrophobic", "He wants to be buried at sea", "He fears ghosts"], "correct": 0},
            {"type": "detail", "text": "Where did Sam McGee come from?", "choices": ["Alaska", "Tennessee", "Canada", "Norway"], "correct": 1},
            {"type": "purpose", "text": "Why use dialect like 'Cap' and 'cursèd cold'?", "choices": ["To feel authentic to the Yukon setting", "To confuse readers", "The poet didn't know English", "To rhyme more easily"], "correct": 0}
        ]
    },
    # p20
    {
        "id": "p20",
        "title": "We Wear the Mask",
        "passage": """We wear the mask that grins and lies,
It hides our cheeks and shades our eyes,—
This debt we pay to human guile;
With torn and bleeding hearts we smile,
And mouth with myriad subtleties.

Why should the world be over-wise,
In counting all our tears and sighs?
Nay, let them only see us, while
We wear the mask.

We smile, but, O great Christ, our cries
To thee from tortured souls arise.
We sing, but oh the clay is vile
Beneath our feet, and long the mile;
But let the world dream otherwise,
We wear the mask!
— Paul Laurence Dunbar""",
        "questions": [
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Masks are fashionable", "The speaker describes how oppressed people hide pain behind a smiling mask", "Everyone should show true feelings", "Smiling is always good"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Joyful", "Bitter and sorrowful", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'myriad' most nearly means", "choices": ["One", "Countless", "Simple", "Loud"], "correct": 1},
            {"type": "inference", "text": "Why shouldn't the world see 'our tears and sighs'?", "choices": ["The world wouldn't understand", "The speaker is ashamed", "Tears are ugly", "No one cries"], "correct": 0},
            {"type": "detail", "text": "What does the mask do according to line 1?", "choices": ["Makes people angry", "Grins and lies", "Cries", "Is made of clay"], "correct": 1},
            {"type": "purpose", "text": "Why repeat 'We wear the mask'?", "choices": ["He forgot", "To emphasize forced concealment of suffering", "To describe a party", "To argue masks are fun"], "correct": 1}
        ]
    }
]
}




# ======================
# READING COMPREHENSION GENERATOR 
# ======================

def gen_reading_comprehension(category=None, n=1):
    """
    Generate reading comprehension questions.
    category: 'nonfiction', 'fiction', 'poetry', or None for random
    n: number of passages (will return passage + 6 questions per passage)
    Returns a list where each item is (passage_text, list_of_6_question_tuples)
    """
    import random as rand
    
    all_passages = []
    if category == 'nonfiction':
        all_passages = reading_passages['nonfiction'][:]
    elif category == 'fiction':
        all_passages = reading_passages['fiction'][:]
    elif category == 'poetry':
        all_passages = reading_passages['poetry'][:]
    else:
        all_passages = (reading_passages['nonfiction'] + 
                       reading_passages['fiction'] + 
                       reading_passages['poetry'])[:]
    
    if n > len(all_passages):
        n = len(all_passages)
    
    selected = rand.sample(all_passages, n)
    results = []
    
    for passage_data in selected:
        # Format passage with title (no button text)
        formatted_passage = f"<div style='background:#f0f4fa; padding:16px; border-radius:12px; margin-bottom:20px;'><b>📖 {passage_data['title']}</b><br><br>{passage_data['passage']}</div>"
        
        # Generate 6 questions for this passage
        questions_for_passage = []
        for q in passage_data['questions']:
            question_text = q['text']
            choices = q['choices']
            correct = q['correct']
            questions_for_passage.append((question_text, choices, correct))
        
        # Store as a tuple: (passage_text, list_of_question_tuples)
        results.append((formatted_passage, questions_for_passage))
    
    return results



# ======================
# ANALOGY GENERATOR FUNCTION (no duplicates)
# ======================

_analogy_index = 0
_shuffled_analogies = None

def gen_analogies(n=10):
    global _analogy_index, _shuffled_analogies

    if _shuffled_analogies is None:
        _shuffled_analogies = analogy_templates[:]
        random.shuffle(_shuffled_analogies)

    if n > len(_shuffled_analogies):
        raise ValueError("Requested number of questions exceeds available analogy templates.")

    questions = []

    # build a giant cross-category distractor bank using the renamed dictionary
    all_distractors = []
    for words in analogy_distractor_bank.values():
        for w in words:
            if isinstance(w, str) and w.isalpha():
                all_distractors.append(w)

    for _ in range(n):
        # Reset after full cycle
        if _analogy_index >= len(_shuffled_analogies):
            random.shuffle(_shuffled_analogies)
            _analogy_index = 0

        A, B, C, correct_D, category = _shuffled_analogies[_analogy_index]
        _analogy_index += 1

        forbidden = {A, B, C, correct_D}

        mixed_pool = [w for w in all_distractors if w not in forbidden]

        if len(mixed_pool) < 4:
            # Fallback: add some generic distractors if pool is too small
            fallback = ["Apple", "Blue", "Large", "Quick", "Round"]
            mixed_pool.extend([f for f in fallback if f not in forbidden])

        wrongs = random.sample(mixed_pool, 4)
        choices = wrongs + [correct_D]
        random.shuffle(choices)

        correct_index = choices.index(correct_D)
        question_text = f"{A} : {B} :: {C} : ?"

        questions.append((question_text, choices, correct_index))

    return questions


# ======================
# QUANTITATIVE GENERATOR FUNCTIONS
# ======================


def gen_number_sense_arithmetic(n=10):
    """
    Generate n number sense & arithmetic questions for SSAT middle level.
    Question types:
    1) Add/Subtract fractions or decimals
    2) Multi-step problem with factors, multiples, or divisibility
    3) Order of operations with four integers (one negative)
    4) Ratio or percent word problem
    5) Multi-step arithmetic word problem
    
    The types cycle evenly:
    - n=5 → one of each type
    - n=10 → two of each type, etc.
    
    Returns a list of tuples: (question_text, choices, correct_index)
    """
    questions = []
    types = [1, 2, 3, 4, 5]

    for i in range(n):
        q_type = types[i % len(types)]  # cycle through question types

        if q_type == 1:  # fraction or decimal addition/subtraction
        
            if random.random() < 0.5:
                # ---------- FRACTIONS ----------
                a = Fraction(random.randint(1, 9), random.randint(2, 10))
                b = Fraction(random.randint(1, 9), random.randint(2, 10))
                op = random.choice(["+", "-"])

                # Prevent negative results
                if op == "-" and b > a:
                    a, b = b, a

                answer = a + b if op == "+" else a - b
                if answer <= 0:
                    answer = abs(answer)

                expr = f"{a} {op} {b}"
                answer = answer.limit_denominator()

                answer_str = (
                    str(answer.numerator)
                    if answer.denominator == 1
                    else f"{answer.numerator}/{answer.denominator}"
                )

                # Generate unique positive distractors
                distractors = set()
                while len(distractors) < 4:
                    delta = Fraction(random.choice([1, 2, 3]), random.randint(2, 6))
                    distractor = answer + random.choice([-delta, delta])
                    if distractor > 0 and distractor != answer:
                        d = distractor.limit_denominator()
                        s = (
                            str(d.numerator)
                            if d.denominator == 1
                            else f"{d.numerator}/{d.denominator}"
                        )
                        distractors.add(s)

                choices = list(distractors) + [answer_str]

            else:
                # ---------- DECIMALS ----------
                a = round(random.uniform(1, 20), 2)
                b = round(random.uniform(1, 20), 2)
                op = random.choice(["+", "-"])

                # Prevent negative results
                if op == "-" and b > a:
                    a, b = b, a

                answer = round(a + b, 2) if op == "+" else round(a - b, 2)
                if answer <= 0:
                    answer = round(abs(answer), 2)

                expr = f"{a} {op} {b}"
                answer_str = f"{answer:.2f}"

                # Generate unique positive distractors
                distractors = set()
                while len(distractors) < 4:
                    delta = round(random.uniform(0.5, 5), 2)
                    distractor = round(answer + random.choice([-delta, delta]), 2)
                    if distractor > 0 and distractor != answer:
                        distractors.add(f"{distractor:.2f}")

                choices = list(distractors) + [answer_str]

            random.shuffle(choices)
            correct_index = choices.index(answer_str)
            question_text = f"Solve: {expr}"

        elif q_type == 2:  # factors, multiples, divisibility
            factor = random.randint(2, 12)
            answer_multiplier = random.randint(2, 6)
            answer = factor * answer_multiplier
            Y = factor
            X = answer * random.randint(2, 5)

            distractors_set = set()
            while len(distractors_set) < 4:
                variation = random.choice([-factor*2, -factor, -1, 1, factor, factor*2])
                distractor = answer + variation
                if distractor <= 0 or distractor == answer:
                    continue
                is_factor_of_X = (X % distractor == 0)
                is_multiple_of_Y = (distractor % Y == 0)
                if not (is_factor_of_X and is_multiple_of_Y):
                    distractors_set.add(distractor)

            choices = list(distractors_set) + [answer]
            random.shuffle(choices)
            correct_index = choices.index(answer)
            question_text = f"Which number is a factor of {X} and a multiple of {Y}?"

        elif q_type == 3:  # order of operations
            superscript_2 = "²"

            while True:
                # 4 numbers
                nums = random.sample(range(2, 10), 4)

                # 3 distinct binary operations
                ops = random.sample(["+", "-", "×", "÷"], 3)

                # Choose which number is squared
                square_index = random.randint(0, 3)

                display = []
                eval_tokens = []

                for i in range(4):
                    n = nums[i]

                    # Apply square
                    if i == square_index:
                        display.append(f"{n}{superscript_2}")
                        eval_tokens.append(f"({n}**2)")
                    else:
                        display.append(str(n))
                        eval_tokens.append(str(n))

                    # Add operator between numbers
                    if i < 3:
                        op = ops[i]
                        display.append(op)

                        if op == "×":
                            eval_tokens.append("*")
                        elif op == "÷":
                            eval_tokens.append("/")
                        else:
                            eval_tokens.append(op)

                # Evaluate ONCE (preserves PEMDAS)
                try:
                    result = eval(" ".join(eval_tokens))
                except ZeroDivisionError:
                    continue

                # Positive integer answers only
                if isinstance(result, (int, float)) and result > 0 and result == int(result):
                    question_text = f"Evaluate: {' '.join(display)}"
                    answer = int(result)

                    # Generate distractors
                    choices = set()
                    choices.add(answer)

                    while len(choices) < 5:
                        delta = random.randint(-10, 10)
                        if delta != 0:
                            choices.add(answer + delta)

                    choices = list(choices)
                    random.shuffle(choices)

                    correct_index = choices.index(answer)
                    break
        elif q_type == 4:  # ratio or percent word problem

            # allowed totals
            allowed_totals = [5, 10, 20, 25, 50, 200, 300, 400]

            # choose a total
            total = random.choice(allowed_totals)

            # generate a percent that gives a whole number of students
            possible_percents = [p for p in range(10, 91) if (p * total) % 100 == 0]
            percent = random.choice(possible_percents)

            # calculate the number of students
            part = (percent * total) // 100

            # generate distractors
            distractors = set()
            while len(distractors) < 4:
                variation = random.choice([-15, -10, -5, 5, 10, 15])
                distractor = percent + variation
                if 1 <= distractor <= 100 and distractor != percent:
                    distractors.add(distractor)

            # prepare choices and shuffle
            choices = list(distractors) + [percent]
            random.shuffle(choices)

            # store the correct index
            correct_index = choices.index(percent)

            # create the question
            question_text = f"{part} out of {total} students passed the test. What percent passed?"

        elif q_type == 5:  # multi-step word problem
            a = random.randint(10,40)
            b = random.randint(2,5)
            c = random.randint(5,15)
            d = random.randint(3,12)
            answer = (a*b) + (c*d)
            answer_str = str(answer)
            distractors = set()
            while len(distractors) < 4:
                distractor = answer + random.choice([-5,-3,3,4,5])
                if distractor != answer:
                    distractors.add(str(distractor))
            choices = list(distractors) + [answer_str]
            random.shuffle(choices)
            correct_index = choices.index(answer_str)
            question_text = f"There are {a} boxes with {b} apples each and there are {c} boxes with {d} oranges each. How many fruit are in the boxes in total?"

        questions.append((question_text, choices, correct_index))

    return questions


def gen_algebraic_thinking(n=5):
    """
    Generate n algebraic thinking questions for SSAT middle level.
    Cycles through 5 types of problems:
    1) Two-step algebraic equation (x or y)
    2) Simplifying algebraic expressions
    3) Algebraic inequality (select correct value)
    4) Word problem translating to an equation
    5) Word problem with three people, sum of expressions
    Returns a list of tuples: (question_text, choices, correct_index)
    """
    questions = []
    types = [1, 2, 3, 4, 5]

    for i in range(n):
        q_type = types[i % len(types)]  # cycle through 1-5

        if q_type == 1:  # Two-step algebraic equation

            a = random.randint(2, 10)
            b = random.randint(1, 20)
            x = random.randint(1, 20)

            if random.choice([True, False]):
                result = a * x + b
                eq = f"{a}x + {b} = {result}"
            else:
                result = a * x - b
                eq = f"{a}x - {b} = {result}"

            question_text = f"Solve for x:<br><br>{eq}"
            correct = x

            distractors = set()
            offsets = [-3, -2, -1, 1, 2, 3]

            while len(distractors) < 4:
                choice = correct + random.choice(offsets)
                if choice > 0:
                    distractors.add(choice)

            choices = list(distractors) + [correct]
            random.shuffle(choices)
            correct_index = choices.index(correct)

        elif q_type == 2:  # Simplifying algebraic expression

            a = random.randint(2, 6)
            b = random.randint(1, 10)
            c = random.randint(1, 10)

            include_var = random.choice([True, False])
            sign1 = random.choice(["+", "-"])
            sign2 = random.choice(["+", "-"])

            # Determine coefficients and constant
            if include_var:
                outside_coeff = random.randint(2, 5)  # never 1
                x_coeff = a + (outside_coeff if sign1 == "+" else -outside_coeff)
                const_total = a * b + (c if sign2 == "+" else -c)
                expr = f"{a}(x + {b}) {sign1} {outside_coeff}x {sign2} {c}"
            else:
                x_coeff = a
                const_total = a * b + (c if sign1 == "+" else -c) + (b if sign2 == "+" else -b)
                expr = f"{a}(x + {b}) {sign1} {c} {sign2} {b}"

            # Build final answer string
            answer = ""
            if x_coeff != 0:
                if x_coeff == 1:
                    answer += "x"
                elif x_coeff == -1:
                    answer += "-x"
                else:
                    answer += f"{x_coeff}x"

            if const_total != 0:
                if answer:
                    answer += f" + {const_total}" if const_total > 0 else f" - {abs(const_total)}"
                else:
                    answer += f"{const_total}"

            # Generate distractors
            distractors = set()
            while len(distractors) < 4:
                dx = random.choice([-2, -1, 1, 2])
                dc = random.choice([-2, -1, 1, 2])
                nx = x_coeff + dx
                nc = const_total + dc

                choice = ""
                if nx != 0:
                    if nx == 1:
                        choice += "x"
                    elif nx == -1:
                        choice += "-x"
                    else:
                        choice += f"{nx}x"
                if nc != 0:
                    if choice:
                        choice += f" + {nc}" if nc > 0 else f" - {abs(nc)}"
                    else:
                        choice += f"{nc}"

                if choice != answer:
                    distractors.add(choice)

            choices = list(distractors) + [answer]
            random.shuffle(choices)
            correct_index = choices.index(answer)

            question_text = f"Simplify the expression:<br><br>{expr}"

        elif q_type == 3:  # Algebraic inequality - FIXED with <br> tags

            a = random.randint(2, 10)

            # Randomly decide + or - for constant term
            sign_b = random.choice(["+", "-"])
            b_val = random.randint(1, 20)
            b = b_val if sign_b == "+" else -b_val

            c = random.randint(10, 50)

            # Randomly choose inequality
            ineq_sign = random.choice(["<", ">"])
            inequality = f"{a}x {'+' if b >=0 else '-'} {abs(b)} {ineq_sign} {c}"

            # Compute solution boundary
            if ineq_sign == "<":
                # a*x + b < c -> a*x < c - b -> x < (c - b)/a
                boundary = (c - b) / a
                correct = math.floor(boundary)
                # Correct x <= floor(boundary)
                # Distractors must be > boundary
                distractors = set()
                distractors.add(correct + 1)  # tricky distractor, just outside
                while len(distractors) < 4:
                    val = correct + random.randint(2, 5)
                    distractors.add(val)
            else:
                # a*x + b > c -> a*x > c - b -> x > (c - b)/a
                boundary = (c - b) / a
                correct = math.ceil(boundary)
                # Correct x >= ceil(boundary)
                # Distractors must be < boundary
                distractors = set()
                distractors.add(correct - 1)  # tricky distractor, just below
                while len(distractors) < 4:
                    val = correct - random.randint(2, 5)
                    distractors.add(val)

            choices = list(distractors) + [correct]
            random.shuffle(choices)
            correct_index = choices.index(correct)

            # FIXED: Use <br> instead of \n for HTML line break
            question_text = f"Which value of x satisfies the inequality?<br><br>{inequality}"

        elif q_type == 4:  # Word problem translating to equation
            # Decide if we multiply or divide
            op = random.choice(["*", "/"])
            add_sub = random.choice(["+", "-"])

            # Choose mystery number x
            x = random.randint(2, 10)

            # Choose multiplier/divisor ensuring integer results
            if op == "*":
                multiplier = random.randint(2, 5)
                result_after_op = x * multiplier
                op_text = f"multiplied by {multiplier}"
            else:
                # Ensure x * divisor gives integer
                divisor = random.randint(2, 5)
                x = x * divisor  # adjust x so division is integer
                result_after_op = x // divisor
                op_text = f"divided by {divisor}"

            # Choose add/sub number
            num = random.randint(1, 20)
            if add_sub == "+":
                total = result_after_op + num
                action_text = f"increased by {num}"
            else:
                total = result_after_op - num
                action_text = f"decreased by {num}"

            # Create question text
            question_text = f"A number is {op_text} and then {action_text}. The result is {total}. What is the number?"

            # Correct answer
            correct = x

            # Generate distractors
            distractors = set()
            # 1 distractor very close
            distractors.add(correct + 1 if random.choice([True, False]) else correct - 1)

            while len(distractors) < 4:
                offset = random.randint(2, 4)
                val = correct + offset if random.choice([True, False]) else correct - offset
                if val != correct and val > 0:
                    distractors.add(val)

            choices = list(distractors) + [correct]
            random.shuffle(choices)
            correct_index = choices.index(correct)

        elif q_type == 5:  # Three people algebraic sum
            
            x = random.randint(1, 20)
            y_offset = random.randint(5, 20)
            z_offset = random.randint(1, 10)
            question_text = (
                f"Mason has x cards, Russ has x + {y_offset} cards, and Sam has {z_offset} less than Russ. "
                f"In terms of x, how many cards do they have in total?"
            )
            # sum expression: x + (x + y_offset) + (x + y_offset - z_offset) = 3x + 2*y_offset - z_offset
            answer_expr = f"3x + {2*y_offset - z_offset}"
            choices = set([
                f"3x + {2*y_offset - z_offset + 1}",
                f"3x + {2*y_offset - z_offset - 1}",
                f"3x + {y_offset - z_offset}",
                f"2x + {2*y_offset - z_offset}"
            ])
            choices = list(choices) + [answer_expr]
            random.shuffle(choices)
            correct_index = choices.index(answer_expr)

        # Append the question tuple
        questions.append((question_text, [str(ch) for ch in choices], correct_index))

    return questions


## Scalar Vector Graphics Generator

def get_triangle_svg(base, height):
    """Generate SVG for a triangle with given base and height"""
    return f'''<svg width="200" height="160" viewBox="0 0 200 160" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <polygon points="100,20 20,130 180,130" fill="#cce5ff" stroke="#006" stroke-width="2"/>
    <line x1="100" y1="20" x2="100" y2="130" stroke="#c33" stroke-width="1.5" stroke-dasharray="4,4"/>
    <line x1="20" y1="130" x2="180" y2="130" stroke="#c33" stroke-width="1.5"/>
    <text x="108" y="80" font-size="13" fill="#c33">h = {height}</text>
    <text x="75" y="148" font-size="13" fill="#c33">b = {base}</text>
    <text x="80" y="15" font-size="14" fill="#006" font-weight="bold">Triangle</text>
</svg>'''


def get_circle_svg(radius=None, diameter=None):
    """
    Generate SVG for a circle.
    Pass EITHER radius OR diameter (not both).
    The visual diagram will match the verbal description.
    
    Examples:
        get_circle_svg(radius=5)   # Diagram shows r = 5
        get_circle_svg(diameter=10) # Diagram shows d = 10
    """
    if radius is None and diameter is None:
        raise ValueError("Must provide either radius or diameter")
    if radius is not None and diameter is not None:
        raise ValueError("Provide only one: radius OR diameter, not both")
    
    # Calculate radius for drawing (scaled for visibility)
    if radius is not None:
        r_value = radius
        label_type = "r"
        label_text = f"r = {r_value}"
    else:
        r_value = diameter / 2
        label_type = "d"
        label_text = f"d = {diameter}"
    
    # 100% larger dimensions (doubled from original)
    # Original: width=220, height=180, cx=100, cy=85
    # New: width=440, height=360, cx=200, cy=170
    width = 440
    height = 360
    cx = 200
    cy = 170
    
    # Scale radius for visibility (original multiplier was 4)
    r_scaled = r_value * 8  # Doubled the scale factor for 100% larger diagram
    
    # Ensure circle stays within bounds
    max_r = min(cx - 20, width - cx - 20, cy - 20, height - cy - 20)
    if r_scaled > max_r:
        r_scaled = max_r
    
    # Draw based on whether showing radius or diameter
    if label_type == "r":
        # Radius line from center to edge (right side)
        return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <circle cx="{cx}" cy="{cy}" r="{r_scaled}" fill="#cce5ff" stroke="#006" stroke-width="3"/>
    <line x1="{cx}" y1="{cy}" x2="{cx + r_scaled}" y2="{cy}" stroke="#c33" stroke-width="3"/>
    <rect x="{cx-4}" y="{cy-4}" width="8" height="8" fill="#c33"/>
    <text x="{cx + 10}" y="{cy - 12}" font-size="18" fill="#c33" font-weight="bold">{label_text}</text>
    <text x="160" y="35" font-size="20" fill="#006" font-weight="bold">Circle</text>
</svg>'''
    else:
        # Diameter line from left edge to right edge through center
        return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <circle cx="{cx}" cy="{cy}" r="{r_scaled}" fill="#cce5ff" stroke="#006" stroke-width="3"/>
    <line x1="{cx - r_scaled}" y1="{cy}" x2="{cx + r_scaled}" y2="{cy}" stroke="#c33" stroke-width="3"/>
    <rect x="{cx-4}" y="{cy-4}" width="8" height="8" fill="#c33"/>
    <text x="{cx - 45}" y="{cy - 12}" font-size="18" fill="#c33" font-weight="bold">{label_text}</text>
    <text x="160" y="35" font-size="20" fill="#006" font-weight="bold">Circle</text>
</svg>'''


def get_rectangle_svg(length=None, width=None, show_length=True, show_width=True):
    """
    Generate SVG for a rectangle.
    Pass length and/or width as needed. The diagram will match the verbal description.
    
    Parameters:
        length: length value (can be None if not given)
        width: width value (can be None if not given)
        show_length: whether to label the length on the diagram
        show_width: whether to label the width on the diagram
    
    Examples:
        # Verbal: "length = 10 ft, width = 5 ft" - show both
        get_rectangle_svg(length=10, width=5, show_length=True, show_width=True)
        
        # Verbal: "length = 8 ft, perimeter = 24 ft" - show length only, width hidden
        get_rectangle_svg(length=8, show_length=True, show_width=False)
        
        # Verbal: "width = 6 ft, area = 48 sq ft" - show width only, length hidden
        get_rectangle_svg(width=6, show_length=False, show_width=True)
        
        # Verbal: "perimeter = 30 ft, length = 9 ft" - show length only
        get_rectangle_svg(length=9, show_length=True, show_width=False)
    """
    # Default values if not provided (for scaling only)
    l_val = length if length is not None else 1
    w_val = width if width is not None else 1
    
    # 100% larger dimensions (doubled from original)
    # Original: width=260, height=180, rect x=30, y=30
    # New: width=520, height=360, rect x=60, y=60
    svg_width = 520
    svg_height = 360
    rect_x = 60
    rect_y = 60
    
    # Scale for visibility (original multiplier was 6)
    l_scaled = l_val * 12  # Doubled scale factor
    w_scaled = w_val * 12
    
    # Ensure rectangle stays within bounds
    max_width = svg_width - rect_x - 40
    max_height = svg_height - rect_y - 40
    if l_scaled > max_width:
        l_scaled = max_width
    if w_scaled > max_height:
        w_scaled = max_height
    
    # Build the SVG
    svg = f'''<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <rect x="{rect_x}" y="{rect_y}" width="{l_scaled}" height="{w_scaled}" fill="#cce5ff" stroke="#006" stroke-width="3"/>
'''
    
    # Add length label (top edge)
    if show_length and length is not None:
        svg += f'''    <line x1="{rect_x}" y1="{rect_y}" x2="{rect_x + l_scaled}" y2="{rect_y}" stroke="#c33" stroke-width="2.5"/>
    <text x="{rect_x + l_scaled//2}" y="{rect_y - 12}" font-size="16" fill="#c33" text-anchor="middle" font-weight="bold">L = {length}</text>
'''
    
    # Add width label (left edge)
    if show_width and width is not None:
        svg += f'''    <line x1="{rect_x}" y1="{rect_y}" x2="{rect_x}" y2="{rect_y + w_scaled}" stroke="#c33" stroke-width="2.5"/>
    <text x="{rect_x - 12}" y="{rect_y + w_scaled//2}" font-size="16" fill="#c33" text-anchor="middle" font-weight="bold" transform="rotate(-90, {rect_x - 12}, {rect_y + w_scaled//2})">W = {width}</text>
'''
    
    svg += f'''    <text x="{svg_width//2}" y="35" font-size="20" fill="#006" font-weight="bold" text-anchor="middle">Rectangle</text>
</svg>'''
    
    return svg


def get_cube_svg(side):
    """
    Generate clean 2.5D isometric cube with given side length.
    Label placed completely outside the drawing area with NO overlap.
    Visual matches verbal description exactly.
    
    Parameters:
        side: side length of the cube
    
    Example:
        get_cube_svg(side=8)
    """
    # Scale for visibility (increased for 100% larger diagram)
    s = side * 12  # Doubled from original 6
    
    # Base position (adjusted to leave room for labels)
    x0 = 120  # Center X position for front face left edge
    y0 = 150  # Top Y position for front face
    
    # Isometric offset
    iso_offset = s * 0.7
    
    # Diagram size (increased to fit labels without overlap)
    svg_width = 500
    svg_height = 400
    
    return f'''<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Front face -->
    <rect x="{x0}" y="{y0}" width="{s}" height="{s}" fill="#cce5ff" stroke="#006" stroke-width="3"/>
    
    <!-- Top face (isometric) -->
    <polygon points="{x0},{y0} {x0 + iso_offset},{y0 - iso_offset} {x0 + s + iso_offset},{y0 - iso_offset} {x0 + s},{y0}" fill="#e6f2fa" stroke="#006" stroke-width="3"/>
    
    <!-- Right face (isometric) -->
    <polygon points="{x0 + s},{y0} {x0 + s + iso_offset},{y0 - iso_offset} {x0 + s + iso_offset},{y0 + s - iso_offset} {x0 + s},{y0 + s}" fill="#a8d0e6" stroke="#006" stroke-width="3"/>
    
    <!-- Bottom edge of front face -->
    <line x1="{x0}" y1="{y0 + s}" x2="{x0 + s}" y2="{y0 + s}" stroke="#006" stroke-width="3"/>
    
    <!-- ===== DIMENSION LABEL (placed BELOW the cube, completely outside the drawing area) ===== -->
    <!-- Side label with leader lines from bottom edge -->
    <line x1="{x0}" y1="{y0 + s + 25}" x2="{x0 + s}" y2="{y0 + s + 25}" stroke="#c33" stroke-width="2"/>
    <line x1="{x0}" y1="{y0 + s}" x2="{x0}" y2="{y0 + s + 25}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="{x0 + s}" y1="{y0 + s}" x2="{x0 + s}" y2="{y0 + s + 25}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="{x0 + s//2}" y="{y0 + s + 50}" font-size="18" fill="#c33" text-anchor="middle" font-weight="bold">side = {side}</text>
    
    <!-- Title -->
    <text x="{svg_width//2}" y="40" font-size="20" fill="#006" font-weight="bold" text-anchor="middle">Cube</text>
</svg>'''


def get_rectangular_prism_svg(l, w, h):
    """
    Generate clean 2.5D isometric rectangular prism.
    Dimensions displayed cleanly away from diagram with NO overlap.
    Visual matches verbal description exactly.
    
    Parameters:
        l: length (front face horizontal)
        w: width (depth, goes into the page - isometric)
        h: height (vertical)
    
    Example:
        get_rectangular_prism_svg(l=10, w=6, h=4)
    """
    # Scale factors (doubled from original for 100% larger diagram)
    l_scaled = l * 10
    w_scaled = w * 10
    h_scaled = h * 10
    
    # Base position (adjusted to leave room for labels on all sides)
    x0 = 120  # Moved right to leave space for height label on left
    y0 = 220  # Moved down to leave space for length label below
    
    # Isometric angle factor (0.7 is standard for pseudo-3D)
    iso_factor = 0.7
    w_offset = w_scaled * iso_factor
    
    # Diagram size (increased to fit labels without overlap)
    svg_width = 600
    svg_height = 500
    
    return f'''<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Front face (length × height) -->
    <rect x="{x0}" y="{y0 - h_scaled}" width="{l_scaled}" height="{h_scaled}" fill="#cce5ff" stroke="#006" stroke-width="3"/>
    
    <!-- Top face (length × width) - isometric -->
    <polygon points="{x0},{y0 - h_scaled} {x0 + l_scaled},{y0 - h_scaled} {x0 + l_scaled + w_offset},{y0 - h_scaled - w_offset} {x0 + w_offset},{y0 - h_scaled - w_offset}" fill="#e6f2fa" stroke="#006" stroke-width="3"/>
    
    <!-- Right face (width × height) - isometric -->
    <polygon points="{x0 + l_scaled},{y0 - h_scaled} {x0 + l_scaled},{y0} {x0 + l_scaled + w_offset},{y0 - w_offset} {x0 + l_scaled + w_offset},{y0 - h_scaled - w_offset}" fill="#a8d0e6" stroke="#006" stroke-width="3"/>
    
    <!-- Bottom edge of front face -->
    <line x1="{x0}" y1="{y0}" x2="{x0 + l_scaled}" y2="{y0}" stroke="#006" stroke-width="3"/>
    
    <!-- ===== DIMENSION LABELS (placed completely outside the drawing area) ===== -->
    
    <!-- Length label (BELOW the front face, with leader line from bottom edge) -->
    <line x1="{x0}" y1="{y0 + 30}" x2="{x0 + l_scaled}" y2="{y0 + 30}" stroke="#c33" stroke-width="2"/>
    <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + 30}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="{x0 + l_scaled}" y1="{y0}" x2="{x0 + l_scaled}" y2="{y0 + 30}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="{x0 + l_scaled//2}" y="{y0 + 50}" font-size="18" fill="#c33" text-anchor="middle" font-weight="bold">length = {l}</text>
    
    <!-- Height label (LEFT of front face, with leader line from left edge) -->
    <line x1="{x0 - 35}" y1="{y0 - h_scaled}" x2="{x0 - 35}" y2="{y0}" stroke="#c33" stroke-width="2"/>
    <line x1="{x0}" y1="{y0 - h_scaled}" x2="{x0 - 35}" y2="{y0 - h_scaled}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="{x0}" y1="{y0}" x2="{x0 - 35}" y2="{y0}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="{x0 - 55}" y="{y0 - h_scaled//2}" font-size="18" fill="#c33" text-anchor="middle" font-weight="bold" transform="rotate(-90, {x0 - 55}, {y0 - h_scaled//2})">height = {h}</text>
    
    <!-- Width label (RIGHT of right face, along isometric depth, with leader lines) -->
    <!-- Leader line from top front corner to label area -->
    <line x1="{x0 + l_scaled + w_offset + 20}" y1="{y0 - h_scaled - w_offset - 20}" x2="{x0 + l_scaled + w_offset + 20}" y2="{y0 - h_scaled - w_offset - 60}" stroke="#c33" stroke-width="2"/>
    <line x1="{x0 + l_scaled + w_offset}" y1="{y0 - h_scaled - w_offset}" x2="{x0 + l_scaled + w_offset + 20}" y2="{y0 - h_scaled - w_offset}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="{x0 + l_scaled}" y1="{y0 - h_scaled}" x2="{x0 + l_scaled + w_offset + 20}" y2="{y0 - h_scaled}" stroke="#c33" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="{x0 + l_scaled + w_offset + 45}" y="{y0 - h_scaled - w_offset - 40}" font-size="18" fill="#c33" text-anchor="start" font-weight="bold">width = {w}</text>
    
    <!-- Title -->
    <text x="{svg_width//2}" y="40" font-size="20" fill="#006" font-weight="bold" text-anchor="middle">Rectangular Prism</text>
</svg>'''


def get_angle_svg(angles, total=180):
    """
    Generate SVG for adjacent angles that sum to a total (90° or 180°).
    All angles share a single vertex.
    angles: list of known angle values (excludes 'x')
    total: 90 for complementary angles, 180 for supplementary angles
    
    For 2 angles total: 1 known + x = total
    For 3 angles total: 2 known + x = total
    """
    known_sum = sum(angles)
    unknown = total - known_sum
    
    if unknown <= 0:
        raise ValueError(f"Known angles sum to {known_sum}, which exceeds total {total}")
    
    if total == 90:
        angle_type = "Complementary"
    elif total == 180:
        angle_type = "Supplementary"
    else:
        angle_type = "Adjacent"
    
    if len(angles) == 1:
        # 2 angles: known + x = total
        return _get_two_angles_svg(angles[0], unknown, total, angle_type)
    
    elif len(angles) == 2:
        # 3 angles: known1 + x + known2 = total (or known1 + known2 + x = total)
        return _get_three_angles_svg(angles[0], angles[1], unknown, total, angle_type)
    
    else:
        return _get_two_angles_svg(60, 120, 180, "Supplementary")


def _get_two_angles_svg(known, unknown, total, angle_type):
    """Generate SVG with 2 adjacent angles sharing a single vertex"""
    cx, cy = 160, 110
    ray_length = 80
    arc_radius = 50
    
    angle_rad = math.radians(known)
    total_rad = math.radians(total)
    
    # Right side of base line
    base_right_x = cx + ray_length
    
    # Ray for the known angle (measured from right horizontal, going counterclockwise)
    ray_x = cx - ray_length * math.cos(angle_rad)
    ray_y = cy - ray_length * math.sin(angle_rad)
    
    # If total is 90°, we need the left base line
    base_left_x = cx - ray_length * math.cos(total_rad) if total == 90 else cx - ray_length
    
    # Arc endpoints
    arc_start_x = cx - arc_radius
    arc_start_y = cy
    arc_end_x = cx - arc_radius * math.cos(angle_rad)
    arc_end_y = cy - arc_radius * math.sin(angle_rad)
    
    # Total arc endpoint
    total_end_x = cx - arc_radius * math.cos(total_rad)
    total_end_y = cy - arc_radius * math.sin(total_rad)
    
    # Label positions
    mid_known = angle_rad / 2
    known_label_x = cx - (arc_radius + 18) * math.cos(mid_known)
    known_label_y = cy - (arc_radius + 18) * math.sin(mid_known)
    
    mid_unknown = angle_rad + (total_rad - angle_rad) / 2
    unknown_label_x = cx - (arc_radius + 18) * math.cos(mid_unknown)
    unknown_label_y = cy - (arc_radius + 18) * math.sin(mid_unknown)
    
    # Base line: right side always extends right
    if total == 90:
        # For 90°, base line goes left and right from vertex
        base_line = f'''
    <line x1="{base_left_x:.1f}" y1="{cy}" x2="{base_right_x}" y2="{cy}" stroke="#006" stroke-width="3"/>'''
        svg_width = 300
        viewbox = "0 0 300 200"
        title_x = 70
    else:
        base_line = f'''
    <line x1="{cx - ray_length}" y1="{cy}" x2="{base_right_x}" y2="{cy}" stroke="#006" stroke-width="3"/>'''
        svg_width = 340
        viewbox = "0 0 340 200"
        title_x = 90
    
    # Right angle square indicator for 90°
    right_angle_indicator = ""
    if total == 90:
        square_size = 15
        right_angle_indicator = f'''
    <polyline points="{cx - square_size},{cy} {cx - square_size},{cy - square_size} {cx},{cy - square_size}" 
              fill="none" stroke="#c33" stroke-width="2"/>'''
    
    return f'''<svg width="{svg_width}" height="200" viewBox="{viewbox}" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Horizontal base line -->{base_line}
    
    <!-- Vertex point -->
    <circle cx="{cx}" cy="{cy}" r="4.5" fill="#c33"/>
    
    <!-- Ray separating the two angles -->
    <line x1="{cx}" y1="{cy}" x2="{ray_x:.1f}" y2="{ray_y:.1f}" stroke="#006" stroke-width="3"/>
    
    <!-- Known angle arc and fill -->
    <path d="M {arc_start_x:.1f},{cy} A {arc_radius},{arc_radius} 0 0,1 {arc_end_x:.1f},{arc_end_y:.1f} L {cx},{cy} Z" 
          fill="rgba(100,150,255,0.25)" stroke="#006" stroke-width="1.5"/>
    
    <!-- Unknown angle arc and fill -->
    <path d="M {arc_end_x:.1f},{arc_end_y:.1f} A {arc_radius},{arc_radius} 0 0,1 {total_end_x:.1f},{total_end_y:.1f} L {cx},{cy} Z" 
          fill="rgba(255,150,100,0.25)" stroke="#006" stroke-width="1.5"/>
    {right_angle_indicator}
    
    <!-- Labels -->
    <text x="{known_label_x:.1f}" y="{known_label_y:.1f}" font-size="16" fill="#c33" font-weight="bold" text-anchor="middle">{known}°</text>
    <text x="{unknown_label_x:.1f}" y="{unknown_label_y:.1f}" font-size="16" fill="#006" font-weight="bold" text-anchor="middle">x°</text>
    
    <!-- Small angle indicator arc for known angle -->
    <path d="M {cx - 20},{cy} A 20,20 0 0,1 {cx - 20 * math.cos(angle_rad):.1f},{cy - 20 * math.sin(angle_rad):.1f}" 
          fill="none" stroke="#c33" stroke-width="2"/>
    
    <text x="{title_x}" y="25" font-size="14" fill="#006" font-weight="bold">{angle_type} Angles (sum = {total}°)</text>
</svg>'''


def _get_three_angles_svg(known1, known2, unknown, total, angle_type):
    """Generate SVG with 3 adjacent angles sharing a single vertex"""
    cx, cy = 160, 110
    ray_length = 80
    arc_radius = 50
    
    # Convert to radians
    angle1_rad = math.radians(known1)
    angle2_rad = math.radians(known2)
    unknown_rad = math.radians(unknown)
    total_rad = math.radians(total)
    
    # Calculate cumulative angles for positioning rays
    # First ray separates known1 from unknown
    ray1_x = cx - ray_length * math.cos(angle1_rad)
    ray1_y = cy - ray_length * math.sin(angle1_rad)
    
    # Second ray separates unknown from known2
    ray2_angle = angle1_rad + unknown_rad
    ray2_x = cx - ray_length * math.cos(ray2_angle)
    ray2_y = cy - ray_length * math.sin(ray2_angle)
    
    # Base line endpoints
    base_right_x = cx + ray_length
    if total == 90:
        base_left_x = cx - ray_length * math.cos(total_rad)
    else:
        base_left_x = cx - ray_length
    
    # Arc endpoints for the three angle segments
    # Known1 arc: from right horizontal to first ray
    arc1_start_x = cx - arc_radius
    arc1_start_y = cy
    arc1_end_x = cx - arc_radius * math.cos(angle1_rad)
    arc1_end_y = cy - arc_radius * math.sin(angle1_rad)
    
    # Unknown arc: from first ray to second ray
    arc2_end_x = cx - arc_radius * math.cos(ray2_angle)
    arc2_end_y = cy - arc_radius * math.sin(ray2_angle)
    
    # Known2 arc: from second ray to total limit
    arc3_end_x = cx - arc_radius * math.cos(total_rad)
    arc3_end_y = cy - arc_radius * math.sin(total_rad)
    
    # Label positions
    mid_known1 = angle1_rad / 2
    known1_label_x = cx - (arc_radius + 18) * math.cos(mid_known1)
    known1_label_y = cy - (arc_radius + 18) * math.sin(mid_known1)
    
    mid_unknown = angle1_rad + unknown_rad / 2
    unknown_label_x = cx - (arc_radius + 18) * math.cos(mid_unknown)
    unknown_label_y = cy - (arc_radius + 18) * math.sin(mid_unknown)
    
    mid_known2 = ray2_angle + (total_rad - ray2_angle) / 2
    known2_label_x = cx - (arc_radius + 18) * math.cos(mid_known2)
    known2_label_y = cy - (arc_radius + 18) * math.sin(mid_known2)
    
    # Base line
    if total == 90:
        base_line = f'''
    <line x1="{base_left_x:.1f}" y1="{cy}" x2="{base_right_x}" y2="{cy}" stroke="#006" stroke-width="3"/>'''
        svg_width = 340
        title_x = 90
    else:
        base_line = f'''
    <line x1="{base_left_x}" y1="{cy}" x2="{base_right_x}" y2="{cy}" stroke="#006" stroke-width="3"/>'''
        svg_width = 380
        title_x = 105
    
    # Right angle square indicator for 90°
    right_angle_indicator = ""
    if total == 90:
        square_size = 15
        right_angle_indicator = f'''
    <polyline points="{cx - square_size},{cy} {cx - square_size},{cy - square_size} {cx},{cy - square_size}" 
              fill="none" stroke="#c33" stroke-width="2"/>'''
    
    return f'''<svg width="{svg_width}" height="220" viewBox="0 0 {svg_width} 220" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Horizontal base line -->{base_line}
    
    <!-- Single vertex point -->
    <circle cx="{cx}" cy="{cy}" r="4.5" fill="#c33"/>
    
    <!-- First ray (separates known1 from x) -->
    <line x1="{cx}" y1="{cy}" x2="{ray1_x:.1f}" y2="{ray1_y:.1f}" stroke="#006" stroke-width="3"/>
    
    <!-- Second ray (separates x from known2) -->
    <line x1="{cx}" y1="{cy}" x2="{ray2_x:.1f}" y2="{ray2_y:.1f}" stroke="#006" stroke-width="3"/>
    
    <!-- Known1 angle arc (right side, blue) -->
    <path d="M {arc1_start_x:.1f},{cy} A {arc_radius},{arc_radius} 0 0,1 {arc1_end_x:.1f},{arc1_end_y:.1f} L {cx},{cy} Z" 
          fill="rgba(100,150,255,0.25)" stroke="#006" stroke-width="1.5"/>
    
    <!-- Unknown angle arc (middle, green) -->
    <path d="M {arc1_end_x:.1f},{arc1_end_y:.1f} A {arc_radius},{arc_radius} 0 0,1 {arc2_end_x:.1f},{arc2_end_y:.1f} L {cx},{cy} Z" 
          fill="rgba(150,255,100,0.25)" stroke="#006" stroke-width="1.5"/>
    
    <!-- Known2 angle arc (top/left, orange) -->
    <path d="M {arc2_end_x:.1f},{arc2_end_y:.1f} A {arc_radius},{arc_radius} 0 0,1 {arc3_end_x:.1f},{arc3_end_y:.1f} L {cx},{cy} Z" 
          fill="rgba(255,150,100,0.25)" stroke="#006" stroke-width="1.5"/>
    {right_angle_indicator}
    
    <!-- Labels -->
    <text x="{known1_label_x:.1f}" y="{known1_label_y:.1f}" font-size="15" fill="#c33" font-weight="bold" text-anchor="middle">{known1}°</text>
    <text x="{unknown_label_x:.1f}" y="{unknown_label_y:.1f}" font-size="15" fill="#006" font-weight="bold" text-anchor="middle">x°</text>
    <text x="{known2_label_x:.1f}" y="{known2_label_y:.1f}" font-size="15" fill="#c33" font-weight="bold" text-anchor="middle">{known2}°</text>
    
    <!-- Small angle indicator arcs -->
    <path d="M {cx - 20},{cy} A 20,20 0 0,1 {cx - 20 * math.cos(angle1_rad):.1f},{cy - 20 * math.sin(angle1_rad):.1f}" 
          fill="none" stroke="#c33" stroke-width="2"/>
    <path d="M {cx - 20 * math.cos(angle1_rad):.1f},{cy - 20 * math.sin(angle1_rad):.1f} A 20,20 0 0,1 {cx - 20 * math.cos(ray2_angle):.1f},{cy - 20 * math.sin(ray2_angle):.1f}" 
          fill="none" stroke="#006" stroke-width="2"/>
    
    <text x="{title_x}" y="25" font-size="14" fill="#006" font-weight="bold">{angle_type} Angles (sum = {total}°)</text>
</svg>'''


def get_clock_svg(hours=None, minutes=None):
    """Generate SVG for a standard clock face (no special time shown).
    For elapsed time problems - clock is just a reference graphic."""
    return f'''<svg width="160" height="160" viewBox="0 0 160 160" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Clock face -->
    <circle cx="80" cy="80" r="65" fill="white" stroke="#006" stroke-width="2.5"/>
    
    <!-- Hour markers (12, 3, 6, 9) -->
    <line x1="80" y1="18" x2="80" y2="30" stroke="#006" stroke-width="2.5"/>
    <line x1="80" y1="130" x2="80" y2="142" stroke="#006" stroke-width="2.5"/>
    <line x1="18" y1="80" x2="30" y2="80" stroke="#006" stroke-width="2.5"/>
    <line x1="130" y1="80" x2="142" y2="80" stroke="#006" stroke-width="2.5"/>
    
    <!-- Hour numbers -->
    <text x="80" y="38" font-size="12" fill="#006" text-anchor="middle" font-weight="bold">12</text>
    <text x="118" y="85" font-size="12" fill="#006" text-anchor="middle" font-weight="bold">3</text>
    <text x="80" y="138" font-size="12" fill="#006" text-anchor="middle" font-weight="bold">6</text>
    <text x="42" y="85" font-size="12" fill="#006" text-anchor="middle" font-weight="bold">9</text>
    
    <!-- Small tick marks for other hours -->
    <g stroke="#999" stroke-width="1">
        <line x1="80" y1="20" x2="80" y2="26" />
        <line x1="80" y1="134" x2="80" y2="140" />
        <line x1="20" y1="80" x2="26" y2="80" />
        <line x1="134" y1="80" x2="140" y2="80" />
    </g>
    
    <!-- Center dot -->
    <circle cx="80" cy="80" r="4" fill="#c33"/>
    
    <!-- Neutral hands (both pointing up to 12 - no time implied) -->
    <line x1="80" y1="80" x2="80" y2="35" stroke="#c33" stroke-width="3" stroke-linecap="round"/>
    <line x1="80" y1="80" x2="80" y2="45" stroke="#006" stroke-width="2.5" stroke-linecap="round"/>
    
    <text x="55" y="18" font-size="14" fill="#006" font-weight="bold">Clock</text>
</svg>'''




def gen_geometry_measurement(n=5):
    problems = []
    max_attempts = 50

    for i in range(n):
        problem_type = i % 5
        q_text = ""
        choices = []
        answer_str = ""
        correct_index = 0
        
        # 1) Area of triangle or circle
        if problem_type == 0:
            if random.choice(["triangle", "circle"]) == "triangle":
                b = random.randint(5, 15)
                h = random.randint(3, 12)
                ans = round(0.5 * b * h, 2)
                diagram = get_triangle_svg(b, h)
                q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Triangle Area</div>A triangle has a base of {b} cm and a height of {h} cm. What is its area in cm²?'
            else:
                d = random.randint(4, 16)
                r = d / 2
                ans = round(math.pi * r ** 2, 2)
                diagram = get_circle_svg(d)
                q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Circle Area</div>A circle has a diameter of {d} cm. What is its area in cm²? (Use π ≈ 3.14)'

            answer_str = str(ans)
            choices = [
                answer_str,
                str(round(ans * 1.1, 2)),
                str(round(ans * 0.9, 2)),
                str(round(ans + 5, 2)),
                str(round(max(ans - 5, 1), 2)),
            ]
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # 2) Rectangle
        elif problem_type == 1:
            L = random.randint(5, 15)
            W = random.randint(3, 12)
            diagram = get_rectangle_svg(L, W)

            if i % 2 == 0:
                area = L * W
                known_side = L
                ans = round(2 * (known_side + area / known_side), 2)
                q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Rectangle Perimeter</div>A rectangle has an area of {area} cm² and one side of length {known_side} cm. What is its perimeter in cm?'
            else:
                perimeter = 2 * (L + W)
                known_side = L
                ans = round((perimeter / 2 - known_side) * known_side, 2)
                q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Rectangle Area</div>A rectangle has a perimeter of {perimeter} cm and one side of length {known_side} cm. What is its area in cm²?'

            answer_str = str(ans)
            choices = [
                answer_str,
                str(round(ans + 2, 2)),
                str(round(max(ans - 2, 1), 2)),
                str(round(ans + 4, 2)),
                str(round(ans + 6, 2)),
            ]
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # 3) Volume
        elif problem_type == 2:
            if random.choice(["cube", "prism"]) == "cube":
                s = random.randint(2, 10)
                ans = s ** 3
                diagram = get_cube_svg(s)
                q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Cube Volume</div>A cube has sides of length {s} cm. What is its volume in cm³?'
            else:
                l = random.randint(3, 10)
                w = random.randint(2, 8)
                h = random.randint(2, 6)
                ans = l * w * h
                diagram = get_rectangular_prism_svg(l, w, h)
                q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Rectangular Prism Volume</div>A rectangular prism has dimensions {l} cm × {w} cm × {h} cm. What is its volume in cm³?'

            answer_str = str(ans)
            choices = [
                answer_str,
                str(ans + 5),
                str(max(ans - 5, 1)),
                str(ans + 10),
                str(ans - 3),
            ]
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # 4) Angles
        elif problem_type == 3:
            total = random.choice([90, 180])
            num_angles = random.choice([2, 3])  # Total angles including x
            
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                if num_angles == 2:
                    # Two angles total: one known + x = total
                    known_angle = random.randint(10, total - 10)
                    answer = total - known_angle
                    if answer >= 10:
                        known_angles = [known_angle]  # List with ONE angle
                        break
                else:
                    # Three angles total: two known + x = total
                    angle1 = random.randint(10, total - 20)
                    angle2 = random.randint(10, total - angle1 - 10)
                    answer = total - angle1 - angle2
                    if answer >= 10:
                        known_angles = [angle1, angle2]  # List with TWO angles
                        break
            
            diagram = get_angle_svg(known_angles, total)
            answer_str = f"{answer}°"
            
            # Create display text for the problem
            if len(known_angles) == 1:
                angle_display = f"{known_angles[0]}° and x°"
            else:
                angle_display = f"{known_angles[0]}°, {known_angles[1]}°, and x°"
            
            q_text = f'{diagram}<div style="text-align:center; font-weight:bold; margin-top:5px;">Angle Problem</div>Find the value of x if the angles {angle_display} add up to {total}°.'
            
            choices = [
                answer_str,
                f"{answer + 5}°",
                f"{max(answer - 5, 1)}°",
                f"{answer + 10}°",
                f"{max(answer - 10, 1)}°",
            ]
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # 5) Time
        else:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                m1 = random.randint(10, 59)
                m2 = random.randint(10, 59)
                h1 = random.randint(0, 3)
                h2 = random.randint(0, 3)
                
                total_m = h1 * 60 + m1 + h2 * 60 + m2
                h, m = divmod(total_m, 60)
                
                if h >= 1 and h <= 8 and m >= 10 and m <= 59:
                    break
            
            diagram1 = get_clock_svg(h1, m1)
            #diagram2 = get_clock_svg(h2, m2)
            diagram2 = None
            
            if m == 0:
                time_str = f"{h} hours"
            elif h == 0:
                time_str = f"{m} minutes"
            else:
                time_str = f"{h} hours and {m} minutes"
            
            answer_str = time_str
            
            q_text = f'<div style="display:flex; justify-content:space-around; flex-wrap:wrap;">{diagram1}{diagram2}</div><div style="text-align:center; font-weight:bold; margin-top:5px;">Elapsed Time</div>Antonio played outside for {h1} hours and {m1} minutes on Saturday, and for {h2} hours and {m2} minutes on Sunday. How many total hours and minutes did he play outside?'
            
            choices_set = {answer_str}
            
            variations = [
                f"{h+1} hours and {m} minutes" if h+1 <= 12 else None,
                f"{max(h-1, 1)} hours and {m} minutes" if h-1 >= 1 else None,
                f"{h} hours and {min(m+15, 59)} minutes" if m+15 <= 59 else None,
                f"{h} hours and {max(m-15, 10)} minutes" if m-15 >= 10 else None,
            ]
            
            for var in variations:
                if var and var != answer_str and len(choices_set) < 5:
                    choices_set.add(var)
            
            choices = list(choices_set)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        problems.append((q_text, choices, correct_index))

    return problems



def gen_data_probability(num_problems=5):
    problems = []
    max_attempts = 100  # Prevent infinite loops

    for i in range(num_problems):
        problem_type = i % 5
        q_text = ""
        choices = []
        answer_str = ""
        correct_index = 0

        # ---------- TYPE 1: Marble probability ----------
        if problem_type == 0:
            colors = random.sample(["red", "blue", "green", "yellow"], random.randint(3, 4))
            counts = [random.randint(1, 6) for _ in colors]
            total = sum(counts)

            if random.choice([True, False]):
                color = random.choice(colors)
                favorable = counts[colors.index(color)]
                q_text = (
                    "A bag contains the following marbles:<br><br>"
                    f"{', '.join([f'{c}: {n}' for c, n in zip(colors, counts)])}<br><br>"
                    f"What is the probability of selecting a {color} marble?"
                )
            else:
                color_pair = random.sample(colors, 2)
                favorable = sum([counts[colors.index(c)] for c in color_pair])
                q_text = (
                    "A bag contains the following marbles:<br><br>"
                    f"{', '.join([f'{c}: {n}' for c, n in zip(colors, counts)])}<br><br>"
                    f"What is the probability of selecting a {color_pair[0]} or {color_pair[1]} marble?"
                )

            frac = Fraction(favorable, total).limit_denominator()
            answer_str = f"{frac.numerator}/{frac.denominator}"

            # Generate unique distractors with attempt limit
            wrong = set()
            attempts = 0
            while len(wrong) < 4 and attempts < max_attempts:
                attempts += 1
                # Add small random variation to numerator and denominator
                num_variation = random.randint(-2, 2)
                den_variation = random.randint(-2, 2)
                
                num = max(1, frac.numerator + num_variation)
                den = max(1, frac.denominator + den_variation)
                
                # Ensure fraction is simplified and different from answer
                simplified = Fraction(num, den).limit_denominator()
                s = f"{simplified.numerator}/{simplified.denominator}"
                
                if s != answer_str and s not in wrong:
                    wrong.add(s)
            
            # If we couldn't generate enough distractors, add simple fallbacks
            fallbacks = ["1/2", "1/3", "2/3", "1/4", "3/4", "1/5", "2/5", "3/5", "4/5"]
            for fb in fallbacks:
                if len(wrong) >= 4:
                    break
                if fb != answer_str and fb not in wrong:
                    wrong.add(fb)

            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # ---------- TYPE 2: Rainfall ----------
        elif problem_type == 1:
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            rainfall = [random.randint(2, 10) for _ in days]

            if random.choice([True, False]):
                weekday_total = sum(rainfall[:5])
                weekend_total = sum(rainfall[5:])
                ans = weekday_total - weekend_total
                q_text = (
                    "The table shows inches of rainfall:<br><br>"
                    f"{', '.join([f'{d}: {r}' for d, r in zip(days, rainfall)])}<br><br>"
                    "How many more inches of rain fell on weekdays than on the weekend?"
                )
            else:
                ans = sum(rainfall)
                q_text = (
                    "The table shows inches of rainfall:<br><br>"
                    f"{', '.join([f'{d}: {r}' for d, r in zip(days, rainfall)])}<br><br>"
                    "How many inches of rain fell in total for the week?"
                )

            answer_str = str(ans)
            
            # Generate unique distractors with attempt limit
            wrong = set()
            attempts = 0
            while len(wrong) < 4 and attempts < max_attempts:
                attempts += 1
                delta = random.choice([-3, -2, -1, 1, 2, 3])
                val = max(0, ans + delta)
                s = str(val)
                if s != answer_str and s not in wrong:
                    wrong.add(s)
            
            # Fallback distractors
            fallbacks = [str(ans + i) for i in range(1, 5)] + [str(max(0, ans - i)) for i in range(1, 5)]
            for fb in fallbacks:
                if len(wrong) >= 4:
                    break
                if fb != answer_str and fb not in wrong:
                    wrong.add(fb)

            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # ---------- TYPE 3: Favorite subject ----------
        elif problem_type == 2:
            subjects = ["Math", "English", "Science", "History"]
            total_students = random.choice([50, 200, 300])
            remaining = total_students
            
            # Ensure counts sum to total without going negative
            counts = []
            for idx in range(len(subjects) - 1):
                max_val = remaining
                min_val = 0
                n = random.randint(min_val, max_val)
                counts.append(n)
                remaining -= n
            counts.append(remaining)  # Last subject gets whatever remains

            subject = random.choice(subjects)
            count = counts[subjects.index(subject)]
            percent = round((count / total_students) * 100)

            q_text = (
                f"A survey asked students their favorite subject:<br><br>"
                f"{', '.join([f'{s}: {c}' for s, c in zip(subjects, counts)])}<br><br>"
                f"What percent of students chose {subject}?"
            )

            # Generate unique percent choices with attempt limit
            wrong = set()
            attempts = 0
            while len(wrong) < 4 and attempts < max_attempts:
                attempts += 1
                delta = random.choice([-15, -10, -5, 5, 10, 15])
                val = max(0, min(100, percent + delta))
                s = f"{val}%"
                if s != f"{percent}%" and s not in wrong:
                    wrong.add(s)
            
            # Fallback percentages
            fallbacks = [f"{percent + 5}%", f"{percent - 5}%", f"{percent + 10}%", f"{percent - 10}%"]
            for fb in fallbacks:
                if len(wrong) >= 4:
                    break
                if fb != f"{percent}%" and fb not in wrong:
                    wrong.add(fb)

            choices = [f"{percent}%"] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(f"{percent}%")

        # ---------- TYPE 4: Average ----------
        elif problem_type == 3:
            avg = random.randint(10, 20)
            # Generate 5 random numbers, then calculate the 6th to achieve the target average
            nums = [random.randint(1, 2*avg) for _ in range(5)]
            total_needed = avg * 6
            last_num = total_needed - sum(nums)
            # Ensure last_num is reasonable (not negative or huge)
            if last_num < 0 or last_num > 100:
                # Regenerate with simpler approach
                nums = [avg + random.randint(-3, 3) for _ in range(5)]
                last_num = total_needed - sum(nums)
                if last_num < 0 or last_num > 100:
                    last_num = avg  # fallback
            
            nums.append(last_num)

            q_text = (
                "Find the average of the following numbers:<br><br>"
                f"{', '.join(map(str, nums))}<br><br>"
            )

            answer_str = str(avg)
            
            # Generate unique distractors
            wrong = set()
            attempts = 0
            while len(wrong) < 4 and attempts < max_attempts:
                attempts += 1
                delta = random.choice([-3, -2, -1, 1, 2, 3])
                val = max(0, avg + delta)
                s = str(val)
                if s != answer_str and s not in wrong:
                    wrong.add(s)
            
            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # ---------- TYPE 5: Median/Range ----------
        else:
            nums = [random.randint(1, 50) for _ in range(7)]
            sorted_nums = sorted(nums)
            
            if random.choice([True, False]):
                ans = sorted_nums[3]  # median
                q_text = (
                    "Find the median of the following numbers:<br><br>"
                    f"{', '.join(map(str, random.sample(nums, len(nums))))}<br><br>"
                )
            else:
                ans = max(nums) - min(nums)  # range
                q_text = (
                    "Find the range of the following numbers:<br><br>"
                    f"{', '.join(map(str, random.sample(nums, len(nums))))}<br><br>"
                )

            answer_str = str(ans)

            # Generate unique distractors
            wrong = set()
            attempts = 0
            while len(wrong) < 4 and attempts < max_attempts:
                attempts += 1
                delta = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                val = max(0, ans + delta)
                s = str(val)
                if s != answer_str and s not in wrong:
                    wrong.add(s)

            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # Append question to problems list
        problems.append((q_text, choices, correct_index))

    return problems

def gen_ssat_math(n=17):
    """
    Generate SSAT math practice problems.
    
    Args:
        n: Number of problems to generate
        
    Returns:
        List of tuples (question_text, choices, correct_index)
    """
    problems = []
    max_attempts = 50

    available_types = list(range(17))
    
    # Shuffle them randomly
    random.shuffle(available_types)
    
    # Select the first n types (or all 17 if n > 17)
    selected_types = available_types[:min(n, 17)]

    for problem_type in selected_types:
        
        q_text = ""
        choices = []
        answer_str = ""
        correct_index = 0

        if problem_type == 0:
            
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Choose the operation type
                op_type = random.choice(['square_minus_2n', 'square_plus_2n', 'n_times_n_minus_2'])
                
                if op_type == 'square_minus_2n':
                    # n^ = n² - 2n (original)
                    n = random.randint(2, 12)
                    result = n * n - 2 * n
                    formula = "n^2 - 2n"
                    answer_str = str(result)
                    q_text = f"If \\(\\widehat{{n}} = n^2 - 2n\\), then \\(\\widehat{{{n}}} =\\)"
                    
                elif op_type == 'square_plus_2n':
                    # n^ = n² + 2n
                    n = random.randint(2, 10)
                    result = n * n + 2 * n
                    formula = "n^2 + 2n"
                    answer_str = str(result)
                    q_text = f"If \\(\\widehat{{n}} = n^2 + 2n\\), then \\(\\widehat{{{n}}} =\\)"
                    
                else:  # n_times_n_minus_2
                    # n^ = n(n - 2) which is the same as n² - 2n but written differently
                    n = random.randint(3, 12)
                    result = n * (n - 2)
                    formula = "n(n - 2)"
                    answer_str = str(result)
                    q_text = f"If \\(\\widehat{{n}} = n(n - 2)\\), then \\(\\widehat{{{n}}} =\\)"
                
                # Generate distractors
                distractors = [
                    str(result + 1),
                    str(max(result - 1, 0)),
                    str(result + n),
                    str(max(result - n, 0)),
                    str(n * n),  # square only
                    str(n * 2),  # 2n only
                    str(abs(n * n - n)),  # n² - n
                    str(n * (n + 2)),  # n(n+2)
                ]
                
                # Remove duplicates
                unique_distractors = []
                for d in distractors:
                    if d != answer_str and d not in unique_distractors:
                        unique_distractors.append(d)
                
                choices = [answer_str] + unique_distractors[:4]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break
            
            # Fallback
            if not q_text:
                q_text = "If \\(\\widehat{n} = n^2 - 2n\\), then \\(\\widehat{4} =\\)"
                answer_str = "8"
                choices = ["8", "12", "16", "4", "6"]
                random.shuffle(choices)
                correct_index = choices.index("8")

        
        elif problem_type == 1:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
            
                a = random.randint(10, 50)
                b = random.randint(5, 45)
                c = random.randint(40, 100)
            
                symbol_sum = c - a + b
            
                if symbol_sum > 0:
                    answer_str = str(symbol_sum)
                    
                    # Using \blacksquare and \blacktriangle for more formal symbols
                    q_text = f"If \\(\\blacksquare + \\blacktriangle + {a} - {b} = {c}\\), what does \\(\\blacksquare + \\blacktriangle\\) equal?"
                    
                    choices = [
                        f"\\({symbol_sum}\\)",
                        f"\\({symbol_sum + random.randint(5, 15)}\\)",
                        f"\\({max(symbol_sum - random.randint(5, 15), 1)}\\)",
                        f"\\({symbol_sum + random.randint(1, 5)}\\)",
                        f"\\({symbol_sum * 2}\\)",
                    ]
                    
                    choices = list(dict.fromkeys(choices))
                    choices = choices[:5]
                    
                    answer_with_tex = f"\\({symbol_sum}\\)"
                    if answer_with_tex not in choices:
                        choices[0] = answer_with_tex
            
                    random.shuffle(choices)
                    correct_index = choices.index(answer_with_tex)
                    break
            
        
        elif problem_type == 2:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1

                # Format: a × N is less than b, N is integer, find what N + c MUST be less than

                a = random.randint(2, 5)           # coefficient (3 in example)
                b = random.randint(a * 1, a * 5)    # upper bound (6 in example)
                c = random.randint(3, 8)            # number added to N (4 in example)

                # Solve inequality: a × N < b
                # N < b/a
                max_N_float = b / a

                # N is integer, so N ≤ floor(b/a - epsilon)
                if b % a == 0:
                    # If b is divisible, N must be strictly less than b/a
                    max_N = b // a - 1
                else:
                    max_N = b // a

                # If no possible integer N, regenerate
                if max_N < -10:
                    continue

                # Find what N + c MUST be less than
                # Maximum possible N is max_N, so N + c ≤ max_N + c
                # Since N is an integer, N + c must be less than (max_N + c + 1)
                must_be_less_than = max_N + c + 1

                answer_str = str(must_be_less_than)

                # Question with LaTeX formatting
                q_text = f"If \\({a} \\times N < {b}\\) and \\(N\\) is an integer, what is the smallest possible value that \\(N + {c}\\) MUST be less than?"

                # Alternative with display math (more prominent)
                # q_text = f"If \\[{a} \\times N < {b}\\] and \\(N\\) is an integer, what is the smallest possible value that \\(N + {c}\\) MUST be less than?"

                # Generate distractors with LaTeX
                choices = [
                    f"\\({must_be_less_than}\\)",
                    f"\\({must_be_less_than - 1}\\)",
                    f"\\({must_be_less_than + 1}\\)",
                    f"\\({must_be_less_than - 2}\\)",
                    f"\\({must_be_less_than + 2}\\)",
                ]

                # Remove duplicates and ensure positive
                choices = list(dict.fromkeys(choices))
                choices = choices[:5]
                
                answer_with_tex = f"\\({must_be_less_than}\\)"
                if answer_with_tex not in choices:
                    choices[0] = answer_with_tex

                random.shuffle(choices)
                correct_index = choices.index(answer_with_tex)
                break
        
        # TEMPLATE 4: [Description of problem type 4]
        elif problem_type == 3:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Format: If x items cost $y, how much will z items cost?
                
                # Generate numbers that will yield a whole number per item or total
                x = random.randint(3, 12)  # number of items in first scenario
                z = random.randint(x + 1, x + 15)  # number of items in second scenario
                
                # Ensure that total cost is divisible by x for whole number per item
                price_per_item = random.randint(4, 20)  # whole dollar per item
                total_cost_x = x * price_per_item
                
                # Calculate cost for z items
                total_cost_z = z * price_per_item
                answer_str = f"\\${total_cost_z}"
                
                # Question with LaTeX formatting
                q_text = f"If {x} LED light bulbs cost \\${total_cost_x}, how much will {z} LED light bulbs cost?"
                
                # Alternative with proportion setup
                # q_text = f"If {x} LED light bulbs cost \\${total_cost_x}, how much will {z} LED light bulbs cost?\n\n\\[ \\frac{{{x}}}{{{total_cost_x}}} = \\frac{{{z}}}{{x}} \\]\n\\[ x = \\frac{{{z} \\times {total_cost_x}}}{{{x}}} = \\text{{?}} \\]"
                
                # Generate distractors
                distractors = [
                    f"\\${total_cost_z + price_per_item}",
                    f"\\${total_cost_z - price_per_item}",
                    f"\\${total_cost_z + (price_per_item // 2)}",
                    f"\\${total_cost_z - (price_per_item // 2)}",
                    f"\\${total_cost_z + random.randint(1, 5)}",
                    f"\\${max(total_cost_z - random.randint(1, 5), 1)}",
                ]
                
                choices = [f"\\${total_cost_z}"] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(f"\\${total_cost_z}")
                break
        
        # TEMPLATE 5: [Description of problem type 5]
        elif problem_type == 4:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Simpler pattern types for SSAT level
                pattern_type = random.choice(['add_constant', 'multiply_constant', 'linear'])
                
                if pattern_type == 'add_constant':
                    # Pattern where numerator and denominator increase by same amount
                    # Example: 1/3, 2/4, 3/5, 4/6, ... x/8
                    start_num = random.randint(1, 3)
                    start_denom = random.randint(3, 5)
                    target_denom = random.randint(7, 12)
                    
                    # Find the term number where denominator = target_denom
                    term_num = target_denom - start_denom
                    x = start_num + term_num
                    
                    answer_str = str(x)
                    
                    # Generate first 3 terms in LaTeX
                    terms = []
                    for i in range(3):
                        num = start_num + i
                        denom = start_denom + i
                        terms.append(f"\\(\\frac{{{num}}}{{{denom}}}\\)")
                    terms_display = ", ".join(terms)
                    
                    q_text = f"Pattern: {terms_display}, ... \\(\\frac{{x}}{{{target_denom}}}\\)\n\nIf the pattern above is continued, what is the value of \\(x\\)?"
                
                elif pattern_type == 'multiply_constant':
                    # Pattern where numerator and denominator follow simple multiplication
                    # Example: 2/3, 4/6, 6/9, 8/12, ... x/15
                    start_num = random.choice([2, 3, 4])
                    start_denom = random.choice([3, 4, 5])
                    multiplier = random.choice([2, 3])
                    
                    target_denom = start_denom * random.randint(4, 6)
                    
                    # Find the multiplier for denominator
                    denom_mult = target_denom // start_denom
                    x = start_num * denom_mult
                    
                    answer_str = str(x)
                    
                    # Generate first 3 terms in LaTeX
                    terms = []
                    for i in range(1, 4):
                        num = start_num * i
                        denom = start_denom * i
                        terms.append(f"\\(\\frac{{{num}}}{{{denom}}}\\)")
                    terms_display = ", ".join(terms)
                    
                    q_text = f"Pattern: {terms_display}, ... \\(\\frac{{x}}{{{target_denom}}}\\)\n\nIf the pattern above is continued, what is the value of \\(x\\)?"
                
                else:  # linear pattern (like the original)
                    # Pattern: numerator increases by 2, denominator increases by 1
                    # Example: 3/1, 5/2, 7/3, 9/4, ... x/8
                    start_num = random.choice([3, 4, 5])
                    start_denom = random.choice([1, 2])
                    num_increment = random.choice([2, 3])
                    
                    target_denom = random.randint(5, 10)
                    
                    # Find term where denominator = target_denom
                    term_num = target_denom - start_denom
                    x = start_num + (term_num * num_increment)
                    
                    answer_str = str(x)
                    
                    # Generate first 3 terms in LaTeX
                    terms = []
                    for i in range(3):
                        num = start_num + (i * num_increment)
                        denom = start_denom + i
                        terms.append(f"\\(\\frac{{{num}}}{{{denom}}}\\)")
                    terms_display = ", ".join(terms)
                    
                    q_text = f"Pattern: {terms_display}, ... \\(\\frac{{x}}{{{target_denom}}}\\)\n\nIf the pattern above is continued, what is the value of \\(x\\)?"
                
                # Generate simpler distractors (closer to correct answer)
                correct_val = int(answer_str)
                distractors = [
                    str(correct_val + 1),
                    str(max(correct_val - 1, 1)),
                    str(correct_val + 2),
                    str(correct_val * 2),
                ]
                
                choices = [answer_str] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break


        elif problem_type == 5:  
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Format: sqrt(n) is between which two integers?
                
                # Generate a number that is not a perfect square
                perfect_squares = [i*i for i in range(1, 20)]  # 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361
                
                # Pick a random perfect square and add a value to make it non-perfect
                lower_square = random.choice(perfect_squares[:-1])  # avoid the last one
                upper_square = perfect_squares[perfect_squares.index(lower_square) + 1]
                
                # Generate n between lower_square and upper_square (exclusive)
                n = random.randint(lower_square + 1, upper_square - 1)
                
                lower_int = int(math.sqrt(lower_square))
                upper_int = int(math.sqrt(upper_square))
                
                answer_str = f"{lower_int} and {upper_int}"
                
                # Question with LaTeX formatting
                q_text = f"\\(\\sqrt{{{n}}}\\) is between which two integers?"
                
                # Alternative with step-by-step
                # q_text = f"\\[\\sqrt{{{n}}} \\text{{ is between which two integers?}}\\]\n\n\\[\\sqrt{{{lower_square}}} = {lower_int}, \\quad \\sqrt{{{upper_square}}} = {upper_int}\\]\n\n\\[\\text{{Since }} {lower_square} < {n} < {upper_square}\\text{{, we know:}}\\]\n\\[\\sqrt{{{n}}} \\text{{ is between }} {lower_int} \\text{{ and }} {upper_int}\\]"
                
                # Generate distractors
                distractors = [
                    f"{lower_int - 1} and {lower_int}",
                    f"{upper_int} and {upper_int + 1}",
                    f"{lower_int - 2} and {lower_int - 1}",
                    f"{upper_int + 1} and {upper_int + 2}",
                    f"{lower_int} and {lower_int + 1}",
                    f"{upper_int - 1} and {upper_int}",
                ]
                
                choices = [answer_str] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break


        elif problem_type == 6:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Choose number of cubs (must allow total to be divisible)
                num_items = random.choice([4, 5, 6, 8, 10])
                initial_avg = random.randint(10, 30)
                
                group1_size = random.randint(2, num_items - 2)
                group2_size = num_items - group1_size
                
                group1_gain = random.randint(2, 5)
                group2_gain = random.randint(1, group1_gain - 1)
                
                initial_total = initial_avg * num_items
                total_gain = (group1_size * group1_gain) + (group2_size * group2_gain)
                new_total = initial_total + total_gain
                
                # Ensure divisible by num_items
                if new_total % num_items == 0:
                    new_avg = new_total // num_items
                    answer_str = str(new_avg)
                    
                    # Question with LaTeX for the calculation
                    q_text = f"The average weight of {num_items} lion cubs is {initial_avg} pounds. If during a week {group1_size} of the cubs gain {group1_gain} pounds each and the other {group2_size} cubs gain {group2_gain} pound{'s' if group2_gain > 1 else ''} each, what will be their average weight?"
                    
                    # Generate distractors
                    distractors = [
                        str(new_avg + 1),
                        str(max(new_avg - 1, 1)),
                        str(new_avg + group1_gain),
                        str(max(new_avg - group1_gain, 1)),
                        str(initial_avg),
                        str(new_avg + group2_gain),
                    ]
                    
                    unique_distractors = []
                    for d in distractors:
                        if d != answer_str and d not in unique_distractors:
                            unique_distractors.append(d)
                    
                    choices = [answer_str] + unique_distractors[:4]
                    random.shuffle(choices)
                    correct_index = choices.index(answer_str)
                    break
        elif problem_type == 7:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Generate realistic heights in inches (4'6" = 54 inches to 6'4" = 76 inches)
                shaun_height = random.randint(54, 76)
                
                # Generate friend's height using yards, feet, inches (realistic range)
                # Friend height between 4'6" (54 inches) and 6'4" (76 inches)
                
                # Option 1: Generate friend height in inches first, then convert to yards/feet/inches
                friend_height_inches = random.randint(54, 76)
                
                # Convert to yards, feet, inches
                friend_yards = friend_height_inches // 36  # 0 or 1 (since max 76 inches)
                remaining_after_yards = friend_height_inches % 36
                friend_feet = remaining_after_yards // 12
                friend_inches = remaining_after_yards % 12
                
                # Ensure Shaun is taller (if not, swap heights)
                if shaun_height <= friend_height_inches:
                    # Swap Shaun and friend
                    shaun_height, friend_height_inches = friend_height_inches, shaun_height
                    
                    # Recalculate friend's yards, feet, inches after swap
                    friend_yards = friend_height_inches // 36
                    remaining_after_yards = friend_height_inches % 36
                    friend_feet = remaining_after_yards // 12
                    friend_inches = remaining_after_yards % 12
                
                height_diff = shaun_height - friend_height_inches
                answer_str = str(height_diff)
                
                # Format friend's height text with proper pluralization
                friend_parts = []
                if friend_yards > 0:
                    yard_text = "yard" if friend_yards == 1 else "yards"
                    friend_parts.append(f"{friend_yards} {yard_text}")
                if friend_feet > 0:
                    foot_text = "foot" if friend_feet == 1 else "feet"
                    friend_parts.append(f"{friend_feet} {foot_text}")
                if friend_inches > 0 or not friend_parts:  # include inches even if 0? No, only if >0
                    if friend_inches > 0:
                        inch_text = "inch" if friend_inches == 1 else "inches"
                        friend_parts.append(f"{friend_inches} {inch_text}")
                
                # If friend has no inches and no feet? That would be 0 yards, 0 feet, 0 inches - not possible with realistic heights
                # So join with commas
                friend_height_text = ", ".join(friend_parts)
                
                # Question with LaTeX formatting (numbers only in LaTeX)
                q_text = f"Shaun is \\({shaun_height}\\) inches tall. His friend is {friend_height_text} tall. How many inches taller is Shaun than his friend?"
                
                # Generate distractors
                distractors = [
                    height_diff + 12,
                    max(height_diff - 12, 1),
                    height_diff + 6,
                    max(height_diff - 6, 1),
                    height_diff + 3,
                    height_diff + 24,
                ]
                
                choices = [str(height_diff)] + [str(d) for d in list(dict.fromkeys(distractors)) if d != height_diff]
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(str(height_diff))
                break

        elif problem_type == 8:

            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Format: Mason made X batches with Y cookies in each batch.
                # He gave Z cookies to each neighbor and had W left.
                # How many neighbors does he have?
                
                # Step 1: Choose number of neighbors (whole number)
                num_neighbors = random.randint(3, 15)
                
                # Step 2: Choose cookies per neighbor
                cookies_per_neighbor = random.randint(5, 15)
                
                # Step 3: Choose cookies left over (less than cookies_per_neighbor)
                cookies_left = random.randint(1, cookies_per_neighbor - 1)
                
                # Step 4: Calculate total cookies
                total_cookies = (num_neighbors * cookies_per_neighbor) + cookies_left
                
                # Step 5: Choose number of batches that divides evenly into total cookies
                possible_batches = []
                for i in range(1, min(10, total_cookies // 2 + 1)):
                    if total_cookies % i == 0:
                        possible_batches.append(i)
                
                if not possible_batches:
                    continue
                    
                num_batches = random.choice(possible_batches)
                cookies_per_batch = total_cookies // num_batches
                
                # Ensure cookies per batch is reasonable (between 12 and 36)
                if cookies_per_batch < 12 or cookies_per_batch > 36:
                    continue
                
                answer_str = str(num_neighbors)
                
                # Question text
                q_text = f"Mason made {num_batches} batches of cookies with {cookies_per_batch} cookies in each batch. If he gave {cookies_per_neighbor} cookies to each of his neighbors and had {cookies_left} left, how many neighbors does Mason have?"
                
                # Generate distractors - ensure they are positive whole numbers
                distractors = []
                
                # Add common wrong answers
                possible_wrong = [
                    num_neighbors + 1,
                    max(num_neighbors - 1, 1),
                    num_neighbors + 2,
                    max(num_neighbors - 2, 1),
                    num_neighbors + 3,
                    num_neighbors * 2,
                    num_neighbors // 2 + 1,
                    num_neighbors + 4,
                    num_neighbors - 3,
                    cookies_per_neighbor,
                    cookies_per_batch,
                    num_batches,
                    total_cookies // cookies_per_neighbor,
                    (total_cookies - cookies_left) // cookies_per_neighbor,
                ]
                
                # Filter to only positive whole numbers that aren't the answer
                for w in possible_wrong:
                    if w != num_neighbors and w > 0 and w not in distractors:
                        distractors.append(w)
                
                # Shuffle and take first 4 distractors
                random.shuffle(distractors)
                distractors = distractors[:4]
                
                # Build choices with answer + 4 distractors
                choices = [str(num_neighbors)] + [str(d) for d in distractors]
                
                # Shuffle choices
                random.shuffle(choices)
                correct_index = choices.index(str(num_neighbors))
                break
            
            # Fallback if no valid problem found
            else:
                q_text = "Mason made 3 batches of cookies with 12 cookies in each batch. If he gave 4 cookies to each of his neighbors and had 4 left, how many neighbors does Mason have?"
                choices = ["8", "7", "9", "6", "10"]
                random.shuffle(choices)
                correct_index = choices.index("8")
            
        elif problem_type == 9:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Format: 14◊ × 8 = 1,168
                # Find the missing digit ◊
                
                # Generate possible missing digits (0-9)
                missing_digit = random.randint(0, 9)
                
                # Create the 3-digit number: 1,4,missing_digit
                three_digit_num = 140 + missing_digit
                
                # Choose a multiplier (1-digit number between 4 and 9)
                multiplier = random.randint(4, 9)
                
                # Calculate the product
                product = three_digit_num * multiplier
                
                # Ensure product is between 1000 and 9999 (4 digits) for reasonable problems
                if product < 1000 or product > 9999:
                    continue
                
                answer_str = str(missing_digit)
                
                # Format the multiplication problem with proper alignment
                # Display as:
                #    14◊
                #  ×  8
                #  -----
                #   1,168
                
                q_text = f"""In the multiplication problem shown, \\(\\lozenge\\) is equal to which of the following digits?

        \\[
        \\begin{{array}}{{r}}
           14\\lozenge \\\\
         \\times\\ \\; {multiplier} \\\\
         \\hline
           {product:,}
        \\end{{array}}
        \\]"""
                
                # Generate distractors (other digits 0-9 that are not the answer)
                possible_digits = [str(d) for d in range(10) if d != missing_digit]
                random.shuffle(possible_digits)
                distractors = possible_digits[:4]
                
                choices = [answer_str] + distractors
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break

        elif problem_type == 10:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Generate numbers where the percent is a whole number
                total_people = random.choice([15, 20, 25, 30, 40, 50, 100])
                
                # Choose a number that does the activity
                do_activity = random.randint(int(total_people * 0.3), int(total_people * 0.9))
                
                # Calculate number that do NOT do it
                do_not = total_people - do_activity
                
                # Calculate percent (should be a whole number)
                if (do_not * 100) % total_people != 0:
                    continue
                    
                percent_do_not = (do_not * 100) // total_people
                answer_str = f"{percent_do_not}%"
                
                # Question text
                q_text = f"In a survey of {total_people} people, {do_activity} reported watching television every day. What percent of people do not watch television every day?"
                
                # Generate distractors
                distractors = [
                    f"{percent_do_not + 5}%",
                    f"{max(percent_do_not - 5, 0)}%",
                    f"{percent_do_not + 10}%",
                    f"{max(percent_do_not - 10, 0)}%",
                    f"{100 - percent_do_not}%",
                ]
                
                choices = [answer_str] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break
        elif problem_type == 11:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Generate the difference between length and width
                difference = random.randint(3, 12)
                
                # Width is w, length is w + difference
                # Area = length × width = w × (w + difference) = w² + (difference)w
                
                # Answer with LaTeX
                answer_str = f"\\(w^2 + {difference}w\\)"
                
                # Question with LaTeX
                q_text = f"If the length of a rectangle is {difference} more than the width, \\(w\\), what is the area of the rectangle in terms of \\(w\\)?"
                
                # Generate distractors with LaTeX (common mistakes)
                distractors = [
                    f"\\(w^2 + {difference}\\)",
                    f"\\({difference}w^2\\)",
                    f"\\(2w + {difference}\\)",
                    f"\\(w^2 + {difference + 2}w\\)",
                    f"\\({difference}w\\)",
                    f"\\(w^2 + {difference - 1}w\\)",
                ]
                
                # Remove duplicates and ensure answer is in choices
                choices = [answer_str] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break
        elif problem_type == 12:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Format: n items at $X each, which expression shows total cost?
                
                # Generate price per item
                price_per_item = random.choice([8, 10, 12, 15, 20, 25])
                
                # Answer is n × price_per_item or price_per_item × n
                answer_str = f"\\({price_per_item}n\\)"
                
                # Question with LaTeX
                q_text = f"Paige purchased \\(n\\) shirts for ${price_per_item} each. Which tells how many dollars she paid for the shirts?"
                
                # Generate distractors (common mistakes)
                distractors = [
                    f"\\(n + {price_per_item}\\)",
                    f"\\(n - {price_per_item}\\)",
                    f"\\({price_per_item} - n\\)",
                    f"\\(\\frac{{{price_per_item}}}{{n}}\\)",
                    f"\\(\\frac{{n}}{{{price_per_item}}}\\)",
                    f"\\({price_per_item}\\)",
                    f"\\(n\\)",
                ]
                
                # Remove duplicates and ensure answer is in choices
                choices = [answer_str] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break
        elif problem_type == 13:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Format: The ratio of a to b is the same as the ratio of ? to c
                
                # Generate the original ratio
                a = random.randint(2, 12)
                b = random.randint(a + 1, a + 15)
                
                # Choose a multiplier to create equivalent ratio
                multiplier = random.randint(2, 6)
                
                # The equivalent ratio is (a × m) : (b × m)
                given_first = a * multiplier
                answer = b * multiplier
                
                answer_str = str(answer)
                
                # Question with LaTeX
                q_text = f"The ratio of {a} to {b} is the same as the ratio of {given_first} to ____."
                
                # Generate distractors
                distractors = [
                    str(answer + 1),
                    str(max(answer - 1, 1)),
                    str(answer + 2),
                    str(answer - 2) if answer > 2 else str(answer + 3),
                    str(b * (multiplier + 1)),
                    str(b * (multiplier - 1)) if multiplier > 1 else str(b * (multiplier + 2)),
                ]
                
                choices = [answer_str] + list(dict.fromkeys(distractors))
                choices = choices[:5]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break
        elif problem_type == 14:

            
            attempts = 0
            q_text = ""
            answer_str = ""
            choices = []
            correct_index = 0
            
            while attempts < max_attempts:
                attempts += 1
                
                # Andre walks (num/den) mile for every X miles he runs
                walk_num = 1
                walk_den = random.randint(2, 5)  # 2, 3, 4, or 5
                run_dist = random.randint(2, 6)  # miles run per walking fraction
                
                # Choose multiplier to ensure whole number answer
                multiplier = random.randint(1, 8)
                total_run = run_dist * walk_den * multiplier
                
                # Total walked = walk_num * multiplier
                total_walk = walk_num * multiplier
                
                # Set the question text
                q_text = f"Andre walks \\(\\frac{{{walk_num}}}{{{walk_den}}}\\) mile for every {run_dist} miles he runs. How many miles will he walk if he runs {total_run} miles?"
                
                answer_str = str(total_walk)
                
                # Generate distractors
                distractors = [
                    str(total_walk + 1),
                    str(max(total_walk - 1, 0)),
                    str(total_run),
                    str(total_run // run_dist),
                    str(total_walk * 2),
                    str(total_run // (run_dist * walk_den)),
                ]
                
                # Remove duplicates
                unique_distractors = []
                for d in distractors:
                    if d != answer_str and d not in unique_distractors:
                        unique_distractors.append(d)
                
                choices = [answer_str] + unique_distractors[:4]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break  # Always break on first attempt since numbers always work
            
            # Fallback (should never be needed now)
            if not q_text:
                q_text = "Andre walks \\(\\frac{1}{2}\\) mile for every 2 miles he runs. How many miles will he walk if he runs 8 miles?"
                answer_str = "2"
                choices = ["2", "3", "1", "4", "6"]
                random.shuffle(choices)
                correct_index = choices.index("2")

        elif problem_type == 15:
            # Define possible fractions with their word forms and divisors
            fractions = {
                'one-third': 3,
                'one-fourth': 4,
                'one-fifth': 5,
                'one-sixth': 6,
                'one-eighth': 8
            }
            
            # Choose a random fraction
            fraction_text = random.choice(list(fractions.keys()))
            divisor = fractions[fraction_text]
            
            # Choose a dozen price that is divisible by the divisor
            # Generate multiples of the divisor between $12 and $60
            max_multiple = 60 // divisor
            multiplier = random.randint(2, max_multiple)
            dozen_price = divisor * multiplier
            
            # Calculate the price for the fraction
            fraction_price = dozen_price // divisor
            answer_str = f"${fraction_price}"
            
            # Question with fraction in word form
            q_text = f"If a cake cost ${dozen_price}, how much does {fraction_text} of a cake cost?"
            
            # Generate distractors
            distractors = [
                f"${fraction_price + (dozen_price // 12)}",
                f"${max(fraction_price - (dozen_price // 12), 0)}",
                f"${fraction_price + 1}",
                f"${max(fraction_price - 1, 0)}",
                f"${dozen_price // 2}",
                f"${dozen_price // 6}",
                f"${dozen_price // 3}",
            ]
            
            # Remove duplicates
            unique_distractors = []
            for d in distractors:
                if d != answer_str and d not in unique_distractors:
                    unique_distractors.append(d)
            
            choices = [answer_str] + unique_distractors[:4]
            random.shuffle(choices)
            correct_index = choices.index(answer_str)
            
        elif problem_type == 16:

            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # Generate random changes (down and up amounts)
                # Ensure down amount is less than up amount for positive net change
                down_amount = random.randint(1, 5)
                up_amount = random.randint(down_amount + 1, down_amount + 8)
                
                # Calculate net change (up - down = positive)
                net_change = up_amount - down_amount
                
                # Answer with variable d (always positive in this version)
                answer_str = f"\\(d + {net_change}\\)"
                
                # Question with variable d
                q_text = f"The depth of a lake was \\(d\\) feet at the beginning of the year. What was the depth, in feet, after it went down {down_amount} feet and up {up_amount} feet?"
                
                # Generate distractors - common mistakes
                distractors = []
                
                # 1. d - (up - down) - reversing the sign
                distractors.append(f"\\(d - {net_change}\\)")
                
                # 2. d - up_amount + down_amount (wrong order)
                wrong1 = down_amount - up_amount  # This is negative
                distractors.append(f"\\(d - {abs(wrong1)}\\)")
                
                # 3. d - (up_amount + down_amount) or d + (up_amount + down_amount)
                total = down_amount + up_amount
                distractors.append(f"\\(d + {total}\\)")
                distractors.append(f"\\(d - {total}\\)")
                
                # 4. d - down_amount (only subtract down, forget up)
                distractors.append(f"\\(d - {down_amount}\\)")
                
                # 5. d + up_amount (only add up, forget down)
                distractors.append(f"\\(d + {up_amount}\\)")
                
                # 6. d - up_amount (subtract up, forget down)
                distractors.append(f"\\(d - {up_amount}\\)")
                
                # 7. d + down_amount (add down instead of subtract)
                distractors.append(f"\\(d + {down_amount}\\)")
                
                # 8. d - (up_amount - down_amount + 1) or d - (up_amount - down_amount - 1)
                if net_change > 1:
                    distractors.append(f"\\(d - {net_change + 1}\\)")
                    distractors.append(f"\\(d + {net_change + 1}\\)")
                    distractors.append(f"\\(d - {net_change - 1}\\)")
                    distractors.append(f"\\(d + {net_change - 1}\\)")
                
                # Remove duplicates and ensure answer is in choices
                unique_distractors = []
                for d in distractors:
                    if d != answer_str and d not in unique_distractors:
                        unique_distractors.append(d)
                
                choices = [answer_str] + unique_distractors[:4]
                random.shuffle(choices)
                correct_index = choices.index(answer_str)
                break
            
            # Fallback (should never be needed)
            if not q_text:
                q_text = "The depth of a lake was \\(d\\) feet at the beginning of the year. What was the depth, in feet, after it went down 2 feet and up 3 feet?"
                answer_str = "\\(d + 1\\)"
                choices = ["\\(d + 1\\)", "\\(d - 1\\)", "\\(d + 5\\)", "\\(d - 5\\)", "\\(d\\)"]
                random.shuffle(choices)
                correct_index = choices.index("\\(d + 1\\)")
            
        
        problems.append((q_text, choices, correct_index))

    return problems


def gen_random_mix(n=5, section='verbal'):
    """
    Deterministic mixed practice generator.
    
    - Quant:
        * Generates 5 problem types from each generator in order
        * If n < 5 → only generate from the first generator (Number Sense & Arithmetic)
        * If n <= 20 → fills generators in order: Number Sense → Algebra → Geometry → Data
    - Verbal:
        * Alternates synonym / analogy
        * No repeats
    """

    problems = []
    n = min(n, 10)

    if section == 'quant':
        generators = [
            gen_number_sense_arithmetic,
            gen_algebraic_thinking,
            gen_geometry_measurement,
            gen_data_probability
        ]

        # Each generator can contribute up to 5 questions
        per_generator = 5

        total_generated = 0
        for gen in generators:
            remaining = n - total_generated
            num_to_generate = min(per_generator, remaining)
            if num_to_generate > 0:
                problems.extend(gen(num_to_generate))
                total_generated += num_to_generate
            if total_generated >= n:
                break

    elif section == 'verbal':
        for i in range(n):
            if i % 2 == 0:
                problems.extend(gen_synonyms(1))
            else:
                problems.extend(gen_analogies(1))
    else:
        raise ValueError("section must be 'quant' or 'verbal'")

    return problems

# ============================================
# FUNDAMENTALS MATH QUESTION GENERATORS
# ============================================

def generate_fundamentals_problem(operation, number_type):
    """Generate a single fundamentals math problem with 5 choices."""
    
    if operation == "addition":
        return generate_addition_problem(number_type)
    elif operation == "subtraction":
        return generate_subtraction_problem(number_type)
    elif operation == "multiplication":
        return generate_multiplication_problem(number_type)
    elif operation == "division":
        return generate_division_problem(number_type)
    else:
        return generate_addition_problem(number_type)

def generate_addition_problem(number_type):
    """Generate addition problems with 5 choices."""
    attempts = 0
    while attempts < 50:
        attempts += 1
        
        if number_type == "whole":
            a = random.randint(20, 999)
            b = random.randint(20, 999)
            answer = a + b
            q_text = f"What is {a} + {b}?"
            
        elif number_type == "fraction":
            # Generate fractions with different denominators
            denom1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            denom2 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            a_num = random.randint(1, denom1 - 1)
            b_num = random.randint(1, denom2 - 1)
            
            # Find common denominator
            common_den = denom1 * denom2 // math.gcd(denom1, denom2)
            a_adjusted = a_num * (common_den // denom1)
            b_adjusted = b_num * (common_den // denom2)
            answer_num = a_adjusted + b_adjusted
            
            # Simplify the result
            gcd = math.gcd(answer_num, common_den)
            if gcd > 1:
                answer_num = answer_num // gcd
                common_den = common_den // gcd
            
            if answer_num >= common_den:
                whole = answer_num // common_den
                remainder = answer_num % common_den
                if remainder == 0:
                    answer_str = str(whole)
                else:
                    answer_str = f"{whole} {remainder}/{common_den}"
            else:
                answer_str = f"{answer_num}/{common_den}"
            
            q_text = f"What is {a_num}/{denom1} + {b_num}/{denom2}?"
            choices = generate_fraction_choices(answer_num, common_den, answer_str)
            return (q_text, choices, 0)
            
        elif number_type == "decimal":
            a = round(random.uniform(0.1, 99.9), 1)
            b = round(random.uniform(0.1, 99.9), 1)
            answer = round(a + b, 1)
            q_text = f"What is {a} + {b}?"
            
        else:  # integer (including negative)
            a = random.randint(-50, 50)
            b = random.randint(-50, 50)
            answer = a + b
            q_text = f"What is {a} + {b}?"
        
        # Generate 5 choices for non-fraction problems
        choices = generate_choices(answer, number_type)
        if choices:
            return (q_text, choices, 0)
    
    # Fallback
    return ("What is 5 + 3?", ["8", "7", "9", "6", "10"], 0)

def generate_subtraction_problem(number_type):
    """Generate subtraction problems with 5 choices."""
    attempts = 0
    while attempts < 50:
        attempts += 1
        
        if number_type == "whole":
            a = random.randint(50, 999)
            b = random.randint(20, a - 1)
            answer = a - b
            q_text = f"What is {a} - {b}?"
            
        elif number_type == "fraction":
            # Generate fractions with different denominators
            denom1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            denom2 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            a_num = random.randint(denom1 // 2 + 1, denom1 - 1) if denom1 > 2 else random.randint(1, denom1 - 1)
            b_num = random.randint(1, min(a_num * (denom2 // denom1) - 1, denom2 - 1)) if denom1 <= denom2 else random.randint(1, denom2 - 1)
            
            # Ensure a_num/denom1 > b_num/denom2
            while (a_num * denom2) <= (b_num * denom1):
                b_num = random.randint(1, max(1, b_num - 1))
                if b_num <= 0:
                    b_num = 1
                    break
            
            # Find common denominator
            common_den = denom1 * denom2 // math.gcd(denom1, denom2)
            a_adjusted = a_num * (common_den // denom1)
            b_adjusted = b_num * (common_den // denom2)
            answer_num = a_adjusted - b_adjusted
            
            # Simplify the result
            gcd = math.gcd(answer_num, common_den)
            if gcd > 1:
                answer_num = answer_num // gcd
                common_den = common_den // gcd
            
            if answer_num >= common_den:
                whole = answer_num // common_den
                remainder = answer_num % common_den
                if remainder == 0:
                    answer_str = str(whole)
                else:
                    answer_str = f"{whole} {remainder}/{common_den}"
            else:
                answer_str = f"{answer_num}/{common_den}"
            
            q_text = f"What is {a_num}/{denom1} - {b_num}/{denom2}?"
            choices = generate_fraction_choices(answer_num, common_den, answer_str)
            return (q_text, choices, 0)
            
        elif number_type == "decimal":
            a = round(random.uniform(1.0, 99.9), 1)
            b = round(random.uniform(0.1, a - 0.1), 1)
            answer = round(a - b, 1)
            q_text = f"What is {a} - {b}?"
            
        else:  # integer
            a = random.randint(-30, 30)
            b = random.randint(-30, 30)
            answer = a - b
            q_text = f"What is {a} - {b}?"
        
        choices = generate_choices(answer, number_type)
        if choices:
            return (q_text, choices, 0)
    
    return ("What is 10 - 3?", ["7", "8", "6", "9", "5"], 0)

def generate_multiplication_problem(number_type):
    """Generate multiplication problems with 5 choices."""
    attempts = 0
    while attempts < 50:
        attempts += 1
        
        if number_type == "whole":
            a = random.randint(2, 20)
            b = random.randint(2, 20)
            answer = a * b
            q_text = f"What is {a} × {b}?"
            
        elif number_type == "fraction":
            # Multiply fractions
            denom1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            denom2 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            a_num = random.randint(1, denom1 - 1)
            b_num = random.randint(1, denom2 - 1)
            answer_num = a_num * b_num
            answer_den = denom1 * denom2
            
            # Simplify if possible
            gcd = math.gcd(answer_num, answer_den)
            if gcd > 1:
                answer_num = answer_num // gcd
                answer_den = answer_den // gcd
            
            if answer_num >= answer_den:
                whole = answer_num // answer_den
                remainder = answer_num % answer_den
                if remainder == 0:
                    answer_str = str(whole)
                else:
                    answer_str = f"{whole} {remainder}/{answer_den}"
            else:
                answer_str = f"{answer_num}/{answer_den}"
            
            q_text = f"What is {a_num}/{denom1} × {b_num}/{denom2}?"
            choices = generate_fraction_choices(answer_num, answer_den, answer_str)
            return (q_text, choices, 0)
            
        elif number_type == "decimal":
            a = round(random.uniform(0.1, 9.9), 1)
            b = round(random.uniform(0.1, 9.9), 1)
            answer = round(a * b, 2)
            q_text = f"What is {a} × {b}?"
            
        else:  # integer
            a = random.randint(-12, 12)
            b = random.randint(-12, 12)
            answer = a * b
            q_text = f"What is {a} × {b}?"
        
        choices = generate_choices(answer, number_type)
        if choices:
            return (q_text, choices, 0)
    
    return ("What is 6 × 7?", ["42", "43", "41", "44", "40"], 0)

def generate_division_problem(number_type):
    """Generate division problems with 5 choices."""
    attempts = 0
    while attempts < 50:
        attempts += 1
        
        if number_type == "whole":
            answer = random.randint(1, 15)
            divisor = random.randint(1, 15)
            dividend = answer * divisor
            q_text = f"What is {dividend} ÷ {divisor}?"
            
        elif number_type == "fraction":
            # Divide fractions (multiply by reciprocal)
            denom1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            denom2 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
            a_num = random.randint(1, denom1 - 1)
            b_num = random.randint(1, denom2 - 1)
            
            # Division: a/b ÷ c/d = a/b × d/c
            answer_num = a_num * denom2
            answer_den = denom1 * b_num
            
            gcd = math.gcd(answer_num, answer_den)
            if gcd > 1:
                answer_num = answer_num // gcd
                answer_den = answer_den // gcd
            
            if answer_num >= answer_den:
                whole = answer_num // answer_den
                remainder = answer_num % answer_den
                if remainder == 0:
                    answer_str = str(whole)
                else:
                    answer_str = f"{whole} {remainder}/{answer_den}"
            else:
                answer_str = f"{answer_num}/{answer_den}"
            
            q_text = f"What is {a_num}/{denom1} ÷ {b_num}/{denom2}?"
            choices = generate_fraction_choices(answer_num, answer_den, answer_str)
            return (q_text, choices, 0)
            
        elif number_type == "decimal":
            # Generate problems where answer terminates at tenths place
            # Either whole number or one decimal place
            answer = random.choice([
                random.randint(1, 20),  # Whole number
                round(random.randint(1, 20) + random.randint(1, 9) / 10, 1)  # One decimal
            ])
            divisor = round(random.uniform(0.1, 5.0), 1)
            dividend = round(answer * divisor, 2)
            q_text = f"What is {dividend} ÷ {divisor}?"
            # Ensure answer doesn't have floating point issues
            if isinstance(answer, float):
                answer = round(answer, 1)
            else:
                answer = int(answer)
            
        else:  # integer
            answer = random.randint(-15, 15)
            if answer == 0:
                answer = random.randint(1, 15)
            divisor = random.randint(-15, 15)
            if divisor == 0:
                divisor = random.randint(1, 15)
            dividend = answer * divisor
            q_text = f"What is {dividend} ÷ {divisor}?"
        
        choices = generate_choices(answer, number_type)
        if choices:
            return (q_text, choices, 0)
    
    return ("What is 24 ÷ 6?", ["4", "5", "3", "6", "7"], 0)

def generate_choices(answer, number_type):
    """Generate 5 choices including the correct answer."""
    if number_type == "fraction":
        # Fractions handled separately
        return None
    
    # Convert answer to string properly
    if isinstance(answer, float):
        # Round to avoid floating point issues
        answer = round(answer, 2)
        if answer.is_integer():
            answer_str = str(int(answer))
        else:
            answer_str = str(answer)
            # Remove trailing zeros
            if '.' in answer_str:
                answer_str = answer_str.rstrip('0').rstrip('.')
    else:
        answer_str = str(answer)
    
    # Generate distractors
    distractors = set()
    distractors.add(answer_str)
    
    # Different strategies for generating wrong answers
    if isinstance(answer, (int, float)):
        offset = max(1, abs(int(answer)) // 4 + 1) if answer != 0 else 5
        
        for _ in range(30):
            # Various distractor generation methods
            strategies = [
                lambda: str(answer + random.randint(1, offset * 2)),
                lambda: str(answer - random.randint(1, offset * 2)),
                lambda: str(answer + random.randint(1, 5)),
                lambda: str(answer - random.randint(1, 5)),
                lambda: str(answer * 2),
                lambda: str(answer // 2 + 1) if answer > 0 else str(answer - 1),
                lambda: str(answer + 10),
                lambda: str(answer - 10),
                lambda: str(answer + 100) if isinstance(answer, int) else str(answer + 10),
                lambda: str(abs(answer) + random.randint(1, 3)),
                lambda: str(answer + random.randint(-2, 2)),
                lambda: str(answer * 3),
                lambda: str(answer + 50) if isinstance(answer, int) else str(answer + 5),
            ]
            
            for strategy in strategies:
                try:
                    dist = strategy()
                    # Only add if different and not already in set
                    if dist != answer_str and dist not in distractors:
                        distractors.add(dist)
                except:
                    pass
                
                if len(distractors) >= 5:
                    break
            
            if len(distractors) >= 5:
                break
    
    # Ensure we have exactly 5 choices
    choices = list(distractors)[:5]
    
    # If we don't have 5 choices, add more
    counter = 1
    while len(choices) < 5:
        if isinstance(answer, (int, float)):
            extra = str(answer + random.randint(1, 10) * counter)
        else:
            extra = str(random.randint(1, 100))
        if extra not in choices:
            choices.append(extra)
        counter += 1
    
    random.shuffle(choices)
    return choices

def generate_fraction_choices(answer_num, answer_den, answer_str):
    """Generate 5 fraction choices."""
    choices = set()
    choices.add(answer_str)
    
    # Generate wrong fractions
    for _ in range(30):
        # Various ways to generate wrong fractions
        strategies = [
            lambda: (answer_num + random.randint(1, max(2, answer_den // 3)), answer_den),
            lambda: (max(1, answer_num - random.randint(1, max(2, answer_den // 3))), answer_den),
            lambda: (answer_num + random.randint(1, 5), answer_den + random.randint(1, 3)),
            lambda: (max(1, answer_num - random.randint(1, 3)), max(1, answer_den - random.randint(1, 2))),
            lambda: (answer_num + random.randint(1, 3), answer_den + random.randint(1, 3)),
        ]
        
        for strategy in strategies:
            try:
                wrong_num, wrong_den = strategy()
                if wrong_num > 0 and wrong_den > 0:
                    # Simplify if possible
                    gcd = math.gcd(wrong_num, wrong_den)
                    if gcd > 1:
                        w_num = wrong_num // gcd
                        w_den = wrong_den // gcd
                    else:
                        w_num = wrong_num
                        w_den = wrong_den
                    
                    if w_num >= w_den:
                        whole = w_num // w_den
                        rem = w_num % w_den
                        if rem == 0:
                            frac_str = str(whole)
                        else:
                            frac_str = f"{whole} {rem}/{w_den}"
                    else:
                        frac_str = f"{w_num}/{w_den}"
                    
                    if frac_str != answer_str:
                        choices.add(frac_str)
            except:
                pass
            
            if len(choices) >= 5:
                break
        
        if len(choices) >= 5:
            break
    
    # Ensure we have exactly 5 choices
    choices_list = list(choices)[:5]
    counter = 1
    while len(choices_list) < 5:
        extra_num = answer_num + random.randint(1, 3) * counter
        extra_den = answer_den + random.randint(0, 2)
        if extra_den <= 0:
            extra_den = 2
        gcd = math.gcd(extra_num, extra_den)
        if gcd > 1:
            extra_num = extra_num // gcd
            extra_den = extra_den // gcd
        extra = f"{extra_num}/{extra_den}"
        if extra not in choices_list:
            choices_list.append(extra)
        counter += 1
    
    random.shuffle(choices_list)
    return choices_list

# ============================================
# INSPIRATIONAL QUOTES
# ============================================

INSPIRATIONAL_QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("The only impossible journey is the one you never begin.", "Tony Robbins"),
    ("Your education is a dress rehearsal for a life that is yours to lead.", "Nora Ephron"),
    ("The mind is not a vessel to be filled, but a fire to be kindled.", "Plutarch"),
    ("Education is the most powerful weapon which you can use to change the world.", "Nelson Mandela"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Don't let what you cannot do interfere with what you can do.", "John Wooden"),
    ("The beautiful thing about learning is that nobody can take it away from you.", "B.B. King"),
    ("Education is not preparation for life; education is life itself.", "John Dewey"),
    ("The only person who is educated is the one who has learned how to learn and change.", "Carl Rogers"),
]

def get_inspirational_quote():
    """Return a random inspirational quote and its author."""
    return random.choice(INSPIRATIONAL_QUOTES)

# ============================================
# FLASK ROUTES TO ADD
# ============================================



# === Mobile-friendly HTML template ===

PAGE_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>SSAT Study App</title>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
* {
    box-sizing: border-box;
}
body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background: #f0f4f8; 
    color: #1a2a3a; 
    padding: 12px; 
    margin: 0;
}
.container { 
    max-width: 900px; 
    margin: 0 auto; 
    background: white; 
    padding: 16px; 
    border-radius: 16px; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
h1 { 
    margin-top: 0; 
    color: #003366; 
    font-size: 1.6rem;
}
h2 {
    font-size: 1.3rem;
    margin: 0 0 12px 0;
}
form.inline { 
    display: flex; 
    gap: 10px; 
    align-items: center; 
    flex-wrap: wrap; 
    margin-bottom: 20px;
}
select, input[type=number] { 
    padding: 10px 12px; 
    font-size: 16px; 
    border-radius: 10px; 
    border: 2px solid #006; 
    background: #eef; 
    width: auto;
    min-width: 140px;
}
button { 
    background: #006; 
    color: #cff; 
    border: none; 
    padding: 10px 18px; 
    border-radius: 10px; 
    cursor: pointer; 
    font-size: 16px;
    font-weight: 600;
    transition: background 0.2s;
}
button:active {
    background: #004;
}
button.secondary { 
    background: #024; 
    font-weight: normal;
}
button.danger {
    background: #900;
}
button.danger:active {
    background: #600;
}
button.test-btn {
    background: #2d6a4f;
}
button.test-btn:active {
    background: #1b4d3e;
}
.problem { 
    margin: 20px 0; 
    padding: 16px; 
    border-radius: 12px; 
    border: 1px solid #ccd; 
    background: #fefefe;
}
.choices {
    margin-top: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
}
.choice {
    background: #f2f8ff;
    padding: 12px 16px;
    border-radius: 10px;
    border: 1px solid #cde;
    cursor: pointer;
    display: inline-block;
    width: auto;
    font-size: 16px;
    transition: all 0.2s;
    touch-action: manipulation;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
.choice:active {
    transform: scale(0.98);
    background: #e0e8f0;
}
.selected { 
    outline: 3px solid #88f; 
    background: #e8eeff;
}
.result { 
    margin-left: 12px; 
    font-weight: 700; 
    margin-top: 10px;
}
.correct { 
    color: #2a7a2a; 
}
.incorrect { 
    color: #c33; 
}
.score { 
    font-size: 20px; 
    font-weight: 700; 
    margin-top: 16px; 
    padding: 12px;
    background: #e8f0fe;
    border-radius: 12px;
    text-align: center;
}
.header { 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 16px;
}
.small { 
    font-size: 14px; 
    color: #446; 
}
.choice.correct {
    background-color: #d4edda;
    border-color: #a6d8a8;
}
.choice.incorrect {
    background-color: #f8d7da;
    border-color: #f5a6a6;
}
hr {
    margin: 16px 0;
    border: none;
    border-top: 2px solid #e0e8f0;
}
@media (max-width: 600px) {
    .container {
        padding: 12px;
    }
    h1 {
        font-size: 1.4rem;
    }
    .choice {
        padding: 10px 14px;
        font-size: 15px;
        width: 100%;
    }
    select, input[type=number] {
        width: 100%;
        min-width: auto;
    }
    form.inline {
        flex-direction: column;
        align-items: stretch;
    }
    button {
        width: 100%;
    }
    .header {
        flex-direction: column;
        text-align: center;
    }
    .problem {
        padding: 12px;
    }
}

/* ========== READING PASSAGE STYLES ========== */
.passage-text {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 1.4rem;
    line-height: 1.6;
    color: #1a2a3a;
    background: #fafcfd;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #003366;
    margin-bottom: 20px;
    letter-spacing: 0.01em;
}

.poetry-text {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 1.4rem;
    line-height: 1.8;
    color: #1a2a3a;
    background: #fafcfd;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #6a0dad;
    margin-bottom: 20px;
    white-space: pre-wrap;
    font-style: normal;
    letter-spacing: 0.01em;
}

.poetry-text br {
    margin-bottom: 0.5em;
}

.passage-title {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 1.3rem;
    font-weight: bold;
    color: #003366;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid #cde;
}

.problem > div:first-child {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 12px;
}

.diagram {
    text-align: center;
    margin: 15px 0;
    padding: 10px;
    background: #f5f7fa;
    border-radius: 12px;
}
.diagram svg {
    max-width: 100%;
    height: auto;
}

.button-group {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

/* ========== CROWN DISPLAY FOR SCORED ASSIGNMENTS ========== */
.score-display {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 25px 35px;
    border-radius: 16px;
    border: 2px solid #dee2e6;
    margin-top: 16px;
}

.score-text {
    text-align: center;
}

.score-text .percentage {
    font-size: 3rem;
    font-weight: 800;
    color: #003366;
}

.score-text .score-detail {
    font-size: 1rem;
    color: #495057;
}

.crown-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5px;
}

.crown-svg {
    width: 120px;
    height: 120px;
    display: block;
    filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2));
    transition: transform 0.3s ease;
}

.crown-svg:hover {
    transform: scale(1.08) rotate(-3deg);
}

.crown-label {
    font-size: 0.9rem;
    font-weight: 700;
    color: #495057;
    text-align: center;
    margin-top: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Crown animations */
@keyframes crownGlow {
    0% { filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2)); }
    50% { filter: drop-shadow(0 4px 30px rgba(255,215,0,0.6)) drop-shadow(0 0 60px rgba(255,215,0,0.3)); }
    100% { filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2)); }
}

.crown-diamond .crown-svg {
    animation: crownGlow 2.5s ease-in-out infinite;
}

@keyframes sparkle {
    0%, 100% { opacity: 0.3; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

.sparkle-star {
    animation: sparkle 2s ease-in-out infinite;
}

@media (max-width: 600px) {
    .score-display {
        flex-direction: column;
        padding: 15px 20px;
        gap: 15px;
    }
    
    .crown-svg {
        width: 90px;
        height: 90px;
    }
    
    .score-text .percentage {
        font-size: 2.4rem;
    }
}
</style>
<script>

function updateTopicOptions(){
    const section = document.getElementById('section').value;
    const topic = document.getElementById('topic');
    const numContainer = document.getElementById('num_container');
    
    topic.innerHTML = '';
    let options = [];
    
    if(section === 'verbal'){ 
        options = ['Synonyms', 'Analogies', 'Mixed Practice'];
        numContainer.style.display = 'flex';
    }
    else if(section === 'reading'){ 
        options = ['Nonfiction', 'Fiction', 'Poetry'];
        numContainer.style.display = 'none';
    }
    else if(section === 'quant'){ 
        options = ['Number Sense and Arithmetic', 'Algebraic Thinking', 'Geometry and Measurement', 'Data and Probability', 'SSAT Practice'];
        numContainer.style.display = 'flex';
    }
    
    for(const opt of options){
        const el = document.createElement('option'); 
        el.value = opt; 
        el.text = opt; 
        topic.appendChild(el);
    }
}
document.addEventListener('DOMContentLoaded', ()=>{
    const section = document.getElementById('section');
    if(section){ updateTopicOptions(); section.addEventListener('change', updateTopicOptions); }
});

function selectChoice(pIdx, cIdx){
    const container=document.getElementById('p'+pIdx);
    container.querySelectorAll('.choice').forEach((it,i)=>it.classList.toggle('selected',i===cIdx));
    document.getElementById('answer_'+pIdx).value=cIdx;
}

</script>

</head>
<body>
<div class="container">
<div class="header">
    <h1>📚 SSAT Study App</h1>
    <div class="small">
        <form style="display:inline" method="post" action="/reset">
            <button class="secondary danger" type="submit">Reset Session</button>
        </form>
    </div>
</div>

<!-- Crown Display Viewer -->
<details style="margin: 15px 0; background: #f8f9fa; padding: 15px; border-radius: 12px; border: 2px solid #dee2e6;">
    <summary style="cursor: pointer; font-weight: 700; color: #003366; font-size: 1.1rem;">
        👑 View Crown Collection
    </summary>
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; padding: 20px 0; gap: 15px;">
        
        <!-- Bronze Crown (70-79%) -->
        <div style="text-align: center;">
            <svg width="100" height="100" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2));">
                <defs>
                    <linearGradient id="viewBronze" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#e8a85c;stop-opacity:1" />
                        <stop offset="30%" style="stop-color:#cd7f32;stop-opacity:1" />
                        <stop offset="70%" style="stop-color:#cd7f32;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#8b5a2b;stop-opacity:1" />
                    </linearGradient>
                    <radialGradient id="viewAmber" cx="40%" cy="40%" r="60%">
                        <stop offset="0%" style="stop-color:#f0c060;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#cd7f32;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#8b5a2b;stop-opacity:1" />
                    </radialGradient>
                </defs>
                <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#viewBronze)" stroke="#8b5a2b" stroke-width="1"/>
                <path d="M16,86 C20,82 24,89 28,86 C32,82 36,89 40,86 C44,82 48,89 52,86 C56,82 60,89 64,86 C68,82 72,89 76,86 C80,82 84,89 88,86 C92,82 96,89 100,86 C104,82" stroke="#a0672a" stroke-width="1.5" fill="none"/>
                <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#viewBronze)" stroke="#8b5a2b" stroke-width="0.5"/>
                <polygon points="50,25 60,15 70,25" fill="white" opacity="0.15"/>
                <circle cx="24" cy="35" r="7" fill="url(#viewAmber)" stroke="#8b5a2b" stroke-width="1.5"/>
                <circle cx="60" cy="20" r="10" fill="url(#viewAmber)" stroke="#8b5a2b" stroke-width="2"/>
                <circle cx="96" cy="35" r="7" fill="url(#viewAmber)" stroke="#8b5a2b" stroke-width="1.5"/>
                <circle cx="42" cy="48" r="5" fill="#d4a050"/>
                <circle cx="78" cy="48" r="5" fill="#d4a050"/>
                <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.4"/>
                <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.3"/>
                <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.3"/>
                <path d="M32,52 C36,44 40,44 44,50" stroke="#a0672a" stroke-width="1.5" fill="none"/>
                <path d="M76,50 C80,44 84,44 88,52" stroke="#a0672a" stroke-width="1.5" fill="none"/>
                <circle cx="36" cy="70" r="2.5" fill="#a0672a"/>
                <circle cx="60" cy="68" r="2.5" fill="#a0672a"/>
                <circle cx="84" cy="70" r="2.5" fill="#a0672a"/>
                <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">BRONZE</text>
            </svg>
            <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">70-79%</div>
        </div>

        <!-- Silver Crown (80-89%) -->
        <div style="text-align: center;">
            <svg width="100" height="100" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2));">
                <defs>
                    <linearGradient id="viewSilver" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#f0f0f0;stop-opacity:1" />
                        <stop offset="30%" style="stop-color:#c0c0c0;stop-opacity:1" />
                        <stop offset="70%" style="stop-color:#c0c0c0;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#8a8a8a;stop-opacity:1" />
                    </linearGradient>
                    <radialGradient id="viewSapphire" cx="40%" cy="40%" r="60%">
                        <stop offset="0%" style="stop-color:#8ab3d4;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#4a6fa5;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#2a4a7a;stop-opacity:1" />
                    </radialGradient>
                </defs>
                <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#viewSilver)" stroke="#8a8a8a" stroke-width="1"/>
                <path d="M14,86 L20,82 L26,86 L32,82 L38,86 L44,82 L50,86 L56,82 L62,86 L68,82 L74,86 L80,82 L86,86 L92,82 L98,86 L104,82" stroke="#9a9a9a" stroke-width="1.5" fill="none"/>
                <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#viewSilver)" stroke="#8a8a8a" stroke-width="0.5"/>
                <polygon points="50,25 60,15 70,25" fill="white" opacity="0.25"/>
                <circle cx="24" cy="35" r="7" fill="url(#viewSapphire)" stroke="#2a4a7a" stroke-width="1.5"/>
                <circle cx="60" cy="20" r="10" fill="url(#viewSapphire)" stroke="#2a4a7a" stroke-width="2"/>
                <circle cx="96" cy="35" r="7" fill="url(#viewSapphire)" stroke="#2a4a7a" stroke-width="1.5"/>
                <circle cx="42" cy="48" r="5" fill="#6a9ec9"/>
                <circle cx="78" cy="48" r="5" fill="#6a9ec9"/>
                <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.5"/>
                <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                <path d="M32,52 C36,44 40,44 44,50" stroke="#9a9a9a" stroke-width="1.5" fill="none"/>
                <path d="M76,50 C80,44 84,44 88,52" stroke="#9a9a9a" stroke-width="1.5" fill="none"/>
                <circle cx="36" cy="70" r="2.5" fill="#9a9a9a"/>
                <circle cx="60" cy="68" r="2.5" fill="#9a9a9a"/>
                <circle cx="84" cy="70" r="2.5" fill="#9a9a9a"/>
                <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">SILVER</text>
            </svg>
            <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">80-89%</div>
        </div>

        <!-- Gold Crown (90-99%) -->
        <div style="text-align: center;">
            <svg width="100" height="100" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2));">
                <defs>
                    <linearGradient id="viewGold" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#fff8dc;stop-opacity:1" />
                        <stop offset="30%" style="stop-color:#ffd700;stop-opacity:1" />
                        <stop offset="70%" style="stop-color:#ffd700;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#c8960a;stop-opacity:1" />
                    </linearGradient>
                    <radialGradient id="viewRuby" cx="40%" cy="40%" r="60%">
                        <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#dc143c;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#8b0000;stop-opacity:1" />
                    </radialGradient>
                </defs>
                <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#viewGold)" stroke="#c8960a" stroke-width="1"/>
                <path d="M12,86 C18,82 24,89 30,86 C36,82 42,89 48,86 C54,82 60,89 66,86 C72,82 78,89 84,86 C90,82 96,89 102,86 C108,82 110,86" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#viewGold)" stroke="#c8960a" stroke-width="0.5"/>
                <polygon points="50,25 60,15 70,25" fill="white" opacity="0.2"/>
                <circle cx="24" cy="35" r="7" fill="url(#viewRuby)" stroke="#8b0000" stroke-width="1.5"/>
                <circle cx="60" cy="20" r="10" fill="url(#viewRuby)" stroke="#8b0000" stroke-width="2"/>
                <circle cx="96" cy="35" r="7" fill="url(#viewRuby)" stroke="#8b0000" stroke-width="1.5"/>
                <circle cx="42" cy="48" r="5" fill="#ff4444"/>
                <circle cx="78" cy="48" r="5" fill="#ff4444"/>
                <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.5"/>
                <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                <path d="M32,52 C36,44 40,44 44,50" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                <path d="M76,50 C80,44 84,44 88,52" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                <circle cx="36" cy="70" r="2.5" fill="#d4a017"/>
                <circle cx="60" cy="68" r="2.5" fill="#d4a017"/>
                <circle cx="84" cy="70" r="2.5" fill="#d4a017"/>
                <path d="M60,8 L60,4 M60,8 L60,12 M56,8 L52,8 M64,8 L68,8" stroke="#fff8dc" stroke-width="1.5" fill="none" opacity="0.6"/>
                <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">GOLD</text>
            </svg>
            <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">90-99%</div>
        </div>

        <!-- Diamond Crown (100%) -->
        <div style="text-align: center;">
            <svg width="100" height="100" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2)); animation: viewGlow 2.5s ease-in-out infinite;">
                <defs>
                    <style>
                        @keyframes viewGlow {
                            0% { filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2)); }
                            50% { filter: drop-shadow(0 4px 30px rgba(255,215,0,0.6)) drop-shadow(0 0 60px rgba(255,215,0,0.3)); }
                            100% { filter: drop-shadow(0 4px 15px rgba(0,0,0,0.2)); }
                        }
                        @keyframes viewSparkle {
                            0%, 100% { opacity: 0.3; transform: scale(0.8); }
                            50% { opacity: 1; transform: scale(1.2); }
                        }
                        .sparkle-view { animation: viewSparkle 2s ease-in-out infinite; }
                    </style>
                    <linearGradient id="viewDiamond" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#fff8dc;stop-opacity:1" />
                        <stop offset="30%" style="stop-color:#ffd700;stop-opacity:1" />
                        <stop offset="70%" style="stop-color:#ffd700;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#c8960a;stop-opacity:1" />
                    </linearGradient>
                    <radialGradient id="viewDiamondGem" cx="40%" cy="40%" r="60%">
                        <stop offset="0%" style="stop-color:#e0f7fa;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#b9f2ff;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#80cde0;stop-opacity:1" />
                    </radialGradient>
                </defs>
                <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#viewDiamond)" stroke="#c8960a" stroke-width="1"/>
                <path d="M15,86 C20,82 25,89 30,86 C35,82 40,89 45,86 C50,82 55,89 60,86 C65,82 70,89 75,86 C80,82 85,89 90,86 C95,82 100,89 105,86" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#viewDiamond)" stroke="#c8960a" stroke-width="0.5"/>
                <polygon points="50,25 60,15 70,25" fill="white" opacity="0.3"/>
                <circle cx="24" cy="35" r="7" fill="url(#viewDiamondGem)" stroke="#80cde0" stroke-width="1.5"/>
                <circle cx="60" cy="20" r="10" fill="url(#viewDiamondGem)" stroke="#80cde0" stroke-width="2"/>
                <circle cx="96" cy="35" r="7" fill="url(#viewDiamondGem)" stroke="#80cde0" stroke-width="1.5"/>
                <circle cx="42" cy="48" r="5" fill="url(#viewDiamondGem)"/>
                <circle cx="78" cy="48" r="5" fill="url(#viewDiamondGem)"/>
                <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.6"/>
                <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.5"/>
                <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.5"/>
                <path class="sparkle-view" d="M60,8 L60,4 M60,8 L60,12 M56,8 L52,8 M64,8 L68,8" stroke="#fff8dc" stroke-width="2" fill="none"/>
                <path class="sparkle-view" d="M24,25 L22,22 M24,25 L26,22" stroke="#fff8dc" stroke-width="1.5" fill="none" style="animation-delay:0.5s"/>
                <path class="sparkle-view" d="M96,25 L94,22 M96,25 L98,22" stroke="#fff8dc" stroke-width="1.5" fill="none" style="animation-delay:1s"/>
                <circle cx="36" cy="70" r="2.5" fill="#d4a017"/>
                <circle cx="60" cy="68" r="2.5" fill="#d4a017"/>
                <circle cx="84" cy="70" r="2.5" fill="#d4a017"/>
                <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">DIAMOND</text>
            </svg>
            <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">100%</div>
        </div>

    </div>
    <div style="text-align: center; font-size: 0.9rem; color: #666; padding-top: 10px; border-top: 1px solid #dee2e6; margin-top: 5px;">
        🏆 Crowns are earned based on your practice test scores
    </div>
</details>

<div class="button-group">
    <form method="get" action="/sample_test">
        <button class="test-btn" type="submit">📝 Take Full Practice Test</button>
    </form>
</div>

<hr>
<form method="post" action="/generate" class="inline">
<label>Section:
<select id="section" name="section">
    <option value="verbal">Verbal Reasoning</option>
    <option value="quant">Quantitative Reasoning</option>
    <option value="reading">Reading Comprehension</option>
</select>
</label>
<label>Topic:
<select id="topic" name="topic"></select>
</label>
<div id="num_container">
    <label>Number of problems:
    <input type="number" name="num" min="1" max="10" value="5">
    </label>
</div>
<button type="submit">Generate</button>
</form>

{% if problems %}
<form method="post" action="/submit">
<div style="margin-top:16px">

{% set question_counter = namespace(value=1) %}
{% for idx,p in enumerate(problems) %}
<div class="problem" id="p{{idx}}">
    {% if p[1]|length == 0 %}
        {# This is a passage or poem display - no question number #}
        {% set passage_text = p[0] %}
        {% if '—' in passage_text and passage_text|length < 2000 %}
            <div class="poetry-text">{{ passage_text|safe }}</div>
        {% else %}
            <div class="passage-text">{{ passage_text|safe }}</div>
        {% endif %}
    {% else %}
        <div><strong>{{ question_counter.value }}.</strong> {{ p[0]|safe }}</div>
        {% set question_counter.value = question_counter.value + 1 %}
        <input type="hidden" id="answer_{{idx}}" name="answer_{{idx}}" value="">
        <div class="choices">
            {% for cidx,choice in enumerate(p[1]) %}
                <div class="choice" onclick="selectChoice({{idx}},{{cidx}})">{{ choice|safe }}</div>
            {% endfor %}
        </div>
        {% if results %}
            <div class="result">
                {% if results[idx] == True %}
                    <span class="correct">✓ Correct</span>
                {% else %}
                    <span class="incorrect">✗ Incorrect</span>
                {% endif %}
            </div>
        {% endif %}
    {% endif %}
</div>
{% endfor %}

<div style="margin-top:12px">
<button type="submit">Submit Answers</button>
</div>
</form>
{% endif %}

{% if score is not none %}
    <div class="score-display">
        <div class="score-text">
            <div class="percentage">{{ percent }}%</div>
            <div class="score-detail">{{ correct_count }}/{{ total }} correct</div>
        </div>
        <div class="crown-container">
            {% if percent >= 100 %}
                <!-- Diamond Crown - 100% -->
                <svg class="crown-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="diamondGold" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#fff8dc;stop-opacity:1" />
                            <stop offset="30%" style="stop-color:#ffd700;stop-opacity:1" />
                            <stop offset="70%" style="stop-color:#ffd700;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#c8960a;stop-opacity:1" />
                        </linearGradient>
                        <radialGradient id="diamondGemGrad" cx="40%" cy="40%" r="60%">
                            <stop offset="0%" style="stop-color:#e0f7fa;stop-opacity:1" />
                            <stop offset="50%" style="stop-color:#b9f2ff;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#80cde0;stop-opacity:1" />
                        </radialGradient>
                    </defs>
                    <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#diamondGold)" stroke="#c8960a" stroke-width="1"/>
                    <path d="M15,86 C20,82 25,89 30,86 C35,82 40,89 45,86 C50,82 55,89 60,86 C65,82 70,89 75,86 C80,82 85,89 90,86 C95,82 100,89 105,86" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                    <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#diamondGold)" stroke="#c8960a" stroke-width="0.5"/>
                    <polygon points="50,25 60,15 70,25" fill="white" opacity="0.3"/>
                    <circle cx="24" cy="35" r="7" fill="url(#diamondGemGrad)" stroke="#80cde0" stroke-width="1.5"/>
                    <circle cx="60" cy="20" r="10" fill="url(#diamondGemGrad)" stroke="#80cde0" stroke-width="2"/>
                    <circle cx="96" cy="35" r="7" fill="url(#diamondGemGrad)" stroke="#80cde0" stroke-width="1.5"/>
                    <circle cx="42" cy="48" r="5" fill="url(#diamondGemGrad)"/>
                    <circle cx="78" cy="48" r="5" fill="url(#diamondGemGrad)"/>
                    <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.6"/>
                    <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.5"/>
                    <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.5"/>
                    <path class="sparkle-star" d="M60,8 L60,4 M60,8 L60,12 M56,8 L52,8 M64,8 L68,8" stroke="#fff8dc" stroke-width="2" fill="none"/>
                    <path class="sparkle-star" d="M24,25 L22,22 M24,25 L26,22" stroke="#fff8dc" stroke-width="1.5" fill="none" style="animation-delay:0.5s"/>
                    <path class="sparkle-star" d="M96,25 L94,22 M96,25 L98,22" stroke="#fff8dc" stroke-width="1.5" fill="none" style="animation-delay:1s"/>
                    <circle cx="36" cy="70" r="2.5" fill="#d4a017"/>
                    <circle cx="60" cy="68" r="2.5" fill="#d4a017"/>
                    <circle cx="84" cy="70" r="2.5" fill="#d4a017"/>
                    <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">✦ PERFECT ✦</text>
                </svg>
                
            {% elif percent >= 90 %}
                <!-- Gold Crown - 90-99% -->
                <svg class="crown-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#fff8dc;stop-opacity:1" />
                            <stop offset="30%" style="stop-color:#ffd700;stop-opacity:1" />
                            <stop offset="70%" style="stop-color:#ffd700;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#c8960a;stop-opacity:1" />
                        </linearGradient>
                        <radialGradient id="rubyGrad" cx="40%" cy="40%" r="60%">
                            <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
                            <stop offset="50%" style="stop-color:#dc143c;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#8b0000;stop-opacity:1" />
                        </radialGradient>
                    </defs>
                    <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#goldGrad)" stroke="#c8960a" stroke-width="1"/>
                    <path d="M12,86 C18,82 24,89 30,86 C36,82 42,89 48,86 C54,82 60,89 66,86 C72,82 78,89 84,86 C90,82 96,89 102,86 C108,82 110,86" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                    <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#goldGrad)" stroke="#c8960a" stroke-width="0.5"/>
                    <polygon points="50,25 60,15 70,25" fill="white" opacity="0.2"/>
                    <circle cx="24" cy="35" r="7" fill="url(#rubyGrad)" stroke="#8b0000" stroke-width="1.5"/>
                    <circle cx="60" cy="20" r="10" fill="url(#rubyGrad)" stroke="#8b0000" stroke-width="2"/>
                    <circle cx="96" cy="35" r="7" fill="url(#rubyGrad)" stroke="#8b0000" stroke-width="1.5"/>
                    <circle cx="42" cy="48" r="5" fill="#ff4444"/>
                    <circle cx="78" cy="48" r="5" fill="#ff4444"/>
                    <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.5"/>
                    <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                    <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                    <path d="M32,52 C36,44 40,44 44,50" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                    <path d="M76,50 C80,44 84,44 88,52" stroke="#d4a017" stroke-width="1.5" fill="none"/>
                    <circle cx="36" cy="70" r="2.5" fill="#d4a017"/>
                    <circle cx="60" cy="68" r="2.5" fill="#d4a017"/>
                    <circle cx="84" cy="70" r="2.5" fill="#d4a017"/>
                    <path d="M60,8 L60,4 M60,8 L60,12 M56,8 L52,8 M64,8 L68,8" stroke="#fff8dc" stroke-width="1.5" fill="none" opacity="0.6"/>
                    <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">✦ EXCELLENT ✦</text>
                </svg>
                
            {% elif percent >= 80 %}
                <!-- Silver Crown - 80-89% -->
                <svg class="crown-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="silverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#f0f0f0;stop-opacity:1" />
                            <stop offset="30%" style="stop-color:#c0c0c0;stop-opacity:1" />
                            <stop offset="70%" style="stop-color:#c0c0c0;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#8a8a8a;stop-opacity:1" />
                        </linearGradient>
                        <radialGradient id="sapphireGrad" cx="40%" cy="40%" r="60%">
                            <stop offset="0%" style="stop-color:#8ab3d4;stop-opacity:1" />
                            <stop offset="50%" style="stop-color:#4a6fa5;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#2a4a7a;stop-opacity:1" />
                        </radialGradient>
                    </defs>
                    <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#silverGrad)" stroke="#8a8a8a" stroke-width="1"/>
                    <path d="M14,86 L20,82 L26,86 L32,82 L38,86 L44,82 L50,86 L56,82 L62,86 L68,82 L74,86 L80,82 L86,86 L92,82 L98,86 L104,82" stroke="#9a9a9a" stroke-width="1.5" fill="none"/>
                    <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#silverGrad)" stroke="#8a8a8a" stroke-width="0.5"/>
                    <polygon points="50,25 60,15 70,25" fill="white" opacity="0.25"/>
                    <circle cx="24" cy="35" r="7" fill="url(#sapphireGrad)" stroke="#2a4a7a" stroke-width="1.5"/>
                    <circle cx="60" cy="20" r="10" fill="url(#sapphireGrad)" stroke="#2a4a7a" stroke-width="2"/>
                    <circle cx="96" cy="35" r="7" fill="url(#sapphireGrad)" stroke="#2a4a7a" stroke-width="1.5"/>
                    <circle cx="42" cy="48" r="5" fill="#6a9ec9"/>
                    <circle cx="78" cy="48" r="5" fill="#6a9ec9"/>
                    <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.5"/>
                    <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                    <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.4"/>
                    <path d="M32,52 C36,44 40,44 44,50" stroke="#9a9a9a" stroke-width="1.5" fill="none"/>
                    <path d="M76,50 C80,44 84,44 88,52" stroke="#9a9a9a" stroke-width="1.5" fill="none"/>
                    <circle cx="36" cy="70" r="2.5" fill="#9a9a9a"/>
                    <circle cx="60" cy="68" r="2.5" fill="#9a9a9a"/>
                    <circle cx="84" cy="70" r="2.5" fill="#9a9a9a"/>
                    <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">✦ GREAT ✦</text>
                </svg>
                
            {% elif percent >= 70 %}
                <!-- Bronze Crown - 70-79% -->
                <svg class="crown-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="bronzeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#e8a85c;stop-opacity:1" />
                            <stop offset="30%" style="stop-color:#cd7f32;stop-opacity:1" />
                            <stop offset="70%" style="stop-color:#cd7f32;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#8b5a2b;stop-opacity:1" />
                        </linearGradient>
                        <radialGradient id="amberGrad" cx="40%" cy="40%" r="60%">
                            <stop offset="0%" style="stop-color:#f0c060;stop-opacity:1" />
                            <stop offset="50%" style="stop-color:#cd7f32;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#8b5a2b;stop-opacity:1" />
                        </radialGradient>
                    </defs>
                    <rect x="10" y="80" width="100" height="14" rx="4" fill="url(#bronzeGrad)" stroke="#8b5a2b" stroke-width="1"/>
                    <path d="M16,86 C20,82 24,89 28,86 C32,82 36,89 40,86 C44,82 48,89 52,86 C56,82 60,89 64,86 C68,82 72,89 76,86 C80,82 84,89 88,86 C92,82 96,89 100,86 C104,82" stroke="#a0672a" stroke-width="1.5" fill="none"/>
                    <polygon points="18,80 24,28 36,62 60,15 84,62 96,28 102,80" fill="url(#bronzeGrad)" stroke="#8b5a2b" stroke-width="0.5"/>
                    <polygon points="50,25 60,15 70,25" fill="white" opacity="0.15"/>
                    <circle cx="24" cy="35" r="7" fill="url(#amberGrad)" stroke="#8b5a2b" stroke-width="1.5"/>
                    <circle cx="60" cy="20" r="10" fill="url(#amberGrad)" stroke="#8b5a2b" stroke-width="2"/>
                    <circle cx="96" cy="35" r="7" fill="url(#amberGrad)" stroke="#8b5a2b" stroke-width="1.5"/>
                    <circle cx="42" cy="48" r="5" fill="#d4a050"/>
                    <circle cx="78" cy="48" r="5" fill="#d4a050"/>
                    <ellipse cx="58" cy="18" rx="4" ry="3" fill="white" opacity="0.4"/>
                    <ellipse cx="23" cy="33" rx="2.5" ry="2" fill="white" opacity="0.3"/>
                    <ellipse cx="95" cy="33" rx="2.5" ry="2" fill="white" opacity="0.3"/>
                    <path d="M32,52 C36,44 40,44 44,50" stroke="#a0672a" stroke-width="1.5" fill="none"/>
                    <path d="M76,50 C80,44 84,44 88,52" stroke="#a0672a" stroke-width="1.5" fill="none"/>
                    <circle cx="36" cy="70" r="2.5" fill="#a0672a"/>
                    <circle cx="60" cy="68" r="2.5" fill="#a0672a"/>
                    <circle cx="84" cy="70" r="2.5" fill="#a0672a"/>
                    <text x="60" y="112" text-anchor="middle" font-size="10" fill="#495057" font-weight="bold" letter-spacing="1">✦ GOOD ✦</text>
                </svg>
                
            {% else %}
                <!-- No crown for below 70% -->
                <div style="text-align: center; padding: 10px;">
                    <div style="font-size: 50px; opacity: 0.4;">📚</div>
                    <div style="font-size: 0.8rem; color: #6c757d; margin-top: 6px; font-weight: 600;">Keep practicing!</div>
                </div>
            {% endif %}
        </div>
    </div>
{% endif %}

</div>
</body>
</html>"""


###############################################################################################

SAMPLE_TEST_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSAT Practice Test</title>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }
.container { max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
h1 { color: #003366; margin-top: 0; }
.problem { 
    margin: 24px 0; 
    padding: 20px; 
    border-radius: 12px; 
    border: 1px solid #ccd; 
    background: #fefefe;
    page-break-inside: avoid;
    break-inside: avoid;
}
.passage-text { 
    font-family: Georgia, serif; 
    font-size: 1.2rem; 
    line-height: 1.6; 
    background: #fafcfd; 
    padding: 20px; 
    border-radius: 12px; 
    border-left: 5px solid #003366; 
    margin-bottom: 20px;
    max-height: 400px;
    overflow-y: auto;
}
.poetry-text { 
    font-family: Georgia, serif; 
    font-size: 1.2rem; 
    line-height: 1.8; 
    background: #fafcfd; 
    padding: 20px; 
    border-radius: 12px; 
    border-left: 5px solid #6a0dad; 
    margin-bottom: 20px; 
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}
.choices { 
    display: flex; 
    flex-direction: column;
    gap: 12px; 
    margin-top: 16px; 
}
.choice { 
    background: #f2f8ff; 
    padding: 14px 18px; 
    border-radius: 10px; 
    border: 2px solid #cde; 
    cursor: pointer; 
    transition: all 0.2s;
    font-size: 16px;
    width: 100%;
}
.choice:hover { 
    background: #e0e8f0; 
    border-color: #88f;
}
.choice.selected { 
    outline: none;
    border: 2px solid #006; 
    background: #e8eeff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.choice.correct { 
    background-color: #d4edda; 
    border-color: #28a745; 
}
.choice.incorrect { 
    background-color: #f8d7da; 
    border-color: #dc3545; 
}
button { 
    background: #006; 
    color: white; 
    border: none; 
    padding: 12px 24px; 
    border-radius: 10px; 
    cursor: pointer; 
    font-size: 16px; 
    margin: 5px;
    font-weight: 600;
}
button:hover { 
    background: #004; 
}
button.secondary {
    background: #6c757d;
}
button.home-btn {
    background: #2d6a4f;
}
button.home-btn:hover {
    background: #1b4d3e;
}
.score-box { 
    display: inline-block; 
    padding: 8px 16px; 
    margin: 5px; 
    background: #e8f0fe; 
    border-radius: 8px;
    font-weight: bold;
}
.result { 
    margin-top: 12px; 
    font-weight: bold; 
    padding: 8px;
    border-radius: 8px;
}
.correct { 
    color: #155724;
    background: #d4edda;
    padding: 8px 12px;
    border-radius: 8px;
    display: inline-block;
}
.incorrect { 
    color: #721c24;
    background: #f8d7da;
    padding: 8px 12px;
    border-radius: 8px;
    display: inline-block;
}
.question-text {
    font-weight: 600;
    font-size: 1.1rem;
    line-height: 1.5;
    margin-bottom: 16px;
}
.section-header {
    background: #e8f0fe;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 20px 0 10px 0;
    font-weight: bold;
    color: #003366;
    border-left: 4px solid #003366;
}
.button-group {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 20px 0;
}

/* ========== CROWN DISPLAY STYLES ========== */
.score-display {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 45px;
    flex-wrap: wrap;
    background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 35px 50px;
    border-radius: 24px;
    border: 3px solid #dee2e6;
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.8), 0 8px 25px rgba(0,0,0,0.1);
}

.score-text {
    text-align: center;
}

.score-text h2 {
    margin: 0;
    color: #003366;
    font-size: 2.2rem;
}

.score-text .percentage {
    font-size: 4.2rem;
    font-weight: 800;
    color: #003366;
    text-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.score-crown-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5px;
}

.score-crown-svg {
    width: 240px;
    height: 190px;
    display: block;
    filter: drop-shadow(0 8px 35px rgba(0,0,0,0.25));
    transition: transform 0.3s ease;
}

.score-crown-svg:hover {
    transform: scale(1.05) rotate(-2deg);
}

.section-score-display {
    display: flex;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    justify-content: center;
}

/* Crown glow animations */
.crown-bronze .score-crown-svg {
    animation: bronzeGlow 3s ease-in-out infinite;
}

.crown-silver .score-crown-svg {
    animation: silverGlow 3s ease-in-out infinite;
}

.crown-gold .score-crown-svg {
    animation: goldGlow 2.5s ease-in-out infinite;
}

.crown-diamond .score-crown-svg {
    animation: diamondGlow 2s ease-in-out infinite;
}

@keyframes bronzeGlow {
    0%, 100% { filter: drop-shadow(0 8px 35px rgba(205,127,50,0.3)); }
    50% { filter: drop-shadow(0 8px 55px rgba(205,127,50,0.6)) drop-shadow(0 0 80px rgba(205,127,50,0.15)); }
}

@keyframes silverGlow {
    0%, 100% { filter: drop-shadow(0 8px 35px rgba(192,192,192,0.3)); }
    50% { filter: drop-shadow(0 8px 55px rgba(192,192,192,0.6)) drop-shadow(0 0 80px rgba(192,192,192,0.15)); }
}

@keyframes goldGlow {
    0%, 100% { filter: drop-shadow(0 8px 35px rgba(255,215,0,0.3)); }
    50% { filter: drop-shadow(0 8px 55px rgba(255,215,0,0.7)) drop-shadow(0 0 100px rgba(255,215,0,0.2)); }
}

@keyframes diamondGlow {
    0%, 100% { filter: drop-shadow(0 8px 35px rgba(255,215,0,0.3)) drop-shadow(0 0 20px rgba(185,242,255,0.15)); }
    50% { filter: drop-shadow(0 8px 55px rgba(255,215,0,0.7)) drop-shadow(0 0 80px rgba(185,242,255,0.3)) drop-shadow(0 0 120px rgba(255,215,0,0.2)); }
}

/* Sparkle animations */
.sparkle-star {
    animation: sparkleFloat 3s ease-in-out infinite;
}

.sparkle-star-delay-1 { animation-delay: 0.8s; }
.sparkle-star-delay-2 { animation-delay: 1.6s; }
.sparkle-star-delay-3 { animation-delay: 2.4s; }
.sparkle-star-delay-4 { animation-delay: 0.5s; }
.sparkle-star-delay-5 { animation-delay: 1.2s; }

@keyframes sparkleFloat {
    0%, 100% { opacity: 0.3; transform: scale(0.8) rotate(0deg); }
    50% { opacity: 1; transform: scale(1.3) rotate(180deg); }
}

/* Sparkle pulse for attached decorations */
.sparkle-pulse {
    animation: sparklePulse 3.5s ease-in-out infinite;
}

.sparkle-pulse-delay-1 { animation-delay: 0.7s; }
.sparkle-pulse-delay-2 { animation-delay: 1.4s; }
.sparkle-pulse-delay-3 { animation-delay: 2.1s; }

@keyframes sparklePulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

/* Shine sweep animation */
.shine-sweep {
    animation: shineSweep 5s ease-in-out infinite;
}

@keyframes shineSweep {
    0% { opacity: 0; transform: translateX(-100%) rotate(25deg); }
    15% { opacity: 0.3; }
    25% { opacity: 0.5; transform: translateX(0%) rotate(25deg); }
    35% { opacity: 0.3; }
    45% { opacity: 0; transform: translateX(100%) rotate(25deg); }
    100% { opacity: 0; transform: translateX(100%) rotate(25deg); }
}

/* Gem pulse */
.gem-pulse {
    animation: gemPulse 3.5s ease-in-out infinite;
}

.gem-pulse-delay-1 { animation-delay: 0.7s; }
.gem-pulse-delay-2 { animation-delay: 1.4s; }
.gem-pulse-delay-3 { animation-delay: 2.1s; }

@keyframes gemPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@media (max-width: 600px) {
    .score-display {
        flex-direction: column;
        padding: 20px 25px;
        gap: 20px;
    }
    
    .score-crown-svg {
        width: 200px;
        height: 160px;
    }
    
    .score-text .percentage {
        font-size: 3rem;
    }
    
    .section-score-display {
        flex-direction: column;
        gap: 10px;
    }
}
</style>
<script>
function selectChoice(pIdx, cIdx){
    const container = document.getElementById('p'+pIdx);
    container.querySelectorAll('.choice').forEach((it,i)=>it.classList.toggle('selected',i===cIdx));
    document.getElementById('answer_'+pIdx).value = cIdx;
}
</script>
</head>
<body>
<div class="container">
<h1>📝 SSAT Practice Test</h1>

<p style="background: #e8f0fe; padding: 12px; border-radius: 8px;">
    📖 Reading: {{ reading_type|capitalize if reading_type else 'Reading' }} passage (6 questions) | 
    💬 Verbal: 20 questions | 
    🔢 Math: 15 questions
</p>

<div class="button-group">
    <form method="get" action="/home" style="display:inline;">
        <button class="home-btn" type="submit">🏠 Back to Home</button>
    </form>
    <form method="get" action="/sample_test" style="display:inline;">
        <button type="submit">🔄 New Practice Test</button>
    </form>
</div>

<!-- SCORE DISPLAY WITH CROWN (ONLY SHOWS AFTER GRADING) -->
{% if score %}
    <div style="background: #e8f0fe; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <div class="score-display">
            <div class="score-text">
                <h2>Your Score</h2>
                <div class="percentage">{{ percent }}%</div>
                <div style="font-size: 1rem; color: #495057;">({{ correct_count }}/{{ total }})</div>
            </div>
            <div class="score-crown-container">
                {% if percent >= 100 %}
                    <!-- DIAMOND CROWN - Wider, Shorter, 500% More Intricate, 5 Spikes with Orbs Not Touching -->
                    <svg class="score-crown-svg crown-diamond" viewBox="0 0 220 170" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="diamondGoldBase" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#fff8dc;stop-opacity:1" />
                                <stop offset="15%" style="stop-color:#ffed4a;stop-opacity:1" />
                                <stop offset="30%" style="stop-color:#ffd700;stop-opacity:1" />
                                <stop offset="50%" style="stop-color:#ffed4a;stop-opacity:1" />
                                <stop offset="70%" style="stop-color:#ffd700;stop-opacity:1" />
                                <stop offset="85%" style="stop-color:#ffed4a;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#c8960a;stop-opacity:1" />
                            </linearGradient>
                            <radialGradient id="diamondOrb" cx="40%" cy="35%" r="65%">
                                <stop offset="0%" style="stop-color:#e0f7fa;stop-opacity:1" />
                                <stop offset="25%" style="stop-color:#b9f2ff;stop-opacity:1" />
                                <stop offset="55%" style="stop-color:#80cde0;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#4a9bb5;stop-opacity:1" />
                            </radialGradient>
                            <radialGradient id="diamondOrbShine" cx="35%" cy="30%" r="55%">
                                <stop offset="0%" style="stop-color:rgba(255,255,255,0.9);stop-opacity:1" />
                                <stop offset="40%" style="stop-color:rgba(255,255,255,0.3);stop-opacity:1" />
                                <stop offset="100%" style="stop-color:rgba(255,255,255,0);stop-opacity:1" />
                            </radialGradient>
                        </defs>
                        <!-- Wider, shorter base band -->
                        <rect x="12" y="130" width="196" height="16" rx="4" fill="url(#diamondGoldBase)" stroke="#c8960a" stroke-width="1.5"/>
                        <!-- Filigree layer 1 -->
                        <path d="M18,136 C23,132 28,138 33,136 C38,132 43,138 48,136 C53,132 58,138 63,136 C68,132 73,138 78,136 C83,132 88,138 93,136 C98,132 103,138 108,136 C113,132 118,138 123,136 C128,132 133,138 138,136 C143,132 148,138 153,136 C158,132 163,138 168,136 C173,132 178,138 183,136 C188,132 193,138 198,136 C203,132 206,136" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.9"/>
                        <!-- Filigree layer 2 -->
                        <path d="M21,141 C26,137 31,143 36,141 C41,137 46,143 51,141 C56,137 61,143 66,141 C71,137 76,143 81,141 C86,137 91,143 96,141 C101,137 106,143 111,141 C116,137 121,143 126,141 C131,137 136,143 141,141 C146,137 151,143 156,141 C161,137 166,143 171,141 C176,137 181,143 186,141 C191,137 196,143 201,141" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.7"/>
                        <!-- Filigree layer 3 -->
                        <path d="M24,146 C29,142 34,148 39,146 C44,142 49,148 54,146 C59,142 64,148 69,146 C74,142 79,148 84,146 C89,142 94,148 99,146 C104,142 109,148 114,146 C119,142 124,148 129,146 C134,142 139,148 144,146 C149,142 154,148 159,146 C164,142 169,148 174,146 C179,142 184,148 189,146 C194,142 199,146" stroke="#d4a017" stroke-width="1.2" fill="none" opacity="0.5"/>
                        <!-- Crown points - 5 spikes, wider and shorter -->
                        <polygon points="32,130 38,40 52,80 72,28 88,72 110,22 132,72 148,28 168,80 182,40 188,130" fill="url(#diamondGoldBase)" stroke="#c8960a" stroke-width="1.5"/>
                        <!-- Inner point filigree -->
                        <polygon points="40,48 48,40 56,48" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="72,34 80,28 88,34" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="105,27 112,22 119,27" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="132,34 140,28 148,34" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="164,48 172,40 180,48" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <!-- Orbs on 5 spikes - NOT TOUCHING -->
                        <circle cx="38" cy="38" r="8" fill="url(#diamondOrb)" stroke="#80cde0" stroke-width="2" class="gem-pulse"/>
                        <circle cx="72" cy="26" r="9" fill="url(#diamondOrb)" stroke="#80cde0" stroke-width="2" class="gem-pulse gem-pulse-delay-1"/>
                        <circle cx="110" cy="20" r="10" fill="url(#diamondOrb)" stroke="#80cde0" stroke-width="2" class="gem-pulse gem-pulse-delay-2"/>
                        <circle cx="148" cy="26" r="9" fill="url(#diamondOrb)" stroke="#80cde0" stroke-width="2" class="gem-pulse gem-pulse-delay-3"/>
                        <circle cx="182" cy="38" r="8" fill="url(#diamondOrb)" stroke="#80cde0" stroke-width="2" class="gem-pulse"/>
                        <!-- Orb shine overlays -->
                        <circle cx="36" cy="35" r="5" fill="url(#diamondOrbShine)" opacity="0.9"/>
                        <circle cx="70" cy="23" r="6" fill="url(#diamondOrbShine)" opacity="0.9"/>
                        <circle cx="108" cy="17" r="7" fill="url(#diamondOrbShine)" opacity="0.9"/>
                        <circle cx="146" cy="23" r="6" fill="url(#diamondOrbShine)" opacity="0.9"/>
                        <circle cx="180" cy="35" r="5" fill="url(#diamondOrbShine)" opacity="0.9"/>
                        <!-- Intricate filigree swirls -->
                        <path d="M50,85 C53,78 57,76 63,82" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M82,68 C85,61 89,59 95,65" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M125,65 C131,59 135,61 138,68" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M157,82 C163,76 167,78 170,85" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M60,95 C65,88 70,88 75,95" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.4"/>
                        <path d="M95,80 C100,73 105,73 110,80" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.4"/>
                        <path d="M145,95 C150,88 155,88 160,95" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.4"/>
                        <!-- Sparkle stars -->
                        <path class="sparkle-star" d="M110,14 L110,11 M110,14 L110,17" stroke="#fff8dc" stroke-width="2.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-1" d="M38,30 L36,27 M38,30 L40,27" stroke="#fff8dc" stroke-width="2" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-2" d="M182,30 L180,27 M182,30 L184,27" stroke="#fff8dc" stroke-width="2" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-3" d="M72,18 L70,15 M72,18 L74,15" stroke="#fff8dc" stroke-width="1.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-4" d="M148,18 L146,15 M148,18 L150,15" stroke="#fff8dc" stroke-width="1.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-5" d="M55,60 L53,57 M55,60 L57,57" stroke="#fff8dc" stroke-width="1.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-1" d="M165,60 L163,57 M165,60 L167,57" stroke="#fff8dc" stroke-width="1.5" fill="none"/>
                        <!-- Decorative dots -->
                        <circle cx="30" cy="135" r="2" fill="#fff8dc" opacity="0.9" class="sparkle-pulse"/>
                        <circle cx="60" cy="135" r="2" fill="#fff8dc" opacity="0.9" class="sparkle-pulse sparkle-pulse-delay-1"/>
                        <circle cx="90" cy="135" r="2" fill="#fff8dc" opacity="0.9" class="sparkle-pulse sparkle-pulse-delay-2"/>
                        <circle cx="130" cy="135" r="2" fill="#fff8dc" opacity="0.9" class="sparkle-pulse sparkle-pulse-delay-3"/>
                        <circle cx="160" cy="135" r="2" fill="#fff8dc" opacity="0.9" class="sparkle-pulse"/>
                        <circle cx="190" cy="135" r="2" fill="#fff8dc" opacity="0.9" class="sparkle-pulse sparkle-pulse-delay-1"/>
                        <text x="110" y="160" text-anchor="middle" font-size="14" fill="#495057" font-weight="bold" letter-spacing="2">✦ PERFECT ✦</text>
                    </svg>
                    
                {% elif percent >= 90 %}
                    <!-- GOLD CROWN - Wider, Shorter, 500% More Intricate -->
                    <svg class="score-crown-svg crown-gold" viewBox="0 0 220 170" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="goldBase" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#fff8dc;stop-opacity:1" />
                                <stop offset="15%" style="stop-color:#ffed4a;stop-opacity:1" />
                                <stop offset="30%" style="stop-color:#ffd700;stop-opacity:1" />
                                <stop offset="50%" style="stop-color:#ffed4a;stop-opacity:1" />
                                <stop offset="70%" style="stop-color:#ffd700;stop-opacity:1" />
                                <stop offset="85%" style="stop-color:#ffed4a;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#c8960a;stop-opacity:1" />
                            </linearGradient>
                            <radialGradient id="goldOrb" cx="40%" cy="35%" r="65%">
                                <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
                                <stop offset="25%" style="stop-color:#ff3333;stop-opacity:1" />
                                <stop offset="55%" style="stop-color:#dc143c;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#8b0000;stop-opacity:1" />
                            </radialGradient>
                            <radialGradient id="goldOrbShine" cx="35%" cy="30%" r="55%">
                                <stop offset="0%" style="stop-color:rgba(255,255,255,0.8);stop-opacity:1" />
                                <stop offset="40%" style="stop-color:rgba(255,255,255,0.25);stop-opacity:1" />
                                <stop offset="100%" style="stop-color:rgba(255,255,255,0);stop-opacity:1" />
                            </radialGradient>
                        </defs>
                        <rect x="12" y="130" width="196" height="16" rx="4" fill="url(#goldBase)" stroke="#c8960a" stroke-width="1.5"/>
                        <path d="M18,136 C23,132 28,138 33,136 C38,132 43,138 48,136 C53,132 58,138 63,136 C68,132 73,138 78,136 C83,132 88,138 93,136 C98,132 103,138 108,136 C113,132 118,138 123,136 C128,132 133,138 138,136 C143,132 148,138 153,136 C158,132 163,138 168,136 C173,132 178,138 183,136 C188,132 193,138 198,136 C203,132 206,136" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.9"/>
                        <path d="M21,141 C26,137 31,143 36,141 C41,137 46,143 51,141 C56,137 61,143 66,141 C71,137 76,143 81,141 C86,137 91,143 96,141 C101,137 106,143 111,141 C116,137 121,143 126,141 C131,137 136,143 141,141 C146,137 151,143 156,141 C161,137 166,143 171,141 C176,137 181,143 186,141 C191,137 196,143 201,141" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.7"/>
                        <path d="M24,146 C29,142 34,148 39,146 C44,142 49,148 54,146 C59,142 64,148 69,146 C74,142 79,148 84,146 C89,142 94,148 99,146 C104,142 109,148 114,146 C119,142 124,148 129,146 C134,142 139,148 144,146 C149,142 154,148 159,146 C164,142 169,148 174,146 C179,142 184,148 189,146 C194,142 199,146" stroke="#d4a017" stroke-width="1.2" fill="none" opacity="0.5"/>
                        <polygon points="32,130 38,40 52,80 72,28 88,72 110,22 132,72 148,28 168,80 182,40 188,130" fill="url(#goldBase)" stroke="#c8960a" stroke-width="1.5"/>
                        <polygon points="40,48 48,40 56,48" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="72,34 80,28 88,34" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="105,27 112,22 119,27" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="132,34 140,28 148,34" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <polygon points="164,48 172,40 180,48" fill="rgba(255,255,255,0.12)" stroke="#d4a017" stroke-width="1"/>
                        <!-- Orbs on 5 spikes -->
                        <circle cx="38" cy="38" r="8" fill="url(#goldOrb)" stroke="#8b0000" stroke-width="2" class="gem-pulse"/>
                        <circle cx="72" cy="26" r="9" fill="url(#goldOrb)" stroke="#8b0000" stroke-width="2" class="gem-pulse gem-pulse-delay-1"/>
                        <circle cx="110" cy="20" r="10" fill="url(#goldOrb)" stroke="#8b0000" stroke-width="2" class="gem-pulse gem-pulse-delay-2"/>
                        <circle cx="148" cy="26" r="9" fill="url(#goldOrb)" stroke="#8b0000" stroke-width="2" class="gem-pulse gem-pulse-delay-3"/>
                        <circle cx="182" cy="38" r="8" fill="url(#goldOrb)" stroke="#8b0000" stroke-width="2" class="gem-pulse"/>
                        <circle cx="36" cy="35" r="5" fill="url(#goldOrbShine)" opacity="0.9"/>
                        <circle cx="70" cy="23" r="6" fill="url(#goldOrbShine)" opacity="0.9"/>
                        <circle cx="108" cy="17" r="7" fill="url(#goldOrbShine)" opacity="0.9"/>
                        <circle cx="146" cy="23" r="6" fill="url(#goldOrbShine)" opacity="0.9"/>
                        <circle cx="180" cy="35" r="5" fill="url(#goldOrbShine)" opacity="0.9"/>
                        <path d="M50,85 C53,78 57,76 63,82" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M82,68 C85,61 89,59 95,65" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M125,65 C131,59 135,61 138,68" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M157,82 C163,76 167,78 170,85" stroke="#d4a017" stroke-width="1.8" fill="none" opacity="0.6"/>
                        <path d="M60,95 C65,88 70,88 75,95" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.4"/>
                        <path d="M145,95 C150,88 155,88 160,95" stroke="#d4a017" stroke-width="1.5" fill="none" opacity="0.4"/>
                        <path class="sparkle-star" d="M110,14 L110,11 M110,14 L110,17" stroke="#fff8dc" stroke-width="2.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-1" d="M38,30 L36,27 M38,30 L40,27" stroke="#fff8dc" stroke-width="2" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-2" d="M182,30 L180,27 M182,30 L184,27" stroke="#fff8dc" stroke-width="2" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-3" d="M72,18 L70,15 M72,18 L74,15" stroke="#fff8dc" stroke-width="1.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-4" d="M148,18 L146,15 M148,18 L150,15" stroke="#fff8dc" stroke-width="1.5" fill="none"/>
                        <text x="110" y="160" text-anchor="middle" font-size="14" fill="#495057" font-weight="bold" letter-spacing="2">✦ EXCELLENT ✦</text>
                    </svg>
                    
                {% elif percent >= 80 %}
                    <!-- SILVER CROWN - Wider, Shorter, 500% More Intricate -->
                    <svg class="score-crown-svg crown-silver" viewBox="0 0 220 170" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="silverBase" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#f8f8f8;stop-opacity:1" />
                                <stop offset="15%" style="stop-color:#e8e8e8;stop-opacity:1" />
                                <stop offset="30%" style="stop-color:#d8d8d8;stop-opacity:1" />
                                <stop offset="50%" style="stop-color:#d0d0d0;stop-opacity:1" />
                                <stop offset="70%" style="stop-color:#c8c8c8;stop-opacity:1" />
                                <stop offset="85%" style="stop-color:#c0c0c0;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#8a8a8a;stop-opacity:1" />
                            </linearGradient>
                            <radialGradient id="silverOrb" cx="40%" cy="35%" r="65%">
                                <stop offset="0%" style="stop-color:#aac8e0;stop-opacity:1" />
                                <stop offset="25%" style="stop-color:#8ab3d4;stop-opacity:1" />
                                <stop offset="55%" style="stop-color:#4a6fa5;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#2a4a7a;stop-opacity:1" />
                            </radialGradient>
                            <radialGradient id="silverOrbShine" cx="35%" cy="30%" r="55%">
                                <stop offset="0%" style="stop-color:rgba(255,255,255,0.8);stop-opacity:1" />
                                <stop offset="40%" style="stop-color:rgba(255,255,255,0.25);stop-opacity:1" />
                                <stop offset="100%" style="stop-color:rgba(255,255,255,0);stop-opacity:1" />
                            </radialGradient>
                        </defs>
                        <rect x="12" y="130" width="196" height="16" rx="4" fill="url(#silverBase)" stroke="#8a8a8a" stroke-width="1.5"/>
                        <path d="M18,136 L23,132 L28,136 L33,132 L38,136 L43,132 L48,136 L53,132 L58,136 L63,132 L68,136 L73,132 L78,136 L83,132 L88,136 L93,132 L98,136 L103,132 L108,136 L113,132 L118,136 L123,132 L128,136 L133,132 L138,136 L143,132 L148,136 L153,132 L158,136 L163,132 L168,136 L173,132 L178,136 L183,132 L188,136 L193,132 L198,136 L203,132 L206,136" stroke="#9a9a9a" stroke-width="1.8" fill="none" opacity="0.8"/>
                        <path d="M21,141 L26,137 L31,141 L36,137 L41,141 L46,137 L51,141 L56,137 L61,141 L66,137 L71,141 L76,137 L81,141 L86,137 L91,141 L96,137 L101,141 L106,137 L111,141 L116,137 L121,141 L126,137 L131,141 L136,137 L141,141 L146,137 L151,141 L156,137 L161,141 L166,137 L171,141 L176,137 L181,141 L186,137 L191,141 L196,137 L201,141" stroke="#9a9a9a" stroke-width="1.5" fill="none" opacity="0.6"/>
                        <path d="M24,146 L29,142 L34,146 L39,142 L44,146 L49,142 L54,146 L59,142 L64,146 L69,142 L74,146 L79,142 L84,146 L89,142 L94,146 L99,142 L104,146 L109,142 L114,146 L119,142 L124,146 L129,142 L134,146 L139,142 L144,146 L149,142 L154,146 L159,142 L164,146 L169,142 L174,146 L179,142 L184,146 L189,142 L194,146 L199,142 L204,146" stroke="#9a9a9a" stroke-width="1.2" fill="none" opacity="0.4"/>
                        <polygon points="32,130 38,40 52,80 72,28 88,72 110,22 132,72 148,28 168,80 182,40 188,130" fill="url(#silverBase)" stroke="#8a8a8a" stroke-width="1.5"/>
                        <polygon points="40,48 48,40 56,48" fill="rgba(255,255,255,0.15)" stroke="#9a9a9a" stroke-width="1"/>
                        <polygon points="72,34 80,28 88,34" fill="rgba(255,255,255,0.15)" stroke="#9a9a9a" stroke-width="1"/>
                        <polygon points="105,27 112,22 119,27" fill="rgba(255,255,255,0.15)" stroke="#9a9a9a" stroke-width="1"/>
                        <polygon points="132,34 140,28 148,34" fill="rgba(255,255,255,0.15)" stroke="#9a9a9a" stroke-width="1"/>
                        <polygon points="164,48 172,40 180,48" fill="rgba(255,255,255,0.15)" stroke="#9a9a9a" stroke-width="1"/>
                        <circle cx="38" cy="38" r="8" fill="url(#silverOrb)" stroke="#2a4a7a" stroke-width="2" class="gem-pulse"/>
                        <circle cx="72" cy="26" r="9" fill="url(#silverOrb)" stroke="#2a4a7a" stroke-width="2" class="gem-pulse gem-pulse-delay-1"/>
                        <circle cx="110" cy="20" r="10" fill="url(#silverOrb)" stroke="#2a4a7a" stroke-width="2" class="gem-pulse gem-pulse-delay-2"/>
                        <circle cx="148" cy="26" r="9" fill="url(#silverOrb)" stroke="#2a4a7a" stroke-width="2" class="gem-pulse gem-pulse-delay-3"/>
                        <circle cx="182" cy="38" r="8" fill="url(#silverOrb)" stroke="#2a4a7a" stroke-width="2" class="gem-pulse"/>
                        <circle cx="36" cy="35" r="5" fill="url(#silverOrbShine)" opacity="0.9"/>
                        <circle cx="70" cy="23" r="6" fill="url(#silverOrbShine)" opacity="0.9"/>
                        <circle cx="108" cy="17" r="7" fill="url(#silverOrbShine)" opacity="0.9"/>
                        <circle cx="146" cy="23" r="6" fill="url(#silverOrbShine)" opacity="0.9"/>
                        <circle cx="180" cy="35" r="5" fill="url(#silverOrbShine)" opacity="0.9"/>
                        <path d="M50,85 C53,78 57,76 63,82" stroke="#9a9a9a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M82,68 C85,61 89,59 95,65" stroke="#9a9a9a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M125,65 C131,59 135,61 138,68" stroke="#9a9a9a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M157,82 C163,76 167,78 170,85" stroke="#9a9a9a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M60,95 C65,88 70,88 75,95" stroke="#9a9a9a" stroke-width="1.5" fill="none" opacity="0.3"/>
                        <path d="M145,95 C150,88 155,88 160,95" stroke="#9a9a9a" stroke-width="1.5" fill="none" opacity="0.3"/>
                        <path class="sparkle-star" d="M110,14 L110,11 M110,14 L110,17" stroke="#f0f0f0" stroke-width="2.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-1" d="M38,30 L36,27 M38,30 L40,27" stroke="#f0f0f0" stroke-width="2" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-2" d="M182,30 L180,27 M182,30 L184,27" stroke="#f0f0f0" stroke-width="2" fill="none"/>
                        <text x="110" y="160" text-anchor="middle" font-size="14" fill="#495057" font-weight="bold" letter-spacing="2">✦ GREAT ✦</text>
                    </svg>
                    
                {% elif percent >= 70 %}
                    <!-- BRONZE CROWN - Wider, Shorter, 500% More Intricate -->
                    <svg class="score-crown-svg crown-bronze" viewBox="0 0 220 170" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="bronzeBase" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" style="stop-color:#e8a85c;stop-opacity:1" />
                                <stop offset="15%" style="stop-color:#d4883a;stop-opacity:1" />
                                <stop offset="30%" style="stop-color:#cd7f32;stop-opacity:1" />
                                <stop offset="50%" style="stop-color:#d4883a;stop-opacity:1" />
                                <stop offset="70%" style="stop-color:#cd7f32;stop-opacity:1" />
                                <stop offset="85%" style="stop-color:#b8702a;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#8b5a2b;stop-opacity:1" />
                            </linearGradient>
                            <radialGradient id="bronzeOrb" cx="40%" cy="35%" r="65%">
                                <stop offset="0%" style="stop-color:#f5d080;stop-opacity:1" />
                                <stop offset="25%" style="stop-color:#e8a85c;stop-opacity:1" />
                                <stop offset="55%" style="stop-color:#cd7f32;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#8b5a2b;stop-opacity:1" />
                            </radialGradient>
                            <radialGradient id="bronzeOrbShine" cx="35%" cy="30%" r="55%">
                                <stop offset="0%" style="stop-color:rgba(255,255,255,0.7);stop-opacity:1" />
                                <stop offset="40%" style="stop-color:rgba(255,255,255,0.2);stop-opacity:1" />
                                <stop offset="100%" style="stop-color:rgba(255,255,255,0);stop-opacity:1" />
                            </radialGradient>
                        </defs>
                        <rect x="12" y="130" width="196" height="16" rx="4" fill="url(#bronzeBase)" stroke="#8b5a2b" stroke-width="1.5"/>
                        <path d="M18,136 C23,132 28,138 33,136 C38,132 43,138 48,136 C53,132 58,138 63,136 C68,132 73,138 78,136 C83,132 88,138 93,136 C98,132 103,138 108,136 C113,132 118,138 123,136 C128,132 133,138 138,136 C143,132 148,138 153,136 C158,132 163,138 168,136 C173,132 178,138 183,136 C188,132 193,138 198,136 C203,132 206,136" stroke="#a0672a" stroke-width="1.8" fill="none" opacity="0.8"/>
                        <path d="M21,141 C26,137 31,143 36,141 C41,137 46,143 51,141 C56,137 61,143 66,141 C71,137 76,143 81,141 C86,137 91,143 96,141 C101,137 106,143 111,141 C116,137 121,143 126,141 C131,137 136,143 141,141 C146,137 151,143 156,141 C161,137 166,143 171,141 C176,137 181,143 186,141 C191,137 196,143 201,141" stroke="#a0672a" stroke-width="1.5" fill="none" opacity="0.6"/>
                        <path d="M24,146 C29,142 34,148 39,146 C44,142 49,148 54,146 C59,142 64,148 69,146 C74,142 79,148 84,146 C89,142 94,148 99,146 C104,142 109,148 114,146 C119,142 124,148 129,146 C134,142 139,148 144,146 C149,142 154,148 159,146 C164,142 169,148 174,146 C179,142 184,148 189,146 C194,142 199,146" stroke="#a0672a" stroke-width="1.2" fill="none" opacity="0.4"/>
                        <polygon points="32,130 38,40 52,80 72,28 88,72 110,22 132,72 148,28 168,80 182,40 188,130" fill="url(#bronzeBase)" stroke="#8b5a2b" stroke-width="1.5"/>
                        <polygon points="40,48 48,40 56,48" fill="rgba(255,255,255,0.1)" stroke="#a0672a" stroke-width="1"/>
                        <polygon points="72,34 80,28 88,34" fill="rgba(255,255,255,0.1)" stroke="#a0672a" stroke-width="1"/>
                        <polygon points="105,27 112,22 119,27" fill="rgba(255,255,255,0.1)" stroke="#a0672a" stroke-width="1"/>
                        <polygon points="132,34 140,28 148,34" fill="rgba(255,255,255,0.1)" stroke="#a0672a" stroke-width="1"/>
                        <polygon points="164,48 172,40 180,48" fill="rgba(255,255,255,0.1)" stroke="#a0672a" stroke-width="1"/>
                        <circle cx="38" cy="38" r="8" fill="url(#bronzeOrb)" stroke="#8b5a2b" stroke-width="2" class="gem-pulse"/>
                        <circle cx="72" cy="26" r="9" fill="url(#bronzeOrb)" stroke="#8b5a2b" stroke-width="2" class="gem-pulse gem-pulse-delay-1"/>
                        <circle cx="110" cy="20" r="10" fill="url(#bronzeOrb)" stroke="#8b5a2b" stroke-width="2" class="gem-pulse gem-pulse-delay-2"/>
                        <circle cx="148" cy="26" r="9" fill="url(#bronzeOrb)" stroke="#8b5a2b" stroke-width="2" class="gem-pulse gem-pulse-delay-3"/>
                        <circle cx="182" cy="38" r="8" fill="url(#bronzeOrb)" stroke="#8b5a2b" stroke-width="2" class="gem-pulse"/>
                        <circle cx="36" cy="35" r="5" fill="url(#bronzeOrbShine)" opacity="0.9"/>
                        <circle cx="70" cy="23" r="6" fill="url(#bronzeOrbShine)" opacity="0.9"/>
                        <circle cx="108" cy="17" r="7" fill="url(#bronzeOrbShine)" opacity="0.9"/>
                        <circle cx="146" cy="23" r="6" fill="url(#bronzeOrbShine)" opacity="0.9"/>
                        <circle cx="180" cy="35" r="5" fill="url(#bronzeOrbShine)" opacity="0.9"/>
                        <path d="M50,85 C53,78 57,76 63,82" stroke="#a0672a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M82,68 C85,61 89,59 95,65" stroke="#a0672a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M125,65 C131,59 135,61 138,68" stroke="#a0672a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M157,82 C163,76 167,78 170,85" stroke="#a0672a" stroke-width="1.8" fill="none" opacity="0.5"/>
                        <path d="M60,95 C65,88 70,88 75,95" stroke="#a0672a" stroke-width="1.5" fill="none" opacity="0.3"/>
                        <path d="M145,95 C150,88 155,88 160,95" stroke="#a0672a" stroke-width="1.5" fill="none" opacity="0.3"/>
                        <path class="sparkle-star" d="M110,14 L110,11 M110,14 L110,17" stroke="#e8a85c" stroke-width="2.5" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-1" d="M38,30 L36,27 M38,30 L40,27" stroke="#e8a85c" stroke-width="2" fill="none"/>
                        <path class="sparkle-star sparkle-star-delay-2" d="M182,30 L180,27 M182,30 L184,27" stroke="#e8a85c" stroke-width="2" fill="none"/>
                        <text x="110" y="160" text-anchor="middle" font-size="14" fill="#495057" font-weight="bold" letter-spacing="2">✦ GOOD ✦</text>
                    </svg>
                    
                {% else %}
                    <!-- No crown for below 70% -->
                    <div style="text-align: center; padding: 10px;">
                        <div style="font-size: 60px; opacity: 0.4;">📚</div>
                        <div style="font-size: 0.9rem; color: #6c757d; margin-top: 8px; font-weight: 600;">Keep practicing!</div>
                    </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Section Scores -->
        <div class="section-score-display" style="margin-top: 18px; padding-top: 18px; border-top: 2px solid #dee2e6;">
            <div style="display:flex; align-items:center; gap:8px; background: #f8f9fa; padding: 6px 14px; border-radius: 20px;">
                <span style="font-weight:600;">📖 Reading: {{ reading_score }}%</span>
                {% if reading_score >= 90 %}⭐{% elif reading_score >= 80 %}🌟{% elif reading_score >= 70 %}✨{% endif %}
            </div>
            <div style="display:flex; align-items:center; gap:8px; background: #f8f9fa; padding: 6px 14px; border-radius: 20px;">
                <span style="font-weight:600;">💬 Verbal: {{ verbal_score }}%</span>
                {% if verbal_score >= 90 %}⭐{% elif verbal_score >= 80 %}🌟{% elif verbal_score >= 70 %}✨{% endif %}
            </div>
            <div style="display:flex; align-items:center; gap:8px; background: #f8f9fa; padding: 6px 14px; border-radius: 20px;">
                <span style="font-weight:600;">🔢 Math: {{ math_score }}%</span>
                {% if math_score >= 90 %}⭐{% elif math_score >= 80 %}🌟{% elif math_score >= 70 %}✨{% endif %}
            </div>
        </div>
    </div>
{% endif %}

<form method="post" action="/sample_test">
{% set question_counter = namespace(value=1) %}
{% set reading_displayed = namespace(value=False) %}
{% set verbal_displayed = namespace(value=False) %}
{% set math_displayed = namespace(value=False) %}

{% for idx,p in enumerate(problems) %}
    {% if p[1]|length == 0 %}
        {# This is a passage or poem #}
        {% if not reading_displayed.value %}
            <div class="section-header">📖 READING SECTION</div>
            {% set reading_displayed.value = True %}
        {% endif %}
        <div class="problem" id="p{{idx}}">
            {% set passage_text = p[0] %}
            {% if '—' in passage_text and passage_text|length < 2000 %}
                <div class="poetry-text">{{ passage_text|safe }}</div>
            {% else %}
                <div class="passage-text">{{ passage_text|safe }}</div>
            {% endif %}
        </div>
    {% else %}
        {# This is a real question #}
        {% if question_counter.value == 1 %}
            <div class="section-header">📖 READING QUESTIONS</div>
        {% elif question_counter.value == 7 %}
            <div class="section-header">💬 VERBAL REASONING</div>
        {% elif question_counter.value == 27 %}
            <div class="section-header">🔢 QUANTITATIVE REASONING</div>
        {% endif %}
        
        <div class="problem" id="p{{idx}}">
            <div class="question-text"><strong>{{ question_counter.value }}.</strong> {{ p[0]|safe }}</div>
            {% set question_counter.value = question_counter.value + 1 %}
            <input type="hidden" id="answer_{{idx}}" name="answer_{{idx}}" value="">
            <div class="choices">
                {% for cidx,choice in enumerate(p[1]) %}
                    <div class="choice" onclick="selectChoice({{idx}},{{cidx}})">{{ choice|safe }}</div>
                {% endfor %}
            </div>
            {% if results %}
                <div class="result">
                    {% if results[idx] == True %}
                        <span class="correct">✓ Correct</span>
                    {% else %}
                        <span class="incorrect">✗ Incorrect</span>
                    {% endif %}
                </div>
            {% endif %}
        </div>
    {% endif %}
{% endfor %}

{% if not score %}
    <div style="margin-top: 30px; text-align: center;">
        <button type="submit">Submit Test</button>
    </div>
{% endif %}
</form>
</div>

<script>
// Force MathJax to render after page is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    if (typeof MathJax !== 'undefined') {
        MathJax.typesetPromise();
    }
});
</script>
</body>
</html>"""
###############################################################################################

LOGIN_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSAT Study App</title>
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }
.container { max-width: 900px; margin: 40px auto; background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }
h1 { color: #003366; }
button { background: #006; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-size: 16px; margin-top: 20px; }
button:hover { background: #004; }
</style>
</head>
<body>
<div class="container">
    <h1>📚 SSAT Study App</h1>
    <div style="padding: 20px;">
        <p style="font-size: 1.2rem;">Welcome to the SSAT Study App!</p>
        <p style="color: #446; margin-top: 10px;">This application runs in local mode and does not require login.</p>
        <p style="color: #446;">All features are available to all users.</p>
        <form method="get" action="/home">
            <button type="submit">Enter App</button>
        </form>
    </div>
</div>
</body>
</html>
"""

###############################################################################################

DATA_VIEW_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSAT Study App - Data Unavailable</title>
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }
.container { max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }
h1 { color: #003366; }
button { background: #006; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-size: 16px; margin-top: 20px; }
button:hover { background: #004; }
</style>
</head>
<body>
<div class="container">
    <h1>📊 Data Tracking Unavailable</h1>
    <div style="padding: 40px 20px;">
        <p style="font-size: 1.2rem; margin-bottom: 20px;">This feature is currently unavailable.</p>
        <p style="color: #666;">The application is running in local mode without a database.</p>
        <p style="color: #666; margin-top: 10px;">Your practice sessions are still fully functional!</p>
        <form method="get" action="/home">
            <button type="submit">Back to Home</button>
        </form>
    </div>
</div>
</body>
</html>
"""

###############################################################################################

ADMIN_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSAT Study App - Admin Unavailable</title>
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; }
.container { max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }
h1 { color: #003366; }
button { background: #006; color: white; border: none; padding: 12px 24px; border-radius: 10px; cursor: pointer; font-size: 16px; margin-top: 20px; }
button:hover { background: #004; }
</style>
</head>
<body>
<div class="container">
    <h1>🔐 Admin Panel Unavailable</h1>
    <div style="padding: 40px 20px;">
        <p style="font-size: 1.2rem; margin-bottom: 20px;">The admin panel is currently unavailable.</p>
        <p style="color: #666;">This application is running in local mode without user management features.</p>
        <p style="color: #666; margin-top: 10px;">All functionality is available to all users.</p>
        <form method="get" action="/home">
            <button type="submit">Back to Home</button>
        </form>
    </div>
</div>
</body>
</html>
"""

###############################################################################################


@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_user(username, password):
            session['user'] = username
            session['is_admin'] = is_admin(username)
            session['problems'] = []
            session['answers'] = []
            session['correct_indices'] = []
            return redirect(url_for('home'))
        else:
            error = '<p style="color:red">Invalid credentials</p>'
    
    login_form = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - SSAT Study App</title>
        <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#f0f4f8; padding:20px; margin:0; }}
        .login {{ max-width:420px; margin:80px auto; background:white; padding:24px; border-radius:20px; box-shadow:0 8px 24px rgba(0,0,0,0.1); }}
        input {{ width:100%; padding:12px; margin:8px 0; font-size:16px; border-radius:12px; border:2px solid #006; box-sizing: border-box; }}
        button {{ background:#006; color:white; border:none; padding:12px; border-radius:12px; cursor:pointer; width:100%; font-size:16px; font-weight:600; }}
        h2 {{ margin-top:0; color:#003366; text-align:center; }}
        .error {{ color:#c33; text-align:center; }}
        .note {{ text-align:center; margin-top:20px; color:#666; font-size:12px; }}
        </style>
    </head>
    <body>
        <div class="login">
            <h2>📚 SSAT Study App</h2>
            {error}
            <form method='post'>
                <input name='username' placeholder='Username' required><br>
                <input type='password' name='password' placeholder='Password' required><br>
                <button type='submit'>Login</button>
            </form>
            <div class="note">
                Contact your administrator for login credentials.
            </div>
        </div>
    </body>
    </html>
    """
    return login_form


@app.route('/home')
def home():
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    problems = session.get('problems')
    
    return render_template_string(PAGE_TEMPLATE,
                                  user=session.get('user'),
                                  problems=problems,
                                  results=None,
                                  score=None,
                                  correct_count=0,
                                  total=0,
                                  percent=0,
                                  enumerate=enumerate)


@app.route('/generate', methods=['POST'])
def generate():
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    # Clear previous submission data
    session.pop('submitted', None)
    session.pop('saved_results', None)
    session.pop('saved_answers', None)
    session.pop('saved_correct_count', None)
    session.pop('saved_total_questions', None)
    
    section = request.form.get('section')
    topic = request.form.get('topic')
    
    # ============================================================
    # READING COMPREHENSION SECTION
    # ============================================================
    if section == 'reading':
        problems = []
        
        if topic == 'Nonfiction':
            passages = gen_reading_comprehension('nonfiction', 1)
        elif topic == 'Fiction':
            passages = gen_reading_comprehension('fiction', 1)
        elif topic == 'Poetry':
            passages = gen_reading_comprehension('poetry', 1)
        else:
            passages = gen_reading_comprehension('nonfiction', 1)
        
        for passage_text, questions in passages:
            problems.append((passage_text, [], -1))
            for q_text, choices, correct in questions:
                problems.append((q_text, choices, correct))
        
        session['problems'] = problems
        session['answers'] = [None] * len(problems)
        session['correct_indices'] = [p[2] for p in problems]
        
        return redirect(url_for('home'))
    
    # ============================================================
    # VERBAL AND QUANTITATIVE SECTIONS
    # ============================================================
    else:
        num = int(request.form.get('num', 5))
        num = max(1, min(10, num))  # Limit to 10 to keep size manageable
        
        if section == 'verbal':
            if topic == 'Synonyms': 
                problems = gen_synonyms(num)
            elif topic == 'Analogies': 
                problems = gen_analogies(num)
            elif topic == 'Mixed Practice': 
                problems = gen_random_mix(num, 'verbal')
            else:
                problems = gen_synonyms(num)
        
        else:  # section == 'quant'
            if topic == 'Number Sense and Arithmetic': 
                problems = gen_number_sense_arithmetic(num)
            elif topic == 'Algebraic Thinking': 
                problems = gen_algebraic_thinking(num)
            elif topic == 'Geometry and Measurement': 
                problems = gen_geometry_measurement(num)
            elif topic == 'Data and Probability': 
                problems = gen_data_probability(num)
            elif topic == 'SSAT Practice': 
                problems = gen_ssat_math(num)
            else:
                problems = gen_ssat_math(num)
        
        # Shuffle problems
        random.shuffle(problems)
        
        # Normalize problems
        normalized = []
        for q, choices, correct in problems:
            choices = list(choices)
            while len(choices) < 5:
                fake = str(random.randint(1, 99))
                if fake not in choices:
                    choices.append(fake)
            if len(choices) > 5:
                choices = choices[:5]
                if correct >= 5:
                    correct = 0
            normalized.append((q, choices, correct))
        
        session['problems'] = normalized
        session['answers'] = [None] * len(normalized)
        session['correct_indices'] = [p[2] for p in normalized]
        
        return redirect(url_for('home'))

    


@app.route('/submit', methods=['POST'])
def submit_answers():
    if 'user' not in session: 
        return redirect(url_for('login'))

    problems = session.get('problems', [])
    corrects = session.get('correct_indices', [])
    
    if not problems:
        return redirect(url_for('home'))
    
    results = []
    correct_count = 0
    submitted_answers = []
    total_questions = 0

    for i in range(len(problems)):
        raw_ans = request.form.get(f'answer_{i}', '')
        
        if i < len(corrects) and corrects[i] == -1:
            results.append(True)
            submitted_answers.append(-1)
            continue
        
        total_questions += 1
        
        try:
            ans = int(raw_ans)
        except (ValueError, TypeError):
            ans = -1

        submitted_answers.append(ans)

        if i < len(corrects) and ans != -1 and ans == corrects[i]:
            results.append(True)
            correct_count += 1
        else:
            results.append(False)

    percent = round((correct_count / total_questions) * 100) if total_questions > 0 else 0

    session['submitted'] = True
    session['saved_results'] = results
    session['saved_answers'] = submitted_answers
    session['saved_correct_count'] = correct_count
    session['saved_total_questions'] = total_questions

    return render_template_string(PAGE_TEMPLATE,
                                  user=session.get('user'),
                                  problems=problems,
                                  results=results,
                                  answers=submitted_answers,
                                  score=True,
                                  correct_count=correct_count,
                                  total=total_questions,
                                  percent=percent,
                                  enumerate=enumerate)



@app.route('/sample_test', methods=['GET', 'POST'])
def sample_test():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        all_problems = []
        
        # === READING COMPREHENSION (1 passage, 6 questions) ===
        reading_type = random.choice(['poetry', 'fiction', 'nonfiction'])
        
        if reading_type == 'poetry':
            passages = gen_reading_comprehension('poetry', 1)
        elif reading_type == 'fiction':
            passages = gen_reading_comprehension('fiction', 1)
        else:
            passages = gen_reading_comprehension('nonfiction', 1)
        
        for passage_text, questions in passages:
            all_problems.append((passage_text, [], -1))
            # All 6 reading questions
            for q_text, choices, correct in questions:
                all_problems.append((q_text, choices, correct))
        
        # === VERBAL SECTION (5 synonyms + 5 analogies = 10 total) ===
        synonyms = gen_synonyms(5)
        for q_text, choices, correct in synonyms:
            all_problems.append((q_text, choices, correct))
        
        analogies = gen_analogies(5)
        for q_text, choices, correct in analogies:
            all_problems.append((q_text, choices, correct))
        
        # === QUANTITATIVE SECTION (10 SSAT math questions) ===
        math_problems = gen_ssat_math(10)
        for q_text, choices, correct in math_problems:
            all_problems.append((q_text, choices, correct))
        
        # Store in session
        session['sample_test_problems'] = all_problems
        session['sample_test_correct_indices'] = [p[2] for p in all_problems]
        session['sample_test_reading_type'] = reading_type
        session['sample_test_submitted'] = False
        session.modified = True
        
        return render_template_string(SAMPLE_TEST_TEMPLATE,
                                      user=session.get('user'),
                                      problems=all_problems,
                                      reading_type=reading_type,
                                      enumerate=enumerate)
    
    else:  # POST
        problems = session.get('sample_test_problems', [])
        corrects = session.get('sample_test_correct_indices', [])
        reading_type = session.get('sample_test_reading_type', 'unknown')
        username = session.get('user')
        
        if not problems:
            return redirect(url_for('sample_test'))
        
        # Initialize counters
        results = []
        reading_correct = 0
        reading_total = 0
        verbal_correct = 0
        verbal_total = 0
        math_correct = 0
        math_total = 0
        
        reading_count = 0
        verbal_count = 0
        
        # Loop through all answers
        for i in range(len(problems)):
            raw_ans = request.form.get(f'answer_{i}', '')
            
            if corrects[i] == -1:
                results.append(True)
                continue
            
            try:
                ans = int(raw_ans)
            except (ValueError, TypeError):
                ans = -1
            
            # First 6 questions after passage are Reading
            if reading_count < 6:
                reading_total += 1
                if ans != -1 and ans == corrects[i]:
                    reading_correct += 1
                    results.append(True)
                else:
                    results.append(False)
                reading_count += 1
            
            # Next 10 questions are Verbal (5 synonyms + 5 analogies)
            elif verbal_count < 10:
                verbal_total += 1
                if ans != -1 and ans == corrects[i]:
                    verbal_correct += 1
                    results.append(True)
                else:
                    results.append(False)
                verbal_count += 1
            
            # Remaining 10 questions are Math
            else:
                math_total += 1
                if ans != -1 and ans == corrects[i]:
                    math_correct += 1
                    results.append(True)
                else:
                    results.append(False)
        
        # Calculate totals
        total_questions = reading_total + verbal_total + math_total
        correct_count = reading_correct + verbal_correct + math_correct
        
        reading_percent = round((reading_correct / reading_total) * 100) if reading_total > 0 else 0
        verbal_percent = round((verbal_correct / verbal_total) * 100) if verbal_total > 0 else 0
        math_percent = round((math_correct / math_total) * 100) if math_total > 0 else 0
        total_percent = round((correct_count / total_questions) * 100) if total_questions > 0 else 0
        
        # Save attempt
        save_user_attempt(username, reading_type, total_percent, reading_percent, verbal_percent, math_percent)
        
        return render_template_string(SAMPLE_TEST_TEMPLATE,
                                      user=username,
                                      problems=problems,
                                      results=results,
                                      score=True,
                                      correct_count=correct_count,
                                      total=total_questions,
                                      percent=total_percent,
                                      reading_score=reading_percent,
                                      verbal_score=verbal_percent,
                                      math_score=math_percent,
                                      reading_type=reading_type,
                                      enumerate=enumerate)

    

@app.route('/view_data')
def view_data():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session.get('user')
    print(f"View data - User: {username}")
    
    try:
        attempts = get_user_attempts(username)
        print(f"Found {len(attempts)} attempts for {username}")
    except Exception as e:
        print(f"Error getting attempts: {e}")
        attempts = []
    
    # Calculate statistics
    total_attempts = len(attempts)
    
    if total_attempts > 0:
        # Last attempt
        last_attempt = attempts[-1]
        
        # Average of last 5 attempts
        last_5 = attempts[-5:] if total_attempts >= 5 else attempts
        avg_total = sum(float(a.get('total_score', 0)) for a in last_5) / len(last_5)
        avg_reading = sum(float(a.get('reading_score', 0)) for a in last_5) / len(last_5)
        avg_verbal = sum(float(a.get('verbal_score', 0)) for a in last_5) / len(last_5)
        avg_math = sum(float(a.get('math_score', 0)) for a in last_5) / len(last_5)
        
        # Prepare data for chart
        attempts_numbers = list(range(1, total_attempts + 1))
        total_scores = [float(a.get('total_score', 0)) for a in attempts]
        reading_scores = [float(a.get('reading_score', 0)) for a in attempts]
        verbal_scores = [float(a.get('verbal_score', 0)) for a in attempts]
        math_scores = [float(a.get('math_score', 0)) for a in attempts]
    else:
        last_attempt = None
        avg_total = avg_reading = avg_verbal = avg_math = 0
        attempts_numbers = []
        total_scores = reading_scores = verbal_scores = math_scores = []
    
    # Render the template
    return render_template_string(DATA_VIEW_TEMPLATE,
                                  user=username,
                                  total_attempts=total_attempts,
                                  last_attempt=last_attempt,
                                  avg_total=round(avg_total, 1),
                                  avg_reading=round(avg_reading, 1),
                                  avg_verbal=round(avg_verbal, 1),
                                  avg_math=round(avg_math, 1),
                                  attempts_numbers=attempts_numbers,
                                  total_scores=total_scores,
                                  reading_scores=reading_scores,
                                  verbal_scores=verbal_scores,
                                  math_scores=math_scores,
                                  enumerate=enumerate)



@app.route('/reset_data', methods=['POST'])
def reset_data():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    import csv
    import os
    import json
    from flask import jsonify
    
    data = request.get_json()
    password = data.get('password')
    
    # Check password
    if password != '1234':
        return jsonify({'success': False, 'message': 'Incorrect password'})
    
    csv_file = 'sample_test_data.csv'
    username = session.get('user')
    
    if not os.path.isfile(csv_file):
        return jsonify({'success': False, 'message': 'No data file found'})
    
    # Read all rows and keep only those NOT belonging to current user
    rows_to_keep = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['username'] != username:
                rows_to_keep.append(row)
    
    # Write back only the rows from other users
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_to_keep)
    
    return jsonify({'success': True, 'message': 'Data reset successfully'})

@app.route('/admin')
def admin_panel():
    if 'user' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = get_all_users()
    return render_template_string(ADMIN_TEMPLATE, users=users, enumerate=enumerate)

@app.route('/create_user', methods=['POST'])
def create_user_route():
    if 'user' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'true'
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'})
    
    if create_user(username, password, is_admin):
        return jsonify({'success': True, 'message': f'User {username} created successfully'})
    else:
        return jsonify({'success': False, 'message': 'User already exists'})

@app.route('/delete_user', methods=['POST'])
def delete_user_route():
    if 'user' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    username = request.form.get('username')
    
    if delete_user(username):
        return jsonify({'success': True, 'message': f'User {username} deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Cannot delete admin user'})


@app.route('/fundamentals', methods=['POST'])
def fundamentals_generate():
    """Generate fundamentals of mathematics practice problems."""
    operation = request.form.get('operation', 'addition')
    number_type = request.form.get('number_type', 'whole')
    num_questions = int(request.form.get('fnum', 5))
    
    fproblems = []
    for _ in range(min(num_questions, 10)):
        problem = generate_fundamentals_problem(operation, number_type)
        if problem:
            # problem is (q_text, choices, correct_index)
            # Shuffle choices and find correct index
            q_text = problem[0]
            choices = problem[1]
            correct_answer = choices[0]  # First is correct before shuffle
            random.shuffle(choices)
            correct_index = choices.index(correct_answer)
            fproblems.append((q_text, choices, correct_index))
    
    session['fproblems'] = fproblems
    session['fresults'] = None
    session['fscore'] = None
    session['fpercent'] = None
    session['fcorrect_count'] = None
    session['ftotal'] = None
    session['fquote'] = None
    session['fauthor'] = None
    
    return render_template('page.html', 
                         fproblems=fproblems,
                         fresults=None,
                         fscore=None,
                         fpercent=None,
                         fcorrect_count=None,
                         ftotal=None,
                         fquote=None,
                         fauthor=None,
                         # Keep existing template variables
                         problems=session.get('problems', []),
                         results=session.get('results', []),
                         score=session.get('score', None),
                         percent=session.get('percent', None),
                         correct_count=session.get('correct_count', None),
                         total=session.get('total', None))

@app.route('/fundamentals_submit', methods=['POST'])
def fundamentals_submit():
    """Submit and grade fundamentals practice problems."""
    fproblems = session.get('fproblems', [])
    
    if not fproblems:
        return redirect(url_for('home'))
    
    fresults = []
    correct_count = 0
    
    for idx, problem in enumerate(fproblems):
        user_answer = request.form.get(f'fanswer_{idx}')
        correct_index = problem[2]
        correct_answer = problem[1][correct_index]
        
        is_correct = (user_answer == str(correct_answer))
        fresults.append(is_correct)
        if is_correct:
            correct_count += 1
    
    total = len(fproblems)
    percent = int((correct_count / total) * 100) if total > 0 else 0
    
    # Get an inspirational quote
    quote, author = get_inspirational_quote()
    
    session['fresults'] = fresults
    session['fscore'] = True
    session['fpercent'] = percent
    session['fcorrect_count'] = correct_count
    session['ftotal'] = total
    session['fquote'] = quote
    session['fauthor'] = author
    
    return render_template('page.html',
                         fproblems=fproblems,
                         fresults=fresults,
                         fscore=True,
                         fpercent=percent,
                         fcorrect_count=correct_count,
                         ftotal=total,
                         fquote=quote,
                         fauthor=author,
                         # Keep existing template variables
                         problems=session.get('problems', []),
                         results=session.get('results', []),
                         score=session.get('score', None),
                         percent=session.get('percent', None),
                         correct_count=session.get('correct_count', None),
                         total=session.get('total', None))
    




@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# NEW: Reset route - clears everything
@app.route('/reset', methods=['POST'])
def reset():
    """Complete reset - clear session and logout"""
    session.clear()
    return redirect(url_for('login'))


if __name__=='__main__':

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True, use_reloader=False)
