import pytest
import wagtail_factories

from tests.testapp.models import PageWithStreamBlock

pytestmark = pytest.mark.django_db


@pytest.fixture()
def page_factory_factory():
    """
    Returns a function that generates a page factory class
    """

    def get_page_factory(stream_field_factory_defaults=None):
        """
        Create a page factory class with optional stream field defaults
        """

        class Factory(wagtail_factories.PageFactory):
            body = wagtail_factories.StreamFieldFactory(
                default_block_values=stream_field_factory_defaults or {}
            )

            class Meta:
                model = PageWithStreamBlock

        return Factory

    return get_page_factory


def test_generate_stream_block_factory(page_factory_factory):
    """
    The generated stream block factory should be a subclass of wagtail_factories.StreamBlockFactory
    """
    page_factory = page_factory_factory()
    assert page_factory.body.stream_block_factory is None
    page_factory.build()
    assert issubclass(
        page_factory.body.stream_block_factory, wagtail_factories.StreamBlockFactory
    )


def test_generate_stream_block_factory_with_stream_field_defaults(page_factory_factory):
    """
    The generated stream block factory should use the default values from the stream field factory
    """
    page_factory = page_factory_factory(
        stream_field_factory_defaults={
            "0__char_block": "char block value",
            "1__struct_block__title": "struct block title",
            "1__struct_block__item__label": "struct block item label",
            "1__struct_block__item__value": 42,
            "1__struct_block__items__0__label": "struct block items label",
            "1__struct_block__items__0__value": 43,
        }
    )
    instance = page_factory.build()
    stream_block_factory = page_factory.body.stream_block_factory

    assert stream_block_factory is not None
    assert issubclass(
        stream_block_factory.char_block.get_factory(),
        wagtail_factories.CharBlockFactory,
    )
    assert issubclass(
        stream_block_factory.struct_block.get_factory(),
        wagtail_factories.StructBlockFactory,
    )
    assert issubclass(
        stream_block_factory.struct_block.get_factory().title.get_factory(),
        wagtail_factories.CharBlockFactory,
    )

    assert instance.body[0].block_type == "char_block"
    assert instance.body[0].value == "char block value"
    assert instance.body[1].block_type == "struct_block"
    assert instance.body[1].value["title"] == "struct block title"
    assert instance.body[1].value["item"]["label"] == "struct block item label"
    assert instance.body[1].value["item"]["value"] == 42
    assert instance.body[1].value["items"][0]["label"] == "struct block items label"
    assert instance.body[1].value["items"][0]["value"] == 43


def test_registry_populated_with_generated_factory(page_factory_factory):
    """
    The registry should be populated with the generated factory after the first build
    """
    from tests.testapp.models import MyStreamBlock

    registry = wagtail_factories.generator._registry
    if MyStreamBlock in registry:
        del registry[MyStreamBlock]
    assert MyStreamBlock not in registry

    page_factory = page_factory_factory()
    page_factory.build()
    assert MyStreamBlock in registry
    assert registry[MyStreamBlock] is page_factory.body.stream_block_factory
