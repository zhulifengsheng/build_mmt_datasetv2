# Generated by Django 3.2.4 on 2022-03-25 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0006_auto_20220325_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fixinfo',
            name='user_obj',
        ),
        migrations.AddField(
            model_name='fixinfo',
            name='username',
            field=models.CharField(default=1, max_length=5, verbose_name='用户名'),
            preserve_default=False,
        ),
    ]