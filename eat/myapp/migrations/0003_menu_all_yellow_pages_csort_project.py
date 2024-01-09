# Generated by Django 4.2.6 on 2023-10-15 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_menu0_menu1_menu2_menu3_menu4_menu5_menu6_menu7_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='menu_all',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cStore_Name', models.CharField(max_length=30)),
                ('cProduct_name0', models.CharField(max_length=100)),
                ('cUnit_price0', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='yellow_pages',
            name='cSort_project',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]