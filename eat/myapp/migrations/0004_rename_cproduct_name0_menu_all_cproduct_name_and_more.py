# Generated by Django 4.2.6 on 2023-10-15 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_menu_all_yellow_pages_csort_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu_all',
            old_name='cProduct_name0',
            new_name='cProduct_name',
        ),
        migrations.RenameField(
            model_name='menu_all',
            old_name='cUnit_price0',
            new_name='cUnit_price',
        ),
        migrations.AddField(
            model_name='menu_all',
            name='cSort_project',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
