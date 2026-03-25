"""
Headless Blender Worker
========================
Command-line entry point for generating golf plaques without a GUI.

Run via the Blender executable in background (``-b``) mode::

    blender -b --python scripts/golf/blender_worker.py -- \\
        --svg /path/to/course.svg \\
        --params '{"width": 100, "height": 140, "thickness": 6}' \\
        --format stl \\
        --output /tmp/plaque

Supported ``--params`` keys
---------------------------
Dimensional parameters:

* ``width``          – Plaque width in mm  (default: 100.0)
* ``height``         – Plaque height in mm (default: 140.0)
* ``thickness``      – Base depth in mm    (default: 6.0)

Feature flags (boolean, default ``false``):

* ``use_manual_scale``        – Fit scale to largest SVG object
* ``generate_protective_frame`` – Auto-create frame around Rough
* ``use_draft_angle``         – Taper cutter walls
* ``draft_factor``            – Draft angle steepness (default: 1.1)
* ``use_floor_texture``       – Procedural floor displacement
* ``use_layer_depths``        – Use per-layer depth overrides (enabled
                                automatically when any ``*_depth`` key
                                is present)

Per-layer depth overrides (mm):

* ``water_depth``    – Carved depth of Water layers
* ``sand_depth``     – Carved depth of Sand layers
* ``green_depth``    – Carved depth of Green layers
* ``fairway_depth``  – Carved depth of Fairway layers
* ``rough_depth``    – Carved depth of Rough layers

Output format (``--format``):

* ``blend`` – Save the ``.blend`` project with modifiers intact (default)
* ``stl``   – Apply all modifiers and export a flattened ``.stl`` mesh
"""

import argparse
import json
import sys

import bpy

from .geometry_utils import carve_plaque

# ---------------------------------------------------------------------------
# API-key → PropertyGroup-attribute mapping
# ---------------------------------------------------------------------------

# Translates the short, user-facing API keys to the internal attribute names
# used by both the PropertyGroup (Addon UI path) and the get_val helper.
_API_KEY_MAP = {
    "width": "plaque_width",
    "height": "plaque_height",
    "thickness": "plaque_thick",
    "water_depth": "depth_water",
    "sand_depth": "depth_sand",
    "green_depth": "depth_green",
    "fairway_depth": "depth_fairway",
    "rough_depth": "depth_rough",
}

# Keys that imply layer-depth overrides are active.
_DEPTH_OVERRIDE_KEYS = frozenset(
    {"water_depth", "sand_depth", "green_depth", "fairway_depth", "rough_depth"}
)


def normalize_params(api_params):
    """Translate API-style keys to internal PropGroup-style keys.

    This allows callers to use short, descriptive names (e.g. ``"width"``)
    while the geometry pipeline continues to use the PropGroup attribute names
    (e.g. ``"plaque_width"``) that ensure backward compatibility with the
    Blender Addon GUI path.

    If any per-layer depth override key is present, ``use_layer_depths`` is
    automatically set to ``True`` so the pipeline activates the per-layer
    depth logic.

    Args:
        api_params: Raw :class:`dict` parsed from the ``--params`` JSON string.

    Returns:
        A new :class:`dict` with internal key names.
    """
    normalized = {}
    has_depth_override = False

    for key, value in api_params.items():
        if key in _DEPTH_OVERRIDE_KEYS:
            has_depth_override = True
        internal_key = _API_KEY_MAP.get(key, key)
        normalized[internal_key] = value

    if has_depth_override:
        normalized.setdefault("use_layer_depths", True)

    return normalized


def _parse_args():
    """Parse worker arguments that follow the ``--`` separator in Blender's argv."""
    # Blender passes its own arguments before ``--``; only parse what comes after.
    try:
        separator_index = sys.argv.index("--")
        worker_args = sys.argv[separator_index + 1:]
    except ValueError:
        worker_args = []

    parser = argparse.ArgumentParser(
        prog="blender_worker",
        description="Headless golf plaque generator",
    )
    parser.add_argument(
        "--svg",
        metavar="PATH",
        default=None,
        help="Path to a Plain SVG file to import before generating the plaque",
    )
    parser.add_argument(
        "--params",
        metavar="JSON",
        default="{}",
        help="JSON string of generation parameters (see module docstring)",
    )
    parser.add_argument(
        "--format",
        choices=["blend", "stl"],
        default="blend",
        help="Output format: 'blend' saves the project, 'stl' exports a mesh",
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        default="/tmp/plaque",
        help="Output file path (without extension)",
    )
    return parser.parse_args(worker_args)


def _init_scene():
    """Reset the Blender scene to a clean factory state for headless use."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Ensure a default scene exists (factory-empty leaves one active scene).
    if not bpy.context.scene:
        bpy.ops.scene.new()


def _import_svg(svg_path):
    """Import a Plain SVG file into the current scene.

    Args:
        svg_path: Absolute or relative path to the ``.svg`` file.
    """
    bpy.ops.import_curve.svg(filepath=svg_path)


def _export_stl(output_path):
    """Apply all modifiers and export the plaque as an STL file.

    All objects in the scene are selected, modifiers are applied, and the
    combined mesh is written to *output_path* + ``.stl``.

    Args:
        output_path: Destination path without the ``.stl`` extension.
    """
    # Select all mesh objects for export.
    bpy.ops.object.select_all(action="SELECT")
    stl_path = output_path if output_path.endswith(".stl") else output_path + ".stl"
    bpy.ops.export_mesh.stl(filepath=stl_path, use_selection=True)


def _save_blend(output_path):
    """Save the current scene as a ``.blend`` file with modifiers intact.

    Args:
        output_path: Destination path without the ``.blend`` extension.
    """
    blend_path = (
        output_path if output_path.endswith(".blend") else output_path + ".blend"
    )
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)


def main():
    """Entry point: parse args, generate the plaque, and write the output."""
    args = _parse_args()

    try:
        api_params = json.loads(args.params)
    except json.JSONDecodeError as exc:
        print(f"blender_worker: invalid --params JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    params = normalize_params(api_params)

    _init_scene()

    if args.svg:
        _import_svg(args.svg)

    carve_plaque(params)

    if args.format == "stl":
        _export_stl(args.output)
    else:
        _save_blend(args.output)


if __name__ == "__main__":
    main()
