# Generated by Django 4.0.5 on 2022-06-20 09:59

from django.db import migrations, models
import django.db.models.deletion
import tests.testapp.models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageWithNestedStreamBlock',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('inner_stream', wagtail.blocks.StreamBlock([('struct_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100)), ('item', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('value', wagtail.blocks.IntegerBlock())])), ('items', wagtail.blocks.ListBlock(tests.testapp.models.MyBlockItem)), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('char_block', wagtail.blocks.CharBlock())]))], use_json_field=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PageWithStreamBlock',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('struct_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100)), ('item', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('value', wagtail.blocks.IntegerBlock())])), ('items', wagtail.blocks.ListBlock(tests.testapp.models.MyBlockItem)), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('char_block', wagtail.blocks.CharBlock())], use_json_field=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PageWithStreamBlockInListBlock',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('list_block', wagtail.blocks.ListBlock(wagtail.blocks.StreamBlock([('struct_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100)), ('item', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('value', wagtail.blocks.IntegerBlock())])), ('items', wagtail.blocks.ListBlock(tests.testapp.models.MyBlockItem)), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('char_block', wagtail.blocks.CharBlock())])))], use_json_field=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PageWithStreamBlockInStructBlock',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('struct_block', wagtail.blocks.StructBlock([('inner_stream', wagtail.blocks.StreamBlock([('struct_block', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100)), ('item', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('value', wagtail.blocks.IntegerBlock())])), ('items', wagtail.blocks.ListBlock(tests.testapp.models.MyBlockItem)), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('char_block', wagtail.blocks.CharBlock())]))]))], use_json_field=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='mytestpage',
            name='body',
            field=wagtail.fields.StreamField([('char_array', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock())), ('int_array', wagtail.blocks.ListBlock(wagtail.blocks.IntegerBlock())), ('struct', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100)), ('item', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('value', wagtail.blocks.IntegerBlock())])), ('items', wagtail.blocks.ListBlock(tests.testapp.models.MyBlockItem)), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=None),
        ),
    ]
