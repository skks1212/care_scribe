# Generated by Django 4.2.10 on 2024-04-12 14:11

import care_scribe.models.scribe
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ScribeFile",
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
                (
                    "external_id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
                ),
                ("name", models.CharField(max_length=2000)),
                ("internal_name", models.CharField(max_length=2000)),
                ("associating_id", models.CharField(max_length=100)),
                (
                    "file_category",
                    models.CharField(
                        choices=[
                            ("UNSPECIFIED", "UNSPECIFIED"),
                            ("XRAY", "XRAY"),
                            ("AUDIO", "AUDIO"),
                            ("IDENTITY_PROOF", "IDENTITY_PROOF"),
                        ],
                        default="UNSPECIFIED",
                        max_length=100,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True, db_index=True, null=True),
                ),
                (
                    "modified_date",
                    models.DateTimeField(auto_now=True, db_index=True, null=True),
                ),
                ("upload_completed", models.BooleanField(default=False)),
                ("deleted", models.BooleanField(db_index=True, default=False)),
                (
                    "file_type",
                    models.IntegerField(
                        choices=[(0, "Other"), (1, "Scribe")], default=1
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Scribe",
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
                (
                    "external_id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
                ),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True, db_index=True, null=True),
                ),
                (
                    "modified_date",
                    models.DateTimeField(auto_now=True, db_index=True, null=True),
                ),
                ("deleted", models.BooleanField(db_index=True, default=False)),
                (
                    "form_data",
                    models.JSONField(
                        blank=True,
                        null=True,
                        validators=[care_scribe.models.scribe.validate_json_schema],
                    ),
                ),
                ("transcript", models.TextField(blank=True, null=True)),
                ("ai_response", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CREATED", "Created"),
                            ("READY", "Ready"),
                            ("GENERATING_TRANSCRIPT", "Generating Transcript"),
                            ("GENERATING_AI_RESPONSE", "Generating Ai Response"),
                            ("COMPLETED", "Completed"),
                            ("FAILED", "Failed"),
                        ],
                        default="CREATED",
                        max_length=50,
                    ),
                ),
                (
                    "requested_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]