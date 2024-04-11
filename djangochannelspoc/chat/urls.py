from django.urls import path
from chat.views import *
urlpatterns = [
    path('', home,name='home'),
    path("signup", signup, name="signup"),
    path("login", logins, name="login"),
    path("logout", logouts, name="logout"),
    path("autosuggest", autosuggest, name="autosuggest"),
    path("chat/<int:to_user_id>", chat, name="chat"),
]