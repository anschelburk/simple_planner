# Generated by Django 5.0.6 on 2024-06-17 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_listitem_list_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='listitem',
            name='list_id',
        ),
        migrations.AddField(
            model_name='listitem',
            name='list_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='planner.listname'),
            preserve_default=False,
        ),
    ]
