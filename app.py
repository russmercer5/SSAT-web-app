"""
SSAT Study App - Flask
Editable single-file Flask application for SSAT Verbal & Quantitative practice.
Mobile-friendly version with all fixes applied.
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
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Great Pacific Garbage Patch is a solid island of trash that fishing boats can land on", "The Great Pacific Garbage Patch is a massive collection of microplastics that threatens marine life", "The Great Pacific Garbage Patch was discovered in 1997 and will double in size by 2050", "Plastics in the ocean break down into harmless particles that fish can eat safely"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone in this passage?", "choices": ["Celebratory", "Indifferent", "Concerned", "Humorous"], "correct": 2},
                {"type": "vocab", "text": "The word 'microplastics' (line 3) most nearly means", "choices": ["Large fishing nets", "Tiny plastic particles", "Chemical pollutants from factories", "Natural ocean sediments"], "correct": 1},
                {"type": "inference", "text": "Based on the passage, what can be inferred about the future of ocean ecosystems?", "choices": ["They will thrive due to increased nutrients from plastics", "They will remain unchanged because plastics are harmless", "They will face serious challenges from plastic pollution", "They will naturally filter out all plastic within 10 years"], "correct": 2},
                {"type": "detail", "text": "According to the passage, when was the Great Pacific Garbage Patch discovered?", "choices": ["1997", "2050", "1985", "2001"], "correct": 0},
                {"type": "purpose", "text": "What is the author's primary purpose in writing this passage?", "choices": ["To entertain readers with an ocean adventure story", "To inform readers about an environmental problem", "To persuade readers to stop using all plastic products immediately", "To describe how to clean up the garbage patch"], "correct": 1}
            ]
        },
        # Original nf2
        {
            "id": "nf2",
            "title": "The Invention of the Printing Press",
            "passage": """Before Johannes Gutenberg invented the printing press around 1440, books were copied by hand, usually by monks in monasteries. This process was extremely slow and expensive, making books rare treasures that only the wealthy could afford. Gutenberg's revolutionary machine used movable metal type that could be arranged and rearranged to print pages quickly. His most famous printed work was the Gutenberg Bible, of which about 180 copies were produced. The printing press sparked an information revolution, allowing knowledge to spread rapidly across Europe. Within fifty years, millions of books were printed, literacy rates began to rise, and ideas about science, religion, and politics spread faster than ever before.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Monks worked very hard copying books in monasteries", "Gutenberg's printing press revolutionized how information spread in Europe", "The Gutenberg Bible was the most important book ever printed", "Books were too expensive for most people before 1440"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward Gutenberg's invention?", "choices": ["Dismissive", "Angry", "Admiring", "Confused"], "correct": 2},
                {"type": "vocab", "text": "The word 'revolutionary' (line 5) most nearly means", "choices": ["Dangerous", "Inexpensive", "Groundbreaking", "Complicated"], "correct": 2},
                {"type": "inference", "text": "What can be inferred about European society before the printing press?", "choices": ["Most people were able to read and write fluently", "Information and ideas spread very slowly", "Books were available to everyone at low cost", "Monks were the only people who knew how to read"], "correct": 1},
                {"type": "detail", "text": "According to the passage, approximately how many copies of the Gutenberg Bible were produced?", "choices": ["50", "100", "150", "180"], "correct": 3},
                {"type": "purpose", "text": "Why did the author include the fact that literacy rates began to rise after the printing press?", "choices": ["To show that books became cheaper", "To demonstrate the impact of easier access to books", "To criticize people who couldn't read", "To prove that Gutenberg was a good businessman"], "correct": 1}
            ]
        },
        # Original nf3
        {
            "id": "nf3",
            "title": "The Migration of Monarch Butterflies",
            "passage": """Each year, millions of monarch butterflies embark on an extraordinary journey of up to 3,000 miles from Canada and the northern United States to central Mexico. What makes this migration truly remarkable is that no single butterfly completes the round trip. Instead, it takes three to four generations to complete the annual cycle. The butterflies that return to Mexico in the fall are known as the 'super generation'—they live eight times longer than their parents and possess unique navigational abilities. Scientists believe monarchs use a combination of the sun's position and Earth's magnetic field to find their way. Unfortunately, habitat loss and climate change have reduced monarch populations by 90% in recent decades.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Monarch butterflies migrate to escape cold weather", "Monarch butterflies have a complex multi-generational migration that faces threats", "Scientists have fully explained how monarch butterflies navigate", "Monarch butterflies are the most beautiful of all insects"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone when discussing the monarch population decline?", "choices": ["Optimistic", "Unconcerned", "Alarmed", "Confused"], "correct": 2},
                {"type": "vocab", "text": "The word 'embark' (line 1) most nearly means", "choices": ["End", "Begin a journey", "Cancel", "Observe"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about the 'super generation' of monarchs?", "choices": ["They are the same as all other monarch generations", "They have special abilities that other generations lack", "They cannot fly as far as other generations", "They only live in Mexico year-round"], "correct": 1},
                {"type": "detail", "text": "According to the passage, how far do monarch butterflies migrate?", "choices": ["Up to 1,000 miles", "Up to 2,000 miles", "Up to 3,000 miles", "Up to 4,000 miles"], "correct": 2},
                {"type": "purpose", "text": "Why did the author include information about the 90% population decline?", "choices": ["To celebrate the butterflies' success", "To raise concern about threats to monarchs", "To prove that butterflies are unimportant", "To explain why migration is unnecessary"], "correct": 1}
            ]
        },
        # Original nf4
        {
            "id": "nf4",
            "title": "The Underground Railroad",
            "passage": """The Underground Railroad was not a real railroad but a secret network of routes and safe houses used by enslaved African Americans to escape to free states and Canada. Operating primarily in the decades before the Civil War, this network included brave individuals known as 'conductors,' the most famous being Harriet Tubman, who made 13 missions and rescued over 70 people. Travelers moved at night, guided by the North Star and coded messages in songs and quilts. Safe houses, called 'stations,' were often located in homes, barns, and churches. It is estimated that over 100,000 enslaved people escaped using the Underground Railroad between 1810 and 1850.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Harriet Tubman was the only person who helped enslaved people escape", "The Underground Railroad was a secret network that helped enslaved people reach freedom", "The Underground Railroad was an actual train system in the northern states", "Enslaved people escaped by following railroad tracks north"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's attitude toward the Underground Railroad participants?", "choices": ["Critical", "Respectful", "Confused", "Bored"], "correct": 1},
                {"type": "vocab", "text": "The word 'conductors' (line 4) most nearly means", "choices": ["Train operators", "People who guided escapees along the Underground Railroad", "Musicians who played during escapes", "People who built safe houses"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why escapees traveled at night?", "choices": ["Night was colder and more comfortable", "Darkness provided cover to avoid being caught", "The North Star was only visible during the day", "All safe houses were only open at night"], "correct": 1},
                {"type": "detail", "text": "According to the passage, approximately how many people did Harriet Tubman rescue?", "choices": ["13", "50", "70", "100"], "correct": 2},
                {"type": "purpose", "text": "What is the author's primary purpose in writing this passage?", "choices": ["To entertain with adventure stories", "To inform about an important part of American history", "To persuade readers to build a new Underground Railroad", "To criticize the people who helped escapees"], "correct": 1}
            ]
        },
        # Original nf5
        {
            "id": "nf5",
            "title": "The Water Cycle",
            "passage": """Earth's water is constantly moving in a process called the water cycle. This cycle has four main stages: evaporation, condensation, precipitation, and collection. When the sun heats water in oceans, lakes, and rivers, it turns into vapor and rises into the air—this is evaporation. As the vapor rises, it cools and turns back into tiny water droplets, forming clouds in a process called condensation. When these droplets become heavy enough, they fall as rain, snow, or hail—precipitation. Finally, the water collects in bodies of water or soaks into the ground, where the cycle begins again. This continuous process has been happening for billions of years and provides fresh water for all life on Earth.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The water cycle is a continuous process that provides fresh water for Earth's living things", "Evaporation happens when the sun heats water", "Rain is the most important part of the water cycle", "The water cycle only takes place in oceans"], "correct": 0},
                {"type": "tone", "text": "Which word best describes the author's tone?", "choices": ["Excited", "Educational/Factual", "Skeptical", "Humorous"], "correct": 1},
                {"type": "vocab", "text": "The word 'precipitation' (line 5) most nearly means", "choices": ["Water soaking into the ground", "Water turning into vapor", "Water falling from clouds as rain or snow", "Clouds forming from water droplets"], "correct": 2},
                {"type": "inference", "text": "What can be inferred about what would happen if the sun stopped heating Earth's water?", "choices": ["The water cycle would continue unchanged", "Evaporation would stop and the water cycle would be disrupted", "More rain would fall than ever before", "All water would instantly freeze"], "correct": 1},
                {"type": "detail", "text": "According to the passage, how many main stages does the water cycle have?", "choices": ["Two", "Three", "Four", "Five"], "correct": 2},
                {"type": "purpose", "text": "Why did the author write this passage?", "choices": ["To explain a natural process that sustains life on Earth", "To persuade readers to conserve water", "To entertain with a story about a raindrop", "To criticize how humans use water"], "correct": 0}
            ]
        },
        # NEW nf6 - Slightly longer
        {
            "id": "nf6",
            "title": "The Discovery of Penicillin",
            "passage": """In September 1928, Scottish bacteriologist Alexander Fleming returned to his laboratory at St. Mary's Hospital in London after a month-long vacation. Before leaving, he had stacked several petri dishes containing Staphylococcus bacteria on a bench near an open window. When Fleming sorted through the dishes to discard contaminated ones, he noticed something unusual: on one dish, a mold called Penicillium notatum had grown, and the bacteria surrounding the mold had been destroyed. Rather than throwing the dish away, Fleming became curious. He cultured the mold and discovered that it produced a substance that killed several disease-causing bacteria. He named this substance 'penicillin.' However, Fleming struggled to purify penicillin in large quantities, and his work was largely forgotten for a decade. In 1939, Australian scientist Howard Florey and German-born biochemist Ernst Chain rediscovered Fleming's research and developed methods to mass-produce penicillin. By 1945, penicillin was being widely used to treat infected wounds in soldiers during World War II, saving countless lives. That same year, Fleming, Florey, and Chain shared the Nobel Prize in Medicine. Penicillin became the first antibiotic, revolutionizing medicine and proving that even accidental discoveries can change the world.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Alexander Fleming discovered penicillin by accident, and later scientists developed it into a life-saving antibiotic", "Penicillin was the only antibiotic ever discovered in the 20th century", "World War II soldiers were the first people to benefit from any form of medicine", "Alexander Fleming won a Nobel Prize for his vacation planning skills"], "correct": 0},
                {"type": "tone", "text": "Which word best describes the author's tone toward Fleming's discovery?", "choices": ["Dismissive", "Celebratory and respectful", "Sarcastic", "Indifferent"], "correct": 1},
                {"type": "vocab", "text": "The word 'bacteriologist' (line 1) most nearly means", "choices": ["A doctor who treats only children", "A scientist who studies bacteria", "A person who cleans laboratories", "A specialist in mold growth"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why Fleming's work was 'largely forgotten for a decade'?", "choices": ["He intentionally hid his research from other scientists", "He could not produce penicillin in large enough quantities to be practical", "Other scientists had already discovered better antibiotics", "The Nobel Prize committee ignored his work"], "correct": 1},
                {"type": "detail", "text": "According to the passage, who helped mass-produce penicillin?", "choices": ["Alexander Fleming alone", "Florey and Chain", "St. Mary's Hospital staff", "World War II soldiers"], "correct": 1},
                {"type": "purpose", "text": "Why did the author include the detail about the open window?", "choices": ["To criticize Fleming's lab safety practices", "To explain how the mold likely entered the petri dish", "To prove that Fleming was careless", "To suggest that fresh air kills bacteria"], "correct": 1}
            ]
        },
        # NEW nf7
        {
            "id": "nf7",
            "title": "The Great Wall of China",
            "passage": """Stretching over 13,000 miles, the Great Wall of China is the longest structure ever built by humans. Contrary to popular belief, the wall cannot be seen from space with the naked eye, but its historical significance remains immense. Construction began as early as the 7th century BCE, when various Chinese states built walls to protect against northern invaders. In 221 BCE, Emperor Qin Shi Huang connected and extended these walls into a unified defensive system. Most of the existing wall today was built during the Ming Dynasty (1368–1644), using stone, brick, and rammed earth. The wall includes watchtowers, barracks, and beacon towers for signaling. Over 1 million workers—including soldiers, peasants, and prisoners—died building it, leading some to call it 'the longest cemetery on Earth.' Despite its massive scale, the wall was never completely effective at preventing invasions; nomadic armies repeatedly breached it. Today, the Great Wall is a UNESCO World Heritage Site and one of the most visited tourist attractions globally, though large sections have crumbled due to erosion and human activity.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Great Wall of China was a perfect defensive structure that never failed", "The Great Wall is a massive, historically significant structure built over centuries, though it was not completely effective", "Emperor Qin Shi Huang built the entire Great Wall by himself", "The Great Wall is clearly visible from space without any equipment"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone when discussing the wall's effectiveness?", "choices": ["Exaggerated", "Balanced and factual", "Dismissive", "Angry"], "correct": 1},
                {"type": "vocab", "text": "The word 'breached' (line 11) most nearly means", "choices": ["Built", "Repaired", "Broke through or penetrated", "Admired from a distance"], "correct": 2},
                {"type": "inference", "text": "What can be inferred about why the wall is called 'the longest cemetery on Earth'?", "choices": ["Many workers died during its construction", "It was built on top of ancient graves", "It contains tombs of emperors", "Tourists frequently die there"], "correct": 0},
                {"type": "detail", "text": "During which dynasty was most of the existing wall built?", "choices": ["Qin Dynasty", "Ming Dynasty", "Han Dynasty", "Song Dynasty"], "correct": 1},
                {"type": "purpose", "text": "Why did the author mention that the wall cannot be seen from space?", "choices": ["To correct a common misconception", "To prove the wall is not impressive", "To argue against space exploration", "To show that astronauts have poor vision"], "correct": 0}
            ]
        },
        # NEW nf8
        {
            "id": "nf8",
            "title": "Coral Bleaching: The Oceans' Warning Sign",
            "passage": """Coral reefs, often called the 'rainforests of the sea,' support about 25% of all marine species despite covering less than 1% of the ocean floor. These vibrant ecosystems depend on a symbiotic relationship between coral polyps and microscopic algae called zooxanthellae. The algae live inside the coral tissue, providing up to 90% of the coral's energy through photosynthesis, while the coral gives the algae a protected home. When ocean temperatures rise even 1–2 degrees Celsius above normal, the coral becomes stressed and expels the algae. Without the algae, the coral loses its main food source and turns white—a process called coral bleaching. Bleached corals are not dead immediately, but they are starving and vulnerable to disease. If temperatures return to normal quickly, corals can recover. However, prolonged warming leads to mass die-offs. Major bleaching events have increased dramatically since the 1980s, driven by climate change. The 2016 bleaching event on Australia's Great Barrier Reef killed nearly 30% of shallow-water corals. Scientists warn that without urgent action to reduce carbon emissions, most of the world's coral reefs could disappear by 2050, devastating marine biodiversity and the millions of people who depend on reefs for food and tourism income.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Coral reefs are beautiful but unimportant to ocean health", "Rising ocean temperatures cause coral bleaching, threatening marine ecosystems and human communities", "Zooxanthellae are harmful parasites that damage coral reefs", "The Great Barrier Reef has fully recovered from all bleaching events"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone?", "choices": ["Urgent and concerned", "Lighthearted and funny", "Angry and accusatory", "Completely neutral without emotion"], "correct": 0},
                {"type": "vocab", "text": "The word 'symbiotic' (line 3) most nearly means", "choices": ["Parasitic and harmful", "Mutually beneficial", "Competitive", "Independent"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why bleached corals are described as 'starving'?", "choices": ["They refuse to eat other food", "They have lost the algae that provided most of their energy", "Ocean warming destroys all food in the water", "Other fish steal all their food"], "correct": 1},
                {"type": "detail", "text": "According to the passage, what percentage of shallow-water corals died on the Great Barrier Reef in 2016?", "choices": ["10%", "20%", "30%", "50%"], "correct": 2},
                {"type": "purpose", "text": "Why did the author call coral reefs the 'rainforests of the sea'?", "choices": ["To emphasize their biodiversity and ecological importance", "To suggest that coral grows on trees", "To confuse readers with a metaphor", "To argue that coral reefs are actually forests"], "correct": 0}
            ]
        },
        # NEW nf9
        {
            "id": "nf9",
            "title": "The Rosetta Stone: Cracking Ancient Egyptian Code",
            "passage": """In July 1799, French soldiers digging the foundations of a fort near the town of Rosetta (modern-day Rashid), Egypt, uncovered a large black granite slab inscribed with text. The stone, now known as the Rosetta Stone, contained three distinct scripts: ancient Greek, Demotic (a later Egyptian script), and hieroglyphics. Scholars could already read Greek, so they realized the stone held the key to deciphering Egyptian hieroglyphics—a script that had been unreadable for nearly 1,400 years. The stone dated back to 196 BCE and recorded a decree issued by Egyptian priests honoring Pharaoh Ptolemy V. After Napoleon's defeat, the British seized the stone and transported it to the British Museum in London, where it remains today. Deciphering the stone proved extremely difficult. English scientist Thomas Young made initial progress by identifying proper names. However, it was French scholar Jean-François Champollion who cracked the code in 1822. By comparing the Greek names with the hieroglyphic versions, Champollion realized that hieroglyphics represented sounds, not just ideas or objects. He identified phonetic characters and essentially created an Egyptian alphabet. His breakthrough unlocked thousands of years of Egyptian history, allowing modern readers to understand temple inscriptions, tomb writings, and papyrus scrolls that had been silent for centuries.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Rosetta Stone was carved by French soldiers in 1799", "The Rosetta Stone contained three identical scripts that were all easy to read", "The Rosetta Stone enabled scholars to decipher Egyptian hieroglyphics, unlocking ancient history", "Champollion discovered the Rosetta Stone in Egypt and kept it in France"], "correct": 2},
                {"type": "tone", "text": "Which word best describes the author's attitude toward Champollion's achievement?", "choices": ["Dismissive", "Admiring", "Jealous", "Confused"], "correct": 1},
                {"type": "vocab", "text": "The word 'deciphering' (line 6) most nearly means", "choices": ["Destroying", "Copying", "Interpreting or figuring out the meaning of", "Hiding"], "correct": 2},
                {"type": "inference", "text": "What can be inferred about why hieroglyphics had been unreadable for 1,400 years?", "choices": ["No one had found any examples of hieroglyphic writing", "The knowledge of how to read them had been lost", "Hieroglyphics were intentionally erased from all monuments", "Scholars were not interested in ancient Egypt"], "correct": 1},
                {"type": "detail", "text": "What year did Champollion decipher the hieroglyphics?", "choices": ["1799", "1822", "196 BCE", "1400 CE"], "correct": 1},
                {"type": "purpose", "text": "Why did the author include the information about Young and Champollion?", "choices": ["To show that multiple scholars contributed to deciphering the stone", "To prove that English scientists were smarter than French ones", "To argue that the stone should have stayed in Egypt", "To criticize how slowly scholars worked"], "correct": 0}
            ]
        },
        # NEW nf10
        {
            "id": "nf10",
            "title": "The Science of Sleep: Why We Need Rest",
            "passage": """Every living creature with a nervous system sleeps, yet scientists are still discovering exactly why. Sleep is not simply a period of rest; it is an active, essential biological process. During sleep, the brain cycles through several stages every 90 minutes, alternating between non-REM (rapid eye movement) and REM sleep. Non-REM sleep includes deep sleep, during which the body repairs tissues, strengthens the immune system, and releases growth hormones. REM sleep, when most vivid dreaming occurs, plays a critical role in memory consolidation and emotional regulation. The consequences of insufficient sleep are severe. Adults who regularly sleep less than seven hours per night face higher risks of obesity, heart disease, diabetes, and depression. In children and teenagers, chronic sleep loss impairs learning, attention, and emotional stability. The body's internal clock, or circadian rhythm, regulates sleep-wake cycles based on light exposure. Exposure to blue light from phones and computers at night disrupts this rhythm by suppressing melatonin, the hormone that induces sleepiness. Scientists recommend maintaining consistent sleep schedules, avoiding caffeine late in the day, and creating a dark, cool bedroom environment. Despite these known benefits, modern society often treats sleep as optional or even wasteful. However, accumulating research shows that sacrificing sleep for productivity ultimately backfires: well-rested people think more clearly, react faster, and perform better on nearly every cognitive task.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Sleep is a waste of time that productive people should minimize", "Sleep is an essential biological process with specific stages that support health and cognition", "Only humans and large mammals need to sleep", "REM sleep is the only important stage of the sleep cycle"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward people who sacrifice sleep?", "choices": ["Supportive", "Warning/Concerned", "Amused", "Indifferent"], "correct": 1},
                {"type": "vocab", "text": "The word 'circadian rhythm' (line 11) most nearly means", "choices": ["A type of sleep disorder", "The body's internal 24-hour clock", "A dream that repeats every night", "A medication for insomnia"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about blue light from phones and computers?", "choices": ["It helps people fall asleep faster", "It disrupts melatonin production, making sleep harder", "It has no effect on the human body", "It only affects children's sleep"], "correct": 1},
                {"type": "detail", "text": "According to the passage, what health risks increase with less than seven hours of sleep?", "choices": ["Only depression", "Obesity, heart disease, diabetes, and depression", "Broken bones and muscle pain", "Hair loss and poor vision"], "correct": 1},
                {"type": "purpose", "text": "Why did the author state that 'sacrificing sleep for productivity ultimately backfires'?", "choices": ["To convince readers that sleep is actually important for good performance", "To encourage people to work more hours", "To argue that sleep has no benefits", "To prove that all successful people sleep very little"], "correct": 0}
            ]
        },
        # NEW nf11
        {
            "id": "nf11",
            "title": "The Eruption of Mount Vesuvius, 79 CE",
            "passage": """On August 24, 79 CE, the Roman cities of Pompeii and Herculaneum were thriving commercial centers near the Bay of Naples. Few residents knew that the mountain looming above them, Mount Vesuvius, was a volcano—volcanoes were not yet understood in the ancient world. At approximately 1:00 PM, Vesuvius erupted violently, sending a mushroom cloud of ash, pumice, and toxic gases over 20 miles into the sky. The eruption lasted over 24 hours. Pompeii, located about 6 miles from the volcano, was buried under 13 to 20 feet of volcanic ash and pumice. Herculaneum, even closer, was destroyed by pyroclastic flows—superheated waves of gas and debris moving at over 50 miles per hour. The pyroclastic flows reached temperatures of about 500°C (930°F), instantly killing anyone in their path. An estimated 2,000 people died in Pompeii alone, though many had already fled. The cities were completely lost for nearly 1,700 years until their rediscovery in the 18th century. Excavations revealed remarkably preserved buildings, artifacts, and even plaster casts of human bodies frozen in their final moments. These discoveries provide an unparalleled snapshot of daily Roman life—from food in market stalls to graffiti on walls. Today, Vesuvius remains an active volcano, and nearly 3 million people live within dangerous proximity. Geologists warn that another major eruption is inevitable, though not immediately imminent.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Mount Vesuvius erupted in 79 CE, destroying Pompeii and Herculaneum but preserving a unique record of Roman life", "All Roman cities were destroyed by volcanoes in 79 CE", "The residents of Pompeii were foolish not to evacuate", "Mount Vesuvius has been dormant since 79 CE and will never erupt again"], "correct": 0},
                {"type": "tone", "text": "Which word best describes the author's tone when describing the destruction?", "choices": ["Humorous", "Sober and factual", "Celebratory", "Angry at the Romans"], "correct": 1},
                {"type": "vocab", "text": "The word 'pyroclastic flows' (line 8) most nearly means", "choices": ["Slow-moving lava rivers", "Fast-moving, superheated clouds of gas and debris", "Rainfall after a volcanic eruption", "Earthquakes caused by volcanoes"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why the cities were so well preserved?", "choices": ["People intentionally buried them to protect them", "The volcanic ash and debris covered and sealed them quickly", "The Romans built them to survive volcanic eruptions", "The cities were made of metal"], "correct": 1},
                {"type": "detail", "text": "Approximately how many people died in Pompeii according to the passage?", "choices": ["500", "2,000", "20,000", "3 million"], "correct": 1},
                {"type": "purpose", "text": "Why did the author mention the plaster casts of human bodies?", "choices": ["To shock readers with gruesome details", "To show how the eruption preserved evidence of ancient life", "To prove that no one survived the eruption", "To argue that the bodies should not be displayed"], "correct": 1}
            ]
        },
        # NEW nf12
        {
            "id": "nf12",
            "title": "The Amazon Rainforest: Lungs of the Planet",
            "passage": """Spanning over 2.7 million square miles across nine South American countries, the Amazon rainforest is the largest tropical rainforest on Earth. It produces approximately 20% of the world's oxygen, earning its nickname 'the lungs of the planet.' However, recent scientific research suggests that the Amazon actually consumes nearly as much oxygen as it produces through respiration, making the 'lungs' label somewhat misleading. More accurately, the Amazon is an enormous carbon sink: its trees store about 100 billion metric tons of carbon, equivalent to roughly 10 years of global fossil fuel emissions. The forest supports extraordinary biodiversity. One in ten known species on Earth lives in the Amazon, including over 40,000 plant species, 1,300 bird species, 3,000 fish species, and 2.5 million insect species. Indigenous peoples have lived in the Amazon for at least 11,000 years, with over 400 tribes currently residing there, some completely uncontacted by modern society. Deforestation poses the greatest threat to the Amazon. Since 1978, over 289,000 square miles—an area larger than Texas—have been cleared primarily for cattle ranching and soybean farming. Deforestation releases stored carbon into the atmosphere, accelerates climate change, and destroys habitats. Scientists warn that the Amazon is approaching a 'tipping point' where it could transition from rainforest to dry savanna, a shift that would have catastrophic global consequences.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Amazon rainforest is a small forest with few species", "The Amazon is a massive, biodiverse ecosystem that stores carbon and faces serious deforestation threats", "Deforestation in the Amazon only affects local animals, not the global climate", "The Amazon produces all of the world's oxygen and has no environmental problems"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone regarding deforestation?", "choices": ["Optimistic that deforestation is stopping", "Alarmed and concerned", "Celebratory", "Indifferent"], "correct": 1},
                {"type": "vocab", "text": "The word 'carbon sink' (line 6) most nearly means", "choices": ["A hole in the ground that collects rainwater", "Something that absorbs and stores more carbon than it releases", "A factory that produces carbon emissions", "A type of tree that grows only in the Amazon"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why the 'lungs of the planet' nickname is somewhat misleading?", "choices": ["The Amazon produces no oxygen at all", "The Amazon consumes nearly as much oxygen as it produces through respiration", "Only scientists are allowed to call it that", "The nickname was invented by a child"], "correct": 1},
                {"type": "detail", "text": "According to the passage, how many indigenous tribes currently live in the Amazon?", "choices": ["40", "400", "4,000", "11,000"], "correct": 1},
                {"type": "purpose", "text": "Why did the author mention the 'tipping point' where the Amazon could become savanna?", "choices": ["To warn readers that deforestation could cause irreversible damage", "To suggest that savannas are better than rainforests", "To claim that climate change is a hoax", "To argue that the Amazon should be cut down intentionally"], "correct": 0}
            ]
        },
        # NEW nf13
        {
            "id": "nf13",
            "title": "The Cold War: A Half-Century of Tension",
            "passage": """Following World War II, the United States and the Soviet Union emerged as the world's two superpowers, but their political and economic systems could not have been more different. The United States promoted democracy and capitalism, while the Soviet Union enforced communist rule and a command economy. This ideological clash sparked the Cold War, a period of intense geopolitical tension from roughly 1947 to 1991. The term 'cold' war was used because the two superpowers never directly fought each other in a conventional war. Instead, they engaged in proxy wars—supporting opposing sides in conflicts in Korea, Vietnam, Afghanistan, and elsewhere. Both nations amassed enormous nuclear arsenals, creating a doctrine called 'Mutually Assured Destruction' (MAD): if either side launched a nuclear attack, the other would retaliate, ensuring total destruction for both. Paradoxically, this terrifying balance prevented direct war. The Cold War also included the Space Race, as each nation sought to demonstrate technological superiority. The Soviets launched Sputnik, the first satellite, in 1957; the Americans landed astronauts on the moon in 1969. The arms race and proxy conflicts cost trillions of dollars and millions of lives. The Cold War finally ended when the Soviet Union collapsed in 1991, largely due to economic stagnation and political reforms led by Mikhail Gorbachev. The end of the Cold War reshaped global politics, but its legacy—including leftover nuclear weapons and regional instability—persists today.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The United States won the Cold War easily without any problems", "The Cold War was a long period of tension between the US and Soviet Union, fought through proxies and nuclear threats", "The Soviet Union was always more powerful than the United States", "The Cold War only involved space exploration, not military conflict"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward the doctrine of Mutually Assured Destruction?", "choices": ["Celebratory", "Terrified but recognizing its paradoxical logic", "Confused", "Humorous"], "correct": 1},
                {"type": "vocab", "text": "The word 'proxy wars' (line 8) most nearly means", "choices": ["Wars fought directly between superpowers", "Conflicts where superpowers supported opposing sides without fighting each other directly", "Wars fought only with nuclear weapons", "Wars that last less than one week"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why the Cold War never became a direct war between the US and USSR?", "choices": ["Both countries were allies and friends", "The doctrine of Mutually Assured Destruction made direct war too dangerous", "The United Nations banned them from fighting", "Neither country had any weapons"], "correct": 1},
                {"type": "detail", "text": "In what year did the Soviet Union collapse?", "choices": ["1947", "1969", "1991", "2001"], "correct": 2},
                {"type": "purpose", "text": "Why did the author include the Space Race in this passage?", "choices": ["To show that the Cold War included competition beyond just military conflict", "To argue that space exploration caused the Cold War", "To prove that the Soviet Union won the Cold War", "To suggest that space exploration was irrelevant"], "correct": 0}
            ]
        },
        # NEW nf14
        {
            "id": "nf14",
            "title": "Photosynthesis: The Basis of Life on Earth",
            "passage": """Nearly all life on Earth depends on a single chemical process: photosynthesis. This process, performed by plants, algae, and some bacteria, converts light energy from the sun into chemical energy stored in sugars. The overall equation appears simple: six molecules of carbon dioxide plus six molecules of water, in the presence of sunlight and chlorophyll, produce one molecule of glucose and six molecules of oxygen. However, the actual process involves two complex stages: the light-dependent reactions and the Calvin cycle (light-independent reactions). In the light-dependent reactions, chlorophyll absorbs sunlight and uses that energy to split water molecules, releasing oxygen as a byproduct and generating energy-carrying molecules called ATP and NADPH. The Calvin cycle then uses ATP and NADPH to convert carbon dioxide from the atmosphere into glucose, which plants use for growth and energy. Photosynthesis not only feeds plants but also produces the oxygen that animals—including humans—breathe. It also removes carbon dioxide from the atmosphere, helping regulate Earth's climate. Scientists estimate that photosynthetic organisms produce about 170 billion tons of organic matter annually. Without photosynthesis, Earth's atmosphere would contain almost no oxygen, and complex life would not exist. Understanding photosynthesis has allowed humans to improve crop yields, develop biofuels, and even inspire technologies like solar cells that mimic natural energy capture.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Photosynthesis is a simple process that only happens in laboratories", "Photosynthesis is a complex, two-stage process that converts sunlight into chemical energy and produces oxygen", "Plants do not need sunlight to survive", "Photosynthesis only produces oxygen, not food for plants"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward photosynthesis?", "choices": ["Dismissive", "Awed and explanatory", "Angry", "Humorous"], "correct": 1},
                {"type": "vocab", "text": "The word 'chlorophyll' (line 4) most nearly means", "choices": ["A type of sugar", "The green pigment in plants that absorbs sunlight", "A waste product of photosynthesis", "A gas released by plants"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about what would happen if photosynthesis stopped?", "choices": ["Nothing would change", "Oxygen levels would drop and most life would die", "Plants would grow faster", "Animals would learn to photosynthesize"], "correct": 1},
                {"type": "detail", "text": "According to the passage, what two stages make up photosynthesis?", "choices": ["Daytime and nighttime reactions", "Light-dependent reactions and the Calvin cycle", "Oxygen production and carbon destruction", "Glucose splitting and water combining"], "correct": 1},
                {"type": "purpose", "text": "Why did the author mention that scientists have developed solar cells inspired by photosynthesis?", "choices": ["To show that understanding natural processes can lead to useful technologies", "To argue that solar cells are better than plants", "To prove that photosynthesis is outdated", "To confuse readers with irrelevant information"], "correct": 0}
            ]
        },
        # NEW nf15
        {
            "id": "nf15",
            "title": "The Harlem Renaissance: A Cultural Explosion",
            "passage": """In the 1920s and early 1930s, the Harlem neighborhood of New York City became the epicenter of a remarkable cultural movement known as the Harlem Renaissance. This period saw an unprecedented flowering of African American literature, music, art, and intellectual thought. The Great Migration had brought hundreds of thousands of African Americans from the rural South to northern cities like New York, Chicago, and Detroit, seeking better economic opportunities and fleeing racial violence. Harlem, in particular, became a magnet for Black artists and thinkers. Writers such as Langston Hughes, Zora Neale Hurston, and Claude McKay produced poetry, novels, and essays that celebrated Black identity and explored the African American experience. Hughes's poems, including 'The Negro Speaks of Rivers,' used jazz and blues rhythms to create a distinctive literary voice. Musicians like Duke Ellington, Louis Armstrong, and Bessie Smith transformed American music, developing jazz into a sophisticated art form that gained international acclaim. Visual artists including Aaron Douglas created paintings and murals inspired by African art and modernism. The movement was not just artistic; it was intellectual. Scholars like W.E.B. Du Bois and Alain Locke argued for racial pride and full citizenship rights. While the Harlem Renaissance faded after the Great Depression, its influence endured. It challenged racist stereotypes, established African American culture as central to American identity, and paved the way for the Civil Rights Movement decades later.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Harlem Renaissance was a small, unimportant art movement in New York", "The Harlem Renaissance was a major cultural movement of African American arts and ideas that reshaped American culture", "Only writers participated in the Harlem Renaissance", "The Harlem Renaissance occurred in the 1950s"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's attitude toward the Harlem Renaissance?", "choices": ["Dismissive", "Celebratory and respectful", "Confused", "Critical"], "correct": 1},
                {"type": "vocab", "text": "The word 'unprecedented' (line 3) most nearly means", "choices": ["Small and insignificant", "Never before seen or done", "Boring and predictable", "Accidental"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why Harlem became a center for Black artists?", "choices": ["The government forced artists to move there", "The Great Migration brought many African Americans north, and Harlem became a cultural hub", "No other cities allowed Black artists to work", "Harlem was chosen randomly"], "correct": 1},
                {"type": "detail", "text": "According to the passage, which poet used jazz and blues rhythms in his work?", "choices": ["Zora Neale Hurston", "Claude McKay", "Langston Hughes", "W.E.B. Du Bois"], "correct": 2},
                {"type": "purpose", "text": "Why did the author include the effects of the Harlem Renaissance on the Civil Rights Movement?", "choices": ["To show that the movement had lasting historical importance", "To argue that art has no impact on politics", "To prove that the Civil Rights Movement failed", "To criticize the Harlem Renaissance for not doing enough"], "correct": 0}
            ]
        },
        # NEW nf16
        {
            "id": "nf16",
            "title": "The Theory of Plate Tectonics",
            "passage": """Earth's surface is not a solid, unbroken shell. Instead, it consists of about 15 major tectonic plates—massive slabs of solid rock that float on the partially molten layer beneath them called the asthenosphere. The theory of plate tectonics, which became widely accepted by geologists in the 1960s, describes how these plates move, interact, and reshape Earth's surface. Plates move incredibly slowly, typically 1 to 10 centimeters per year—about the speed at which fingernails grow. However, over millions of years, this creeping movement produces dramatic results. Where plates diverge (move apart), magma rises to create new crust, forming mid-ocean ridges and rift valleys. Where plates converge (collide), one plate may subduct (sink beneath) the other, creating deep ocean trenches and volcanic mountain ranges like the Andes. When two continental plates collide, neither subducts easily; instead, they crumple to form massive mountain ranges like the Himalayas, which are still rising today as India pushes into Asia. Where plates slide past each other horizontally, they create transform faults—the San Andreas Fault in California is a famous example. These sliding movements often trigger earthquakes. Plate tectonics explains not only earthquakes and volcanoes but also the distribution of fossils, the matching shapes of continents (like South America and Africa), and the locations of mineral deposits. Without plate motion, Earth would likely lack its protective magnetic field and might resemble the geologically dead planet Mars.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Earth's surface is completely solid and never changes", "Plate tectonics explains how slow-moving plates cause earthquakes, volcanoes, and mountain formation", "Only geologists care about tectonic plates", "Earthquakes are random events with no scientific explanation"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone?", "choices": ["Humorous", "Educational and clear", "Angry", "Bored"], "correct": 1},
                {"type": "vocab", "text": "The word 'subduct' (line 12) most nearly means", "choices": ["Rise upward quickly", "Sink or descend beneath another plate", "Explode violently", "Freeze solid"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why the Himalayas are still rising?", "choices": ["The Indian plate continues to push into the Asian plate", "The mountains are made of inflatable rock", "Volcanoes are adding lava to the top", "Humans are building them higher"], "correct": 0},
                {"type": "detail", "text": "According to the passage, how fast do tectonic plates typically move?", "choices": ["1 to 10 centimeters per year", "1 to 10 meters per year", "1 to 10 kilometers per year", "They do not move at all"], "correct": 0},
                {"type": "purpose", "text": "Why did the author compare Earth to Mars?", "choices": ["To suggest humans should move to Mars", "To emphasize that plate tectonics may be essential for a planet to have a magnetic field and remain geologically active", "To prove that Mars once had life", "To show that Earth is completely different from all other planets"], "correct": 1}
            ]
        },
        # NEW nf17
        {
            "id": "nf17",
            "title": "The Industrial Revolution: Transforming Society",
            "passage": """Beginning in Great Britain around 1760 and spreading across Europe and North America by the mid-19th century, the Industrial Revolution fundamentally changed how humans produced goods, worked, and lived. Before industrialization, most people lived in rural agricultural communities, making goods by hand at home or in small workshops. The revolution introduced several key innovations: the steam engine (improved by James Watt), mechanical textile machines (spinning jenny, power loom), iron production techniques, and eventually electricity and the internal combustion engine. These technologies enabled factories to produce goods faster, cheaper, and in larger quantities than ever before. The effects were profound and contradictory. On the positive side, industrialization created new jobs, increased overall wealth, improved transportation (railroads and steamships), and eventually raised living standards. Many consumer goods became affordable to ordinary people for the first time. However, the early Industrial Revolution also brought severe problems. Factory workers—including young children—labored 12 to 16 hours daily in dangerous conditions for low wages. Cities grew explosively but lacked sanitation or adequate housing, leading to disease outbreaks. Air and water pollution reached unprecedented levels. Social reformers like Charles Dickens highlighted these injustices, and gradually labor laws, unions, and public health measures emerged. By the late 19th century, a growing middle class formed, but vast economic inequality persisted. The Industrial Revolution set the stage for modern capitalism, urbanization, and environmental challenges that the world still grapples with today.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["The Industrial Revolution only had negative effects on society", "The Industrial Revolution brought both positive advances and serious problems that reshaped society", "Industrialization began in the United States in 1900", "The Industrial Revolution had no effect on how people lived"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's treatment of the Industrial Revolution?", "choices": ["One-sided and praising", "Balanced, acknowledging both benefits and harms", "Only critical", "Only confused"], "correct": 1},
                {"type": "vocab", "text": "The word 'unprecedented' (line 16) most nearly means", "choices": ["Small and unimportant", "Never seen before to such a degree", "Easily solvable", "Intentionally caused"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why children worked in factories during the early Industrial Revolution?", "choices": ["Children preferred working to going to school", "There were few labor laws, and factory owners wanted cheap labor", "No adults were available to work", "Children were stronger than adults"], "correct": 1},
                {"type": "detail", "text": "According to the passage, who improved the steam engine?", "choices": ["Charles Dickens", "James Watt", "Karl Marx", "Alexander Graham Bell"], "correct": 1},
                {"type": "purpose", "text": "Why did the author mention Charles Dickens?", "choices": ["To show that some writers criticized the negative effects of industrialization", "To argue that Dickens supported child labor", "To prove that all writers ignored industrial problems", "To suggest that Dickens invented the steam engine"], "correct": 0}
            ]
        },
        # NEW nf18
        {
            "id": "nf18",
            "title": "Vaccines: How They Work and Why They Matter",
            "passage": """Before the development of vaccines, infectious diseases like smallpox, polio, measles, and whooping cough killed or disabled millions of people annually. Vaccines have since saved more lives than any medical intervention except clean drinking water. The basic principle of vaccination is remarkably simple and elegant. When a pathogen—a virus or bacterium—enters the body, the immune system typically takes several days to recognize and mount a response. During that delay, the pathogen can multiply and cause severe illness. Vaccines work by exposing the immune system to a harmless version of a pathogen (or pieces of it) so that the immune system learns to recognize and destroy the real pathogen quickly. This creates immunological memory. The first true vaccine was developed by Edward Jenner in 1796. Jenner observed that milkmaids who caught cowpox, a mild disease, did not catch deadly smallpox. He deliberately infected a boy with cowpox, then exposed him to smallpox—the boy remained healthy. The word 'vaccine' comes from 'vacca,' Latin for cow, referring to cowpox. In the 20th century, scientists like Jonas Salk and Albert Sabin developed polio vaccines, nearly eradicating polio worldwide. Vaccination relies on herd immunity: when enough people are vaccinated, the disease cannot spread easily, protecting even those who cannot be vaccinated (infants, allergic individuals). Despite overwhelming scientific evidence, vaccine hesitancy—often based on a debunked 1998 study falsely linking vaccines to autism—has led to outbreaks of previously controlled diseases. The World Health Organization now considers vaccine hesitancy a top global health threat.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Vaccines are unnecessary because most diseases are harmless", "Vaccines train the immune system to recognize pathogens, have saved millions of lives, and face modern hesitancy", "Edward Jenner invented vaccines in 2020", "Vaccines only work for smallpox"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward vaccine hesitancy?", "choices": ["Supportive", "Alarmed and concerned", "Celebratory", "Indifferent"], "correct": 1},
                {"type": "vocab", "text": "The word 'pathogen' (line 5) most nearly means", "choices": ["A type of vaccine", "A disease-causing microorganism", "A part of the human immune system", "A hospital treatment"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about what happened to smallpox due to vaccination?", "choices": ["It was completely eradicated (eliminated worldwide)", "It became more dangerous", "It still kills millions annually", "Vaccines had no effect on it"], "correct": 0},
                {"type": "detail", "text": "What year did Edward Jenner develop the first vaccine?", "choices": ["1796", "1896", "1996", "2020"], "correct": 0},
                {"type": "purpose", "text": "Why did the author mention the debunked 1998 study on vaccines and autism?", "choices": ["To argue that the study was correct", "To explain the origin of modern vaccine hesitancy", "To prove that scientists never make mistakes", "To suggest that autism is caused by something else"], "correct": 1}
            ]
        },
        # NEW nf19
        {
            "id": "nf19",
            "title": "The Search for Exoplanets",
            "passage": """For most of human history, astronomers could only speculate whether planets existed beyond our solar system. The first confirmed detection of an exoplanet—a planet orbiting another star—came in 1992, when astronomers discovered two planets orbiting a pulsar. In 1995, Swiss astronomers Michel Mayor and Didier Queloz found 51 Pegasi b, the first exoplanet orbiting a sun-like star. This discovery earned them a Nobel Prize. Since then, exoplanet research has exploded. NASA's Kepler Space Telescope (launched 2009) and Transiting Exoplanet Survey Satellite (TESS, launched 2018) have identified over 5,000 confirmed exoplanets, with thousands more candidates awaiting confirmation. Most exoplanets are detected using two primary methods: the transit method and the radial velocity method. The transit method observes a star's brightness; if a planet passes in front of the star, it dims slightly and periodically. The radial velocity method detects tiny wobbles in a star's motion caused by an orbiting planet's gravitational pull. The ultimate goal of exoplanet research is to find potentially habitable worlds—planets with conditions that might support life. Scientists focus on the 'habitable zone' (or 'Goldilocks zone'), the region around a star where temperatures could allow liquid water to exist. Some promising candidates include the TRAPPIST-1 system (seven Earth-sized planets, three in the habitable zone) and Proxima Centauri b (orbiting the nearest star to our Sun). Future telescopes, including the James Webb Space Telescope and the planned Habitable Worlds Observatory, will analyze exoplanet atmospheres for biosignature gases like oxygen and methane that could indicate life.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Exoplanets are impossible to detect with current technology", "Astronomers have discovered over 5,000 exoplanets using methods like transit and radial velocity, and are now searching for habitable worlds", "Only one exoplanet has ever been found", "Exoplanets are all exactly like Earth"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward exoplanet discoveries?", "choices": ["Bored", "Excited and informative", "Skeptical", "Angry"], "correct": 1},
                {"type": "vocab", "text": "The word 'exoplanet' (line 2) most nearly means", "choices": ["A planet in our own solar system", "A planet orbiting a star other than our Sun", "A failed star", "A moon of Jupiter"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why the 'habitable zone' is also called the 'Goldilocks zone'?", "choices": ["Because it is too hot, too cold, or just right for liquid water", "Because Goldilocks discovered it", "Because it contains porridge", "Because only bears live there"], "correct": 0},
                {"type": "detail", "text": "In what year was the first exoplanet orbiting a sun-like star discovered?", "choices": ["1992", "1995", "2009", "2018"], "correct": 1},
                {"type": "purpose", "text": "Why did the author mention the James Webb Space Telescope?", "choices": ["To show that future telescopes will help search for signs of life on exoplanets", "To argue that current telescopes are useless", "To prove that exoplanets do not exist", "To suggest that telescopes are only for looking at the moon"], "correct": 0}
            ]
        },
        # NEW nf20
        {
            "id": "nf20",
            "title": "The Psychology of Decision-Making",
            "passage": """Every day, humans make thousands of decisions, from trivial choices like what to eat for breakfast to life-altering ones like career changes or medical treatments. For decades, economists assumed that humans were rational actors who made decisions by carefully weighing costs and benefits. However, psychologists Daniel Kahneman and Amos Tversky revolutionized this understanding, showing that human decision-making is systematically flawed in predictable ways. Their work earned Kahneman a Nobel Prize (Tversky had died by then). They identified numerous cognitive biases—mental shortcuts or heuristics that lead to errors. For example, the availability heuristic causes people to overestimate the likelihood of dramatic but rare events (like plane crashes) because they come easily to mind, while underestimating common but mundane risks (like car accidents). The anchoring effect occurs when an irrelevant number influences a judgment; for instance, seeing a high initial price makes subsequent prices seem reasonable even if still expensive. Loss aversion suggests people feel the pain of losing something twice as intensely as the pleasure of gaining the same thing. This explains why people often stick with bad investments or unhappy relationships—they fear loss more than they value potential gain. Framing effects demonstrate that how a choice is presented changes people's answers: a surgery described as '90% survival rate' is chosen more often than the same surgery described as '10% mortality rate,' even though they are identical. Understanding these biases can help people make better decisions by slowing down, seeking diverse perspectives, and questioning initial instincts. Organizations now use this research to design better choice architectures, such as default enrollment in retirement savings plans, which dramatically increases participation without restricting freedom.""",
            "questions": [
                {"type": "main_idea", "text": "What is the main idea of this passage?", "choices": ["Humans make perfect, rational decisions every time", "Psychologists have shown that human decision-making is often biased and flawed in predictable ways, including loss aversion and framing effects", "Only economists should study decision-making", "Decisions have no effect on people's lives"], "correct": 1},
                {"type": "tone", "text": "Which word best describes the author's tone toward cognitive biases?", "choices": ["Dismissive", "Informative and practical", "Celebratory that humans are perfect", "Angry at humans for being biased"], "correct": 1},
                {"type": "vocab", "text": "The word 'heuristics' (line 8) most nearly means", "choices": ["Complex mathematical formulas", "Mental shortcuts or rules of thumb", "Formal logical proofs", "Random guesses"], "correct": 1},
                {"type": "inference", "text": "What can be inferred about why people fear plane crashes more than car accidents despite cars being more dangerous?", "choices": ["Plane crashes are rare and dramatic, making them more memorable (availability heuristic)", "People never drive cars", "Planes are actually safer than the passage suggests", "Car accidents never happen"], "correct": 0},
                {"type": "detail", "text": "According to the passage, loss aversion means people feel loss about how many times more intensely than gain?", "choices": ["Twice as intensely", "Ten times as intensely", "Half as intensely", "Equally intensely"], "correct": 0},
                {"type": "purpose", "text": "Why did the author include the '90% survival rate' vs '10% mortality rate' example?", "choices": ["To prove that doctors are bad at communicating", "To demonstrate framing effects—how presentation changes decisions", "To argue that surgery is always dangerous", "To suggest that survival rates are meaningless"], "correct": 1}
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
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Fast runners always win races", "Slow but steady effort can overcome overconfidence", "Napping is a good way to relax during a race", "Tortoises are actually faster than hares"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the hare's attitude toward the tortoise before the race?", "choices": ["Respectful", "Arrogant", "Afraid", "Jealous"], "correct": 1},
            {"type": "vocab", "text": "The word 'arrogance' (line 2) most nearly means", "choices": ["Kindness", "Fear", "Excessive pride", "Generosity"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about why the hare decided to nap during the race?", "choices": ["He was genuinely tired from running", "He was overconfident and believed he couldn't lose", "He wanted to give the tortoise a fair chance", "He didn't actually want to win the race"], "correct": 1},
            {"type": "detail", "text": "What did the hare do after taking the lead in the race?", "choices": ["Kept running faster", "Asked the tortoise to stop", "Took a nap under a tree", "Turned around and went home"], "correct": 2},
            {"type": "purpose", "text": "What is the author's purpose in writing this fable?", "choices": ["To teach a moral lesson about humility and persistence", "To entertain with a funny story about animals", "To provide information about animal behavior", "To persuade readers to never race a hare"], "correct": 0}
        ]
    },
    # Original f2
    {
        "id": "f2",
        "title": "The Boy Who Cried Wolf",
        "passage": """A young shepherd boy tended his family's sheep near a dark forest. Bored with his work, he decided to play a trick on the villagers. 'Wolf! Wolf!' he shouted. The villagers came running with sticks and axes, only to find no wolf at all. The boy laughed at their worried faces. A few days later, he did it again, and again the villagers rushed to help, only to be fooled once more. Then one evening, a real wolf appeared and began attacking the sheep. The boy cried out desperately, 'Wolf! Wolf! Please help!' But this time, the villagers thought he was lying again. They didn't come, and the wolf ate many sheep.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this story?", "choices": ["Sheep are valuable animals that must be protected", "Lying destroys trust, so people won't believe you even when you tell the truth", "Wolves are dangerous animals that attack sheep", "Villagers are always willing to help even after being tricked"], "correct": 1},
            {"type": "tone", "text": "Which word best describes how the villagers felt after being tricked twice?", "choices": ["Happy", "Amused", "Frustrated", "Excited"], "correct": 2},
            {"type": "vocab", "text": "The word 'desperately' (line 9) most nearly means", "choices": ["Calmly", "Happily", "With great urgency and fear", "Quietly"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about why the villagers didn't come the third time?", "choices": ["They didn't hear the boy shouting", "They assumed the boy was lying again based on his past behavior", "They were too busy with their own work", "They wanted the wolf to eat the sheep"], "correct": 1},
            {"type": "detail", "text": "What happened when the real wolf appeared?", "choices": ["The villagers came and chased the wolf away", "The boy fought the wolf himself and won", "The wolf ate many sheep because no one came to help", "The sheep chased the wolf back into the forest"], "correct": 2},
            {"type": "purpose", "text": "Why did the author write this story?", "choices": ["To teach children why lying is harmful", "To entertain with an exciting wolf chase", "To provide facts about wolf behavior", "To explain how to be a shepherd"], "correct": 0}
        ]
    },
    # Original f3
    {
        "id": "f3",
        "title": "The Lion and the Mouse",
        "passage": """A lion lay sleeping in the forest when a tiny mouse ran across his nose. The lion woke up and caught the mouse under his huge paw. 'Please let me go!' squeaked the mouse. 'If you spare my life, I will repay your kindness someday.' The lion laughed at the idea that a small mouse could ever help him, but he decided to release the mouse anyway. A few days later, the lion became trapped in a hunter's net. He roared in frustration, unable to escape. The mouse heard the lion's roars and rushed to help. The tiny mouse gnawed through the ropes with his sharp teeth until the lion was free. 'You laughed at me once,' said the mouse, 'but now you see that even a small friend can be a great help.'""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Mice are the smartest animals in the forest", "Lions are always kind to smaller animals", "Even small acts of kindness can be repaid in unexpected ways", "Hunters are the real enemies of animals"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the lion's attitude when the mouse first offered to help him?", "choices": ["Grateful", "Amused/Skeptical", "Frightened", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'gnawed' (line 9) most nearly means", "choices": ["Bit or chewed persistently", "Ignored", "Pushed aside", "Measured carefully"], "correct": 0},
            {"type": "inference", "text": "What can be inferred about why the lion decided to release the mouse?", "choices": ["He was afraid of the mouse", "He was moved by the mouse's plea but didn't really believe the mouse could help him", "He wanted to eat the mouse later", "The mouse offered to give him food"], "correct": 1},
            {"type": "detail", "text": "According to the story, how did the mouse help the lion escape?", "choices": ["He distracted the hunter", "He showed the lion a secret path", "He gnawed through the ropes of the net", "He called other animals to help"], "correct": 2},
            {"type": "purpose", "text": "What message is the author trying to convey through this fable?", "choices": ["Never trust a mouse", "Kindness and help can come from unexpected places", "Lions are dangerous predators", "Always hunt with nets"], "correct": 1}
        ]
    },
    # Original f4
    {
        "id": "f4",
        "title": "The Fox and the Grapes",
        "passage": """A hungry fox was walking through a vineyard when he spotted a bunch of ripe, purple grapes hanging from a high vine. His mouth watered at the sight. He wanted those grapes more than anything. The fox jumped and jumped, trying to reach the grapes, but they were too high. Again and again, he leaped into the air, each time falling short. Finally, exhausted and frustrated, the fox stopped trying. As he walked away, he said to himself, 'Those grapes are probably sour anyway. I didn't really want them.' And he continued on his way, pretending not to care about what he could not have.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Grapes are delicious and worth working for", "People sometimes pretend not to want things they cannot have", "Foxes are clever animals", "Vineyards are good places to find food"], "correct": 1},
            {"type": "tone", "text": "Which word best describes how the fox felt when he finally gave up?", "choices": ["Proud", "Relieved", "Frustrated and bitter", "Joyful"], "correct": 2},
            {"type": "vocab", "text": "The word 'vineyard' (line 1) most nearly means", "choices": ["A forest where wild animals live", "A farm where grapes are grown", "A type of fruit", "A trap for catching foxes"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the fox claimed the grapes were sour?", "choices": ["He actually tasted them and they were sour", "He was making an excuse to feel better about his failure", "Someone told him the grapes were sour", "All purple grapes are sour"], "correct": 1},
            {"type": "detail", "text": "What did the fox do when he couldn't reach the grapes?", "choices": ["Asked another animal for help", "Climbed the vine", "Walked away and pretended not to want them", "Waited for the grapes to fall"], "correct": 2},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Being too persistent", "Sharing food with others", "Making excuses when we fail to achieve something", "Eating too many grapes"], "correct": 2}
        ]
    },
    # Original f5
    {
        "id": "f5",
        "title": "The Wind and the Sun",
        "passage": """The North Wind and the Sun argued about which was stronger. They decided to settle their dispute with a challenge. Seeing a traveler walking down the road, they agreed that whoever could make the traveler remove his coat would be declared the winner. The North Wind went first. He blew with all his might, sending powerful gusts that rattled windows and bent trees. But the harder the wind blew, the tighter the traveler wrapped his coat around himself. Finally, the wind gave up. Then the Sun began to shine. He sent gentle, warm rays down upon the traveler. Soon the traveler, feeling the pleasant heat, unbuttoned his coat and then took it off completely. The Sun had won—not with force, but with warmth and gentleness.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Wind is stronger than the sun", "Gentleness and warmth can achieve more than force and aggression", "Travelers should always wear coats", "The sun and wind should not argue"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the North Wind's approach to the challenge?", "choices": ["Gentle", "Patient", "Aggressive", "Sneaky"], "correct": 2},
            {"type": "vocab", "text": "The word 'dispute' (line 1) most nearly means", "choices": ["Conversation", "Argument or disagreement", "Race", "Game"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the traveler held his coat tighter when the wind blew harder?", "choices": ["He was trying to keep warm against the cold wind", "He wanted to win the challenge for the sun", "His coat was stuck", "He was afraid of losing his coat"], "correct": 0},
            {"type": "detail", "text": "What made the traveler remove his coat?", "choices": ["The strong wind", "A sudden rainstorm", "The gentle warmth of the sun", "He reached his destination"], "correct": 2},
            {"type": "purpose", "text": "What lesson is this fable trying to teach?", "choices": ["Kindness and gentleness are more effective than force", "Always wear a coat when it's windy", "The sun is more powerful than the wind", "Never argue with natural forces"], "correct": 0}
        ]
    },
    # NEW f6 - The Ant and the Grasshopper (original version, longer)
    {
        "id": "f6",
        "title": "The Ant and the Grasshopper",
        "passage": """On a bright summer day, a grasshopper hopped through a field, singing and playing his fiddle. He saw an ant carrying a heavy kernel of corn back to his nest. 'Why work so hard on such a beautiful day?' asked the grasshopper. 'Come sing and dance with me instead.' The ant paused and wiped his brow. 'I am storing food for the winter,' he replied. 'When cold weather comes, you will wish you had done the same.' The grasshopper laughed. 'Winter is far away! There is plenty of food everywhere.' All summer, the ant continued gathering grain, while the grasshopper played. When autumn arrived, the ant worked even harder. The grasshopper grew tired of playing and began to feel hungry, but he still did not prepare. Then winter came with bitter winds and snow. The ground froze, and no food could be found. The grasshopper, weak and starving, stumbled to the ant's underground nest. 'Please, friend ant,' he begged, 'give me some food and shelter. I have nothing.' The ant looked at him sadly. 'What were you doing all summer while I labored?' 'I sang and played,' confessed the grasshopper. 'Then,' said the ant, 'since you sang all summer, you may dance all winter.' But the ant was not cruel. He shared his food, and the grasshopper learned an important lesson: there is a time for work and a time for play, but those who refuse to prepare for hard times will suffer.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Singing is more important than working", "Play should be avoided completely", "Preparation and hard work are necessary to survive difficult times", "Ants are selfish creatures"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the grasshopper's attitude in summer?", "choices": ["Worried", "Industrious", "Carefree and foolish", "Angry"], "correct": 2},
            {"type": "vocab", "text": "The word 'kernel' (line 3) most nearly means", "choices": ["A single seed or grain", "A type of insect", "A musical instrument", "A winter storm"], "correct": 0},
            {"type": "inference", "text": "What can be inferred about why the grasshopper eventually begged for food?", "choices": ["He had eaten all his own stores", "He had never gathered any food and winter made it impossible to find any", "The ant stole his food", "He wanted to test the ant's generosity"], "correct": 1},
            {"type": "detail", "text": "What was the grasshopper doing while the ant worked?", "choices": ["Sleeping", "Singing and playing his fiddle", "Building a nest", "Looking for food"], "correct": 1},
            {"type": "purpose", "text": "Why did the author include the ant's final speech about dancing all winter?", "choices": ["To show that the ant was cruel and refused to help", "To emphasize the consequence of foolish choices before offering mercy", "To prove that ants hate music", "To make the grasshopper leave"], "correct": 1}
        ]
    },
    # NEW f7 - The City Mouse and the Country Mouse
    {
        "id": "f7",
        "title": "The City Mouse and the Country Mouse",
        "passage": """A country mouse lived in a simple hole beneath a farmer's barn. He ate plain wheat and corn, drank water from a puddle, and lived quietly. One day, his cousin from the city came to visit. The city mouse looked around the barn with disdain. 'How can you live like this?' he said. 'In the city, I dine on fine cheeses, meats, and pastries. You must come stay with me.' The country mouse agreed. That night, they arrived at a grand house in the city. The city mouse led his cousin to the dining room, where leftover food from a banquet sat on the table. 'See?' said the city mouse. 'Eat anything you like.' The country mouse had never seen such food. He nibbled a piece of cheese, then a bit of cake. But just as he began to enjoy himself, the kitchen door burst open. A huge cat leaped onto the table, growling. The mice ran for their lives, hiding behind a heavy cabinet. Then a cook entered with a broom, swinging wildly. 'This happens often,' whispered the city mouse, shaking. The country mouse grabbed his cousin's paw. 'Thank you for your kindness,' he said, 'but I would rather eat plain corn in safety than fine food in fear. I am going home tonight.' And he returned to his quiet barn, where no cats or brooms could find him.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this story?", "choices": ["City life is always better than country life", "Country life is always better than city life", "Different creatures value different things—safety over luxury, or adventure over peace", "Cats are the greatest danger to mice"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the city mouse's attitude at the beginning?", "choices": ["Humble", "Proud and dismissive of simple living", "Frightened", "Grateful"], "correct": 1},
            {"type": "vocab", "text": "The word 'disdain' (line 4) most nearly means", "choices": ["Excitement", "A feeling that something is unworthy or beneath one", "Curiosity", "Fear"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the country mouse chose to return home?", "choices": ["He hated the taste of cheese", "He valued safety and peace more than luxury and excitement", "The city mouse kicked him out", "He got lost on the way to the city"], "correct": 1},
            {"type": "detail", "text": "What danger did the mice face in the city house?", "choices": ["A snake", "A cat and a cook with a broom", "Poisoned food", "Another mouse"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Never visit relatives", "The best life depends on what you value most (peace vs. excitement)", "All mice should live in the country", "City food is always rotten"], "correct": 1}
        ]
    },
    # NEW f8 - The Oak and the Reed
    {
        "id": "f8",
        "title": "The Oak and the Reed",
        "passage": """A mighty oak tree stood at the edge of a river. Beside it grew a slender reed that bent in every breeze. The oak often mocked the reed. 'How weak you are,' boomed the oak. 'A gentle wind makes you bow and tremble. Look at me: I stand firm against any storm. No wind can move me.' The reed replied softly, 'You are strong indeed, but do not mock what you do not understand. I bend so that I do not break.' The oak laughed. One autumn night, a terrible hurricane swept across the land. The wind howled and screamed, tearing at everything in its path. The oak planted its roots deep and refused to yield. The harder the wind blew, the more the oak resisted. But the wind grew stronger and stronger, until with a tremendous crack, the oak was ripped from the ground. Its great roots tore free, and the oak crashed into the river. The reed, meanwhile, bent low—almost to the water—and let the storm pass over it. When dawn came, the reed stood up again, unharmed. And it whispered to the fallen oak, 'There is more than one kind of strength. Sometimes, flexibility is the greatest strength of all.'""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["Oak trees are the strongest plants in the forest", "Flexibility and the ability to adapt can be greater strengths than rigid resistance", "Reeds are useless plants", "Hurricanes only happen in autumn"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the oak's attitude toward the reed?", "choices": ["Respectful", "Humble", "Mocking and arrogant", "Frightened"], "correct": 2},
            {"type": "vocab", "text": "The word 'yield' (line 10) most nearly means", "choices": ["Grow taller", "Give way or surrender", "Attack", "Break apart"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the reed survived the hurricane?", "choices": ["It was hidden behind the oak", "It bent instead of resisting the wind", "It had deeper roots than the oak", "The wind did not blow near the river"], "correct": 1},
            {"type": "detail", "text": "What happened to the oak at the end of the story?", "choices": ["It was uprooted and fell into the river", "It remained standing", "It became a reed", "It apologized to the reed"], "correct": 0},
            {"type": "purpose", "text": "Why did the author write this fable?", "choices": ["To teach that pride and rigidity can lead to downfall, while flexibility brings survival", "To provide information about tree species", "To encourage readers to plant oaks", "To describe hurricane patterns"], "correct": 0}
        ]
    },
    # NEW f9 - The Crow and the Pitcher (Aesop)
    {
        "id": "f9",
        "title": "The Crow and the Pitcher",
        "passage": """A thirsty crow searched for water on a hot, dry day. She had flown for miles without finding a single drop. Finally, she spotted a pitcher in a farmer's yard. She flew to it eagerly, hoping for a drink. But when she looked inside, she saw that the water was very low—too low for her beak to reach. She tried tipping the pitcher over, but it was too heavy. She tried pushing her head in farther, but her beak still could not touch the water. The crow was about to give up when she had an idea. Around the yard lay many small pebbles. The crow picked up one pebble in her beak and dropped it into the pitcher. The water rose slightly. She dropped another pebble, and the water rose a little more. Pebble by pebble, the crow continued. The water crept higher and higher until, at last, it reached the brim. The crow drank deeply and flew away satisfied. The moral is that necessity is the mother of invention—and that patience and cleverness can solve problems that strength cannot.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Crows are the smartest birds", "Thirst can be cured by finding a river", "Creative problem-solving and patience can overcome obstacles", "Pitchers are bad containers for water"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the crow's approach to the problem?", "choices": ["Panicked", "Violent", "Clever and persistent", "Lazy"], "correct": 2},
            {"type": "vocab", "text": "The word 'pitcher' (line 3) most nearly means", "choices": ["A type of bird", "A container for liquids", "A baseball player", "A dry well"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why dropping pebbles raised the water level?", "choices": ["The pebbles pushed the water upward by taking up space in the pitcher", "The pebbles melted into water", "The pebbles scared the water upward", "The pitcher shrank"], "correct": 0},
            {"type": "detail", "text": "Why couldn't the crow drink at first?", "choices": ["The water was frozen", "The water was too low for her beak to reach", "Someone had poisoned the water", "She was not actually thirsty"], "correct": 1},
            {"type": "purpose", "text": "What does the phrase 'necessity is the mother of invention' mean in this context?", "choices": ["Inventions require mothers", "Difficult needs inspire creative solutions", "Crows are better than humans", "Water is unnecessary"], "correct": 1}
        ]
    },
    # NEW f10 - The Bundle of Sticks
    {
        "id": "f10",
        "title": "The Bundle of Sticks",
        "passage": """An old farmer had several sons who constantly argued and fought with one another. No matter what their father said, they would not stop quarreling. One day, the farmer called all his sons together. He handed each son a single stick. 'Break it,' he said. Each son easily snapped his stick in two. Then the farmer took a bundle of many sticks tied tightly together. 'Now break this,' he said. The oldest son tried first. He strained and twisted, but the bundle would not break. One by one, the other sons tried. Not one of them could break the bundle. The farmer untied the sticks and let them fall to the ground. 'My sons,' he said, 'you see that alone, you are weak and easily broken. But if you stand together and support one another, no enemy can break you. Your arguments weaken you. Your unity will make you strong.' The sons understood at last. From that day forward, they worked together, and their farm prospered as never before.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this story?", "choices": ["Sticks are stronger than rope", "Old farmers know everything", "Unity and cooperation make people stronger than division and conflict", "Sons should never argue with their fathers"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the farmer's teaching method?", "choices": ["Cruel", "Wise and patient", "Rushed", "Confusing"], "correct": 1},
            {"type": "vocab", "text": "The word 'prospered' (line 16) most nearly means", "choices": ["Failed", "Became wealthy and successful", "Stayed the same", "Was destroyed"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the sons could break single sticks but not the bundle?", "choices": ["The bundle was made of different wood", "Together, the sticks supported each other, distributing the force", "The farmer secretly glued the bundle", "The sons became tired"], "correct": 1},
            {"type": "detail", "text": "What did the farmer give each son first?", "choices": ["A bundle of sticks", "A single stick", "A rope", "A field to farm"], "correct": 1},
            {"type": "purpose", "text": "Why did the author write this fable?", "choices": ["To explain how to farm", "To teach the value of unity and teamwork", "To criticize sons who argue", "To describe different types of wood"], "correct": 1}
        ]
    },
    # NEW f11 - The Milkmaid and Her Pail
    {
        "id": "f11",
        "title": "The Milkmaid and Her Pail",
        "passage": """A milkmaid named Patty carried a pail of milk on her head, walking to the market to sell it. As she walked, she began to daydream. 'With the money from this milk,' she thought, 'I will buy a hundred eggs. Those eggs will hatch into chickens. The chickens will grow fat and lay more eggs. I will sell the eggs and buy a new dress—a beautiful blue one with lace. When I wear that dress to the fair, all the young men will admire me. They will ask me to dance. But I will toss my head and refuse them all.' At that moment, Patty tossed her head—just as she had imagined. The pail of milk fell from her head, crashed to the ground, and spilled everywhere. All the milk was lost. Patty sat down and wept. 'Do not count your chickens before they are hatched,' an old woman told her. Patty had planned for a future that never came, and she had nothing left but tears.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Milk is valuable", "It is foolish to count on future rewards before securing the present", "Dancing at fairs is dangerous", "Old women are wise"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the milkmaid's daydreaming?", "choices": ["Practical", "Overconfident and premature", "Frightening", "Generous"], "correct": 1},
            {"type": "vocab", "text": "The phrase 'Do not count your chickens before they are hatched' most nearly means", "choices": ["Counting eggs is difficult", "Do not assume future success before it actually happens", "Chickens are unreliable", "Only farmers should count chickens"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the milk spilled?", "choices": ["Someone pushed Patty", "Patty tossed her head while daydreaming, forgetting she was carrying milk", "The pail had a hole", "A chicken stole it"], "correct": 1},
            {"type": "detail", "text": "What was Patty planning to buy with her imagined egg money?", "choices": ["A new cow", "A blue dress with lace", "More milk", "A house"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable warning against?", "choices": ["Working too hard", "Planning for the future", "Assuming future success before taking care of present responsibilities", "Selling milk"], "correct": 2}
        ]
    },
    # NEW f12 - The Goose That Laid the Golden Eggs
    {
        "id": "f12",
        "title": "The Goose That Laid the Golden Eggs",
        "passage": """A poor farmer and his wife owned a remarkable goose. Every morning, the goose laid a single egg made of solid gold. The farmer would sell the golden egg at the market and live comfortably. But soon, the farmer grew greedy. 'This goose lays only one egg per day,' he complained. 'If I cut her open, I will find all the gold inside her at once. Then I will be rich immediately!' His wife warned him, 'Do not destroy the goose that feeds you.' But the farmer would not listen. One morning, he took a knife and killed the goose. When he cut her open, he found no gold inside at all—only ordinary goose organs. He had killed the goose, and now there would be no more golden eggs. The farmer wept, but it was too late. He had traded steady, patient wealth for a single moment of greedy foolishness.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Geese are valuable animals", "Greed can destroy a good thing; patience is better than rushing for more", "Farmers should never own geese", "Gold is worthless"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the farmer's decision to kill the goose?", "choices": ["Wise", "Patient", "Greedy and foolish", "Generous"], "correct": 2},
            {"type": "vocab", "text": "The word 'remarkable' (line 1) most nearly means", "choices": ["Ordinary", "Extraordinary or unusual", "Ugly", "Slow"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the farmer killed the goose?", "choices": ["He wanted to eat it", "He believed all the gold was inside and wanted it all at once", "The goose stopped laying eggs", "His wife told him to"], "correct": 1},
            {"type": "detail", "text": "What did the farmer find inside the goose after killing it?", "choices": ["Many golden eggs", "Ordinary goose organs", "A treasure chest", "Nothing at all"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Never trust a goose", "Greed and impatience can destroy a reliable source of wealth", "Always listen to your wife", "Gold eggs are better than regular eggs"], "correct": 1}
        ]
    },
    # NEW f13 - The Dog and His Reflection
    {
        "id": "f13",
        "title": "The Dog and His Reflection",
        "passage": """A dog had stolen a large, juicy piece of meat from a butcher's shop. He held it firmly in his mouth and ran to a quiet stream to eat it alone. As he crossed a wooden bridge over the water, he looked down and saw his own reflection. But the dog did not know it was himself. He saw another dog with another piece of meat—and that piece looked twice as large as his own. 'I want that meat too!' thought the greedy dog. He opened his mouth to snatch the other dog's meat. But when he opened his mouth, his own piece of meat fell from his jaws, splashed into the water, and disappeared. The reflection vanished as well. The dog stood on the bridge, hungry and ashamed, with nothing left at all. He had lost everything because he wanted more than he already had.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Dogs cannot swim", "Greed and envy can cause you to lose what you already have", "Reflections are dangerous", "Butchers should guard their meat better"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the dog's mistake?", "choices": ["Generous", "Cautious", "Foolish and greedy", "Helpful"], "correct": 2},
            {"type": "vocab", "text": "The word 'reflection' (line 4) most nearly means", "choices": ["A loud noise", "An image seen in a mirror or water", "A type of dog breed", "A piece of meat"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the dog thought there was another dog in the water?", "choices": ["He had never seen his own reflection before", "Another dog was actually there", "He was dreaming", "The water was magical"], "correct": 0},
            {"type": "detail", "text": "What happened when the dog opened his mouth?", "choices": ["He bit the other dog", "His own meat fell into the water", "The other dog gave him meat", "He swallowed both pieces"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Sharing food", "Being content with what you have", "Being greedy and wanting more than you need", "Crossing bridges"], "correct": 2}
        ]
    },
    # NEW f14 - The North Wind and the Sun (different version - longer original tale)
    {
        "id": "f14",
        "title": "The North Wind and the Sun (Extended)",
        "passage": """One day, the North Wind and the Sun argued about who was the strongest among all the forces of nature. The North Wind boasted of his power to uproot trees and drive ships onto rocks. The Sun spoke calmly of his ability to warm the earth and make flowers bloom. Neither would yield. Finally, they saw a traveler walking along a winding road, wearing a heavy woolen cloak. 'Whoever can make that traveler remove his cloak is the stronger,' said the Sun. The North Wind agreed eagerly. He went first. The North Wind blew with all his fury. He sent icy blasts that rattled shutters and bent the trees nearly to the ground. Snow flew sideways, and the air turned bitter cold. But the traveler, instead of removing his cloak, wrapped it tighter around himself and buttoned it to his chin. The harder the wind blew, the tighter the traveler held his cloak. Exhausted, the North Wind gave up. Then the Sun began. He sent gentle, warm rays down upon the traveler. The traveler relaxed his grip. The Sun shone brighter, and the traveler unbuttoned his cloak. The Sun shone warmer still, and the traveler removed his cloak entirely, draping it over his arm. The Sun had won—not with violence, but with patience and kindness. And that is how the Sun proved that gentleness is stronger than fury.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main theme of this fable?", "choices": ["The North Wind is the strongest", "Gentleness and warmth can achieve what force and aggression cannot", "Travelers should always wear cloaks", "The Sun is hot because it is angry"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the North Wind's approach?", "choices": ["Gentle", "Patient", "Aggressive", "Sneaky"], "correct": 2},
            {"type": "vocab", "text": "The word 'fury' (line 8) most nearly means", "choices": ["Joy", "Gentle breeze", "Violent anger or force", "Confusion"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about why the traveler held his cloak tighter when the wind blew?", "choices": ["He was trying to stay warm against the cold wind", "He wanted to win the challenge for the Sun", "His cloak was stuck", "He was afraid of losing his cloak"], "correct": 0},
            {"type": "detail", "text": "What made the traveler remove his cloak?", "choices": ["The strong wind", "A sudden rainstorm", "The gentle warmth of the Sun", "He reached his destination"], "correct": 2},
            {"type": "purpose", "text": "What lesson is this fable trying to teach?", "choices": ["Kindness and gentleness are more effective than force", "Always wear a coat when it's windy", "The Sun is more powerful than the Wind", "Never argue with natural forces"], "correct": 0}
        ]
    },
    # NEW f15 - The Fox and the Stork (original longer)
    {
        "id": "f15",
        "title": "The Fox and the Stork",
        "passage": """A fox invited a stork to dinner, intending to play a mean trick. The fox served soup in a very shallow dish. The fox lapped up his soup easily with his tongue. But the stork, with her long, slender beak, could not get a single drop. She only wet the tip of her beak. 'I am sorry you do not like my soup,' said the fox, smiling. The stork said nothing, but she remembered. A few days later, the stork invited the fox to dinner. She served food in a tall, narrow jar with a long, thin neck. The stork slipped her long beak into the jar and ate her fill easily. But the fox could not fit his nose into the narrow opening. He sniffed the delicious smells but could not reach the food. He went home hungry. As he left, the stork said, 'Do not give what you cannot take yourself.' The fox learned that tricks can backfire, and that those who are unkind to others may find themselves treated the same way.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Foxes are always hungry", "Storks have better manners than foxes", "Treat others as you wish to be treated; cruel tricks often backfire", "Soup is best served in shallow dishes"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the fox's first dinner invitation?", "choices": ["Genuinely kind", "Deceitful and mean-spirited", "Accidental", "Generous"], "correct": 1},
            {"type": "vocab", "text": "The word 'backfire' (line 15) most nearly means", "choices": ["To explode", "To have the opposite effect of what was intended", "To succeed perfectly", "To be forgotten"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the stork chose a tall narrow jar?", "choices": ["It was the only dish she owned", "She deliberately chose a container that would be easy for her but hard for the fox", "She did not know the fox would come", "The jar was an accident"], "correct": 1},
            {"type": "detail", "text": "Why couldn't the stork eat from the shallow dish?", "choices": ["She was not hungry", "The soup was poisoned", "Her beak was too long to reach the shallow soup", "The fox ate all the soup first"], "correct": 2},
            {"type": "purpose", "text": "What lesson does this fable teach?", "choices": ["Never accept dinner invitations", "Do not play tricks on others if you cannot handle the same treatment", "Storks are better cooks than foxes", "Soup is bad for foxes"], "correct": 1}
        ]
    },
    # NEW f16 - The Donkey in Lion's Skin
    {
        "id": "f16",
        "title": "The Donkey in Lion's Skin",
        "passage": """A donkey found a lion's skin left behind by a hunter. The donkey draped the skin over his body and admired himself in a pond. 'Now I look like the king of beasts,' he thought. 'No one will dare touch me.' The donkey walked through the forest wearing the lion's skin. All the animals—rabbits, deer, and even wolves—ran away in terror. The donkey laughed to himself, feeling very clever. He decided to visit a nearby farm. The farmer's sheep scattered when they saw the lion approaching. But just as the donkey was about to enjoy his victory, he opened his mouth and let out a loud, unmistakable 'Hee-Haw!' The farmer heard the bray. 'A donkey in a lion's skin!' he shouted. The farmer ran after the donkey with a stick and chased him out of the farm. The moral of the story is that fine clothes may disguise someone for a while, but a fool will eventually reveal himself by his words or actions.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Donkeys are stronger than lions", "Pretending to be something you are not will eventually be exposed", "Lions should protect their skins", "Farmers are afraid of donkeys"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the donkey's self-image?", "choices": ["Humble", "Delusional and overconfident", "Frightened", "Generous"], "correct": 1},
            {"type": "vocab", "text": "The word 'bray' (line 10) most nearly means", "choices": ["The sound a donkey makes", "A type of lion roar", "A farmer's shout", "The rustling of leaves"], "correct": 0},
            {"type": "inference", "text": "What can be inferred about why the donkey was exposed?", "choices": ["The lion's skin fell off", "His donkey sound (braying) gave him away", "The farmer already knew the donkey", "Other animals told the farmer"], "correct": 1},
            {"type": "detail", "text": "What did the donkey find in the forest?", "choices": ["A lion", "A lion's skin", "A hunter", "A pond"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Pretending to be something you are not", "Helping others", "Wearing animal skins", "Walking in forests"], "correct": 0}
        ]
    },
    # NEW f17 - The Two Travelers and the Bear
    {
        "id": "f17",
        "title": "The Two Travelers and the Bear",
        "passage": """Two men were walking through a forest when suddenly a large bear appeared on the path ahead. One man immediately climbed a tall tree and hid among the branches. The other man knew he could not outrun the bear. He fell to the ground and lay perfectly still, holding his breath. The bear approached the man on the ground. It sniffed his ear, then his nose. The man did not move a muscle. Bears are known to avoid touching dead things. After a few minutes, the bear decided the man was dead and wandered away. When the bear was gone, the first man climbed down from the tree. 'What did the bear whisper in your ear?' he asked with a nervous laugh. The second man stood up and brushed off his clothes. 'He told me,' he said, 'never travel with a friend who abandons you in danger.' And he walked away alone, leaving the first man ashamed.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Bears are dangerous", "Always climb a tree when you see a bear", "A true friend does not abandon you in times of danger", "Playing dead is the best defense against bears"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the first traveler's actions?", "choices": ["Brave", "Selfish and cowardly", "Helpful", "Generous"], "correct": 1},
            {"type": "vocab", "text": "The word 'abandons' (line 14) most nearly means", "choices": ["Helps", "Leaves behind in a time of need", "Celebrates", "Follows closely"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the bear did not attack the man on the ground?", "choices": ["The bear was not hungry", "The bear thought the man was dead", "The first man scared the bear away", "The second man was a bear trainer"], "correct": 1},
            {"type": "detail", "text": "What did the first traveler do when he saw the bear?", "choices": ["Played dead", "Climbed a tree", "Fought the bear", "Ran away screaming"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach about friendship?", "choices": ["All friends are unreliable", "A friend who saves only himself is no true friend", "Bears make better friends than humans", "Never travel in forests"], "correct": 1}
        ]
    },
    # NEW f18 - The Farmer and the Snake
    {
        "id": "f18",
        "title": "The Farmer and the Snake",
        "passage": """On a freezing winter morning, a farmer found a snake lying stiff and frozen by the side of the road. The snake was nearly dead from the cold. 'Please, kind farmer,' the snake whispered weakly, 'take me inside and warm me by your fire. I will not hurt you.' The farmer hesitated. He knew snakes could be dangerous. But his heart softened, and he picked up the snake and carried it home. He placed the snake near the hearth. The warmth slowly revived the snake. Its muscles loosened, and its eyes grew bright. The farmer's young son came close to see the snake. As soon as the snake had fully warmed, it reared up and bit the farmer's hand. 'But I saved your life!' cried the farmer, falling to his knees. 'Why did you bite me?' The snake hissed, 'You knew what I was when you picked me up.' And the farmer died. The moral is that kindness to evil does not change its nature.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Snakes are always helpful", "Never help anyone in need", "Kindness will always be repaid with kindness", "Some creatures have unchanging dangerous natures; helping them may bring harm"], "correct": 3},
            {"type": "tone", "text": "Which word best describes the farmer's initial decision?", "choices": ["Wise", "Naively kind but ultimately tragic", "Cruel", "Selfish"], "correct": 1},
            {"type": "vocab", "text": "The word 'revived' (line 8) most nearly means", "choices": ["Killed", "Brought back to life or consciousness", "Froze", "Ignored"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the snake bit the farmer?", "choices": ["It was grateful", "It acted according to its nature despite the farmer's kindness", "The farmer stepped on it", "The snake was playing"], "correct": 1},
            {"type": "detail", "text": "What happened to the farmer at the end?", "choices": ["He killed the snake", "He recovered from the bite", "He died from the snake's bite", "He became friends with the snake"], "correct": 2},
            {"type": "purpose", "text": "What warning does this fable give?", "choices": ["Never go outside in winter", "Be cautious about showing kindness to those known to be dangerous", "All farmers should carry anti-venom", "Snakes are good pets"], "correct": 1}
        ]
    },
    # NEW f19 - The Peacock and the Crane
    {
        "id": "f19",
        "title": "The Peacock and the Crane",
        "passage": """A peacock spread his magnificent tail feathers in the sun. The iridescent blues and greens shimmered like jewels. A plain gray crane walked by, searching for food in the mud. The peacock laughed. 'Look at you,' he said. 'Your feathers are dull as dust. No one ever admires you. See how everyone stops to look at my beauty.' The crane stopped and looked at the peacock calmly. 'You are beautiful indeed,' said the crane. 'But while you strut on the ground showing off your tail, I can soar among the clouds. When danger comes, your fine feathers will not save you. But I can fly away to safety. Beauty is not the only measure of worth.' Just then, a fox appeared in the clearing. The peacock screamed and ran awkwardly, his long tail feathers slowing him down. The crane spread his broad gray wings and rose gracefully into the sky. The fox caught the peacock easily. And the crane flew on, free and alive.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Peacocks are the most beautiful birds", "Beauty is the only thing that matters", "Vanity about appearance is foolish when others have more practical abilities like flight or freedom", "Cranes are jealous of peacocks"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the peacock's attitude toward the crane?", "choices": ["Humble", "Admiring", "Arrogant and mocking", "Frightened"], "correct": 2},
            {"type": "vocab", "text": "The word 'iridescent' (line 2) most nearly means", "choices": ["Dull and gray", "Shimmering with changing colors", "Invisible", "Heavy"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the crane survived while the peacock did not?", "choices": ["The crane could fly away from danger; the peacock's beauty slowed him down", "The crane was stronger", "The peacock was old", "The fox preferred peacock meat"], "correct": 0},
            {"type": "detail", "text": "What happened when the fox appeared?", "choices": ["Both birds flew away", "The peacock was caught; the crane flew to safety", "The crane was caught", "The fox admired the peacock's feathers"], "correct": 1},
            {"type": "purpose", "text": "What behavior is this fable criticizing?", "choices": ["Flying", "Being humble", "Vanity and mocking others for their plainness while ignoring one's own weaknesses", "Eating"], "correct": 2}
        ]
    },
    # NEW f20 - The Old Lion and the Fox
    {
        "id": "f20",
        "title": "The Old Lion and the Fox",
        "passage": """A lion too old and weak to hunt anymore lay in his cave, pretending to be ill. When other animals came to visit the 'sick' king, the lion would pounce and eat them. Many animals—a sheep, a goat, a young deer—entered the cave and never came out. One day, a clever fox approached the cave. He stood outside the entrance and called in, 'How are you feeling today, Your Majesty?' The lion put on his most pitiful voice. 'Oh, I am so weak, dear friend. Please come in and keep me company.' The fox did not move. 'I would love to,' said the fox, 'but I notice that many footprints lead into your cave—but no footprints lead out.' The fox turned and walked away, leaving the hungry lion alone. The lion learned that cleverness can defeat brute strength, and that noticing details others ignore can save your life.""",
        "questions": [
            {"type": "main_idea", "text": "What is the main message of this fable?", "choices": ["Lions are always dangerous", "It is rude to refuse a king's invitation", "Observation and intelligence can protect you from danger", "Old lions should be pitied"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the fox's behavior?", "choices": ["Foolish", "Gullible", "Cautious and clever", "Rude"], "correct": 2},
            {"type": "vocab", "text": "The word 'pounce' (line 3) most nearly means", "choices": ["Welcome warmly", "Spring or swoop suddenly to attack", "Run away", "Fall asleep"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the fox did not enter the cave?", "choices": ["He was not curious", "He noticed that animals went in but never came out, so he suspected a trap", "He was afraid of the dark", "He had met the lion before"], "correct": 1},
            {"type": "detail", "text": "What did the fox notice at the cave entrance?", "choices": ["The lion was sleeping", "Footprints leading in but none leading out", "A hidden escape route", "The cave was empty"], "correct": 1},
            {"type": "purpose", "text": "What lesson does this fable teach about safety?", "choices": ["Never visit sick animals", "Always trust what you are told", "Pay attention to evidence and patterns (like missing footprints) to avoid danger", "Lions make good kings"], "correct": 2}
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker regrets not taking a different path in life", "Life presents choices, and the paths we choose shape who we become", "Taking the easier path is always better", "All roads in the woods look exactly the same"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood of this poem?", "choices": ["Joyful and excited", "Angry and bitter", "Thoughtful and reflective", "Confused and lost"], "correct": 2},
            {"type": "vocab", "text": "The word 'diverged' (line 1) most nearly means", "choices": ["Came together", "Split or went in different directions", "Disappeared", "Became muddy"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the speaker says he will tell this story 'with a sigh' (line 11)?", "choices": ["He will be sad and nostalgic about the choice he made", "He will be out of breath", "He will be angry at himself", "He won't remember what happened"], "correct": 0},
            {"type": "detail", "text": "According to the poem, which road did the speaker ultimately take?", "choices": ["The first road he looked down", "The road that was more worn", "The road less traveled by", "Neither road—he stayed where he was"], "correct": 2},
            {"type": "purpose", "text": "What is the poet's likely purpose in writing this poem?", "choices": ["To give hiking directions", "To explore how choices in life affect our identities and futures", "To complain about having too many options", "To describe a forest in autumn"], "correct": 1}
        ]
    },
    # Original p2
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The ocean is dangerous for birds", "Eagles are afraid of heights", "The poem describes an eagle's power, majesty, and sudden dive from high cliffs", "Mountain walls protect eagles from predators"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the tone of this poem?", "choices": ["Humorous", "Powerful and majestic", "Sad and mournful", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'azure' (line 3) most nearly means", "choices": ["Red", "Green", "Sky blue", "Dark black"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about the eagle's speed when it falls 'like a thunderbolt'?", "choices": ["The eagle falls very slowly", "The eagle falls extremely fast with great force", "The eagle creates lightning when it falls", "The eagle is afraid of thunder"], "correct": 1},
            {"type": "detail", "text": "According to the poem, what is the eagle doing at the beginning of the poem?", "choices": ["Flying over the ocean", "Perched on a mountain cliff", "Building a nest", "Fighting with another eagle"], "correct": 1},
            {"type": "purpose", "text": "Why does the poet compare the eagle's fall to a 'thunderbolt'?", "choices": ["To emphasize the eagle's speed and power", "To suggest the eagle is afraid", "To indicate bad weather is coming", "To show the eagle is weak"], "correct": 0}
        ]
    },
    # Original p3
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Fog is dangerous for ships in harbors", "The poet compares fog to a cat moving silently and gracefully through a city", "Cats are the only animals that like fog", "Fog never moves once it arrives"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood of this poem?", "choices": ["Loud and chaotic", "Quiet, calm, and observant", "Angry and aggressive", "Fast and energetic"], "correct": 1},
            {"type": "vocab", "text": "The word 'haunches' (line 5) most nearly means", "choices": ["Eyes", "Paws", "Hind legs and rear body", "Whiskers"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about how the poet views fog?", "choices": ["He sees fog as a violent storm", "He sees fog as a gentle, quiet visitor", "He thinks fog is dangerous", "He wishes fog would stay longer"], "correct": 1},
            {"type": "detail", "text": "According to the poem, what does the fog do 'on little cat feet'?", "choices": ["Runs away quickly", "Comes into the city", "Makes loud noises", "Disappears instantly"], "correct": 1},
            {"type": "purpose", "text": "Why does the poet compare fog to a cat?", "choices": ["To suggest fog is scary", "To show that fog moves silently and sits quietly before leaving", "To prove that fog is an animal", "To describe what cats look like in fog"], "correct": 1}
        ]
    },
    # Original p4
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Birds are the best pets because they sing beautiful songs", "Hope is like a bird that lives in the soul and never stops singing, even during hard times", "Storms are dangerous to small birds", "The speaker has never needed hope"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone of this poem?", "choices": ["Desperate", "Hopeful and comforting", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'abash' (line 7) most nearly means", "choices": ["Encourage", "Embarrass or dishearten", "Celebrate", "Feed"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the speaker's view of hope?", "choices": ["The speaker thinks hope is a waste of time", "The speaker believes hope is always present and asks for nothing in return", "The speaker has never felt hope", "The speaker thinks hope only exists in good times"], "correct": 1},
            {"type": "detail", "text": "According to the poem, where does hope perch?", "choices": ["In a tree", "In the soul", "On the sea", "In a cage"], "correct": 1},
            {"type": "purpose", "text": "What is Dickinson's primary purpose in this poem?", "choices": ["To describe different types of birds", "To explain that hope is a valuable and enduring presence in human life", "To complain about difficult times", "To persuade readers to buy a pet bird"], "correct": 1}
        ]
    },
    # Original p5
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Apples are the most dangerous fruit in the garden", "Bottling up anger instead of expressing it can cause it to grow into something destructive", "Friends should always agree with each other", "Gardening is a good way to deal with anger"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone of this poem?", "choices": ["Joyful and carefree", "Dark, vengeful, and warning", "Confused and lost", "Romantic and loving"], "correct": 1},
            {"type": "vocab", "text": "The word 'wrath' (line 2) most nearly means", "choices": ["Joy", "Extreme anger", "Confusion", "Fear"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about what happened to the speaker's foe at the end of the poem?", "choices": ["He ate the poisoned apple and died", "He became friends with the speaker", "He ran away from the garden", "He apologized for his actions"], "correct": 0},
            {"type": "detail", "text": "According to the poem, what happened when the speaker told his friend about his anger?", "choices": ["They got into a fight", "The anger ended", "The friend got more angry", "The speaker's anger grew"], "correct": 1},
            {"type": "purpose", "text": "What is Blake's purpose in writing this poem?", "choices": ["To teach a gardening technique", "To warn readers that unexpressed anger can become dangerous", "To describe a beautiful garden", "To encourage people to grow apple trees"], "correct": 1}
        ]
    },
    # NEW p6 - "The Tyger" by William Blake (full)
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Tigers are the most dangerous animals in the forest", "The poet marvels at the terrifying beauty of the tiger and questions what kind of creator could make such a creature", "Tigers should be protected from hunters", "The tiger is afraid of the lamb"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone of this poem?", "choices": ["Humorous", "Awed, fearful, and wondering", "Bored", "Angry"], "correct": 1},
            {"type": "vocab", "text": "The word 'symmetry' (line 4) most nearly means", "choices": ["Color", "Balanced and harmonious proportions", "Speed", "Loudness"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the speaker's view of the tiger's creator?", "choices": ["The speaker is certain the creator is gentle", "The speaker is awed and slightly frightened, wondering if the same creator made both the gentle lamb and the dangerous tiger", "The speaker believes the tiger created itself", "The speaker has never seen a tiger"], "correct": 1},
            {"type": "detail", "text": "According to the poem, what other animal does the speaker mention?", "choices": ["The lion", "The lamb", "The eagle", "The snake"], "correct": 1},
            {"type": "purpose", "text": "Why does the speaker repeat the first stanza at the end?", "choices": ["He forgot he already wrote it", "To emphasize the central question about the tiger's creator and create a circular structure", "To fill space", "To change the subject"], "correct": 1}
        ]
    },
    # NEW p7 - "I Wandered Lonely as a Cloud" by William Wordsworth
    {
        "id": "p7",
        "title": "I Wandered Lonely as a Cloud (Daffodils)",
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker describes seeing daffodils and later finds that the memory brings him joy during lonely moments", "Clouds are lonely", "Daffodils are the prettiest flowers", "The speaker prefers sitting on his couch to walking outdoors"], "correct": 0},
            {"type": "tone", "text": "Which word best describes the mood of this poem?", "choices": ["Angry", "Joyful and reflective", "Frightened", "Bored"], "correct": 1},
            {"type": "vocab", "text": "The word 'jocund' (line 16) most nearly means", "choices": ["Sad", "Cheerful and merry", "Silent", "Angry"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the 'inward eye' mentioned in line 23?", "choices": ["The speaker has a physical eye inside his head", "The speaker's memory and imagination", "A telescope", "A window"], "correct": 1},
            {"type": "detail", "text": "Where does the speaker see the daffodils?", "choices": ["In a garden", "Beside a lake, beneath trees", "On a mountain", "In a dream"], "correct": 1},
            {"type": "purpose", "text": "Why does the poet include the final stanza about being on his couch?", "choices": ["To show that the memory of nature brings lasting happiness even when alone", "To complain about being tired", "To prove that couches are better than walks", "To change the subject completely"], "correct": 0}
        ]
    },
    # NEW p8 - "If" by Rudyard Kipling (excerpt)
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Winning is the most important thing in life", "The poem describes the qualities of a mature, virtuous person: patience, self-trust, resilience, and humility", "Dreams should be avoided", "Only fathers can give advice"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Sarcastic", "Wise, earnest, and encouraging", "Angry", "Childish"], "correct": 1},
            {"type": "vocab", "text": "The word 'impostors' (line 12) most nearly means", "choices": ["Kings", "Fakes or deceivers", "Friends", "Children"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about how the speaker views Triumph and Disaster?", "choices": ["They are equally temporary and should not define a person", "Triumph is always better", "Disaster should be avoided at all costs", "They are the same thing"], "correct": 0},
            {"type": "detail", "text": "According to the poem, what should you do when people lie about you?", "choices": ["Lie back", "Get angry", "Not deal in lies yourself", "Ignore all people"], "correct": 2},
            {"type": "purpose", "text": "Who is the speaker addressing in the final line?", "choices": ["Himself", "His son (or a younger person)", "The reader's father", "A teacher"], "correct": 1}
        ]
    },
    # NEW p9 - "O Captain! My Captain!" by Walt Whitman (excerpt)
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["A captain celebrates a successful voyage", "The poem mourns the death of a beloved captain (symbolizing Abraham Lincoln) just as victory is achieved", "Ships are dangerous", "The speaker is angry at the captain"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's emotion?", "choices": ["Joyful", "Grieving and sorrowful despite the victory", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'exulting' (line 3) most nearly means", "choices": ["Crying", "Rejoicing triumphantly", "Sleeping", "Working"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the relationship between the speaker and the captain?", "choices": ["They are strangers", "They are close—the speaker calls him 'father'", "They are enemies", "The captain does not know the speaker"], "correct": 1},
            {"type": "detail", "text": "What has happened to the captain at the end of the voyage?", "choices": ["He retired", "He is celebrating", "He has died (fallen cold and dead)", "He left the ship"], "correct": 2},
            {"type": "purpose", "text": "Why is this poem considered an elegy?", "choices": ["It celebrates a wedding", "It mourns the death of someone", "It describes a ship", "It is a love poem"], "correct": 1}
        ]
    },
    # NEW p10 - "Fire and Ice" by Robert Frost
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The world will definitely end in fire", "The world will definitely end in ice", "Desire (fire) and hate (ice) are both powerful forces that could destroy the world, metaphorically and literally", "The poet does not care how the world ends"], "correct": 2},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Cheerful", "Darkly contemplative and concise", "Angry", "Long-winded"], "correct": 1},
            {"type": "vocab", "text": "The word 'suffice' (line 9) most nearly means", "choices": ["Be insufficient", "Be enough", "Destroy", "Burn"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about what 'fire' and 'ice' represent metaphorically?", "choices": ["Summer and winter", "Desire/passion and hatred/coldness", "The sun and the moon", "Good and evil"], "correct": 1},
            {"type": "detail", "text": "According to the poet, which destruction does he favor based on his experience with desire?", "choices": ["Ice", "Fire", "Neither", "Both equally"], "correct": 1},
            {"type": "purpose", "text": "Why did Frost write such a short poem about the end of the world?", "choices": ["He was in a hurry", "To pack powerful ideas about human emotions into a compact, memorable form", "He couldn't think of more lines", "He doesn't believe the world will end"], "correct": 1}
        ]
    },
    # NEW p11 - "Still I Rise" by Maya Angelou (excerpt)
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker is sad about her past", "The speaker celebrates her resilience and defiantly declares that she will rise above oppression, lies, and historical shame", "Rising is physically difficult", "History is always accurate"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Defeated", "Defiant, proud, and joyful", "Angry and bitter", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The word 'beset' (line 6) most nearly means", "choices": ["Confused", "Troubled or attacked from all sides", "Happy", "Sleepy"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about who the speaker is addressing?", "choices": ["A friend", "Someone who tried to oppress or diminish her (possibly racists or historical oppressors)", "A child", "Herself only"], "correct": 1},
            {"type": "detail", "text": "According to the poem, what natural phenomena does the speaker compare her rising to?", "choices": ["Earthquakes", "Moons, suns, and tides", "Rainstorms", "Volcanoes"], "correct": 1},
            {"type": "purpose", "text": "Why does the speaker repeat 'I rise' multiple times at the end?", "choices": ["She forgot she already said it", "To emphasize the theme of resilience and create a powerful, rhythmic conclusion", "To fill space", "To show she is tired"], "correct": 1}
        ]
    },
    # NEW p12 - "Sonnet 18" by William Shakespeare
    {
        "id": "p12",
        "title": "Sonnet 18: Shall I compare thee to a summer's day?",
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
            {"type": "main_idea", "text": "What is the main idea of this sonnet?", "choices": ["Summer is the best season", "The speaker's beloved is more beautiful and constant than a summer day, and the poem itself will grant immortality", "All beautiful things fade forever", "Shakespeare did not like summer"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone toward his beloved?", "choices": ["Admiring and confident in the power of poetry", "Jealous", "Angry", "Bored"], "correct": 0},
            {"type": "vocab", "text": "The word 'temperate' (line 2) most nearly means", "choices": ["Hot", "Cold", "Mild and balanced (not extreme)", "Windy"], "correct": 2},
            {"type": "inference", "text": "What can be inferred about how the speaker believes his beloved can achieve immortality?", "choices": ["Through having children", "Through being famous", "Through this poem ('eternal lines')", "Through living forever physically"], "correct": 2},
            {"type": "detail", "text": "What does the speaker say about summer's duration?", "choices": ["It lasts forever", "It has 'too short a date' (does not last long enough)", "It is too hot all the time", "It never arrives"], "correct": 1},
            {"type": "purpose", "text": "What is the function of the final couplet (last two lines)?", "choices": ["To change the subject", "To conclude that as long as people read the poem, the beloved will live on", "To criticize summer", "To ask a question"], "correct": 1}
        ]
    },
    # NEW p13 - "Because I could not stop for Death" by Emily Dickinson
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker describes a car accident", "Death is personified as a kind gentleman who takes the speaker on a carriage ride toward eternity; the poem reflects on mortality and immortality", "The speaker is afraid of death", "The speaker outruns death"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone toward death?", "choices": ["Terrified", "Calm, accepting, and even civil", "Angry", "Humorous"], "correct": 1},
            {"type": "vocab", "text": "The word 'surmised' (line 23) most nearly means", "choices": ["Guessed or inferred", "Saw clearly", "Heard", "Forgot"], "correct": 0},
            {"type": "inference", "text": "What can be inferred about the 'House' in stanza 5?", "choices": ["A real house where the speaker lived", "A grave (swelling of the ground)", "A school", "A church"], "correct": 1},
            {"type": "detail", "text": "What season or time of day is suggested in stanza 4?", "choices": ["Midnight", "Sunset and cool evening (Dews, Chill)", "Morning", "Noon"], "correct": 1},
            {"type": "purpose", "text": "Why does Dickinson personify Death as 'kindly' and 'civil'?", "choices": ["To make death less frightening and show acceptance of mortality", "To argue that death is a person", "To prove that death is evil", "To describe a funeral"], "correct": 0}
        ]
    },
    # NEW p14 - "The Raven" by Edgar Allan Poe (excerpt)
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
            {"type": "main_idea", "text": "What is the main idea of this excerpt?", "choices": ["A student is visited by a talking bird that only says 'Nevermore,' deepening his grief over lost Lenore", "The raven is a pet that can speak many words", "The speaker is happy and entertained", "The poem is about a beautiful summer day"], "correct": 0},
            {"type": "tone", "text": "Which word best describes the mood?", "choices": ["Joyful", "Melancholy, eerie, and mournful", "Excited", "Boring"], "correct": 1},
            {"type": "vocab", "text": "The word 'surcease' (line 10) most nearly means", "choices": ["Increase", "End or relief from", "Celebration", "Beginning"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about Lenore?", "choices": ["She is a lost loved one who has died", "She is a bird", "She is the speaker's enemy", "She is the raven's name"], "correct": 0},
            {"type": "detail", "text": "What word does the raven repeatedly say?", "choices": ["Lenore", "Nevermore", "Forever", "Chamber"], "correct": 1},
            {"type": "purpose", "text": "Why does Poe use a raven instead of a different bird?", "choices": ["Ravens are colorful", "Ravens have historical and literary associations with ill omen, death, and memory", "Ravens are the only talking birds", "He saw one that morning"], "correct": 1}
        ]
    },
    # NEW p15 - "Invictus" by William Ernest Henley
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker is sad about his difficult life", "The speaker declares his resilience and control over his own spirit despite suffering and circumstances", "Fate controls everything", "The speaker prays to gods for help"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's attitude?", "choices": ["Defeated", "Defiant, strong, and unyielding", "Carefree", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'fell' (line 5) most nearly means", "choices": ["Friendly", "Cruel or deadly", "Fallen", "Soft"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the speaker's physical condition from 'My head is bloody, but unbowed'?", "choices": ["He has been injured but refuses to submit", "He is completely healthy", "He is dead", "He is angry at a barber"], "correct": 0},
            {"type": "detail", "text": "What does the speaker call his soul in the first stanza?", "choices": ["Broken", "Unconquerable", "Afraid", "Lost"], "correct": 1},
            {"type": "purpose", "text": "Why did Henley write this poem?", "choices": ["To complain about his illness", "To inspire readers with a message of inner strength and self-mastery despite adversity", "To describe a night scene", "To pray to gods"], "correct": 1}
        ]
    },
    # NEW p16 - "The New Colossus" by Emma Lazarus (sonnet)
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
            {"type": "main_idea", "text": "What is the main idea of this sonnet?", "choices": ["The Statue of Liberty is a weapon", "The Statue of Liberty welcomes immigrants ('tired, poor, huddled masses') to America as a symbol of refuge and freedom", "Ancient Greece was better than America", "The statue is made of brazen giant"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone of the statue's speech?", "choices": ["Exclusionary and harsh", "Welcoming, compassionate, and hopeful", "Angry", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'teeming' (line 12) most nearly means", "choices": ["Empty", "Crowded and overflowing", "Quiet", "Distant"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the 'brazen giant of Greek fame' in line 1?", "choices": ["The Colossus of Rhodes, a symbol of conquest and power", "A famous American statue", "A type of bird", "A war ship"], "correct": 0},
            {"type": "detail", "text": "According to the poem, whom does the statue call to come to America?", "choices": ["Only the wealthy", "Only scientists", "The tired, poor, huddled masses yearning to breathe free", "Only citizens"], "correct": 2},
            {"type": "purpose", "text": "Why is this poem inscribed on the Statue of Liberty?", "choices": ["To advertise tourism", "To define America's identity as a nation of immigrants and refuge", "To scare away immigrants", "To describe how the statue was built"], "correct": 1}
        ]
    },
    # NEW p17 - "Do Not Go Gentle into That Good Night" by Dylan Thomas
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
            {"type": "main_idea", "text": "What is the main message of this villanelle?", "choices": ["Death should be accepted peacefully", "The speaker urges his dying father and all men to fight fiercely against death ('not go gentle')", "Old age is boring", "Light is better than night"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the poem's tone?", "choices": ["Calm and accepting", "Fierce, urgent, and passionate", "Humorous", "Indifferent"], "correct": 1},
            {"type": "vocab", "text": "The phrase 'that good night' (line 1) is a metaphor for", "choices": ["Sleep", "Death", "Evening", "Darkness"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about the speaker's relationship with his father?", "choices": ["They are strangers", "The speaker loves his father and is pleading with him to fight against death", "The speaker hates his father", "The father is already dead"], "correct": 1},
            {"type": "detail", "text": "According to the poem, what should men do against 'the dying of the light'?", "choices": ["Sleep", "Rage and not go gentle", "Sing", "Cry"], "correct": 1},
            {"type": "purpose", "text": "Why does Thomas repeat the two lines 'Do not go gentle...' and 'Rage, rage...' throughout?", "choices": ["He forgot other lines", "The villanelle form requires repetition for emphasis and emotional power", "To fill space", "To make it easier to memorize"], "correct": 1}
        ]
    },
    # NEW p18 - "Phenomenal Woman" by Maya Angelou (excerpt)
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["The speaker is arrogant and rude", "The speaker celebrates her confidence and inner beauty, which make her 'phenomenal' despite not fitting conventional beauty standards", "All women should be fashion models", "Men are foolish"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the speaker's tone?", "choices": ["Insecure", "Confident, proud, and joyful", "Angry", "Sad"], "correct": 1},
            {"type": "vocab", "text": "The word 'phenomenally' (line 14) most nearly means", "choices": ["Boringly", "Remarkably or extraordinarily", "Quietly", "Sadly"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why 'pretty women' wonder where the speaker's secret lies?", "choices": ["They are jealous and confused because she is confident despite not meeting conventional beauty standards", "They want to be her friend", "They hate her", "They don't notice her"], "correct": 0},
            {"type": "detail", "text": "According to the poem, where does the speaker's power come from?", "choices": ["Her money", "Her physical features (reach of arms, span of hips, fire in eyes, etc.) and her inner confidence", "Her fame", "Her clothes"], "correct": 1},
            {"type": "purpose", "text": "Why did Angelou write this poem?", "choices": ["To criticize models", "To celebrate women's confidence and redefine beauty on their own terms", "To make men feel bad", "To describe a party"], "correct": 1}
        ]
    },
    # NEW p19 - "The Cremation of Sam McGee" by Robert W. Service (excerpt)
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
            {"type": "main_idea", "text": "What is the main idea of this excerpt?", "choices": ["Gold mining is easy", "The speaker promises to cremate his friend Sam McGee, who dies from the extreme cold of the Yukon", "Sam McGee returns to Tennessee", "Cremation is illegal"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the mood?", "choices": ["Cheerful and warm", "Eerie, cold, and grim with a touch of dark humor", "Romantic", "Boring"], "correct": 1},
            {"type": "vocab", "text": "The word 'moil' (line 2) most nearly means", "choices": ["Rest", "Work hard in difficult conditions", "Sing", "Travel"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why Sam McGee is so afraid of an 'icy grave'?", "choices": ["He comes from warm Tennessee and hates the cold so much he would rather be burned", "He is claustrophobic", "He wants to be buried at sea", "He is afraid of ghosts"], "correct": 0},
            {"type": "detail", "text": "Where did Sam McGee originally come from?", "choices": ["Alaska", "Tennessee", "Canada", "Norway"], "correct": 1},
            {"type": "purpose", "text": "Why does the poet use dialect and colloquial language ('Cap,' 'cursèd cold')?", "choices": ["To make the poem feel authentic to the Yukon gold rush setting and characters", "To confuse readers", "Because he didn't know proper English", "To rhyme more easily"], "correct": 0}
        ]
    },
    # NEW p20 - "We Wear the Mask" by Paul Laurence Dunbar
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
            {"type": "main_idea", "text": "What is the main idea of this poem?", "choices": ["Masks are fashionable accessories", "The speaker describes how oppressed people (particularly African Americans after slavery) hide their pain and suffering behind a smiling 'mask' to survive in a hostile world", "Everyone should show their true feelings", "Smiling is always good"], "correct": 1},
            {"type": "tone", "text": "Which word best describes the tone?", "choices": ["Joyful", "Bitter, sorrowful, and resigned to hiding pain", "Angry and shouting", "Confused"], "correct": 1},
            {"type": "vocab", "text": "The word 'myriad' (line 5) most nearly means", "choices": ["One", "Countless or many", "Simple", "Loud"], "correct": 1},
            {"type": "inference", "text": "What can be inferred about why the world should not see 'our tears and sighs'?", "choices": ["The world would not understand or would use the knowledge against the oppressed", "The speaker is ashamed", "Tears are ugly", "No one cries"], "correct": 0},
            {"type": "detail", "text": "What does the mask do according to line 1?", "choices": ["It makes people angry", "It grins and lies (hides true feelings)", "It cries", "It is made of clay"], "correct": 1},
            {"type": "purpose", "text": "Why does Dunbar repeat 'We wear the mask'?", "choices": ["He forgot other lines", "To emphasize the theme of forced concealment of suffering", "To describe a party", "To argue that masks are fun"], "correct": 1}
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


def get_circle_svg(radius):
    """Generate SVG for a circle with given radius. Only radius displayed."""
    diameter = radius * 2
    cx, cy = 100, 85
    r_scaled = radius * 4  # Scale for visibility
    
    return f'''<svg width="220" height="180" viewBox="0 0 220 180" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <circle cx="{cx}" cy="{cy}" r="{r_scaled}" fill="#cce5ff" stroke="#006" stroke-width="2.5"/>
    <!-- Radius line from center to edge -->
    <line x1="{cx}" y1="{cy}" x2="{cx + r_scaled}" y2="{cy}" stroke="#c33" stroke-width="2"/>
    <!-- Small square at center -->
    <rect x="{cx-3}" y="{cy-3}" width="6" height="6" fill="#c33"/>
    <!-- Radius label -->
    <text x="{cx + 5}" y="{cy - 8}" font-size="13" fill="#c33" font-weight="bold">r = {radius}</text>
    <text x="80" y="20" font-size="14" fill="#006" font-weight="bold">Circle</text>
</svg>'''


def get_rectangle_svg(length, width):
    """Generate SVG for a rectangle. Only length displayed (width hidden for problem-solving)."""
    # Scale for visibility - width visually represented but not labeled
    l_scaled = length * 6
    w_scaled = width * 6
    
    return f'''<svg width="260" height="180" viewBox="0 0 260 180" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <rect x="30" y="30" width="{l_scaled}" height="{w_scaled}" fill="#cce5ff" stroke="#006" stroke-width="2.5"/>
    <!-- Only show length line at top -->
    <line x1="30" y1="30" x2="{30 + l_scaled}" y2="30" stroke="#c33" stroke-width="2"/>
    <text x="{30 + l_scaled//2}" y="22" font-size="13" fill="#c33" text-anchor="middle" font-weight="bold">L = {length}</text>
    <!-- Width is NOT labeled (user must calculate from perimeter) -->
    <text x="100" y="20" font-size="14" fill="#006" font-weight="bold">Rectangle</text>
</svg>'''


def get_cube_svg(side):
    """Generate clean 2.5D isometric cube with given side length"""
    s = side * 6  # Scale for visibility
    
    return f'''<svg width="220" height="180" viewBox="0 0 220 180" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Front face -->
    <rect x="50" y="70" width="{s}" height="{s}" fill="#cce5ff" stroke="#006" stroke-width="2.5"/>
    
    <!-- Top face (isometric) -->
    <polygon points="50,70 {50 + s*0.7},{70 - s*0.4} {50 + s + s*0.7},{70 - s*0.4} {50 + s},70" fill="#e6f2fa" stroke="#006" stroke-width="2"/>
    
    <!-- Right face (isometric) -->
    <polygon points="{50 + s},70 {50 + s + s*0.7},{70 - s*0.4} {50 + s + s*0.7},{70 + s - s*0.4} {50 + s},{70 + s}" fill="#a8d0e6" stroke="#006" stroke-width="2"/>
    
    <!-- Dimension label -->
    <text x="55" y="165" font-size="13" fill="#c33" font-weight="bold">s = {side}</text>
    <text x="80" y="20" font-size="14" fill="#006" font-weight="bold">Cube</text>
</svg>'''


def get_rectangular_prism_svg(l, w, h):
    """Generate clean 2.5D isometric rectangular prism. Dimensions displayed cleanly away from diagram."""
    # Scale factors
    l_scaled = l * 5
    w_scaled = w * 5
    h_scaled = h * 5
    
    # Base position
    x0, y0 = 40, 100
    
    return f'''<svg width="260" height="200" viewBox="0 0 260 200" style="display:block; margin:10px auto; background:#f9f9f9; border-radius:8px;">
    <!-- Front face (length × height) -->
    <rect x="{x0}" y="{y0 - h_scaled}" width="{l_scaled}" height="{h_scaled}" fill="#cce5ff" stroke="#006" stroke-width="2.5"/>
    
    <!-- Top face (length × width) - isometric -->
    <polygon points="{x0},{y0 - h_scaled} {x0 + l_scaled},{y0 - h_scaled} {x0 + l_scaled + w_scaled*0.7},{y0 - h_scaled - w_scaled*0.4} {x0 + w_scaled*0.7},{y0 - h_scaled - w_scaled*0.4}" fill="#e6f2fa" stroke="#006" stroke-width="2"/>
    
    <!-- Right face (width × height) - isometric -->
    <polygon points="{x0 + l_scaled},{y0 - h_scaled} {x0 + l_scaled},{y0} {x0 + l_scaled + w_scaled*0.7},{y0 - w_scaled*0.4} {x0 + l_scaled + w_scaled*0.7},{y0 - h_scaled - w_scaled*0.4}" fill="#a8d0e6" stroke="#006" stroke-width="2"/>
    
    <!-- Bottom edge of front face -->
    <line x1="{x0}" y1="{y0}" x2="{x0 + l_scaled}" y2="{y0}" stroke="#006" stroke-width="2"/>
    
    <!-- Dimensions labels - placed away from diagram (below and to the right) -->
    <text x="{x0 + l_scaled//2}" y="{y0 + 25}" font-size="12" fill="#c33" text-anchor="middle" font-weight="bold">l = {l}</text>
    <text x="{x0 + l_scaled + 45}" y="{y0 - h_scaled//2}" font-size="12" fill="#c33" font-weight="bold">w = {w}</text>
    <text x="{x0 - 35}" y="{y0 - h_scaled//2}" font-size="12" fill="#c33" font-weight="bold">h = {h}</text>
    
    <text x="90" y="20" font-size="14" fill="#006" font-weight="bold">Rectangular Prism</text>
</svg>'''


import math

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


# === Mobile-friendly HTML template ===


PAGE_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>SSAT Study App</title>
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
.login { 
    max-width: 420px; 
    margin: 60px auto; 
}
input[type="text"], input[type="password"] {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    font-size: 16px;
    border-radius: 10px;
    border: 2px solid #006;
    box-sizing: border-box;
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
/* 40% larger, engaging serif font for comfortable reading */
.passage-text {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 1.4rem;   /* 40% larger than default (1rem → 1.4rem) */
    line-height: 1.6;
    color: #1a2a3a;
    background: #fafcfd;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #003366;
    margin-bottom: 20px;
    letter-spacing: 0.01em;
}

/* Poetry formatting - preserves line breaks and spacing */
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

/* Optional: stanza break styling */
.poetry-text br {
    margin-bottom: 0.5em;
}

/* Passage title styling */
.passage-title {
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 1.3rem;
    font-weight: bold;
    color: #003366;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid #cde;
}

/* Question text styling - distinct from passage */
.problem > div:first-child {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 12px;
}

/* Diagram styling (unchanged) */
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
        options = ['Number Sense and Arithmetic', 'Algebraic Thinking', 'Geometry and Measurement', 'Data and Probability', 'Mixed Practice'];
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
<div class="small">Logged in as <b>{{ user }}</b> | 
<form style="display:inline" method="post" action="/logout"><button class="secondary" type="submit">Reset</button></form>
<form style="display:inline" method="post" action="/reset"><button class="secondary danger" type="submit">Logout</button></form>
</div></div>
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
    <input type="number" name="num" min="1" max="20" value="5">
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
        {# Check if this looks like poetry (contains line breaks or known poetry indicators) #}
        {% set passage_text = p[0] %}
        {% if '—' in passage_text and passage_text|length < 2000 %}
            {# Simple heuristic: if it has an author dash and is relatively short, treat as poetry #}
            <div class="poetry-text">{{ passage_text|safe }}</div>
        {% else %}
            {# Otherwise treat as regular passage #}
            <div class="passage-text">{{ passage_text|safe }}</div>
        {% endif %}
    {% else %}
        {# This is a regular question - use counter then increment #}
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
<div class="score">📊 Score: {{ correct_count }}/{{ total }} ({{ percent }}%)</div>
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - SSAT Study App</title>
        <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#f0f4f8; color:#1a2a3a; padding:20px; margin:0; }}
        .login {{ max-width:420px; margin:80px auto; background:white; padding:24px; border-radius:20px; box-shadow:0 8px 24px rgba(0,0,0,0.1); }}
        input {{ width:100%; padding:12px; margin:8px 0; font-size:16px; border-radius:12px; border:2px solid #006; box-sizing: border-box; }}
        button {{ background:#006; color:white; border:none; padding:12px; border-radius:12px; cursor:pointer; width:100%; font-size:16px; font-weight:600; }}
        h2 {{ margin-top:0; color:#003366; text-align:center; }}
        .error {{ color:#c33; text-align:center; }}
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
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    # RESET SUBMISSION FLAG AND SAVED RESULTS
    session['submitted'] = False
    session.pop('saved_results', None)
    session.pop('saved_answers', None)
    session.pop('saved_correct_count', None)
    
    section = request.form.get('section')
    topic = request.form.get('topic')
    
    # ============================================================
    # READING COMPREHENSION SECTION (Always 6 questions, no num dropdown)
    # ============================================================
    if section == 'reading':
        problems = []
        
        if topic == 'Nonfiction':
            # Generate 1 nonfiction passage with exactly 6 questions
            passages = gen_reading_comprehension('nonfiction', 1)
            for passage_text, questions in passages:
                # Add passage as the first "problem" (display only)
                problems.append((passage_text, [], -1))  # Empty choices list for passage
                # Add the 6 questions
                for q_text, choices, correct in questions:
                    problems.append((q_text, choices, correct))
                    
        elif topic == 'Fiction':
            passages = gen_reading_comprehension('fiction', 1)
            for passage_text, questions in passages:
                problems.append((passage_text, [], -1))
                for q_text, choices, correct in questions:
                    problems.append((q_text, choices, correct))
                    
        elif topic == 'Poetry':
            passages = gen_reading_comprehension('poetry', 1)
            for passage_text, questions in passages:
                problems.append((passage_text, [], -1))
                for q_text, choices, correct in questions:
                    problems.append((q_text, choices, correct))
        
        # Store problems (1 passage + 6 questions = 7 total items)
        session['problems'] = problems
        session['answers'] = [None] * len(problems)
        session['correct_indices'] = [p[2] for p in problems]
        
        return redirect(url_for('home'))
    
    # ============================================================
    # VERBAL AND QUANTITATIVE SECTIONS (use num parameter)
    # ============================================================
    else:
        num = int(request.form.get('num', 5))
        num = max(1, min(20, num))
        
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
            elif topic == 'Mixed Practice': 
                problems = gen_random_mix(num, 'quant')
            else:
                problems = gen_number_sense_arithmetic(num)
        
        # Normalize problems (ensure exactly 5 choices)
        normalized = []
        for p in problems:
            q, choices, correct = p
            if len(choices) < 5:
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

    # Check if already submitted for this problem set
    if session.get('submitted', False):
        # Just re-render the page with the existing results
        problems = session.get('problems', [])
        results = session.get('saved_results', [])
        submitted_answers = session.get('saved_answers', [])
        correct_count = session.get('saved_correct_count', 0)
        total_questions = session.get('saved_total_questions', 0)
        percent = round((correct_count / total_questions) * 100) if total_questions > 0 else 0
        
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

    # Get problems and correct indices from session
    problems = session.get('problems', [])
    corrects = session.get('correct_indices', [])
    results = []
    correct_count = 0
    submitted_answers = []
    total_questions = 0  # Count only real questions (not passage displays)

    # Loop through each problem
    for i in range(len(problems)):
        raw_ans = request.form.get(f'answer_{i}', '')
        
        # Check if this is a passage display item (correct_index = -1)
        if corrects[i] == -1:
            # Auto-mark passage display items as correct
            results.append(True)
            submitted_answers.append(-1)
            continue  # Skip to next problem
        
        # This is a real question that needs grading
        total_questions += 1
        
        try:
            ans = int(raw_ans)
        except (ValueError, TypeError):
            ans = -1  # -1 means unanswered

        # Store the answer in session
        session['answers'][i] = ans
        submitted_answers.append(ans)

        # Check if answer is correct
        if ans != -1 and ans == corrects[i]:
            results.append(True)
            correct_count += 1
        else:
            results.append(False)

    # Calculate percentage score
    percent = round((correct_count / total_questions) * 100) if total_questions > 0 else 0

    # Save results to session and mark as submitted
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
    app.run(debug=True, use_reloader=False)
