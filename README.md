# django-online-store
Django online store

Some important points about this webapp:

1.USER AUTHORIZATION: 
For security reasons each person using this webapp needs to configure his/her own smtp settings, for now, only an EMAIL_BACKEND using django console handles that, but there are commented out lines in settigns.py (lines 160-166) waiting to be filled with proper data in case there is a need to set profile update/password change/notifications/authorization handled by an smtp server (by default an smtp server is set as google); 


2.IN ORDER TO TEST LOG-IN functionality without turning on smtp server: 1. register an account by clcking register account on the main page of the app and follow with the standard procedure, afterwards log in to admin using superuser, set newly created test account status to ACTIVE(by default it's set to INACTIVE since it needs to be email authorised), from now on you can log in with a newly created test account;


3.CHECKOUT FUNCTIONALITY, similarly to smtp due to security reasons I haven't set this app to handle PayPal checkouts; once you proceed to the checkout and click on order checkout the order will be added to the database where it can afterwards be accessed via admin panel;  there are many reasons for not setting up PayPal integration in my project for the time being(security being one of the most important ones), but in case there is a need for that the relevant functionality can easily be added up in checkout.html and settings.py;
