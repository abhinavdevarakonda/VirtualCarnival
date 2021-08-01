from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
#use for reference for any usermodel in the future


class AccountManager(BaseUserManager):
    # create a new user 
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("all users must have an email for their account!")
        if not username:
            raise ValueError("all users must have a username for their account!")
        user = self.model( 
            email = self.normalize_email(email),  #to remove accidental uppercase etc.
            username = username,


        )
        user.set_password(password) #setting password for the user
        user.save(using=self._db)   #then saving the password into the database
        return user

    #create a superuser
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin       = True  #superuser should be admin,staff, and superuser 
        user.is_staff       = True   
        user.is_superuser   = True  
        user.is_active      = True
        user.save(using=self._db)
        return user

def get_pfp_path(self):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'


def get_default_pfp():
    return "VirtualCarnival/defaultpfp.png"  #this will automatically go into the static_cdn folder

class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name='email',max_length=60,unique=True)
    username        = models.CharField(max_length=30, unique=True)
    date_joined     = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin        = models.BooleanField(default=False) #obviously we don't want everyone to be admin
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    profile_image   = models.ImageField(max_length=255,upload_to=get_pfp_path,null=True,blank=True,default=get_default_pfp)   
    hide_email		= models.BooleanField(default=True)
    objects = AccountManager()

    USERNAME_FIELD = 'email' #always have it the same as object defined above
    REQUIRED_FIELDS = ['username'] #same as above

    def __str__(self):
        return self.username
    

    def get_pfp_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):] #returns pfp filename with slashes and all 
                                                                                                     #also we want all profile images to be saved as profile_image.png
                                                                                                         


    def has_perm(self,permission,obj=None):
        return self.is_admin                       #checks whether user is admin, to allow permission
        return self.is_staff


    def has_module_perms(self,app_label):
        return True
