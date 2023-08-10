# Generated by Django 4.0.4 on 2022-06-24 21:06

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'Admins'), (2, 'Staff'), (3, 'student')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='liste_filtrer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodeE', models.TextField(max_length=255)),
                ('Nom', models.CharField(max_length=255)),
                ('Prenom', models.CharField(max_length=255)),
                ('Photo', models.ImageField(upload_to='')),
                ('Module', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ListePresence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Code_Etudiant', models.TextField(max_length=255)),
                ('Nom', models.CharField(max_length=255)),
                ('id_ens', models.TextField(max_length=255)),
                ('Prenom', models.CharField(max_length=255)),
                ('Photo', models.ImageField(upload_to='')),
                ('Temps', models.TimeField(auto_now_add=True)),
                ('Date', models.DateField(auto_now_add=True)),
                ('Modulen', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Etudiant_id', models.TextField(max_length=255)),
                ('Nom', models.CharField(max_length=255)),
                ('Enseignant_id', models.TextField(max_length=255)),
                ('Prenom', models.CharField(max_length=255)),
                ('Photo', models.ImageField(upload_to='')),
                ('Temps', models.TimeField(auto_now_add=True)),
                ('Date', models.DateField(auto_now_add=True)),
                ('Module_num', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('Module_id', models.AutoField(primary_key=True, serialize=False)),
                ('NomModule', models.CharField(max_length=255)),
                ('DateCreation', models.DateTimeField(auto_now_add=True)),
                ('DateModification', models.DateTimeField(auto_now_add=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiants',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('CodeApogee', models.TextField(max_length=255)),
                ('Adresse', models.TextField(max_length=255)),
                ('Genre', models.CharField(max_length=255)),
                ('profile', models.ImageField(upload_to='')),
                ('Date_naissance', models.DateField()),
                ('DateCreation', models.DateTimeField(auto_now_add=True)),
                ('DateModification', models.DateTimeField(auto_now_add=True)),
                ('admin_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('CodeEnseignant', models.AutoField(primary_key=True, serialize=False)),
                ('Adresse', models.TextField(max_length=255)),
                ('Genre', models.CharField(max_length=255)),
                ('DateCreation', models.DateTimeField(auto_now_add=True)),
                ('DateModification', models.DateTimeField(auto_now_add=True)),
                ('admin_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArchiverListePresence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('DateArchive', models.CharField(max_length=255)),
                ('StatusArchive', models.BooleanField(default=False)),
                ('cree_a', models.DateTimeField(auto_now_add=True)),
                ('mise_a_jour_a', models.DateTimeField(auto_now_add=True)),
                ('Etudiants_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.etudiants')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('CleAdmin', models.AutoField(primary_key=True, serialize=False)),
                ('DateCreation', models.DateTimeField(auto_now_add=True)),
                ('DateModification', models.DateTimeField(auto_now_add=True)),
                ('admin_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]