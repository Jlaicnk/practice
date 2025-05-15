from Users.models import SysUser

def getUserPreferences(user_id):
    user = SysUser.objects.get(id=user_id)
    if user != None:
        return user.preferences
    else:
        return None

if __name__ == "__main__":
    user_id = 1
    print(getUserPreferences(user_id))
