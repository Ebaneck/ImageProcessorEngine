# Generated by Django 3.1.7 on 2021-03-24 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageProcessorApp', '0006_auto_20210324_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageprocessormodel',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
