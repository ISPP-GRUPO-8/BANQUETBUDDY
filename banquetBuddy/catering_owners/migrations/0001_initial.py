# Generated by Django 4.2.7 on 2024-03-18 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catering_particular', '0001_initial'),
        ('catering_employees', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CateringCompany',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='CateringCompanyusername', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('cif', models.CharField(max_length=20)),
                ('verification_document', models.FileField(upload_to='verification_documents/')),
                ('is_verified', models.BooleanField(default=False)),
                ('service_description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('price_plan', models.CharField(choices=[('BASE', 'Base'), ('PREMIUM', 'Premium'), ('PREMIUM_PRO', 'Premium Pro'), ('NO_SUBSCRIBED', 'No Subscribed')], max_length=50)),
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
                ('cateringcompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cateringCompany', to='catering_owners.cateringcompany')),
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
                ('cateringservice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='catering_owners.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('diet_restrictions', models.CharField(max_length=255)),
                ('cateringcompany', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='catering_owners.cateringcompany')),
                ('cateringservice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menus', to='catering_owners.cateringservice')),
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
                ('cateringcompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='catering_owners.cateringcompany')),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catering_owners.cateringservice')),
                ('employees', models.ManyToManyField(related_name='tasks', to='catering_employees.employee')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='catering_owners.event')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catering_owners.cateringservice')),
                ('particular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catering_particular.particular')),
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
                ('cateringcompany', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plates', to='catering_owners.cateringcompany')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plates', to='catering_owners.menu')),
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
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='catering_owners.cateringservice')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_application', models.DateField(auto_now_add=True)),
                ('state', models.CharField(choices=[('PENDING', 'Pending'), ('IN_REVIEW', 'In Review'), ('ACCEPTED', 'Accepted')], max_length=50)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='catering_employees.employee')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='catering_owners.offer')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='catering_owners.menu'),
        ),
        migrations.AddField(
            model_name='event',
            name='particular',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catering_particular.particular'),
        ),
        migrations.CreateModel(
            name='EmployeeWorkService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cateringservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_work_services', to='catering_owners.cateringservice')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_work_services', to='catering_employees.employee')),
            ],
        ),
        migrations.AddField(
            model_name='cateringcompany',
            name='cuisine_types',
            field=models.ManyToManyField(related_name='catering_companies', to='catering_owners.cuisinetypemodel'),
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.CheckConstraint(check=models.Q(('assignment_date__lt', models.F('expiration_date'))), name='assignment_before_expiration'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='rating_range'),
        ),
    ]
