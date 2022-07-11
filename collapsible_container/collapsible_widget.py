from ..utils.pyqt_utils import *

DPI_SCALE = get_logicaldpi() / 96.0


class NewCollapsible(QtWidgets.QWidget):
    SPEED = 100

    def __init__(self, title="", parent=None):
        super(NewCollapsible, self).__init__(parent)

        # create main layout
        self.content_height = None
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # create arrow button
        self.arrow_button = QtWidgets.QToolButton()
        self.arrow_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.arrow_button.setArrowType(QtCore.Qt.RightArrow)
        self.arrow_button.setText(title)
        self.arrow_button.setCheckable(True)
        self.arrow_button.setChecked(False)

        # create collapsible scroll area. This will reception use layout
        self.content_area = QtWidgets.QFrame()
        self.content_area.setFrameStyle(6)
        self.content_area.setFixedHeight(0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Fixed)

        # adds widgets to layout
        main_layout.addWidget(self.arrow_button)
        main_layout.addWidget(self.content_area)

        self.size_anim = None

        # adds signal connection
        self.arrow_button.clicked.connect(self.__run_animation)

    def setContentLayout(self, layout):
        # sets the layout into the scroll area
        self.content_area.setLayout(layout)
        self.content_height = layout.sizeHint().height()

    def __run_animation(self):
        """ Runs the animation group
        """
        checked = self.arrow_button.isChecked()
        self.size_anim = QtCore.QPropertyAnimation(self.content_area, b"geometry")
        geometry = self.content_area.geometry()
        width = geometry.width()
        x, y, _, _ = geometry.getCoords()

        size_start = QtCore.QRect(x, y, width, int(not checked) * self.content_height)
        size_end = QtCore.QRect(x, y, width, checked * self.content_height)

        self.size_anim.setStartValue(size_start)
        self.size_anim.setEndValue(size_end)
        self.size_anim.setDuration(self.SPEED)

        size_anim_curve = QtCore.QEasingCurve()
        if checked:
            self.arrow_button.setArrowType(QtCore.Qt.DownArrow)
            size_anim_curve.setType(QtCore.QEasingCurve.InQuad)
        else:
            self.arrow_button.setArrowType(QtCore.Qt.RightArrow)

            size_anim_curve.setType(QtCore.QEasingCurve.OutQuad)
        self.size_anim.setEasingCurve(size_anim_curve)

        self.size_anim.valueChanged.connect(self._forceResize)
        self.size_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def _forceResize(self, new_height):
        self.content_area.setFixedHeight(new_height.height())
