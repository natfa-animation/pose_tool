# SIM posetool (Blender Add-on)

SIM posetool is a Blender add-on for recording, organizing, and applying armature poses (including groups and JSON presets). It includes an interactive **Adjust Pose** drag tool for previewing and committing pose influence with Blender-style confirm/cancel behavior.

Where it appears:
- `View3D -> Sidebar (N) -> SIM anima -> SIM posetool`

## Features

### Pose management
- Record a pose from selected pose bones
- Update an existing pose from current bone transforms
- Select the bones stored in a pose
- Duplicate a pose
- Delete a pose / delete all poses

### Pose grouping
- Create nested pose groups
- Assign poses to groups
- Expand/collapse groups in the UI
- Delete groups (poses are ungrouped safely)

### Apply / adjust a pose (interactive)
- Per pose, use **Adjust Pose** to enter a modal drag tool:
  - Drag to preview pose influence live (non-cumulative / deterministic)
  - `Left Mouse` confirms (commits)
  - `Right Mouse` or `Esc` cancels (reverts)
- Supports **negative values** (drag left) for inverse influence where applicable.
- Supports **Relative/Additive mode** (`+`) which can exceed the normal full-pose limit (> 100%).

### Mirror
- Per-pose mirror toggle
- Mirror name detection supports common conventions:
  - `_Left` / `_Right`
  - `.L` / `.R`

### Import / Export / Merge (JSON)
- Export poses + groups to JSON
- Import poses + groups from JSON (replaces existing)
- Merge poses + groups from JSON (adds missing items)

### Presets (folder-based)
- Choose a presets folder
- Pick a preset from a dropdown (lists `.json` files)
- Load preset into the current armature (replaces current poses/groups)

### Toggles
- Rotation / Location / Scale toggles for application
- Apply to All Bones toggle (otherwise uses selected bones)

## Installation

### Install from ZIP
1. Zip the **add-on folder** (not individual files).
2. In Blender: `Edit -> Preferences -> Add-ons -> Install...`
3. Select the ZIP and enable the add-on.

Correct ZIP structure:

```text
sim_posetool.zip
└── pose_tool/
    ├── __init__.py
    ├── constants.py
    ├── core_apply.py
    ├── props_types.py
    ├── scene_props.py
    ├── operators_pose.py
    ├── operators_io.py
    ├── operators_progress.py
    ├── ui_panel.py
    └── LICENSE
```

## Usage

### 1) Select an armature
- In the panel, set **Armature** (or ensure the active object is an Armature).

### 2) Record a pose
1. Put the armature in Pose Mode.
2. Select the bones you want to store.
3. Click **Add** (Record Pose) and name it.

### 3) Adjust/apply a pose (modal drag tool)
1. In the pose row, click **Adjust Pose**.
2. Drag the mouse:
   - Drag right = positive influence
   - Drag left = negative influence
3. Confirm/cancel:
   - `Left Mouse` confirm (commits the current preview)
   - `Right Mouse` / `Esc` cancel (restores the exact pose state from before the drag started)

Tips:
- In **Absolute (A)** mode, the tool is clamped to `-100% .. +100%`.
- In **Relative/Additive (+)** mode, the tool can exceed `100%` to intensify the pose.
- Hold `Shift` for finer control, `Ctrl` for faster control.

### 4) Absolute vs Relative/Additive
- **A (Absolute)**: blends toward the stored target pose (and supports negative for inverse-style behavior).
- **+ (Relative/Additive)**: applies the pose as a delta on top of the current rig state; values can go beyond 100%.

### 5) Groups
- Click **Create Group** to add a group.
- Use the group field next to a pose name to assign it to a group.

### 6) Import / Export / Merge
- Expand **Settings** and use Export/Import/Merge for JSON workflows.

### 7) Presets
- Expand **Presets**, set the folder, pick a preset, and click **Load Preset**.

## Troubleshooting

### Add-on installs but panel doesn’t show
- Verify the ZIP contains a single top-level folder with `__init__.py` inside it.
- Enable the add-on and check Blender’s system console for import errors.

### “Adjust Pose” cancels immediately
- Ensure an Armature is selected (panel armature selector or active object).
- Ensure the armature can switch to Pose Mode (some contexts can block mode switching).

## Compatibility
- Blender: **5+**
- Many operations are context-sensitive (Pose Mode, active object, selection).

## Developer notes
- The modal adjust tool is implemented as `pt.adjust_pose_progress`:
  - caches a base state once per session
  - recomputes preview from that base on every mouse move (non-cumulative)
  - confirms with LMB and cancels with RMB/Esc

## License
See `LICENSE`.

