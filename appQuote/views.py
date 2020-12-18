from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quotes
import bcrypt

def index(request):
    if 'counter' not in request.session:
        request.session['counter'] = 1
    else:
        request.session['counter'] += 1
    return render(request, 'index.html')

def register(request):
    errors = User.manager.user_validator(request.POST)
    
    if len(errors) > 0:  # if errors conatins anything, then run if loop runs
        for key, value in errors.items(): #checks k,v pairs
            messages.error(request,value)  # for one refresh displays tempoary message
        return redirect('/') 
    
    # password = userInput from register form
    pw_hash = bcrypt.hashpw(request.POST['PW'].encode(), bcrypt.gensalt()).decode()
    print("pw_hash is ",pw_hash)
    
    #below we are creating a new user 
    newUser = User.manager.create(userName=request.POST['userName'],email=request.POST['email'],password=pw_hash)
    
    request.session['loggedIn'] = newUser.id # creating a new session with newUser.id
    print('a new session has started with User ID:',request.session['loggedIn'] )
    
    return redirect('/success')

def login(request):
    print("Data submitted by User:",request.POST)
    errors = User.manager.login_validator(request.POST)
    
    user = User.manager.filter(userName=request.POST['userName'])
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0]
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['PW'].encode(), logged_user.password.encode()):
            #if true we put user ID in session
            request.session['loggedIn'] = logged_user.id
            print('A session has started for id#',request.session['loggedIn'])
            return redirect('/dashboard')
        else:
            return redirect('/')
    if len(errors) > 0:  # if errors conatins anything from above line, then run if loop
        for key, value in errors.items(): #checks k,v pairs
            messages.error(request,value)  # for one refresh displays tempory message
            print('found errors')
            print('errors is ',errors)
        return redirect('/')

def success(request):
    if 'loggedIn' not in request.session:
        return redirect('/')
    loggedUser = User.manager.get(id=request.session['loggedIn'])
    
    context = {
        'logInUser':loggedUser
    }
    return render(request,'success.html',context)
    
def logout(request):
    print('id ',request.session['loggedIn'],'session has ended')
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'loggedIn' not in request.session:
        return redirect('/')
    
    loggedUser = User.manager.get(id=request.session['loggedIn'])
    fave_quotes = loggedUser.quotes_liked.all()
    allQuotes = Quotes.manager.all()
    context = {
        'logInUser':loggedUser,
        'allQuotes':allQuotes,
        'faveQuotes':fave_quotes
    }
    
    return render(request, 'dashboard.html',context)

def addQuote(request):
    print('Youre Quoting',request.POST['Q'])
    errors = User.manager.quotes_validator(request.POST)
    
    if len(errors) > 0:  # if dict conatins anything from above line, then run if
        for key, value in errors.items(): #checks k,v pairs
            messages.error(request,value)  # for one refresh displays tempory message
            print('found errors')
        return redirect('/dashboard')
    
    if 'loggedIn' not in request.session:
        return redirect('/')
    loggedUser = User.manager.get(id=request.session['loggedIn'])
    
    new = Quotes.manager.create(quoter=request.POST["Q"], message=request.POST['quoteMessage'], uploader=loggedUser)
    print(' current loggedUser is :', loggedUser.userName)
    return redirect('/dashboard')

def userPage(request, uploaderId):
    selectedUser = User.manager.get(id=uploaderId)
    quotesUploaded = Quotes.manager.filter(uploader=selectedUser)
    context ={
        'selectedUser': selectedUser,
        'quotesUploaded': quotesUploaded
    }
    return render(request, 'home.html', context)

def delete(request, quoteId):
    delete = Quotes.manager.get(id=quoteId)
    delete.delete()
    return redirect('/dashboard')

def edit(request, quoteId):
    quoteEdit = Quotes.manager.get(id=quoteId)
    context={
        'quote2Edit': quoteEdit
    }
    return render(request,'editQuote.html',context)

def update(request, quoteId):
    errors = User.manager.editQuote_validator(request.POST)
    
    if len(errors) > 0:  # if dict conatins anything from above line, then run if
        for key, value in errors.items(): #checks k,v pairs
            messages.error(request,value)  # for one refresh displays tempory message
            print('found errors')
        return redirect(f'/editQuote/{quoteId}')
    updateQ = Quotes.manager.get(id=quoteId)
    updateQ.quoter = request.POST['updatedQuoter']
    updateQ.message = request.POST['updatedMessage']
    updateQ.save()
    
    return redirect('/dashboard')

def favQuotes(request,quoteId):
    loggedUser = User.manager.get(id=request.session['loggedIn'])
    selectedQuote = Quotes.manager.get(id=quoteId)
    print('*************************************************************')
    print(f"Adding favorite quote to logged in user :{loggedUser.userName}")
    print('************************************************************')
    print(f'this is the Quote you want to add: {selectedQuote.message}')
    print('******************************************************')
    loggedUser.quotes_liked.add(selectedQuote)
    print('******************************************************')
    print(f'These are the quotes the login user likes : {loggedUser.quotes_liked.all()}')
    return redirect('/dashboard')