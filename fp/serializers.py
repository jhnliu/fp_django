from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):

    appearance = serializers.ListField(allow_null=True)
    tips = serializers.ListField(allow_null=True)


    class Meta:
        model = Food
        fields = ('ID',
                  'food_id',
                  'engName',
                  'chiName',
                  'label',
                  'food_type',
                  'appearance',
                  'protein',
                  'fat',
                  'fibre',
                  'iron',
                  'iodine',
                  'magnesium',
                  'potassium',
                  'sodium',
                  'vitamin_b2', 
                  'vitamin_b12',
                  'vitamin_c',
                  'calcium',
                  'zinc',
                  'vitamin_a',
                  'tips',
                #   'variety', # add this https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
                #   'origin' # Need to declare a regular serializer for nested/list objects
                  )
        depth = 1