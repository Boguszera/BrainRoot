from flask import Blueprint, jsonify, request
from .models import Word, Category
from . import db
import re
from flask import session
from .models import Word, Category
from . import db
from sqlalchemy import func
from . import word_service
from .word_service import get_random_word

api_bp = Blueprint('api', __name__, url_prefix='/api')

"""
v1

GET /api/words - all words
POST /api/words - add new word
DELETE /api/words/<wordID> - delete word

GET /api/categories - get all categories
POST /api/categories - add new category
DELETE /api/categories/<categoryID> - delete category

GET /api/lesson/start - start lesson
POST /api/lesson/word - get random word
POST /api/lesson/check - verify user answer
POST /api/lesson/end - end lesson and clear session

GET /api/review - get words to review
POST /api/review/run - start review lesson
"""

@api_bp.route('v1/words', methods=['GET'])
def get_all_words():
    words = Word.query.all()
    words_data = [{'word': word.word, 'translation': word.translation} for word in words]
    return jsonify(words_data)

@api_bp.route('v1/lesson/word', methods=['GET'])
def get_lesson_word():
    category_name = session.get('category_name')
    if not category_name:
        return jsonify({"error": "Category not selected"}), 400

    word_object = get_random_word(category_name)
    if not word_object:
        return jsonify({'error': "No words avaliable"}), 404

    word_data = {
        'word': word_object.word,
        'translation': word_object.translation,
    }
    return jsonify(word_data)
    
@api_bp.route('/lesson/end', methods=['POST'])
def end_lesson():
    session.pop('word', None)
    session.pop('correct_translation', None)
    session.pop('correct_answers', None)
    session.pop('category_name', None)
    return jsonify({'message': 'Lesson ended, session cleared.'})
    
@api_bp.route('/words/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    word = Word.query.get(word_id)

    if not word:
        return jsonify({'error': 'Word not found'}), 404

    db.session.delete(word)
    db.session.commit()

    return jsonify({'message': 'Word deleted successfully'})
    
@api_bp.route('/lesson/check', methods=['POST'])
def check_answer_api():
    data = request.get_json()
    user_translation = data.get('translation')

    correct_translation = session.get('correct_translation')
    word = session.get('word')

    if not correct_translation or not word:
        return jsonify({'error': 'No word in session'}), 400

    is_correct, message = check_answer(user_translation, correct_translation, word)

    return jsonify({'is_correct': is_correct, 'message': message})