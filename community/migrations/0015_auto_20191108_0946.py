# Generated by Django 2.2.6 on 2019-11-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0014_communitytags_datattypetags_posttags'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitytags',
            name='tagName',
            field=models.CharField(help_text='Enter Community Tag', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='datattypetags',
            name='tagName',
            field=models.CharField(help_text='Enter Datatype Tag', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='posttags',
            name='tagName',
            field=models.CharField(help_text='Enter Post Tag', max_length=200, null=True),
        ),
    ]
