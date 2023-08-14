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
        return self._registry[block_class]

    def __setitem__(self, block_class: type, factory_class: type):
        self._registry[block_class] = factory_class

    def __contains__(self, block_class: type):
        return block_class in self._registry

    def get(self, key, default=None):
        return self._registry.get(key, default)

    def register(self, block_class: type):
        def _register(factory):
            self[block_class] = factory
            return factory

        return _register

    def search(self, block_class: type):
        """
        Look up the factory type for block_class, walking up its MRO until a match is found
        """
        for cls in inspect.getmro(block_class):
            if cls in self._registry:
                return self._registry[cls]
        raise KeyError(
            f"Couldn't find registered factory for class {cls} or its superclasses"
        )

_registry = _Registry()
register_block_factory = _registry.register


def generate_block_factory(block):
    if not isinstance(block, wagtail_blocks.StreamBlock):
        raise TypeError("block argument must be a StreamBlock (or subclass)")
    return _generate_block_factory(block, wrapper=lambda x: x)


@singledispatch
def _generate_block_factory(block):
    """
    Generate a block factory for atomic block types
    """
    return factory.SubFactory(_registry.search(type(block)))


@_generate_block_factory.register(wagtail_blocks.StreamBlock)
@_generate_block_factory.register(wagtail_blocks.StructBlock)
def _(block, wrapper=factory.SubFactory):
    """
    Generate a block factory for a StreamBlock or StructBlock

    The `wrapper' kwarg facilitates the top level block, which should
    be returned unwrapped - the public interface passes the identity function.
    All other StructBlocks and StreamBlocks should be wrapped in factory.SubFactory.
    """
    block_class = type(block)
    if factory_class := _registry.get(block_class):
        return wrapper(factory_class)

    attrs = {k: _generate_block_factory(v) for k, v in block.child_blocks.items()}

    factory_class = _registry.search(block_class)

    attrs["Meta"] = type("Meta", (), {"model": block_class})

    block_factory = type(f"{block_class.__name__}Factory", (factory_class,), attrs)

    if block_class not in _registry:
        # Store it in the registry so we don't have to compute it again
        _registry[block_class] = block_factory

    return wrapper(block_factory)


@_generate_block_factory.register(wagtail_blocks.ListBlock)
def _(block):
    """
    Generate a ListBlockFactory
    """
    subfactory_class = _registry.search(type(block.child_block))
    return _registry.search(type(block))(subfactory_class)
