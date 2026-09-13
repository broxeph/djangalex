"""
Clean up after removing django-registration-redux and django.contrib.sites.

Their tables, migration records and content types (with permissions) are
dropped. Every statement is safe on a database that never had them.
"""
from django.db import migrations

REMOVED_APPS = ['registration', 'sites']


def remove_stale_content_types(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ContentType.objects.filter(app_label__in=REMOVED_APPS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_subtitle_author'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL(
            [
                'DROP TABLE IF EXISTS registration_supervisedregistrationprofile',
                'DROP TABLE IF EXISTS registration_registrationprofile',
                'DROP TABLE IF EXISTS django_site',
                "DELETE FROM django_migrations WHERE app IN ('registration', 'sites')",
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunPython(remove_stale_content_types, migrations.RunPython.noop),
    ]
