# Generated by Django 5.0.6 on 2024-08-23 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categrory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Mobile', 'Mobile'), ('Tablet', 'Tablet'), ('Laptop', 'Laptop'), ('Watch', 'Watch'), ('Gadget', 'Gadget'), ('Speaker', 'Speaker'), ('Accessories', 'Accessories'), ('Computer', 'Computer')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('categrory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.categrory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='assets/img/')),
                ('item_title', models.CharField(max_length=100)),
                ('item_desc', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('item_discount_price', models.IntegerField(default=0)),
                ('Trending_product', models.BooleanField(default=False, help_text='@-default,1-Trending')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.brand')),
                ('categrory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.categrory')),
            ],
        ),
    ]
