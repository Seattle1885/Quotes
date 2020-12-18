from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('addQuote', views.addQuote),
    path('users/<uploaderId>', views.userPage),
    path('delete/<quoteId>', views.delete),
    path('editQuote/<quoteId>', views.edit),
    path('update/<quoteId>', views.update),
    path('favQuote/<quoteId>', views.favQuotes)
]
