# Generated by Django 2.0.3 on 2018-03-26 05:31

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('query', models.TextField()),
                ('tweet_volume', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_at_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('text', models.TextField()),
                ('id', models.TextField(primary_key=core.models.Trend, serialize=False)),
                ('polarity', models.FloatField()),
                ('subjectivity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_at_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
