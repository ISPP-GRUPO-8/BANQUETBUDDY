# Generated by Django 4.2.7 on 2024-03-11 18:33

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
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
            name='CateringService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CuisineTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MEDITERRANEAN', 'Mediterránea'), ('ORIENTAL', 'Oriental'), ('MEXICAN', 'Mexicana'), ('ITALIAN', 'Italiana'), ('FRENCH', 'Francesa'), ('SPANISH', 'Española'), ('INDIAN', 'India'), ('CHINESE', 'China'), ('JAPANESE', 'Japonesa'), ('THAI', 'Tailandesa'), ('GREEK', 'Griega'), ('LEBANESE', 'Libanesa'), ('TURKISH', 'Turca'), ('KOREAN', 'Coreana'), ('VIETNAMESE', 'Vietnamita'), ('AMERICAN', 'Americana'), ('BRAZILIAN', 'Brasileña'), ('ARGENTINE', 'Argentina'), ('VEGETARIAN', 'Vegetariana'), ('VEGAN', 'Vegana'), ('GLUTEN_FREE', 'Sin Gluten'), ('SEAFOOD', 'Mariscos'), ('BBQ', 'Barbacoa'), ('FAST_FOOD', 'Comida Rápida'), ('FUSION', 'Fusión'), ('TRADITIONAL', 'Tradicional'), ('ORGANIC', 'Orgánica'), ('GOURMET', 'Gourmet')], max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('details', models.TextField()),
                ('booking_state', models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('CONTRACT_PENDING', 'Contract Pending'), ('CANCELLED', 'Cancelled')], max_length=50)),
                ('number_guests', models.IntegerField()),
                ('cateringservice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='core.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('diet_restrictions', models.CharField(max_length=255)),
                ('cateringservice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menus', to='core.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('assignment_date', models.DateField()),
                ('assignment_state', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], max_length=50)),
                ('expiration_date', models.DateField()),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=50)),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cateringservice')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='core.event')),
            ],
        ),
        migrations.CreateModel(
            name='CateringCompany',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='CateringCompanyusername', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('service_description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos_catering/')),
                ('is_verified', models.BooleanField(default=False)),
                ('price_plan', models.CharField(choices=[('BASE', 'Base'), ('PREMIUM', 'Premium'), ('PREMIUM_PRO', 'Premium Pro'), ('NO_SUBSCRIBED', 'No Subscribed')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='EmployeeUsername', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('profession', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=255)),
                ('skills', models.CharField(max_length=255)),
                ('english_level', models.CharField(choices=[('C2', 'C2'), ('C1', 'C1'), ('B2', 'B2'), ('B1', 'B1'), ('A2', 'A2'), ('A1', 'A1'), ('NONE', 'None')], default='NINGUNO', max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('curriculum', models.BinaryField(blank=True, null=True)),
                ('recommendation_letter', models.BinaryField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Particular',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ParticularUsername', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('preferences', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('is_subscribed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='plates_images/')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plates', to='core.menu')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='core.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('content', models.TextField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_application', models.DateField()),
                ('state', models.CharField(choices=[('PENDING', 'Pending'), ('IN_REVIEW', 'In Review'), ('ACCEPTED', 'Accepted')], max_length=50)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='core.offer')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeWorkService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_work_services', to='core.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='TaskEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_employees', to='core.task')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_employees', to='core.employee')),
            ],
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.CheckConstraint(check=models.Q(('assignment_date__lt', models.F('expiration_date'))), name='assignment_before_expiration'),
        ),
        migrations.AddField(
            model_name='review',
            name='particular',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.particular'),
        ),
        migrations.AddField(
            model_name='plate',
            name='cateringcompany',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plates', to='core.cateringcompany'),
        ),
        migrations.AddConstraint(
            model_name='message',
            constraint=models.CheckConstraint(check=models.Q(('sender', models.F('receiver')), _negated=True), name='sender_is_not_receiver'),
        ),
        migrations.AddField(
            model_name='menu',
            name='cateringcompany',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='core.cateringcompany'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='core.employee'),
        ),
        migrations.AddField(
            model_name='event',
            name='particular',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.particular'),
        ),
        migrations.AddField(
            model_name='employeeworkservice',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_work_services', to='core.employee'),
        ),
        migrations.AddField(
            model_name='cateringservice',
            name='cateringcompany',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cateringCompany', to='core.cateringcompany'),
        ),
        migrations.AddField(
            model_name='cateringcompany',
            name='cuisine_types',
            field=models.ManyToManyField(related_name='catering_companies', to='core.cuisinetypemodel'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range'),
        ),
    ]
