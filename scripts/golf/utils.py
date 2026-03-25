"""Shared utility helpers for the golf plaque generator."""


def get_val(source, key, default=None):
    """Return a value from *source* by *key* in a type-agnostic way.

    Works with both plain :class:`dict` instances (JSON / API input) and
    :class:`bpy.types.PropertyGroup` instances (Blender Addon UI), so the
    same geometry pipeline can be called from a Dockerised headless worker
    and from the interactive Blender panel without any code duplication.

    Args:
        source: A :class:`dict` or a :class:`bpy.types.PropertyGroup`.
        key: The attribute / key name to look up.
        default: Value returned when *key* is absent.

    Returns:
        The resolved value, or *default* if not found.
    """
    if isinstance(source, dict):
        return source.get(key, default)
    return getattr(source, key, default)
