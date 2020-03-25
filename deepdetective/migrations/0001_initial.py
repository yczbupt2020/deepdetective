# Generated by Django 3.0.3 on 2020-03-24 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('username', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(default=None, max_length=45)),
                ('role', models.IntegerField(choices=[(0, 'user')])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=45)),
                ('gender', models.IntegerField(choices=[(0, 'unknown'), (1, 'male'), (2, 'female')])),
            ],
        ),
    ]
