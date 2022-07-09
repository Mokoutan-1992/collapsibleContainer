import random

import pymel.core as pm

from .pyqt_utils import *
from .collapsible_widget import *
from .sample import CollapsibleContainer as sampleContainer

DPI_SCALE = get_logicaldpi() / 96.0


class TestSubWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestSubWidget, self).__init__(parent)
        self.range = random.randrange(10)

        self.setLayout(QtWidgets.QVBoxLayout())
        for i in range(self.range):
            self.layout().addWidget(QtWidgets.QPushButton("Button{}".format(i + 1)))


class TestTab2(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestTab2, self).__init__(parent)

        self.path_le = QtWidgets.QLineEdit()
        export_import_layout = QtWidgets.QHBoxLayout()
        export_import_layout.addWidget(self.path_le)
        self.setLayout(export_import_layout)


class TestMainTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestMainTab, self).__init__(parent)
        self.create_base_layout()
        self.create_paint_layouts()
        self.create_collapsible_layouts()

    def create_base_layout(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        scroll_area.setWidget(main_widget)

    def create_paint_layouts(self):
        paint_layout = QtWidgets.QFormLayout()
        paint_widget = TestSubWidget()
        paint_layout.addWidget(paint_widget)
        self.main_layout.addLayout(paint_layout)

    def create_collapsible_layouts(self):
        self.content_widget = QtWidgets.QWidget()

        # sub widgets >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # mirror widget--sub widget
        mirror_container_widget = TestSubWidget()

        # weight blend--sub widget
        weightBlend_container_widget = QtWidgets.QWidget()

        self.weightBlend_test_btn = QtWidgets.QPushButton("Test weight")
        weightBlend_container_layout = QtWidgets.QGridLayout()
        weightBlend_container_layout.addWidget(self.weightBlend_test_btn)

        weightBlend_container_widget.setLayout(weightBlend_container_layout)

        # cage--sub widget
        create_cage_widget = TestSubWidget()

        # same topology--sub widget
        transfrom_same_topo_widget = TestSubWidget()

        # sub widgets <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # build contents---------------------------------------------------------------------------
        self.content_v_layout = QtWidgets.QVBoxLayout(self.content_widget)

        self.content_v_layout.setContentsMargins(0, 0, 0, 0)
        self.content_v_layout.setSpacing(0)

        self._addCollapsibleContent(mirror_container_widget, "Mirror")
        self._addCollapsibleContent(weightBlend_container_widget, "Weight Blend")
        self._addCollapsibleContent(transfrom_same_topo_widget, "Same Topology Skin Transfer")
        self._addCollapsibleContent(create_cage_widget, "Create Cage / Weight")
        self.content_v_layout.addStretch()
        # build end  ---------------------------------------------------------------------------
        self.main_layout.addWidget(self.content_widget)

    def _addCollapsibleContent(self, sub_content_widget, title="title not set"):
        box = sampleContainer(title)
        self.content_v_layout.addWidget(box)
        temp_layout = QtWidgets.QVBoxLayout()
        temp_layout.addWidget(sub_content_widget)
        box.setContentLayout(temp_layout)


class TestDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        # remove the question mark of a QDialog object
        if sys.version_info.major < 3:
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Skin Tool")
        self.setMinimumWidth(300 * DPI_SCALE)
        self.resize(410 * DPI_SCALE, 700 * DPI_SCALE)

        self.create_main_widgets()

    def create_main_widgets(self):
        self.main_tab = QtWidgets.QTabWidget()
        self.main_tab.addTab(TestMainTab(), "Edit")
        self.main_tab.addTab(TestTab2(), "Export/Import")

        main_tab_layout = QtWidgets.QVBoxLayout()
        main_tab_layout.setContentsMargins(0, 0, 0, 0)
        main_tab_layout.setSpacing(0)
        main_tab_layout.addWidget(self.main_tab)
        self.setLayout(main_tab_layout)


def run():
    try:
        skin_tool_dialog.close()  # noqa
        skin_tool_dialog.deleteLater()  # noqa
    except:
        pass

    skin_tool_dialog = TestDialog()
    skin_tool_dialog.show()


if __name__ == "__main__":
    run()
