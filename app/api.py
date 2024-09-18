from flask import Blueprint, jsonify
from app.models import User

api_bp = Blueprint('api', __name__)

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'username': user.username, 'email': user.email} for user in users])
