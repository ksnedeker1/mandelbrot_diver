import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable
from core.mandelbrot import compute_mandelbrot


class MandelbrotWorkerSignalHandler(QObject):
    """Enable signalling for MandelbrotWorker QRunnable"""
    SIG_FINISHED = pyqtSignal(np.ndarray, tuple)


class MandelbrotWorker(QRunnable):
    """Call compute_mandelbrot() with given params, signal on completion."""
    def __init__(self, chunk_coords, width, height, x_center, y_center, x_width, max_iter=1000):
        super().__init__()
        self.chunk_coords = chunk_coords
        self.width = width
        self.height = height
        self.x_center = x_center
        self.y_center = y_center
        self.x_width = x_width
        self.max_iter = max_iter
        self.worker = MandelbrotWorkerSignalHandler()
        self.stop_requested = False

    def run(self):
        iteration_data = compute_mandelbrot(
            self.width, self.height, self.x_center, self.y_center, self.x_width, max_iter=self.max_iter, worker=self
        )
        if not self.stop_requested:
            self.worker.SIG_FINISHED.emit(iteration_data, self.chunk_coords)

    def stop(self):
        self.stop_requested = True