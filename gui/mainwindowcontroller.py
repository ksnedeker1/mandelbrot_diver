import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui

from gui.qgzbarewindow import Ui_MainWindow
from core.pool import MandelbrotPoolManager


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindow.__init__(self)

        self.setupUi(self)

        stylesheet = "./gui/resources/stylesheet.qss"
        with open(stylesheet, "r") as f:
            self.setStyleSheet(f.read())

        self.color_scheme = "ramp"
        self.max_iter = 200

        self.pool_manager = MandelbrotPoolManager(800, 600, 0, 0, 3.5, max_iter=self.max_iter)
        self.pool_manager.SIG_CHUNK_FINISHED.connect(self.update_view)

        self.test()

    def update_view(self):
        """Fetches current state of the rendered array"""
        mandelbrot_data = self.pool_manager.get_result()

        if self.color_scheme == "ramp":
            # Logarithmic scaling, creates banding effect for colors
            max_iter = self.max_iter
            scaled_data = np.log(mandelbrot_data + 1) / np.log(max_iter + 1)

            # Interpolation from interp_lo to interp_hi
            interp_lo = np.array([0, 0, 255])
            interp_hi = np.array([255, 165, 0])

            # Compute RGB values via linear interpolation
            rgb_data = (
                    (1 - scaled_data[..., np.newaxis]) * interp_lo + scaled_data[..., np.newaxis] * interp_hi
            ).astype(np.uint8)

        elif self.color_scheme == "binary":
            is_odd = mandelbrot_data % 2
            even_color = [255, 255, 255]
            odd_color = [0, 0, 0]

            # Translate iteration counts to a binary color scheme based on parity
            rgb_data = np.zeros((*mandelbrot_data.shape, 3), dtype=np.uint8)
            rgb_data[is_odd == 0] = even_color
            rgb_data[is_odd == 1] = odd_color

        else:
            raise ValueError(f"Unsupported color scheme: {self.color_scheme}")

        # Convert RGB to QImage to QPixmap and add to a QGraphicsScene for display in the QGraphicsDisplay
        image = QtGui.QImage(rgb_data.data, rgb_data.shape[1], rgb_data.shape[0],
                             rgb_data.strides[0], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pixmap)
        self.viewGraphics.setScene(scene)
        self.viewGraphics.show()

    def test(self):
        self.pool_manager.start_computation()


def start_gui():
    app = QtWidgets.QApplication([])
    window = MainWindowController()
    window.show()
    app.exec_()
