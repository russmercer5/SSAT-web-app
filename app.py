"""
SSAT Study App - Flask
Editable single-file Flask application for SSAT Verbal & Quantitative practice.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, render_template
import random
from fractions import Fraction
import math

app = Flask(__name__)
app.secret_key = 'replace_with_a_real_secret'

USERNAME = 'mason' 
PASSWORD = '1899'

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

    distractors = [
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
            [d for d in distractors if d != correct_def],
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
# EXPANDED DISTRACTOR BANKS
# ======================

distractors = {
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

    # build a giant cross-category distractor bank (unchanged)
    all_distractors = []
    for words in distractors.values():
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
            raise ValueError("Not enough distractors after filtering forbidden words.")

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
            #question_text = f"If each of {a} boxes have {b} apples and {c} apples are added, how many apples are there in total?"
            question_text = f"There are {a} boxes with {b} apples each and there are {c} boxes with {d} oranges each, How many fruit are in the boxes in total?"

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

        elif q_type == 3:  # Algebraic inequality

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

            question_text = f"Which value of x satisfies the inequality?\n\n{inequality}"

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


def gen_geometry_measurement(n=5):
    problems = []

    for i in range(n):
        problem_type = i % 5
        q_text = ""
        choices = []
        answer_str = ""
        
        # 1) Area of triangle or circle
        if problem_type == 0:
            if random.choice(["triangle", "circle"]) == "triangle":
                b = random.randint(5, 15)
                h = random.randint(3, 12)
                ans = round(0.5 * b * h, 2)
                q_text = f"A triangle has a base of {b} cm and a height of {h} cm. What is its area in cm²?"
            else:
                d = random.randint(4, 16)
                r = d / 2
                ans = round(math.pi * r ** 2, 2)
                q_text = f"A circle has a diameter of {d} cm. What is its area in cm²? (Use π ≈ 3.14)"

            answer_str = str(ans)
            choices = [
                answer_str,
                str(round(ans * 1.1, 2)),
                str(round(ans * 0.9, 2)),
                str(round(ans + 5, 2)),
                str(round(max(ans - 5, 1), 2)),
            ]

        # 2) Rectangle
        elif problem_type == 1:
            L = random.randint(5, 15)
            W = random.randint(3, 12)

            # Decide problem type based on even/odd index (pass 'i' from main loop)
            # Even i: ask for perimeter (given area + one side)
            # Odd i: ask for area (given perimeter + one side)
            if i % 2 == 0:
                # Type 1: Given area + one side → find perimeter
                area = L * W
                known_side = L
                ans = round(2 * (known_side + area / known_side), 2)
                q_text = (
                    f"A rectangle has an area of {area} cm² and one side of length {known_side} cm. "
                    "What is its perimeter in cm?"
                )
            else:
                # Type 2: Given perimeter + one side → find area
                perimeter = 2 * (L + W)
                known_side = L
                ans = round((perimeter / 2 - known_side) * known_side, 2)
                q_text = (
                    f"A rectangle has a perimeter of {perimeter} cm and one side of length {known_side} cm. "
                    "What is its area in cm²?"
                )

            # Make choices as strings
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
                q_text = f"A cube has sides of length {s} cm. What is its volume in cm³?"
            else:
                l = random.randint(3, 10)
                w = random.randint(2, 8)
                h = random.randint(2, 6)
                ans = l * w * h
                q_text = f"A rectangular prism has dimensions {l} cm × {w} cm × {h} cm. What is its volume in cm³?"

            answer_str = str(ans)
            choices = [
                answer_str,
                str(ans + 5),
                str(max(ans - 5, 1)),
                str(ans + 10),
                str(ans - 3),
            ]

        # 4) Angles 
        elif problem_type == 3:
            total = random.choice([90, 180])
            num_angles = random.choice([2, 3])  # total number including x

            min_angle = 10
            remaining = total - min_angle  # reserve at least 10° for x

            known_angles = []

            for i in range(num_angles - 1):
                # How many angles still need to be generated AFTER this one?
                remaining_slots = (num_angles - 1) - i - 1

                # Minimum we must leave for future angles + x
                min_remaining = remaining_slots * min_angle

                max_angle = remaining - min_remaining
                angle = random.randint(min_angle, max_angle)

                known_angles.append(angle)
                remaining -= angle

            # Remaining is x
            answer = remaining
            answer_str = f"{answer}°"

            display_angles = [f"{a}°" for a in known_angles] + ["x°"]
            random.shuffle(display_angles)

            q_text = (
                f"Find the value of x if the angles "
                f"{', '.join(display_angles)} add up to {total}°."
            )

            choices = [
                answer_str,
                f"{answer + 5}°",
                f"{max(answer - 5, 1)}°",
                f"{answer + 10}°",
                f"{answer - 3}°",
            ]

        # 5) Time
        else:
            h1, m1 = random.randint(0, 3), random.randint(10, 59)
            h2, m2 = random.randint(0, 3), random.randint(10, 59)

            total_m = h1 * 60 + m1 + h2 * 60 + m2
            h, m = divmod(total_m, 60)

            answer_str = f"{h} hours and {m} minutes"
            q_text = (
                f"Antonio studied for {h1} hours and {m1} minutes on Monday, "
                f"and for {h2} hours and {m2} minutes on Tuesday. "
                "How many total hours and minutes did he study?"
            )

            choices = [
                answer_str,
                f"{h+1} hours and {m} minutes",
                f"{h} hours and {m+5} minutes",
                f"{max(h-1,0)} hours and {m} minutes",
                f"{h} hours and {max(m-5,0)} minutes",
            ]

        random.shuffle(choices)
        correct_index = choices.index(answer_str)

        problems.append((q_text, choices, correct_index))

    return problems



def gen_data_probability(n=5):
    problems = []

    for i in range(n):
        problem_type = i % 5
        q_text = ""
        choices = []
        answer_str = ""
        correct_index = 0  # initialize

        # ---------- TYPE 1: Marble probability ----------
        if problem_type == 0:
            colors = random.sample(["red", "blue", "green", "yellow"], random.randint(3, 4))
            counts = [random.randint(1, 6) for _ in colors]
            total = sum(counts)

            if random.choice([True, False]):
                color = random.choice(colors)
                favorable = counts[colors.index(color)]
                q_text = (
                    "A bag contains the following marbles:\n\n"
                    f"{', '.join([f'{c}: {n}' for c, n in zip(colors, counts)])}\n\n"
                    f"What is the probability of selecting a {color} marble?"
                )
            else:
                color_pair = random.sample(colors, 2)
                favorable = sum([counts[colors.index(c)] for c in color_pair])
                q_text = (
                    "A bag contains the following marbles:\n\n"
                    f"{', '.join([f'{c}: {n}' for c, n in zip(colors, counts)])}\n\n"
                    f"What is the probability of selecting a {color_pair[0]} or {color_pair[1]} marble?"
                )

            frac = Fraction(favorable, total).limit_denominator()
            answer_str = f"{frac.numerator}/{frac.denominator}"

            # Generate unique distractors
            wrong = set()
            while len(wrong) < 4:
                num_delta = random.choice([-1, 0, 1])
                den_delta = random.choice([-1, 0, 1])
                num = max(1, frac.numerator + num_delta)
                den = max(num, frac.denominator + den_delta)
                s = f"{Fraction(num, den).limit_denominator().numerator}/{Fraction(num, den).limit_denominator().denominator}"
                if s != answer_str:
                    wrong.add(s)

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
                    "The table shows inches of rainfall:\n\n"
                    f"{', '.join([f'{d}: {r}' for d, r in zip(days, rainfall)])}\n\n"
                    "How many more inches of rain fell on weekdays than on the weekend?"
                )
            else:
                ans = sum(rainfall)
                q_text = (
                    "The table shows inches of rainfall:\n\n"
                    f"{', '.join([f'{d}: {r}' for d, r in zip(days, rainfall)])}\n\n"
                    "How many inches of rain fell in total for the week?"
                )

            answer_str = str(ans)
            # Generate unique distractors
            wrong = set()
            while len(wrong) < 4:
                delta = random.choice([-2, -1, 1, 2])
                val = max(0, ans + delta)
                s = str(val)
                if s != answer_str:
                    wrong.add(s)
            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # ---------- TYPE 3: Favorite subject ----------
        elif problem_type == 2:
            subjects = ["Math", "English", "Science", "History"]
            total_students = random.choice([50, 200, 300])
            remaining = total_students
            counts = []

            for _ in range(len(subjects)-1):
                n = random.randint(0, remaining)
                counts.append(n)
                remaining -= n
            counts.append(remaining)

            subject = random.choice(subjects)
            count = counts[subjects.index(subject)]
            percent = round((count / total_students) * 100)

            q_text = (
                f"A survey asked students their favorite subject:\n\n"
                f"{', '.join([f'{s}: {c}' for s, c in zip(subjects, counts)])}\n\n"
                f"What percent of students chose {subject}?"
            )

            # Generate unique percent choices
            wrong = set()
            while len(wrong) < 4:
                delta = random.choice([-10, -5, 5, 10])
                val = max(0, min(100, percent + delta))
                s = f"{val}%"
                if s != f"{percent}%":
                    wrong.add(s)
            choices = [f"{percent}%"] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(f"{percent}%")

        # ---------- TYPE 4: Average ----------
        elif problem_type == 3:
            avg = random.randint(10, 20)
            nums = [random.randint(0, 2*avg) for _ in range(5)]
            last_num = avg*6 - sum(nums)
            nums.append(last_num)

            q_text = (
                "Find the average of the following numbers:\n\n"
                f"{', '.join(map(str, nums))}\n\n"
            )

            answer_str = str(avg)
            wrong = set()
            while len(wrong) < 4:
                delta = random.choice([-2, -1, 1, 2])
                val = max(0, avg + delta)
                s = str(val)
                if s != answer_str:
                    wrong.add(s)
            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # ---------- TYPE 5: Median/Range ----------
        else:

            nums = [random.randint(1, 50) for _ in range(7)]

            # Determine median/range using a sorted copy
            sorted_nums = sorted(nums)
            if random.choice([True, False]):
                ans = sorted_nums[3]  # median
                q_text = (
                    "Find the median of the following numbers:\n\n"
                    f"{', '.join(map(str, random.sample(nums, len(nums))))}\n\n"  # shuffle for display
                )
            else:
                ans = max(nums) - min(nums)  # range
                q_text = (
                    "Find the range of the following numbers:\n\n"
                    f"{', '.join(map(str, random.sample(nums, len(nums))))}\n\n"  # shuffle for display
                )

            answer_str = str(ans)

            # Generate unique distractors
            wrong = set()
            while len(wrong) < 4:
                delta = random.choice([-3, -2, -1, 1, 2, 3])
                val = max(0, ans + delta)
                s = str(val)
                if s != answer_str:
                    wrong.add(s)

            choices = [answer_str] + list(wrong)
            random.shuffle(choices)
            correct_index = choices.index(answer_str)

        # ---------- APPEND QUESTION TO PROBLEMS ----------
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
    n = min(n, 20)

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


# === HTML template ===



PAGE_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>SSAT Study App</title>
<style>
body { font-family: 'Computer Modern', sans-serif; background:#f8fbff; color:#022; padding:20px; }
.container { max-width:900px; margin:0 auto; background:white; padding:18px; border-radius:10px; box-shadow:0 6px 18px rgba(0,0,0,0.08);}
h1 { margin-top:0; color:#003366; }
form.inline { display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
select,input[type=number] { padding:8px 10px; font-size:16px; border-radius:6px; border:2px solid #006; background:#eef; }
button { background:#006; color:#cff; border:none; padding:10px 16px; border-radius:8px; cursor:pointer; }
button.secondary { background:#024; }
.problem { margin:14px 0; padding:12px; border-radius:8px; border:1px solid #ccd; }
.choices {
    margin-top: 8px;
    display: flex;
    flex-direction: column; /* vertical stacking */
    gap: 8px; /* vertical spacing */
    align-items: flex-start; /* align buttons to the left, so they only take up as much width as needed */
}

.choice {
    background: #f2f8ff;
    padding: 8px 10px;
    border-radius: 6px;
    border: 1px solid #cde;
    cursor: pointer;
    display: inline-block; /* ensures button width fits content */
    width: auto; /* override any inherited width */
}
.choice { background:#f2f8ff; padding:8px 10px; border-radius:6px; border:1px solid #cde; cursor:pointer; }
.selected { outline:3px solid #88f; }
.result { margin-left:12px; font-weight:700; }
.correct { color:green; }
.incorrect { color:red; }
.score { font-size:18px; font-weight:700; margin-top:12px; }
.login { max-width:420px; margin:20px auto; }
.header { display:flex; justify-content:space-between; align-items:center; }
.small { font-size:14px; color:#446; }

.choice.correct {
    background-color: #d4edda; /* soft green */
    border-color: #a6d8a8;
}
.choice.incorrect {
    background-color: #f8d7da; /* soft red */
    border-color: #f5a6a6;
}

</style>
<script>

function updateTopicOptions(){
    const section = document.getElementById('section').value;
    const topic = document.getElementById('topic');
    topic.innerHTML = '';
    let options = [];
    if(section==='verbal'){ options = ['Synonyms','Analogies','Mixed Practice']; }
    else { options = ['Number Sense and Arithmetic','Algebraic Thinking','Geometry and Measurement','Data and Probability','Mixed Practice']; }
    for(const opt of options){
        const el = document.createElement('option'); el.value=opt; el.text=opt; topic.appendChild(el);
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
<h1>SSAT Study App</h1>
<div class="small">Logged in as <b>{{ user }}</b> | 
<form style="display:inline" method="post" action="/logout"><button class="secondary">Logout</button></form>
</div></div>
<hr>
<form method="post" action="/generate" class="inline">
<label>Section:
<select id="section" name="section">
<option value="verbal">Verbal Reasoning</option>
<option value="quant">Quantitative Reasoning</option>
</select>
</label>
<label>Topic:
<select id="topic" name="topic"></select>
</label>
<label>Number of problems:
<input type="number" name="num" min="1" max="20" value="5">
</label>
<button type="submit">Generate</button>
</form>
{% if problems %}
<form method="post" action="/submit">
<div style="margin-top:16px">
{% for idx,p in enumerate(problems) %}
<div class="problem" id="p{{idx}}">
<div><strong>{{ idx+1 }}.</strong> {{ p[0]|safe }}</div>
<input type="hidden" id="answer_{{idx}}" name="answer_{{idx}}" value="">
<div class="choices">
{% for cidx,choice in enumerate(p[1]) %}
<div class="choice
    {% if results %}
        {% if results[idx]==False and cidx==p[2] %}correct{% endif %}
        {% if results[idx]==False and cidx==answers[idx]|int %}incorrect{% endif %}
        {% if results[idx]==True and cidx==answers[idx]|int %}correct{% endif %}
    {% endif %}
" onclick="selectChoice({{idx}},{{cidx}})">{{choice|safe}}</div>
{% endfor %}
</div>
{% if results %}
<div class="result">
{% if results[idx]==True %}<span class="correct">✔</span>{% elif results[idx]==False %}<span class="incorrect">✖</span>{% endif %}
</div>{% endif %}
</div>{% endfor %}
</div>
<div style="margin-top:12px">
<button type="submit">Submit Answers</button>
</div>
</form>
{% endif %}
{% if score is not none %}
<div class="score">Score: {{ correct_count }}/{{ total }} ({{ percent }}%)</div>
{% endif %}
</div>
</body>
</html>"""

# === Routes ===
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method=='POST':
        if request.form.get('username')==USERNAME and request.form.get('password')==PASSWORD:
            session['user']=USERNAME
            session['problems']=[]
            session['answers']=[]
            session['correct_indices']=[]
            return redirect(url_for('home'))
        else:
            error='<p style="color:red">Invalid credentials</p>'
    login_form = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Login - SSAT Study App</title>
        <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background:#f8fbff; color:#022; padding:20px; }}
        .login {{ max-width:420px; margin:80px auto; background:white; padding:18px; border-radius:10px; box-shadow:0 6px 18px rgba(0,0,0,0.08); }}
        input {{ width:100%; padding:10px; margin:6px 0; font-size:16px; border-radius:6px; border:2px solid #006;
         box-sizing: border-box;}}
        button {{ background:#006; color:#cff; border:none; padding:10px 16px; border-radius:8px; cursor:pointer; width:100%; }}
        </style>
    </head>
    <body>
        <div class="login">
            <h2>Login</h2>
            {error}
            <form method='post'>
                <input name='username' placeholder='Username' required><br>
                <input type='password' name='password' placeholder='Password' required><br>
                <button type='submit'>Login</button>
            </form>
        </div>
    </body>
    </html>
    """
    return login_form

@app.route('/home')
def home():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template_string(PAGE_TEMPLATE,
                                  user=session.get('user'),
                                  problems=session.get('problems'),
                                  results=None,score=None,
                                  correct_count=0,
                                  total=0,
                                  percent=0,
                                  enumerate=enumerate)

@app.route('/generate', methods=['POST'])
def generate():
    if 'user' not in session: return redirect(url_for('login'))
    section=request.form.get('section')
    topic=request.form.get('topic')
    num=int(request.form.get('num',5))
    num=max(1,min(20,num))

    if section=='verbal':
        if topic=='Synonyms': problems=gen_synonyms(num)
        elif topic=='Analogies': problems=gen_analogies(num)
        else: problems=gen_random_mix(num,'verbal')
    else:
        if topic=='Number sense and Arithmetic': problems=gen_number_sense_arithmetic(num)
        elif topic=='Algebraic Thinking': problems=gen_algebraic_thinking(num)
        elif topic=='Geometry and Measurement': problems=gen_geometry_measurement(num)
        elif topic=='Data and Probability': problems=gen_data_probability(num)
        else: problems=gen_random_mix(num,'quant')

    normalized=[]
    for p in problems:
        q,choices,correct=p
        if len(choices)<5:
            while len(choices)<5:
                fake=str(random.randint(1,99))
                if fake not in choices: choices.append(fake)
        if len(choices)>5:
            choices=choices[:5]
            if correct>=5: correct=0
        normalized.append((q,choices,correct))

    session['problems']=normalized
    session['answers']=[None]*len(normalized)
    session['correct_indices']=[p[2] for p in normalized]

    return redirect(url_for('home'))


@app.route('/submit', methods=['POST'])
def submit_answers():
    if 'user' not in session: 
        return redirect(url_for('login'))

    problems = session.get('problems', [])
    corrects = session.get('correct_indices', [])
    results = []
    correct_count = 0
    submitted_answers = []

    for i in range(len(problems)):
        raw_ans = request.form.get(f'answer_{i}', '')
        try:
            ans = int(raw_ans)  # try to convert to int
        except (ValueError, TypeError):
            ans = None  # blank or invalid input becomes None

        session['answers'][i] = ans
        submitted_answers.append(ans if ans is not None else -1)  # store -1 for unanswered

        if ans is not None and ans == corrects[i]:
            results.append(True)
            correct_count += 1
        else:
            results.append(False)  # incorrect or blank counts as wrong

    total = len(problems)
    percent = round((correct_count / total) * 100) if total > 0 else 0

    return render_template_string(PAGE_TEMPLATE,
                                  user=session.get('user'),
                                  problems=problems,
                                  results=results,
                                  answers=submitted_answers,
                                  score=True,
                                  correct_count=correct_count,
                                  total=total,
                                  percent=percent,
                                  enumerate=enumerate)



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True, use_reloader=False)
