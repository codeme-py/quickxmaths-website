from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from QuickXMaths import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("accounts/register/", views.register_user, name="register"),
    path("accounts/login/", views.login_user, name="login"),
    path('accounts/logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path("accounts/verify-otp/", views.verify_otp, name="verify-otp"),
    path("accounts/verify-email/", views.verify_email, name="verify-email"),
    path("accounts/forgot-password/", views.forgot_password, name="forgot-password"),
    path("accounts/reset-password/", views.reset_password, name="reset-password"),
    path("apidata/<str:service>/<str:data>", views.post_recent, name="post-recent")
    #path("play/", views.play, name="play"),
]


