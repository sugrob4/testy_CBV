from django.urls import path

from .views import Registration, Logoutauth, Loginauth


urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', Loginauth.as_view(), name='login'),
    path('logout/', Logoutauth.as_view(), name='logout'),
]
