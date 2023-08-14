import inspect
from functools import singledispatch

import factory
from wagtail import blocks as wagtail_blocks

__all__ = [
    "register_block_factory",
    "generate_block_factory",
]


class _Registry:
    _registry = {}

    def __getitem__(self, block_class: type):
        # Look up the factory type for block_class, walking up its MRO
        # until a match is found
        for cls in inspect.getmro(block_class):
            if cls in self._registry:
                return self._registry[cls]
        raise KeyError(
            f"Couldn't find registered factory for class {cls} or its superclasses"
        )

    def __setitem__(self, block_class: type, factory_class: type):
        self._registry[block_class] = factory_class

    def __contains__(self, item):
        return item in self._registry

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def register(self, block):
        def _register(factory):
            self[block] = factory
            return factory

        return _register


_registry = _Registry()
register_block_factory = _registry.register


def generate_block_factory(block):
    if not isinstance(block, wagtail_blocks.StreamBlock):
        raise TypeError("block argument must be a StreamBlock (or subclass)")
    return _generate_block_factory(block, is_top_level=True)


@singledispatch
def _generate_block_factory(block):
    return factory.SubFactory(_registry[type(block)])


@_generate_block_factory.register(wagtail_blocks.StreamBlock)
@_generate_block_factory.register(wagtail_blocks.StructBlock)
def _(block, is_top_level=False):
    attrs = {k: _generate_block_factory(v) for k, v in block.child_blocks.items()}

    factory_class = _registry[type(block)]

    attrs["Meta"] = type("Meta", (), {"model": type(block)})

    block_factory = type(f"{type(block).__name__}Factory", (factory_class,), attrs)
    if is_top_level:
        return block_factory
    return factory.SubFactory(block_factory)


@_generate_block_factory.register(wagtail_blocks.ListBlock)
def _(block):
    subfactory_class = _registry.get(type(block.child_block))
    return _registry.get(type(block))(subfactory_class)
