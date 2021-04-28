from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least two characters'
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least two characters'
        
        if User.objects.filter(email= postData['email']):
            errors['email'] = 'This email is already has in use'
        
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password does not match confirm password'
        
        if len(postData['password']) < 8:
            errors['password_length'] = 'Password length must be at least 8 characters'
            
        return errors


class User(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=60)
    balance = models.IntegerField(default = 100000)
    email= models.EmailField(max_length=50)
    password= models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()