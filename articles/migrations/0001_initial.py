# Generated by Django 2.2.6 on 2019-10-28 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_text', models.TextField()),
                ('article_uuid', models.UUIDField()),
            ],
        ),
    ]
