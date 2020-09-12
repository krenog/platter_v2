from users.models import User


def update_profile(user: User, data: dict):
    user.birth = data['birth']
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()
