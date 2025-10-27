import random

# randomly generated messages depending on the user's emotion_label
def get_mood_message(emotion_label):
    messages = {
        'happy': [
            "😊 That's wonderful! Keep riding this positive wave!",
            "🌞 Love to see you thriving! You deserve all this joy! Keep shining!",
            "😄 Your happiness is contagious! Celebrate this moment.",
            "🎉 Awesome! Remember this feeling for tougher days.",
            "😁 Happiness suits you! Keep spreading those good vibes.",
            "🙏 Stay grateful — joy multiplies when you share it.",
            "🌈 Life feels brighter when you smile like that!",
            "✨ You're glowing with positivity! Keep that energy alive."
        ],
        'calm': [
            "🌿 Peace looks good on you. Enjoy this tranquility.",
            "🕊️ Beautiful! This is your mind finding balance.",
            "💨 Breathe it in. You've found your center today.",
            "🧘‍♂️ This stillness is healing. Soak it in.",
            "🌊 Calm is strength. You’ve mastered your emotions.",
            "😌 Enjoy the silence — it’s your soul resting.",
            "🍃 Still waters run deep, just like your calm energy.",
            "☁️ You're radiating serenity. Keep that balance."
        ],
        'sad': [
            "💔 It's okay to feel this way. Your feelings are valid.",
            "🌧️ Tough days don't last forever. Be gentle with yourself.",
            "😔 You don't have to be strong right now. Just be.",
            "☔ This feeling will pass. You've gotten through before.",
            "🌱 Even rain nourishes the earth — sadness can help you grow.",
            "🤍 You’re not alone. It’s okay to take time to heal.",
            "😭 Cry if you need to. It's strength, not weakness.",
            "🌤️ Healing starts with honesty — and you’ve already begun."
        ],
        'anxious': [
            "🌬️ Take a deep breath. You're safe right now.",
            "🕰️ One moment at a time. You've got this.",
            "👁️ Ground yourself: name 5 things you can see right now.",
            "💪 This feeling is temporary. You're stronger than your anxiety.",
            "☁️ You are not your thoughts. Let them pass like clouds.",
            "🫁 Breathe — in for calm, out for control.",
            "🧠 Anxiety lies; you’ve overcome before and you will again.",
            "🌸 You're allowed to pause. Calm isn’t far away."
        ],
        'angry': [
            "🔥 Your anger is telling you something. It's okay to feel it but don't be irrational!",
            "⏸️ Take a pause before reacting. You're in control.",
            "💢 Feel it, acknowledge it, then let it go at your own pace.",
            "⚙️ Channel this energy into something positive when you're ready.",
            "⚡ Anger is energy — use it to build, not destroy.",
            "😤 You're allowed to feel upset; just don’t let it own you.",
            "🫧 Breathe out the fire, breathe in control.",
            "🧱 You’re stronger than the situation making you angry."
        ],
        'tired': [
            "😴 Rest isn't weakness, it's wisdom. Listen to your body.",
            "🛌 You deserve a break. Recharge without guilt.",
            "💤 Even superheroes need rest. Take care of yourself.",
            "☕ Your body is asking for what it needs. Honor that.",
            "🌙 Pause. Breathe. Sleep. Reset. You’ve earned it.",
            "🧸 Don’t push too hard — recovery is part of progress.",
            "🔋 Your energy matters. Protect it.",
            "🌑 Fatigue is just your body whispering, 'slow down'."
        ],
        'neutral': [
            "😐 Sometimes, just being is enough.",
            "⚖️ It’s okay to feel balanced — not every day has to be intense.",
            "🌻 Stay grounded; peace often hides in ordinary moments.",
            "🪞 Neutral days are perfect for self-reflection and calm progress.",
            "🧭 You're steady today — that’s quiet strength.",
            "🌤️ Balance feels good. Keep this gentle flow.",
            "🌾 No highs or lows, just peace — that’s power.",
            "💫 Enjoy this calm middle ground; it’s where clarity lives."
        ]
    }

    emotion = emotion_label.lower()
    return random.choice(messages.get(emotion, ["🤗 Thank you for sharing how you feel."]))
