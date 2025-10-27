import random
# randomly generated messages from depending on the users emotion_lable
def get_mood_message(emotion_label):
    messages = {
        'happy': [
            "That's wonderful! Keep riding this positive wave!",
            "Love to see you thriving! You deserve all this joy! Keep shining!",
            "Your happiness is contagious! Celebrate this moment.",
            "Awesome! Remember this feeling for tougher days."
        ],
        'calm': [
            "Peace looks good on you. Enjoy this tranquility.",
            "Beautiful! This is your mind finding balance.",
            "Breathe it in. You've found your center today.",
            "This stillness is healing. Soak it in."
        ],
        'sad': [
            "It's okay to feel this way. Your feelings are valid.",
            "Tough days don't last forever. Be gentle with yourself.",
            "You don't have to be strong right now. Just be.",
            "This feeling will pass. You've gotten through before."
        ],
        'anxious': [
            "Take a deep breath. You're safe right now.",
            "One moment at a time. You've got this.",
            "Ground yourself: name 5 things you can see right now.",
            "This feeling is temporary. You're stronger than your anxiety."
        ],
        'angry': [
            "Your anger is telling you something. It's okay to feel it but dont be rational!",
            "Take a pause before reacting. You're in control.",
            "Feel it, acknowledge it, then let it go at your own pace.",
            "Channel this energy into something positive when you're ready."
        ],
        'tired': [
            "Rest isn't weakness, it's wisdom. Listen to your body.",
            "You deserve a break. Recharge without guilt.",
            "Even superheroes need rest. Take care of yourself.",
            "Your body is asking for what it needs. Honor that."
        ]
    }
    
    emotion = emotion_label.lower()
    return random.choice(messages.get(emotion, ["Thank you for sharing how you feel."]))