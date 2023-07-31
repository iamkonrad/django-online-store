from django.urls import path

from . import views                                                                               #in the same directory

from django.contrib.auth import views as auth_views                                               #making use of django's built-in views


urlpatterns = [

        path('register',views.register,name='register'),

        path('email-verification/<str:uidb64><str:token>/', views.email_verification, name='email-verification'),       #making url dynamic

        path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),

        path('email-verification-success', views.email_verification_success, name='email-verification-success'),

        path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),


        path('user-logout',views.user_logout,name='user-logout'),

        path('my-login', views.my_login, name='my-login'),



#DASHBOARD/PROFILE
        path('dashboard',views.dashboard,name='dashboard'),

        path('profile-management', views.profile_management, name='profile-management'),

        path('delete-account', views.delete_account, name='delete-account'),



#PASSWORD MANAGEMENT URLS/VIEWS

        path('reset_password',auth_views.PasswordResetView.as_view(),name='reset_password'),                            #Submitting email form

        path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),              #An email reset password has been sent

        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),    #Password reset link                                                                                                       #Password reset link

        path('reset_password_complete',auth_views.PaswordResetCompleteView.as_view(),name='password_reset_complete'),   #Pasword has been successfully reset

]