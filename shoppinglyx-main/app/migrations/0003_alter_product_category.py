# Generated by Django 4.1.7 on 2023-03-23 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('P', 'Peda'), ('H', 'Halwa'), ('S', 'Shrikhand'), ('SF', 'Sugar Free'), ('DF', 'Dry Fruit'), ('BS', 'Bengali Sweets'), ('NS', 'Natural Sweets')], max_length=2),
        ),
    ]
