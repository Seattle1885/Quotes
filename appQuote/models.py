from django.db import models


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        filterEmail = User.manager.filter(email=postData['email'])
        #above checks all users emails to see if match postdata email
        
        if len(postData['userName']) == 0:
            errors['userName'] = ' "userName is Required"'
        
        if len(postData['email']) == 0:
            errors['email'] = ' "Email required" '
        if len(filterEmail) > 0:
            errors['email'] = ' "Email is taken" '
        
        if len(postData['PW']) == 0:
            errors['PW'] = ' "Password is required" '
        
        if postData['PWC'] != postData['PW']:
            errors['PWC'] = '"Password does not match"'
            print("postData['PWC'] is :", postData['PWC'])
        return errors
    
    def login_validator(self, postData):
        errors = {}

        userNameResults = User.manager.filter(userName=postData['userName'])        
        #emailResults = User.manager.filter(email=postData['email'])
        pwResults = User.manager.filter(password=postData['PW'])
        
#        if len(postData['email']) ==0:
#           errors['email'] = ' "Email is required to login" '
          
#        elif len(emailResults) == 0:
#            errors['noEmailFound'] = ' "Email not registered " '
#        else:
#            print('email found')
        
        if len(postData['userName']) ==0:
            errors['userName'] = ' "UserName is required to login" '
            
        elif len(userNameResults) == 0:
            errors['noUserNameFound'] = ' "UserName not registered " '
        else:
            print('userName found')
            
        if len(postData['PW']) == 0:
            errors['PW'] = ' "Password is required to login" '
        elif len(pwResults) == 0:
            errors['PW'] = ' "Incorrect Password" '
        else:
            print('password found')
        
        print("pwResults is :",pwResults)
        return errors
    
    def quotes_validator(self,postData):
        errors = {}
        if len(postData['Q']) == 0:
            errors['Q'] = '"Who wrote the quote?"'
        if len(postData['quoteMessage']) == 0:
            errors['quoteMessage'] = '"Need to add a Quote"'
        return errors

    def editQuote_validator(self,postData):
        errors = {}
        if len(postData['updatedQuoter']) == 0:
            errors['updatedQuoter'] = '"Who wrote the quote?"'
        if len(postData['updatedMessage']) == 0:
            errors['updatedMessage'] = '"Need to add a Quote"'
        return errors
    
class User(models.Model):
    userName = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    manager = UserManager()
    
class Quotes(models.Model):
    quoter = models.CharField(max_length=255)
    message = models.TextField(max_length=255)
    uploader = models.ForeignKey(User, related_name='quotes_uploaded', on_delete = models.CASCADE, null=True)
    likers = models.ManyToManyField(User,related_name='quotes_liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)  
    manager = models.Manager()      