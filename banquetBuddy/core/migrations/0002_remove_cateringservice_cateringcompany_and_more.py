# Generated by Django 4.2.7 on 2024-03-14 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cateringservice',
            name='cateringcompany',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='employeeworkservice',
            name='cateringservice',
        ),
        migrations.RemoveField(
            model_name='employeeworkservice',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='event',
            name='cateringservice',
        ),
        migrations.RemoveField(
            model_name='event',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='event',
            name='particular',
        ),
        migrations.RemoveField(
            model_name='jobapplication',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='jobapplication',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='cateringcompany',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='cateringservice',
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='cateringservice',
        ),
        migrations.RemoveField(
            model_name='particular',
            name='user',
        ),
        migrations.RemoveField(
            model_name='plate',
            name='cateringcompany',
        ),
        migrations.RemoveField(
            model_name='plate',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='review',
            name='cateringservice',
        ),
        migrations.RemoveField(
            model_name='review',
            name='particular',
        ),
        migrations.RemoveField(
            model_name='task',
            name='cateringcompany',
        ),
        migrations.RemoveField(
            model_name='task',
            name='cateringservice',
        ),
        migrations.RemoveField(
            model_name='task',
            name='employees',
        ),
        migrations.RemoveField(
            model_name='task',
            name='event',
        ),
        migrations.DeleteModel(
            name='CateringCompany',
        ),
        migrations.DeleteModel(
            name='CateringService',
        ),
        migrations.DeleteModel(
            name='CuisineTypeModel',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='EmployeeWorkService',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='JobApplication',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.DeleteModel(
            name='Particular',
        ),
        migrations.DeleteModel(
            name='Plate',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
