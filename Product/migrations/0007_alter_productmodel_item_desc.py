# Generated by Django 5.0.6 on 2024-08-27 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='item_desc',
            field=models.TextField(max_length=100),
        ),
    ]
