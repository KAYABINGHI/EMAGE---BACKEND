# @app.route('/mood/<int:mood_id>', methods=['GET'])
# def get_mood_details(mood_id):
#     mood = Mood.query.get(mood_id)
    
#     if not mood:
#         return jsonify({'error': 'Mood not found'}), 404
    
#     # Access the user through the relationship
#     mood_data = {
#         'id': mood.id,
#         'mood_level': mood.mood_level,
#         'emotion_label': mood.emotion_label,
#         'created_at': mood.created_at.isoformat(),
#         'username': mood.user.username,  # This works because of the relationship!
#         'user_email': mood.user.email}