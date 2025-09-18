from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# Funny messages for different scenarios
FUNNY_MESSAGES = {
    'add': {
        'easy': [
            "🎉 Congratulations! You've mastered the ancient art of counting on fingers!",
            "🧮 Even a toddler with building blocks could figure this out, but hey, good job!",
            "🎪 Ladies and gentlemen, witness the spectacular feat of... basic addition!",
            "🤓 Fun fact: You just performed the same operation our ancestors did 5000 years ago!",
            "🏆 Achievement unlocked: Can add two numbers without a calculator... oh wait.",
        ],
        'medium': [
            "🚀 Houston, we have... slightly more impressive addition!",
            "🎭 *dramatic gasp* Numbers bigger than 10! How adventurous!",
            "🧠 My circuits are warming up for this complex calculation!",
            "⚡ Addition powers: ACTIVATED! (Still pretty basic though)",
        ],
        'large': [
            "🤯 Whoa there, math wizard! These numbers are getting serious!",
            "🦾 Flexing my computational muscles for this big addition!",
            "🎢 Big numbers ahead! Hope you're ready for this wild ride!",
            "🔥 Now THIS is some premium addition action!",
        ]
    },
    'multiply': {
        'easy': [
            "✨ Multiplication magic! Even my calculator from 1985 is impressed!",
            "🎯 Bullseye! You've discovered that numbers can multiply! Revolutionary!",
            "🤖 BEEP BOOP: Multiplication.exe has completed successfully",
            "🎪 And for my next trick, I'll make your confusion... disappear!",
        ],
        'medium': [
            "🚀 Multiplication mode: ENGAGED! Prepare for mathematical mayhem!",
            "⚡ With great multiplication comes great responsibility!",
            "🧙‍♂️ *waves wand* Alakazam! Numbers have been multiplied!",
            "🎭 The crowd goes wild for intermediate multiplication!",
        ],
        'large': [
            "🤯 HOLY CALCULATORS! These numbers are MASSIVE!",
            "🦸 Multiplication superhero to the rescue!",
            "🔥 This multiplication is so hot, it might melt your screen!",
            "🎢 Buckle up! This multiplication is going to be EPIC!",
        ]
    },
    'subtract': {
        'positive': [
            "➖ Subtraction success! No numbers were harmed in this operation!",
            "🔍 Elementary, my dear Watson! The answer is elementary!",
            "🎢 We're going down! What a thrilling mathematical descent!",
            "⚖️ Justice is served... mathematically!",
        ],
        'negative': [
            "😬 Oops! We've entered the mysterious realm of negative numbers!",
            "🌌 Welcome to the upside-down world of negative mathematics!",
            "🔄 Plot twist! The answer is below zero! Mind = blown!",
            "❄️ Brrr! This result is colder than absolute zero!",
        ],
        'zero': [
            "😐 Perfectly balanced, as all things should be. Zero achieved!",
            "🎯 You've hit the mathematical bullseye: ZERO!",
            "🧘 Zen achieved. The answer is nothing, yet everything.",
            "⚡ Zero: The hero of mathematics strikes again!",
        ]
    },
    'divide': {
        'whole': [
            "🔪 Division complete! Clean cut, no remainders harmed!",
            "✨ Perfect division! Even Euclid would be proud!",
            "🎯 Surgical precision! This division is flawless!",
            "🏆 Gold medal performance in the division olympics!",
        ],
        'decimal': [
            "🎭 Ah, the drama of decimal division! So sophisticated!",
            "🔬 Scientific notation activated for this precise calculation!",
            "🎪 Ladies and gentlemen, floating point mathematics!",
            "🧮 Decimal places: because whole numbers are too mainstream!",
        ],
        'by_zero': [
            "💥 ERROR! You tried to divide by zero! The universe nearly collapsed!",
            "🚨 MATH POLICE! Dividing by zero is illegal in 47 dimensions!",
            "🌌 Attempting to divide by zero... black hole detected!",
            "🤖 SYSTEM OVERLOAD: Cannot comprehend the concept of dividing by zero!",
        ]
    }
}

SPECIAL_NUMBERS = {
    42: "🤖 The answer to life, the universe, and everything!",
    69: "😏 Nice.",
    420: "🌿 Dude...",
    666: "😈 Spooky number detected!",
    777: "🎰 Lucky numbers! You're feeling lucky today!",
    1337: "💻 LEET! You're speaking my language!",
    404: "🔍 Number not found... oh wait, there it is!",
    911: "🚨 Emergency mathematics in progress!",
    1000: "🎉 Welcome to the four-digit club!",
    0: "🕳️ The void stares back...",
}

def get_difficulty_level(a, b):
    """Determine difficulty based on number size"""
    max_num = max(abs(a), abs(b))
    if max_num <= 10:
        return 'easy'
    elif max_num <= 100:
        return 'medium'
    else:
        return 'large'

def get_funny_message(operation, a, b, result):
    """Generate funny message based on operation and result"""
    
    # Check for special numbers first
    for num, message in SPECIAL_NUMBERS.items():
        if result == num or a == num or b == num:
            return f"{message} (But seriously, {a} {get_operation_symbol(operation)} {b} = {result})"
    
    if operation in ['add', 'multiply']:
        difficulty = get_difficulty_level(a, b)
        messages = FUNNY_MESSAGES[operation][difficulty]
        return random.choice(messages)
    
    elif operation == 'subtract':
        if result > 0:
            return random.choice(FUNNY_MESSAGES['subtract']['positive'])
        elif result < 0:
            return random.choice(FUNNY_MESSAGES['subtract']['negative'])
        else:
            return random.choice(FUNNY_MESSAGES['subtract']['zero'])
    
    elif operation == 'divide':
        if b == 0:
            return random.choice(FUNNY_MESSAGES['divide']['by_zero'])
        elif result == int(result):  # Whole number
            return random.choice(FUNNY_MESSAGES['divide']['whole'])
        else:
            return random.choice(FUNNY_MESSAGES['divide']['decimal'])
    
    return "🤖 Math happened! My circuits are satisfied!"

def get_operation_symbol(operation):
    symbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    }
    return symbols.get(operation, '?')

def get_mood_emoji(result):
    """Return mood emoji based on result"""
    if result == 0:
        return "😐"
    elif result < 0:
        return "😬"
    elif result > 1000:
        return "🤯"
    elif result == 42:
        return "🤖"
    elif result in [69, 420]:
        return "😏"
    elif result == 666:
        return "😈"
    elif result == 777:
        return "🍀"
    elif result % 2 == 0:
        return "😊"
    else:
        return "🤪"

@app.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Add some suspense (because math is serious business)
        time.sleep(random.uniform(0.1, 0.3))
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "💔 No data? My mathematical heart is broken!",
                "mood": "😢"
            }), 400
        
        a = data.get("a")
        b = data.get("b")
        operation = data.get("operation")
        
        if a is None or b is None or operation is None:
            return jsonify({
                "error": "🧩 Missing puzzle pieces! I need 'a', 'b', and 'operation'!",
                "mood": "🤔"
            }), 400
        
        # Convert to numbers
        a = float(a)
        b = float(b)
        
        # Perform the operation
        if operation == "add":
            result = a + b
        elif operation == "multiply":
            result = a * b
        elif operation == "subtract":
            result = a - b
        elif operation == "divide":
            if b == 0:
                return jsonify({
                    "error": random.choice(FUNNY_MESSAGES['divide']['by_zero']),
                    "mood": "💥",
                    "result": "undefined (universe still intact)"
                }), 400
            result = a / b
        else:
            return jsonify({
                "error": f"🤷‍♂️ '{operation}'? Never heard of it! Try: add, subtract, multiply, divide",
                "mood": "🤷‍♂️"
            }), 400
        
        # Format result (remove .0 for whole numbers)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 6)  # Limit decimal places
        
        funny_message = get_funny_message(operation, int(a), int(b), result)
        mood = get_mood_emoji(result)
        
        return jsonify({
            "result": result,
            "funny_message": funny_message,
            "mood": mood,
            "operation_performed": f"{a} {get_operation_symbol(operation)} {b}",
            "timestamp": time.time(),
            "server_mood": "🧠 Feeling mathematically superior"
        })
        
    except ValueError:
        return jsonify({
            "error": "🤖 Error: Numbers only please! My brain can't compute letters!",
            "mood": "😵‍💫"
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"🔥 Unexpected error: {str(e)} (My circuits are having a moment)",
            "mood": "🤯"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "🧠 Brain functioning at maximum capacity!",
        "mood": "😎",
        "message": "Ready to judge your mathematical abilities!"
    })

if __name__ == "__main__":
    print("🚀 Sarcastic Math Genius Server starting up...")
    print("🧠 Preparing to judge your mathematical abilities...")
    app.run(host="0.0.0.0", port=5000, debug=True)