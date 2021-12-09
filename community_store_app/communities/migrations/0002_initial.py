# Generated by Django 4.0 on 2021-12-09 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0001_initial'),
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member'),
        ),
        migrations.AddField(
            model_name='product',
            name='basket_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.basket'),
        ),
        migrations.AddField(
            model_name='product',
            name='community_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='communities.community'),
        ),
        migrations.AddField(
            model_name='product',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member'),
        ),
        migrations.AddField(
            model_name='membership',
            name='community_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='communities.community'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member'),
        ),
    ]
