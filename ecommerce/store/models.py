from django.db import models
from django.urls import reverse


#1.category, shorts, shoes, pants etc., all unique
class Category(models.Model):

    name=models.CharField(max_length=250,db_index=True)                                                                 #db index to make looking for it faster

    slug=models.SlugField(max_length=250,unique=True)                                                                   #unique cause only one category for every product

    class Meta:
        verbose_name_plural = 'categories'                                                                              #django by default adds an s to category name


    def __str__(self):                                                                                                  #category name returned as a string
        return self.name

    def get_absolute_url(self):                                                                                         #dynamic links for categories
        return reverse('list-category',args=[self.slug])



class Product(models.Model):

    category = models.ForeignKey(Category, related_name='product',on_delete=models.CASCADE, null=True)                  #linking category and product through a fk, will add category to products
                                                                                                                        #deleting a category deletes all the associated products
    title=models.CharField(max_length=250)

    brand=models.CharField(max_length=250,default='un-branded')

    description= models.TextField(blank=True)                                                                           #blank denotes an optional field

    slug=models.SlugField(max_length=255)                                                                               #to make urls more user-friendly and readable/unique

    price=models.DecimalField(max_digits=5,decimal_places=2)                                                            #product price

    image = models.ImageField(upload_to='images/')                                                                      #upon uploading an image will create an image subfolder in media (pillow rqd)

    tags = models.ManyToManyField('Tag', related_name='product_tags', blank=True)                                       #MANY TO MANY RELATIONSHIP with tags,acting as an intermediary


    class Meta:
        verbose_name_plural = 'products'                                                                                #django by default adds an s to category name

    def __str__(self):
        return self.title                                                                        #(products referenced by their correct title instead of product1, or product2)


#dynamic links for products
    def get_absolute_url(self):

        return reverse('product-info',args=[self.slug])

class Tag(models.Model):                                                                                                # Many to many relationship with products class
    tag_name = models.CharField(max_length=128,unique=True)
    tag_slug = models.SlugField(max_length=255, unique=True)                                                            # BEST SELLERS, NEW ARRIVALS

    def __str__(self):
        return self.tag_name
