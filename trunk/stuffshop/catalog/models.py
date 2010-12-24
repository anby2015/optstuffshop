# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel
# Create your models here.



from django.contrib.contenttypes.models import ContentType

class InheritanceCastModel(models.Model):
    """
    An abstract base class that provides a ``real_type`` FK to ContentType.

    For use in trees of inherited models, to be able to downcast
    parent instances to their child types.

    """
    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(InheritanceCastModel, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True




class Product(InheritanceCastModel):
    title = models.CharField(max_length=30,verbose_name='Название')
    slug = models.SlugField(editable=False,unique=True)
    menu_node_id = models.ForeignKey('MenuNode', null=True, blank=True, related_name='products',verbose_name='Раздел')
    price = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='Цена')
    is_special=models.BooleanField(default=False,verbose_name='Спец. акция')
    date = models.DateField(auto_now_add=True)
    description = models.TextField(verbose_name='Описание')
    weight = 0
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_main_image(self):
        return ProductImage.objects.filter(product_id=self.id,is_main=True)[0]

    def get_short_description(self):
        return []

    def get_price(self):
        return self.price*2
    @models.permalink
    def get_absolute_url(self):
        return ('catalog.views.details',[self.slug,])




class Phone(Product):
    NUM_OF_SIM = ((1,'1'),(2,'2'),(3,'3'))
    num_of_sim = models.IntegerField(default=1,choices=NUM_OF_SIM,verbose_name='Количество сим-карт')
    has_wifi = models.BooleanField(default=False,verbose_name='Наличие wi-fi')
    has_bluetooth = models.BooleanField(default=False,verbose_name='Наличие bluetooth')
    has_touchscreen = models.BooleanField(default=False,verbose_name='Наличие Touchscreen')
    has_gps = models.BooleanField(default=False,verbose_name='Наличие GPS')
    has_tv = models.BooleanField(default=False)
    features = models.CharField(max_length=80,null=True, verbose_name='особенности(разделять запятыми)')
    weight = 0.25
    def get_short_description(self):
        list = []
        if self.num_of_sim == 2:
            list.append(u'2 SIM-карты')
        if self.num_of_sim == 3:
            list.append(u'3 SIM-карты')
        if self.has_wifi: list.append(u'Wifi')
        if self.has_bluetooth: list.append(u'bluetooth')
        if self.has_touchscreen: list.append(u'Touchscreen')
        if self.has_gps: list.append(u'GPS')
        if self.has_tv: list.append(u'TV')
        if self.features: list.extend(self.features.split(','))
        return list



class ProductImage(models.Model):
    product_id = models.ForeignKey(Product,related_name='images')
    image = models.ImageField(upload_to='product-images/',verbose_name='Изображение')
    is_main = models.BooleanField(default=False,verbose_name='Основная картинка')

    def __unicode__(self):
        return "%s id%d" % (self.product_id.title, self.id)

    def save(self, *args, **kwargs):
        #if there's no main picture set this to be that
        if len(ProductImage.objects.filter(product_id=self.product_id,is_main=True))!=1:
            self.is_main = True
        #if there's another main picture, unset it
        if self.is_main:
            ProductImage.objects.filter(product_id=self.product_id).update(is_main=False)
        #save image to specified directory
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = "product-images/%s/" % (self.product_id.slug)
        super(ProductImage,self).save(*args, **kwargs)


class MenuNode(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name
    @models.permalink

    def get_absolute_url(self):
        return ('catalog.views.catalog',[self.id,])