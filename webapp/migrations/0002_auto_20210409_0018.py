# Generated by Django 3.1.7 on 2021-04-09 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coffeerecipe',
            old_name='sugar',
            new_name='milk',
        ),
        migrations.AlterField(
            model_name='coffeerecipe',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
