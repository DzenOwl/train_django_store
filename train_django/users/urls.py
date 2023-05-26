from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(next_page='index'), name='login'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    # UpdateView всегда работает с конкретным объектом, передаём PrimaryKey (UserID)
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('verify/<str:username>/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
