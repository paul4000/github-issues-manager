# Generated by Django 2.1.2 on 2019-02-05 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
