# Generated by Django 5.1.3 on 2024-12-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autohorario', '0003_alter_profile_foto_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='profissional',
            name='funcao',
            field=models.CharField(default='Professor', max_length=255),
            preserve_default=False,
        ),
    ]
