from django.utils import timezone
import datetime

# Create your models here.
# from django.db import models
from djongo import models

class Variety(models.Model):
    v_engName = models.CharField(max_length=200,blank=False, default='v_engName')
    v_chiName = models.CharField(max_length=200,blank=False, default='v_chiName')
    v_description = models.CharField(max_length=200,blank=False, default='v_description')

    class Meta:
        abstract = True

class Origin(models.Model):
    o_chiName = models.CharField(max_length=200,blank=False, default='o_chiName')
    o_country = models.CharField(max_length=200,blank=False, default='country')
    o_description = models.CharField(max_length=200,blank=False, default='o_description')

    class Meta:
        abstract = True

class Food(models.Model): # The collection name in mongodb will be app_modelname
    _id = models.ObjectIdField()
    ID = models.IntegerField()
    food_id = models.CharField(max_length=70, blank=False, default='food_id')
    food_type = models.CharField(max_length=200,blank=False, default='type')
    engName = models.CharField(max_length=200,blank=False, default='eName')
    chiName = models.CharField(max_length=200,blank=False, default='cName')
    alias = models.CharField(max_length=200,blank=False, default='alias')
    labels = models.CharField(max_length=200,blank=False, default='labels')
    appearance = models.CharField(max_length=200, default='appearance')
    touch = models.CharField(max_length=200, default='touch')
    smell = models.CharField(max_length=200, default='smell')
    sound = models.CharField(max_length=200, default='sound')
    # variety = models.ArrayField(model_container=Variety,
    #                                default=[{
    #                                    'v_engName':'v_engName',
    #                                    'v_chiName':'v_chiName',
    #                                    'variety_description':'v_description'
    #                                }])
    variety = models.ArrayField(model_container=Variety, null=True)
    # origin = models.ArrayField(model_container=Origin,
    #                               default=[{
    #                                   'country':'country',
    #                                   'origin_description':'o_description'
    #                               }])
    origin = models.ArrayField(model_container=Origin, null=True)
    price = models.CharField(max_length=200, default='price')
    

# class Receipe(models.Model):
#     chiName = models.CharField(max_length=70, blank=False, default='receipe_chiName')
#     engName = models.CharField(max_length=70, blank=False, default='receipe_engName')
#     ingredients = models.ManyToManyField(Food)
#     benefit = models.CharField(max_length=70, blank=False, default='benefit')
    # Add cooking steps later

