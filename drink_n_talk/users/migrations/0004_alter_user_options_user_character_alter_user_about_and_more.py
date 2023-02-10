# Generated by Django 4.0 on 2023-02-10 17:17

from django.db import migrations, models
import spare.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_about_alter_user_birth_day'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id',), 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.AddField(
            model_name='user',
            name='character',
            field=models.IntegerField(choices=[(0, 'Слушать'), (1, 'Говорить')], default=0, verbose_name='слушатель/говорун'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, max_length=254, verbose_name='о себе'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.DateField(validators=[spare.validators.validate_birthday], verbose_name='день рождения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='degree',
            field=models.IntegerField(choices=[(0, 'Безалкогольное'), (1, 'Слабоалкогольное'), (2, 'Крепкое')], verbose_name='степень алкогольности'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='default_user.jpg', upload_to='users_photos', verbose_name='аватар'),
        ),
    ]
