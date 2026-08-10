# Shroud Designer 0.2

Shroud Designer turns an upright GPU connector STL into one print-ready, airtight shroud assembly. It detects the opening at the connector's highest Z layer, generates a straight/offset or compound-curved transition, adds a custom or imported fan connector, then fuses and validates the result before saving it as STL.

## Download — Linux

Download `ShroudDesigner-0.2-linux-x86_64.tar.gz` from the
[v0.2 release](https://github.com/torgles/shroud-designer/releases/tag/v0.2),
extract it, then run:

```bash
./install.sh
```

The installer is per-user and does not require administrator privileges. You
can also run the application portably with `./run.sh`.

## Use

1. Open **Shroud Designer** from the desktop shortcut (or run the Linux binary).
2. Select an upright GPU connector STL. STL units are interpreted as millimetres and the opening must be at maximum Z.
3. Set the connector count from 1–10. Multiple connectors are identical copies and can be stacked along X or Y with a clear spacing between their bodies.
4. Choose a custom 120/140 mm fan plate or import a finished fan connector STL.
5. Adjust the funnel. With multiple connectors, **Split distance** controls how far each separate duct travels before entering the shared collector.
6. Select **Save print-ready STL…**. Export only succeeds when the result is one connected, watertight solid.

Preview controls:

- Mouse wheel: zoom
- Left drag: rotate
- Right drag: move the model
- Double-click or **Fit view**: frame the full assembly

## Geometry notes

- Straight offsets move the fan in X/Y without rotating it.
- Connector spacing is the clear edge-to-edge gap between the connector STL bounding boxes, not center-to-center spacing.
- Split distance is measured from the GPU opening toward the fan. A short collector chamber at that height merges the separate airtight ducts into the main funnel.
- Compound curves combine the X and Y bend values into one smooth centerline bend. The fan is rotated so its plate remains perpendicular to the outlet.
- **Arc diameter** is the free inside diameter of the elbow. A larger value produces a wider, gentler curve without allowing the inside wall to fold through itself.
- The supplied 120 mm reference measures 116 mm at the airflow opening, about 4.6 mm at the screw holes, and uses a 105 mm mounting pattern.
- The generated 140 mm option uses a 136 mm airflow opening and a 124.5 mm mounting pattern. The plate is regenerated at its true dimensions; screw holes are not scaled.

## Development

Requires **Python 3.11** (recommended). On Linux, [uv](https://github.com/astral-sh/uv) is the easiest way to get it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.11
uv venv --python 3.11 .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

Windows (PowerShell):

```powershell
python -m pip install -r requirements-dev.txt
python app.py
```

Test:

```bash
python -m pytest -q
```

### Build — Linux

```bash
./build.sh
```

Produces:

| Output | Description |
|--------|-------------|
| `dist/ShroudDesigner/ShroudDesigner` | Runnable app directory |
| `dist/ShroudDesigner-0.2-linux-x86_64.tar.gz` | Distributable archive |
| `Shroud Designer Linux/` | Portable folder with `install.sh` |
| `public/ShroudDesigner-0.2-linux-x86_64.tar.gz` | Public release archive |

Install for the current user:

```bash
cd "Shroud Designer Linux"
./install.sh
```

See `linux/README.md` for portable-folder details.

### Build — Windows

```powershell
.\build.ps1
```

Creates `dist\ShroudDesigner\ShroudDesigner.exe` and `dist\ShroudDesigner-0.2-Setup.exe`.

## License

Shroud Designer is licensed under the [MIT License](LICENSE). Packaged builds
contain open-source dependencies under their own licenses; see
[Third-party notices](THIRD_PARTY_NOTICES.md).
