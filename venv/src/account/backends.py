'''
i don't understand this part at all but basically it's for the long section being case insensitive
(except for password of course) 
you can use this same file for any other django project for the same function
(directly copy paste)
'''

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    
    
    def authenticate(self,request,username=None,password=None,**kwargs):
        UserModel = get_user_model() #it will get the account.Account user model (check settings.py for AUTH_USER_MODEL)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)


        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)         #no clue what is going on here 
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})    # somehting in django documentation for ignoring case
            #gets the email and then finds the user with that email ignoring case 
        
        except UserModel.DoesNotExist:
            UserModel().set_password(password) 
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
'''
just make sure to add this part in settings.py under AUTH_USER_MODEL = "<>":

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.AllowAllUsersModelBackend',
        'account.backends.CaseInsensitiveModelBackend'
)

'''