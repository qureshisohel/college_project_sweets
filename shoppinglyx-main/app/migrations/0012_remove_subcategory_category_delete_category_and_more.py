# Generated by Django 4.1.7 on 2023-03-28 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_category_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
