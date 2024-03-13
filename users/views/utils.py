

def get_userdata(user):
    return {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'mobile_number': user.mobile_number,
        'is_superuser': user.is_superuser,
        'is_customer': user.is_customer,
        'profile_picture': user.profile_picture.url,
        'last_login': user.last_login,
    }

