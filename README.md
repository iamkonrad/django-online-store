# django-online-store
Django online store (written in Django, using HTML and CSS)



https://github.com/iamkonrad/django-online-store/assets/133384502/a8d92d75-29e6-48d7-8aad-4ec9dbaee4a0



## Some important points about this webapp:

1.USER AUTHORIZATION: 
For security reasons each person using this webapp needs to configure his/her own smtp settings, for now, only an EMAIL_BACKEND using django console handles that, but there are commented out lines in settings.py (lines 160-166) waiting to be filled with proper data in case there is a need to set profile update/password change/notifications/authorization handled by an smtp server (by default an smtp server is set to Google); 


2.IN ORDER TO TEST LOG-IN functionality without turning on smtp server: 1. register an account by clicking register account on the main page of the app and follow with the standard procedure, afterwards log-in to admin using superuser, set newly created test account status to ACTIVE(by default it's set to INACTIVE, since it needs to be activated by a link sent to an email address associated with your account), from now on you can log in with a newly created test account;


3.CHECKOUT FUNCTIONALITY, similarly to smtp due to security reasons I haven't set this app to handle PayPal checkouts; once you proceed to the checkout and click on order checkout the order will be added to the database, where it can afterwards be accessed via admin panel, alternatively if you used checkout with a previously logged-in user account (will not work for a guest user) your past orders will now display in your order history;  there are many reasons for not setting up PayPal integration in my project for the time being(security being one of the most important ones), but in case there is a need for that the relevant functionality can easily be added up in checkout.html and settings.py;

## Some key functionalities:

- Fully functional CRUD cart (created in AJAX)
- Order history
- Fully functional searchbar
- Automatic shipping data filling based on the previous orders
- Order history (only for validated and authenticated users)
- PyTests tests (more than 60 different testing scenarios covered) 
- Both guest and authenticated user checkouts enabled
