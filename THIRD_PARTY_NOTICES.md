# Third-party notices

Shroud Designer is MIT-licensed. Its packaged applications include unmodified
open-source runtime components under their own licenses:

| Component | Version | License | Source |
|---|---:|---|---|
| CPython | 3.11.15 | PSF-2.0 | https://github.com/python/cpython/tree/v3.11.15 |
| PySide6 / Qt for Python | 6.11.1 | LGPL-3.0-only (also offered under GPL/commercial terms) | https://code.qt.io/cgit/pyside/pyside-setup.git/ |
| Qt libraries | 6.11.1 | LGPL-3.0-only or GPL/commercial, depending on component | https://code.qt.io/cgit/qt/ |
| Shiboken6 | 6.11.1 | LGPL-3.0-only (also offered under GPL/commercial terms) | https://code.qt.io/cgit/pyside/pyside-setup.git/ |
| NumPy | 2.4.4 | BSD-3-Clause and bundled-component licenses | https://github.com/numpy/numpy/tree/v2.4.4 |
| trimesh | 5.0.0 | MIT | https://github.com/mikedh/trimesh |
| Shapely / GEOS | 2.1.2 | BSD-3-Clause / LGPL-2.1-or-later | https://github.com/shapely/shapely/tree/2.1.2 |
| Manifold | 3.5.2 | Apache-2.0 | https://github.com/elalish/manifold/tree/v3.5.2 |
| mapbox-earcut | 2.0.0 | ISC / ISC | https://github.com/skogler/mapbox_earcut_python/tree/v2.0.0 |
| PyOpenGL | 3.1.10 | BSD-style | https://github.com/mcfletch/pyopengl/tree/3.1.10 |
| PyInstaller bootloader | 6.21.0 | GPL-2.0-or-later with Bootloader Exception | https://github.com/pyinstaller/pyinstaller/tree/v6.21.0 |

The complete license texts supplied with these components are in the
`licenses` directory. Several packages include additional transitive or
vendored components; their notices are retained in the corresponding license
file.

The Qt/PySide6 shared libraries remain separate files in the portable
application directory. Recipients may replace those libraries with compatible
modified versions as permitted by the LGPL. Corresponding source is available
from the upstream source links above.

No upstream component is relicensed under the Shroud Designer MIT license.
