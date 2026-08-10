from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, radians, sin

import numpy as np
import trimesh
from OpenGL import GL, GLU
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent, QWheelEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget


@dataclass(slots=True)
class RenderMesh:
    mesh: trimesh.Trimesh
    color: tuple[float, float, float, float]


@dataclass(slots=True)
class _RenderBuffer:
    vertices: np.ndarray
    normals: np.ndarray
    color: tuple[float, float, float, float]
    bounds: np.ndarray


class ModelPreview(QOpenGLWidget):
    """Small fixed-pipeline mesh viewer with CAD-style mouse controls."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(560, 480)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self._buffers: list[_RenderBuffer] = []
        self._target = np.zeros(3, dtype=float)
        self._distance = 300.0
        self._yaw = -45.0
        self._pitch = 28.0
        self._last_mouse = QPoint()
        self._active_button = Qt.MouseButton.NoButton
        self._scene_radius = 100.0

    def set_meshes(self, meshes: list[RenderMesh], fit: bool = False) -> None:
        buffers: list[_RenderBuffer] = []
        for item in meshes:
            triangles = np.asarray(item.mesh.triangles, dtype=np.float32)
            if len(triangles) == 0:
                continue
            vertices = np.ascontiguousarray(triangles.reshape((-1, 3)), dtype=np.float32)
            face_normals = np.asarray(item.mesh.face_normals, dtype=np.float32)
            normals = np.ascontiguousarray(np.repeat(face_normals, 3, axis=0), dtype=np.float32)
            buffers.append(_RenderBuffer(vertices, normals, item.color, item.mesh.bounds.copy()))
        first_model = not self._buffers and bool(buffers)
        self._buffers = buffers
        if fit or first_model:
            self.fit_view()
        self.update()

    def fit_view(self) -> None:
        if not self._buffers:
            self._target = np.zeros(3, dtype=float)
            self._distance = 300.0
            self.update()
            return
        lower = np.min(np.array([buffer.bounds[0] for buffer in self._buffers]), axis=0)
        upper = np.max(np.array([buffer.bounds[1] for buffer in self._buffers]), axis=0)
        self._target = (lower + upper) / 2.0
        self._scene_radius = max(float(np.linalg.norm(upper - lower) / 2.0), 1.0)
        # 35° vertical FOV needs roughly 3.2 radii; retain extra room for the
        # window's status/header strips and wide fan plates.
        self._distance = max(self._scene_radius * 3.8, 20.0)
        self.update()

    def initializeGL(self) -> None:
        GL.glClearColor(0.035, 0.047, 0.065, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (0.95, 0.97, 1.0, 1.0))
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_DIFFUSE, (0.35, 0.43, 0.55, 1.0))
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, (0.22, 0.25, 0.30, 1.0))

    def resizeGL(self, width: int, height: int) -> None:
        GL.glViewport(0, 0, max(1, width), max(1, height))

    def _camera_position(self) -> np.ndarray:
        yaw = radians(self._yaw)
        pitch = radians(self._pitch)
        direction = np.array(
            [cos(pitch) * cos(yaw), cos(pitch) * sin(yaw), sin(pitch)], dtype=float
        )
        return self._target + direction * self._distance

    def paintGL(self) -> None:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        width, height = max(1, self.width()), max(1, self.height())
        near = max(0.05, self._distance - self._scene_radius * 2.0)
        far = max(near + 100.0, self._distance + self._scene_radius * 4.0)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(35.0, width / height, near, far)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        camera = self._camera_position()
        GLU.gluLookAt(
            *camera,
            *self._target,
            0.0,
            0.0,
            1.0,
        )
        GL.glLightfv(
            GL.GL_LIGHT0,
            GL.GL_POSITION,
            (camera[0], camera[1], camera[2] + self._scene_radius, 1.0),
        )
        GL.glLightfv(
            GL.GL_LIGHT1,
            GL.GL_POSITION,
            (
                self._target[0] - self._scene_radius,
                self._target[1] + self._scene_radius,
                self._target[2],
                1.0,
            ),
        )

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_NORMAL_ARRAY)
        for buffer in self._buffers:
            GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE, buffer.color)
            GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR, (0.25, 0.28, 0.32, 1.0))
            GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, 28.0)
            GL.glVertexPointer(3, GL.GL_FLOAT, 0, buffer.vertices)
            GL.glNormalPointer(GL.GL_FLOAT, 0, buffer.normals)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(buffer.vertices))
        GL.glDisableClientState(GL.GL_NORMAL_ARRAY)
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._last_mouse = event.position().toPoint()
        self._active_button = event.button()
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._active_button = Qt.MouseButton.NoButton
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        position = event.position().toPoint()
        delta = position - self._last_mouse
        self._last_mouse = position
        if self._active_button == Qt.MouseButton.LeftButton:
            self._yaw -= delta.x() * 0.45
            self._pitch = float(np.clip(self._pitch + delta.y() * 0.45, -88.0, 88.0))
            self.update()
        elif self._active_button == Qt.MouseButton.RightButton:
            camera = self._camera_position()
            forward = self._target - camera
            forward /= max(np.linalg.norm(forward), 1e-9)
            right = np.cross(forward, np.array([0.0, 0.0, 1.0]))
            right /= max(np.linalg.norm(right), 1e-9)
            up = np.cross(right, forward)
            scale = self._distance * 0.0016
            self._target += (-delta.x() * right + delta.y() * up) * scale
            self.update()
        event.accept()

    def wheelEvent(self, event: QWheelEvent) -> None:
        steps = event.angleDelta().y() / 120.0
        self._distance *= exp(-steps * 0.14)
        self._distance = float(
            np.clip(self._distance, max(0.5, self._scene_radius * 0.08), 1_000_000.0)
        )
        self.update()
        event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.fit_view()
        event.accept()
