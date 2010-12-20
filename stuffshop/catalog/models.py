from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()
    price = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    images = generic.GenericRelation('ProductImage')
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('catalog.views.details',[self.slug])

class Phone(Product):
    NUM_OF_SIM = ((1,'1'),(2,'2'),(3,'3'))
    num_of_sim = models.IntegerField(default=1,choices=NUM_OF_SIM)
    has_wifi  = models.BooleanField(default=False)
    has_gps = models.BooleanField(default=False)

class ProductImage(models.Model):
    product_id = models.ForeignKey(Product)
    image = models.ImageField(upload_to="ProductImages/%s"%(product_id))
    is_main_picture = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        #if there's no main picture set this to be that
        if len(ProductImage.objects.filter(product_id=self.product_id,is_main_picture=True))!=1:
            self.is_main_picture = True
        #if there's another main picture, unset it
        if self.is_main_picture:
            ProductImage.objects.filter(product_id=self.product_id).update(is_main_picture=False)
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = "ProductImages/%s/" % (self.product_id.slug)
        super(ProductImage,self).save(*args, **kwargs)


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    def __unicode__(self):
        return self.tag