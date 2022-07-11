import os

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance, getCppPointer
import maya.OpenMayaUI as omui

from .python_compatibility import *

_LOGICAL_DPI_KEY = "_LOGICAL_DPI"


def maya_main_window():
    """Get Maya's main window

    Returns:
        QMainWindow: main window.

    """

    main_window_ptr = omui.MQtUtil.mainWindow()
    if PY2:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)  # noqa
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


# dpi scale test -------------------------------------------------------------
def get_logicaldpi():
    """attempting to "cache" the query to the maya main window for speed

    Returns:
        int: dpi of the monitor
    """
    if _LOGICAL_DPI_KEY not in os.environ.keys():
        try:
            logical_dpi = maya_main_window().logicalDpiX()
        except Exception:
            logical_dpi = 96
        finally:
            os.environ[_LOGICAL_DPI_KEY] = str(logical_dpi)
    return int(os.environ.get(_LOGICAL_DPI_KEY)) or 96


def dpi_scale(value, default=96, min_=1, max_=2):
    """Scale the provided value by the scale that maya is using
    which is derived from the 'average' dpi of 96 from windows, linux, osx.

    Args:
        value (int, float): value to scale
        default (int, optional): assumed default from various platforms
        min_ (int, optional): if you do not want the value under 96 dpi
        max_ (int, optional): if you do not want a value higher than 200% scale

    Returns:
        # int, float: scaled value
    """
    return value * max(min_, min(get_logicaldpi() / float(default), max_))


# class QHLine(QFrame):
#     def __init__(self):
#         super(QHLine, self).__init__()
#         self.setFrameShape(QFrame.HLine)
#         self.setFrameShadow(QFrame.Sunken)


# class QVLine(QFrame):
#     def __init__(self):
#         super(QVLine, self).__init__()
#         self.setFrameShape(QFrame.VLine)
#         self.setFrameShadow(QFrame.Sunken)

class HLine(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(HLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(0)
        self.setMidLineWidth(3)
        self.setContentsMargins(0, 0, 0, 0)