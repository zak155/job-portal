from django.urls import path
from . import views
urlpatterns = [
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('verify-account/',views.verify_account,name="verify-account"),
    path('forgot-password/',views.send_password_reset_link,name="reset-password"),
    path('verify-reset-password-link',views.verifyReset,name="verify-reset"),
    path('set-new-password',views.set_new_passsword_using_reset_link,name="set_new_passsword")
]
