# Generated by Django 4.2.4 on 2024-03-03 15:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(auto_now=True)),
                ("is_customer", models.BooleanField(default=False)),
                (
                    "customer_id",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Customer ID"
                    ),
                ),
                (
                    "mobile_number",
                    models.CharField(
                        max_length=15, null=True, verbose_name="Mobile Number"
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="Date Of Birth"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Men", "Men"),
                            ("Women", "Women"),
                            ("Prefer Not to say", "Prefer Not to say"),
                        ],
                        max_length=25,
                        null=True,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "profile_picture",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="profile/",
                        verbose_name="Profile Picture",
                    ),
                ),
                ("is_suspended", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "ordering": ["-updated_at"],
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="AddressRegister",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(auto_now=True)),
                (
                    "full_name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Full Name"
                    ),
                ),
                (
                    "contact_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Contact Number",
                    ),
                ),
                (
                    "alternative_contact_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Alternative Contact Number",
                    ),
                ),
                (
                    "address_line_1",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="House Address",
                    ),
                ),
                (
                    "address_line_2",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Area Address",
                    ),
                ),
                (
                    "land_mark",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="Landmark"
                    ),
                ),
                (
                    "district",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="District"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="State"
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Country"
                    ),
                ),
                (
                    "pin_code",
                    models.IntegerField(blank=True, null=True, verbose_name="Pincode"),
                ),
                (
                    "address_type",
                    models.CharField(
                        blank=True,
                        choices=[("Billing", "Billing"), ("Shipping", "Shipping")],
                        max_length=10,
                        null=True,
                        verbose_name="Full Name",
                    ),
                ),
                ("is_default", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="useraddress",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
                "abstract": False,
            },
        ),
    ]
