from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Food
        fields = ('food_id',
                  'engName',
                  'chiName',
                  'food_type',
                  'appearance',
                  'price',
                #   'variety', # add this https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
                #   'origin' # Need to declare a regular serializer for nested/list objects
                  )
        depth = 1