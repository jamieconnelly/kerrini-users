import json

from app.tests.base import BaseTestCase
from app import db
from app.api.models import User


def add_user(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""
    # def test_add_user(self):
    #     """Ensure a new user can be added to the database."""
    #     with self.client:
    #         response = self.client.post(
    #             '/users',
    #             data=json.dumps(dict(
    #                 name='trump',
    #                 email='trump@whitehoose.com'
    #             )),
    #             content_type='application/json',
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 201)
    #         self.assertIn('trump@whitehoose.com was added!', data['message'])
    #         self.assertIn('success', data['status'])
