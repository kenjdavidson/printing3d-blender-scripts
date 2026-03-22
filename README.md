# blender-scripts

Random Blender Python scripts to help with various projects.  
Manage them with Git so changes are always in sync between machines.

---

## Repository layout

```
scripts/
  animation/        # Keyframe, timeline, and NLA helpers
  geometry/         # Mesh creation and manipulation utilities
  materials/        # Material and shader node setup helpers
  utilities/        # Scene-wide helpers (renaming, render settings, …)
```

---

## Getting started

### Clone (first time)

```bash
git clone https://github.com/kenjdavidson/blender-scripts.git
```

### Sync changes between machines

```bash
# Pull the latest scripts on whichever machine you sit down at
git pull

# After editing or adding scripts, push them back
git add .
git commit -m "Add/update <script name>"
git push
```

---

## Using a script in Blender

### Option A – Scripting workspace (one-off run)

1. Open Blender and switch to the **Scripting** workspace.
2. Click **Open** in the Text Editor header and browse to the `.py` file.
3. Click **Run Script** (▶) or press **Alt + P**.

### Option B – Text Editor (persistent in .blend file)

1. Open the **Text Editor** (inside any workspace).
2. Click **Open** and select the `.py` file.
3. Enable **Register** (checkbox in the header) to run it on file load.

### Option C – Startup scripts (auto-load on every launch)

Copy (or symlink) the scripts you use daily into Blender's user scripts
directory:

| OS      | Path |
|---------|------|
| Windows | `%APPDATA%\Blender Foundation\Blender\<version>\scripts\startup\` |
| macOS   | `~/Library/Application Support/Blender/<version>/scripts/startup/` |
| Linux   | `~/.config/blender/<version>/scripts/startup/` |

Blender executes every `.py` file in that folder at startup automatically.

> **Tip:** Use a symlink instead of copying so the file stays in sync with
> the repository:
> ```bash
> # Linux / macOS example
> ln -s ~/blender-scripts/scripts/utilities/render_settings_preset.py \
>        ~/.config/blender/4.2/scripts/startup/
> ```

---

## Available scripts

### `scripts/animation/`

| File | Description |
|------|-------------|
| `set_keyframe_interpolation.py` | Bulk-change interpolation mode (BEZIER, LINEAR, CONSTANT, …) for all keyframes on the active object. |

### `scripts/geometry/`

| File | Description |
|------|-------------|
| `add_grid_of_objects.py` | Instantiate an object (or a primitive) in a configurable N×M grid. |

### `scripts/materials/`

| File | Description |
|------|-------------|
| `create_principled_material.py` | Create a Principled BSDF material with common properties and assign it to the active object. |

### `scripts/utilities/`

| File | Description |
|------|-------------|
| `batch_rename_objects.py` | Rename all selected (or all scene) objects with a prefix, suffix, and zero-padded index. |
| `render_settings_preset.py` | Apply a named render preset (draft / final / eevee_preview) to the current scene. |

---

## Contributing / adding new scripts

1. Create the script in the appropriate `scripts/<category>/` folder.
2. Add a module-level docstring explaining what it does, its arguments,
   and how to run it.
3. Guard the entry-point code with `if __name__ == "__main__":`.
4. Update the table above.
5. Commit and push.
