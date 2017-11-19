from app import bcrypt, db
from app.api.models import User
from app.api.utils import authenticate

from flask import Blueprint, jsonify, request

from sqlalchemy import exc, or_

auth_blueprint = Blueprint('auth', __name__)

res_error = {
    'status': 'error',
    'message': 'Invalid payload.',
}


@auth_blueprint.route('/auth/signup', methods=['POST'])
def register_user():
    post_data = request.get_json()

    if not post_data:
        return jsonify(res_error), 400

    name = post_data.get('name')
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        user = User.query.filter(
            or_(User.name == name, User.email == email)
        ).first()

        if not user:
            new_user = User(
                name=name,
                email=email,
                password=password,
            )
            db.session.add(new_user)
            db.session.commit()

            auth_token = new_user.encode_auth_token(new_user.id)
            return jsonify({
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode(),
            }), 201
        else:
            res_error['message'] = 'Sorry. That user already exists.'
            return jsonify(res_error), 400
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(res_error), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    post_data = request.get_json()

    if not post_data:
        return jsonify(res_error), 400

    email = post_data.get('email')
    password = post_data.get('password')

    try:
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return jsonify({
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }), 200
        else:
            res_error['message'] = 'User does not exist.'
            return jsonify(res_error), 404
    except Exception:
        res_error['message'] = 'Try again.'
        return jsonify(res_error), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user():
    return jsonify({
        'status': 'success',
        'message': 'Successfully logged out.'
    }), 200
