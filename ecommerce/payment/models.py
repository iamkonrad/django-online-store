from django.db import models
from django.contrib.auth.models import User
from store.models import Product


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

                       # Foreign key, one_to many relationship                                                          #a user can have multiple shipping addresses, each shipping
                                                                                                                        #address belongs to one user ONLY

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)                                      #cascade= when user deletes his account shipping details get
                                                                                                                        #removed;guest checkouts allowed


    #user = models.ForeignKey(User, on_delete=models.CASCADE)                                                           #NO GUEST CHECKOUTS (if needed)

    class Meta:                                                                                                         #helps to determine the plural of "Shipping Address"
        verbose_name_plural = 'Shipping Address'


    def __str__(self):                                                                                                  #instead of shipping address 1,2 shipping address will
        return 'Shipping Address -' +str(self.id)                                                                       #be created based on the PK Shipping address-1,-2,etc.


class Order(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    shipping_address = models.TextField(max_length=10000)

    amount_paid = models.DecimalField(max_digits=8,decimal_places=2)                                                    #total amount

    date_ordered = models.DateTimeField(auto_now_add=True)                                                              #will automatically add the order date

                            #Foreign key

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,  blank=True)                                    #represents the  user who placed the order, one to many, one user
                                                                                                                        #many orders; user an intermediary field


    def __str__(self):                                                                                                  #orders will get displayed as Order -# 1 instead of Order (1)

        return 'Order - #' + str(self.id)



class OrderItem(models.Model):

                              #Foreign keys

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)                                               #order items linked to order class, multiple items linked to one order

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)                                           #multiple order item objects can be associated with one product


    quantity = models.PositiveBigIntegerField(default=1)

    price = models.DecimalField(max_digits=8,decimal_places=2)                                                          #price per quantity of items, not the total amount


                               #Foreign key

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):                                                                                                  #orders displayed as Order -# 1 instead of Order (1)

        return 'Order Item - #' + str(self.id)