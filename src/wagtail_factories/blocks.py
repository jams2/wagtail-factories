from collections import defaultdict

import factory
from factory.declarations import ParameteredAttribute
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail_factories.factories import ImageFactory


__all__ = [
    "CharBlockFactory",
    "IntegerBlockFactory",
    "StreamBlockFactory",
    "StreamFieldFactory",
    "ListBlockFactory",
    "StructBlockFactory",
    "ImageChooserBlockFactory",
]


class StreamBlockFactory(factory.Factory):
    class Meta:
        abstract = True

    @classmethod
    def _get_block_factory(cls, block_name):
        """
        Look up the factory associated with block_name in the compound block's
        declaration.
        """
        try:
            return cls._meta.declarations[block_name]
        except KeyError:
            raise ValueError("No factory defined for block `%s`" % block_name)

    @classmethod
    def _get_indexed_mappings(cls, params):
        mappings = defaultdict(lambda: defaultdict(lambda: defaultdict()))

        for key, value in params.items():
            if key.isdigit():
                index, block_name = int(key), value
                mappings[index][block_name] = {}
            else:
                try:
                    index, block_name, param = key.split("__", 2)
                except ValueError:
                    continue
                if not index.isdigit():
                    continue

                index = int(index)
                mappings[index][block_name][param] = value
        return mappings

    @classmethod
    def _generate(cls, strategy, params):
        indexed_mappings = cls._get_indexed_mappings(params)
        stream_data = []
        for index, block_items in sorted(indexed_mappings.items()):
            for block_name, block_params in block_items.items():
                block_factory = cls._get_block_factory(block_name)
                if isinstance(block_factory, ListBlockFactory):
                    stream_data.append((block_name, block_factory(**block_params)))
                elif isinstance(block_factory, factory.SubFactory):
                    inner_factory = block_factory.get_factory()
                    stream_data.append(
                        (block_name, inner_factory.generate(strategy, **block_params))
                    )
                else:
                    stream_data.append(
                        (block_name, block_factory.generate(strategy, **block_params))
                    )

        if cls._meta.model is None:
            # We got an old style definition, so aren't aware of a StreamBlock class for
            # the StreamField's child blocks.
            return stream_data
        return blocks.StreamValue(cls._meta.model(), stream_data)


class StreamFieldFactory(ParameteredAttribute):
    """
    Syntax:
        <streamfield>__<index>__<block_name>__<key>='foo',

    Syntax to generate blocks with default factory values:
        <streamfield>__<index>=<block_name>

    """

    def __init__(self, block_types, **kwargs):
        super().__init__(**kwargs)
        if isinstance(block_types, dict):
            # Old style definition, dict mapping block name -> block factory
            self.stream_block_factory = type(
                "_StreamBlockFactory", (StreamBlockFactory,), block_types
            )
        elif isinstance(block_types, type) and issubclass(
            block_types, StreamBlockFactory
        ):
            self.stream_block_factory = block_types
        else:
            raise TypeError(
                "StreamFieldFactory argument must be a StreamBlockFactory subclass or dict "
                "mapping block names to factories"
            )

    def evaluate(self, instance, step, extra):
        return self.stream_block_factory(**extra)


class ListBlockFactory(factory.SubFactory):
    def __call__(self, **kwargs):
        return self.evaluate(None, None, kwargs)

    def evaluate(self, instance, step, extra):
        subfactory = self.get_factory()

        result = defaultdict(dict)
        for key, value in extra.items():
            if key.isdigit():
                result[int(key)]["value"] = value
            else:
                prefix, label = key.split("__", maxsplit=1)
                if prefix and prefix.isdigit():
                    result[int(prefix)][label] = value

        retval = []
        for index, index_params in sorted(result.items()):
            item = subfactory(**index_params)
            retval.append(item)
        return retval

    def generate(self, step, params):
        # This method was used in factory-boy <3.2 instead of evaluate(), it
        # could be removed when we stop to support this older version.
        return self.evaluate(None, step, params)


class BlockFactory(factory.Factory):
    class Meta:
        abstract = True

    @classmethod
    def _build(cls, model_class, value):
        return model_class().clean(value)

    @classmethod
    def _create(cls, model_class, value):
        return model_class().clean(value)


class CharBlockFactory(BlockFactory):
    class Meta:
        model = blocks.CharBlock


class IntegerBlockFactory(BlockFactory):
    class Meta:
        model = blocks.IntegerBlock


class ChooserBlockFactory(BlockFactory):
    pass


class ImageChooserBlockFactory(ChooserBlockFactory):

    image = factory.SubFactory(ImageFactory)

    class Meta:
        model = ImageChooserBlock

    @classmethod
    def _build(cls, model_class, image):
        return image

    @classmethod
    def _create(cls, model_class, image):
        return image


class StructBlockFactory(factory.Factory):
    class Meta:
        model = blocks.StructBlock

    @classmethod
    def _get_child_block_handler(cls, block_name, block_instance, strategy):
        if block_name in cls._meta.declarations:
            declaration = cls._meta.declarations[block_name]
            if isinstance(declaration, ListBlockFactory):
                return lambda **params: declaration(**params)
            elif isinstance(declaration, factory.Factory):
                return lambda **params: declaration.generate(strategy, **params)
            elif isinstance(declaration, factory.SubFactory):
                wrapped_factory = declaration.get_factory()
                return lambda **params: wrapped_factory.generate(strategy, **params)
            else:
                # It's either a scalar or a non-factory callable
                return lambda: declaration
        else:
            return lambda: block_instance.get_default()

    @staticmethod
    def _get_deep_mappings(params):
        mappings = defaultdict(dict)
        for key, value in params.items():
            block_name, *param = key.split("__", maxsplit=1)
            if param:
                # It's a deep declaration, like block__title
                mappings[block_name][param[0]] = value
        return mappings

    @classmethod
    def _generate(cls, strategy, params):
        block = cls._meta.model()
        deep_mappings = cls._get_deep_mappings(params)

        block_data = []
        for block_name, instance in block.child_blocks.items():
            handler = cls._get_child_block_handler(block_name, instance, strategy)
            if block_name in deep_mappings:
                # The user provided a deep declaration
                block_data.append((block_name, handler(**deep_mappings[block_name])))
            elif block_name in params:
                # User provided a declaration for this level of nesting - a scalar
                block_data.append((block_name, params[block_name]))
            else:
                block_data.append((block_name, handler()))

        return blocks.StructValue(block, block_data)

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return cls._generate(factory.enums.BUILD_STRATEGY, kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._generate(factory.enums.CREATE_STRATEGY)
