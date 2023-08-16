# Generated by Django 4.0.10 on 2023-08-16 08:18

import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models

import tests.testapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyTestPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "char_array",
                                wagtail.blocks.ListBlock(wagtail.blocks.CharBlock()),
                            ),
                            (
                                "int_array",
                                wagtail.blocks.ListBlock(wagtail.blocks.IntegerBlock()),
                            ),
                            (
                                "struct",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(max_length=100),
                                        ),
                                        (
                                            "item",
                                            wagtail.blocks.StructBlock(
                                                [
                                                    (
                                                        "label",
                                                        wagtail.blocks.CharBlock(),
                                                    ),
                                                    (
                                                        "value",
                                                        wagtail.blocks.IntegerBlock(),
                                                    ),
                                                ]
                                            ),
                                        ),
                                        (
                                            "items",
                                            wagtail.blocks.ListBlock(
                                                tests.testapp.models.MyBlockItem
                                            ),
                                        ),
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            "rich_text",
                                            wagtail.blocks.RichTextBlock(
                                                required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            ("page", wagtail.blocks.PageChooserBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                            (
                                "document",
                                wagtail.documents.blocks.DocumentChooserBlock(),
                            ),
                            ("rich_text", wagtail.blocks.RichTextBlock()),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PageWithNestedStreamBlock",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "inner_stream",
                                wagtail.blocks.StreamBlock(
                                    [
                                        (
                                            "struct_block",
                                            wagtail.blocks.StructBlock(
                                                [
                                                    (
                                                        "title",
                                                        wagtail.blocks.CharBlock(
                                                            max_length=100
                                                        ),
                                                    ),
                                                    (
                                                        "item",
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "label",
                                                                    wagtail.blocks.CharBlock(),
                                                                ),
                                                                (
                                                                    "value",
                                                                    wagtail.blocks.IntegerBlock(),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                    (
                                                        "items",
                                                        wagtail.blocks.ListBlock(
                                                            tests.testapp.models.MyBlockItem
                                                        ),
                                                    ),
                                                    (
                                                        "image",
                                                        wagtail.images.blocks.ImageChooserBlock(
                                                            required=False
                                                        ),
                                                    ),
                                                    (
                                                        "rich_text",
                                                        wagtail.blocks.RichTextBlock(
                                                            required=False
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ),
                                        ("char_block", wagtail.blocks.CharBlock()),
                                    ]
                                ),
                            )
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PageWithSimpleStructBlockNested",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "inner_stream",
                                wagtail.blocks.StreamBlock(
                                    [
                                        (
                                            "simple_struct_block",
                                            wagtail.blocks.StructBlock(
                                                [
                                                    (
                                                        "text",
                                                        wagtail.blocks.CharBlock(),
                                                    ),
                                                    (
                                                        "number",
                                                        wagtail.blocks.IntegerBlock(),
                                                    ),
                                                    (
                                                        "boolean",
                                                        wagtail.blocks.BooleanBlock(),
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PageWithStreamBlock",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "struct_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(max_length=100),
                                        ),
                                        (
                                            "item",
                                            wagtail.blocks.StructBlock(
                                                [
                                                    (
                                                        "label",
                                                        wagtail.blocks.CharBlock(),
                                                    ),
                                                    (
                                                        "value",
                                                        wagtail.blocks.IntegerBlock(),
                                                    ),
                                                ]
                                            ),
                                        ),
                                        (
                                            "items",
                                            wagtail.blocks.ListBlock(
                                                tests.testapp.models.MyBlockItem
                                            ),
                                        ),
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            "rich_text",
                                            wagtail.blocks.RichTextBlock(
                                                required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            ("char_block", wagtail.blocks.CharBlock()),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PageWithStreamBlockInListBlock",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "list_block",
                                wagtail.blocks.ListBlock(
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "struct_block",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(
                                                                max_length=100
                                                            ),
                                                        ),
                                                        (
                                                            "item",
                                                            wagtail.blocks.StructBlock(
                                                                [
                                                                    (
                                                                        "label",
                                                                        wagtail.blocks.CharBlock(),
                                                                    ),
                                                                    (
                                                                        "value",
                                                                        wagtail.blocks.IntegerBlock(),
                                                                    ),
                                                                ]
                                                            ),
                                                        ),
                                                        (
                                                            "items",
                                                            wagtail.blocks.ListBlock(
                                                                tests.testapp.models.MyBlockItem
                                                            ),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                        (
                                                            "rich_text",
                                                            wagtail.blocks.RichTextBlock(
                                                                required=False
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            ("char_block", wagtail.blocks.CharBlock()),
                                        ]
                                    )
                                ),
                            )
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="PageWithStreamBlockInStructBlock",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "struct_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "inner_stream",
                                            wagtail.blocks.StreamBlock(
                                                [
                                                    (
                                                        "struct_block",
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "title",
                                                                    wagtail.blocks.CharBlock(
                                                                        max_length=100
                                                                    ),
                                                                ),
                                                                (
                                                                    "item",
                                                                    wagtail.blocks.StructBlock(
                                                                        [
                                                                            (
                                                                                "label",
                                                                                wagtail.blocks.CharBlock(),
                                                                            ),
                                                                            (
                                                                                "value",
                                                                                wagtail.blocks.IntegerBlock(),
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ),
                                                                (
                                                                    "items",
                                                                    wagtail.blocks.ListBlock(
                                                                        tests.testapp.models.MyBlockItem
                                                                    ),
                                                                ),
                                                                (
                                                                    "image",
                                                                    wagtail.images.blocks.ImageChooserBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                                (
                                                                    "rich_text",
                                                                    wagtail.blocks.RichTextBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                    (
                                                        "char_block",
                                                        wagtail.blocks.CharBlock(),
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
