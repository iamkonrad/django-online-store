from django.db import models

from django.contrib.auth.models import User


class ShippingAddress(models.Model):

    full_name=models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    address1 = models.CharField(max_length=300)

    address2 = models.CharField(max_length=300)                                                                         #2nd address for more flexibility in case there is more
                                                                                                                        #space needed
    city = models.CharField(max_length=255)

    postal_code = models.CharField(max_length=255)



    #optional

    state = models.CharField(max_length=255, null=True, blank=True)


    # Foreign key, one_to many relationship                                                                             #a user can have multiple shipping addresses, each shipping
                                                                                                                        #address belong to one user ONLY


    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)                                      #cascade= when user deletes his account shipping gets removed
                                                                                                                        #guest checkouts allowed


    #user = models.ForeignKey(User, on_delete=models.CASCADE)                                                           #NO GUEST CHECKOUTS

    class Meta:                                                                                                         #helps to determine the plural of "Shipping Address"
        verbose_name_plural = 'Shipping Address'


    def __str__(self):                                                                                                  #instead of shipping address 1,2 shipping address will be
                                                                                                                        #created based on the PK Shipping address-1,-2,etc.
        return 'Shipping Address -' +str(self.id)