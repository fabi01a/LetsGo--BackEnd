from rest_framework import routers
from facilities.user.viewsets import UserViewSet
from facilities.auth.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet


# routes = SimpleRouter()
routes = routers.DefaultRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    *routes.urls
]
