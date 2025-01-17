# Generated by Django 3.0.5 on 2020-12-14 10:51

from django.db import migrations, models
import djongo.models.fields
import fp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('id', models.IntegerField()),
                ('food_id', models.CharField(default='food_id', max_length=70)),
                ('food_type', models.CharField(default='type', max_length=200)),
                ('engName', models.CharField(default='eName', max_length=200)),
                ('chiName', models.CharField(default='cName', max_length=200)),
                ('alias', models.CharField(default='alias', max_length=200)),
                ('labels', models.CharField(default='labels', max_length=200)),
                ('appearance', models.CharField(default='appearance', max_length=200)),
                ('touch', models.CharField(default='touch', max_length=200)),
                ('smell', models.CharField(default='smell', max_length=200)),
                ('sound', models.CharField(default='sound', max_length=200)),
                ('variety', djongo.models.fields.ArrayField(model_container=fp.models.Variety, null=True)),
                ('origin', djongo.models.fields.ArrayField(model_container=fp.models.Origin, null=True)),
                ('price', models.CharField(default='price', max_length=200)),
            ],
        ),
    ]
