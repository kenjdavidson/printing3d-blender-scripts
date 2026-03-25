"""Compatibility wrapper for the golf plaque generator geometry pipeline."""

from .plaque_builder import carve_plaque
from .utils import get_val

__all__ = ["carve_plaque", "get_val"]
