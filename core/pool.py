import numpy as np
from PyQt5 import QtCore

from core.worker import MandelbrotWorker


class MandelbrotPoolManager(QtCore.QObject):
    """Handle work delegation and communication between worker results and caller."""
    SIG_CHUNK_FINISHED = QtCore.pyqtSignal(np.ndarray, tuple)

    def __init__(self, width, height, x_center, y_center, x_width, max_iter=1000):
        super().__init__()

        self.width = width
        self.height = height
        self.x_center = x_center
        self.y_center = y_center
        self.x_width = x_width
        self.max_iter = max_iter

        self.thread_pool = QtCore.QThreadPool()
        self.mandelbrot_data = np.zeros((height, width), dtype=int)

    def _on_worker_finished(self, data, coords):
        """Merge new chunk data with render array and emit signal"""
        x_start, y_start = coords
        self.mandelbrot_data[y_start:y_start + data.shape[0], x_start:x_start + data.shape[1]] = data
        self.SIG_CHUNK_FINISHED.emit(self.mandelbrot_data, coords)

    def start_computation(self, chunk_size=200):
        """Partition display area into chunks, deduce params, spawn worker."""
        # Re/Im increment per px
        x_increment = self.x_width / self.width
        y_increment = (self.x_width * self.height / self.width) / self.height

        # Partition display area into chunks
        for x in range(0, self.width, chunk_size):
            for y in range(0, self.height, chunk_size):
                width = min(chunk_size, self.width - x)
                height = min(chunk_size, self.height - y)
                chunk_x_center = self.x_center + (x + width / 2 - self.width / 2) * x_increment
                chunk_y_center = self.y_center + (y + height / 2 - self.height / 2) * y_increment
                chunk_x_width = width * x_increment
                # Spawn worker
                task = MandelbrotWorker((x, y), width, height, chunk_x_center, chunk_y_center, chunk_x_width,
                                        self.max_iter)
                task.worker.SIG_FINISHED.connect(self._on_worker_finished)
                self.thread_pool.start(task)

    def get_result(self):
        return self.mandelbrot_data
