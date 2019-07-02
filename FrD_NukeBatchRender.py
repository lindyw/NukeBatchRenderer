# NOTES
'''
1. StyleSheet and Resources
   1.1 Create a resources.py
   cd C:\Python27\Lib\site-packages\PyQt4
   pyrcc4 -o "D:\Python\NukeBatchRenderer\resources.py" "D:\Python\NukeBatchRenderer\RES.xml"
   import resources  (to the main application py)

2. Get the Write Node filename
   node.knob('file').getValue()
   os.path.basename(PATH)
3. Get String without whitespace
   str.strip()

4. Different type of get value
QtGui.QSpinBox -> w.value()
'''
import sys
import os
# import nuke
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QProcess
# initialize Qt resources from file resources.py
# import resources

PROGRAM_VERSION = '2016.1121'

folderQueue = []
folderDict = {}
# UI
form_class = uic.loadUiType('FrD_NukeBatchRender.ui')[0]

# Path
NUKE_EXE = r'C:\\Program Files\\Nuke10.0v4\\Nuke10.0.exe'
CHECKING_NK = r'D:\\Python\\NukeBatchRenderer\\Checking.py'
RENDER_NK = r'D:\\Python\\NukeBatchRenderer\\Rendering.py'


class FrD_NukeBatchRender(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)

        self.setupUi(self)
        self.setWindowTitle('FrD Nuke Batch Render' + PROGRAM_VERSION)
        self.output_LW.setEnabled(0)
    # ============================ STYLE ======================= #
        # Progress Bar Style
        PB_STYLE = """
        QProgressBar
        {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }

        QProgressBar::chunk
        {
            background-color: #d7801a;
            width: 3px;
            margin: 1.5px;
        }
        """
        # self.PB.setStyleSheet(PB_STYLE)

        # QMenuBar Style
        MB_STYLE = """
        QMenuBar::item
        {
            background: transparent;
        }

        QMenuBar::item:selected
        {
            background: background-color: rgb(49,49,49);
            border: 1px solid #000;
        }

        QMenuBar::item:pressed
        {
            background: #444;
            border: 1px solid #000;
            background-color: QLinearGradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:1 #212121,
                stop:0.4 #343434/*,
                stop:0.2 #343434,
                stop:0.1 #ffaa00*/
            );
            margin-bottom:-1px;
            padding-bottom:1px;
        }

        """
        self.menuFiles.setStyleSheet(MB_STYLE)
    # ============================ STYLE ======================= #

        # Enable Drah and Drop
        self.Queue_TW.setAcceptDrops(True)
        # Set up handlers for the TableWidget
        self.Queue_TW.dragEnterEvent = self.twDragEnterEvent
        self.Queue_TW.dragMoveEvent = self.twDragMoveEvent
        self.Queue_TW.dropEvent = self.twDropEvent

        # Size of Table Columns
        self.Queue_TW.setColumnWidth(0, 250)
        self.Queue_TW.setColumnWidth(1, 300)
        self.Queue_TW.setColumnWidth(2, 100)
        self.Queue_TW.setColumnWidth(3, 100)
        self.Queue_TW.setColumnWidth(4, 310)
        self.Queue_TW.setColumnWidth(5, 110)

        # operation ALL
        self.Clear_BN.clicked.connect(self.ClearQueue)
        self.Update_BN.clicked.connect(self.UpdateQueue)
        # Render
        self.Render_BN.clicked.connect(self.NBR_render)

    # ============ Drag and Drop Event) ============ #
    def twDragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def twDragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def twDropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            # print links
            self.nukeProjDropped(links)
        else:
            event.ignore()
    # ============  Drag and Drop Ends  ============ #
    # ============ Clear and Update All ============ #

    def NBR_askMsg(self, title, text):
        qmsgBox = QtGui.QMessageBox()
        qmsgBox.setStyleSheet('QMessageBox {background-color: #333; font-size: 12pt; font-family: Trebuchet MS}\nQLabel{color:white;}')  # 585858
        return QtGui.QMessageBox.question(qmsgBox, title, text, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)  # | QtGui.QMessageBox.No

    def ClearQueue(self):
        global folderQueue
        if self.Queue_TW.rowCount() > 0:
            if (self.NBR_askMsg('Clear Render Queue', 'Are you sure you want to clear the whole Render Queue?') == QtGui.QMessageBox.Yes):
                self.Queue_TW.setRowCount(0)
                folderQueue = []
                QtGui.QApplication.processEvents()

    def UpdateQueue(self):
        global folderQueue
        for project in xrange(len(folderQueue)):
            pass
    # ========== Clear and Update All Ends ========== #

    def nukeProjDropped(self, arg):
        global folderQueue
        appendedList = []

        for url in sorted(arg):
            if os.path.exists(url) and os.path.isfile(url) and url.lower().endswith('.nk'):
                if url in folderQueue:
                    pass
                else:
                    appendedList.append(url)
                    folderQueue.append(url)
                    # Add table row
                    rowPosition = self.Queue_TW.rowCount()
                    self.Queue_TW.insertRow(rowPosition)
                    # get All Write Node from .nk
                    # QProcess for nuke
                    self.nukeProcess = QProcess(self)
                    self.nukeProcess.setProcessChannelMode(QProcess.MergedChannels)
                    args = self.createCmdArg(str(url))
                    self.nukeProcess.start(NUKE_EXE, args)
                    # For debug: read output lines
                    self.nukeProcess.readyRead.connect(self.NBR_debug)
                    self.nukeProcess.waitForFinished()
                    self.nukeProcess.close()
                    # Add row and info to table
                    self.NBR_createCheckBoxItemTableWidget(rowPosition, 0, os.path.splitext(os.path.basename(url))[0])
                    # Get the write nodes from text files (D:/Temp/nukeBatch)
                    layout = QtGui.QVBoxLayout()
                    layout.setAlignment(QtCore.Qt.AlignLeft)
                    with open("D:\\Temp\\nukeBatch\\" + os.path.basename(url) + ".txt", "r") as ins:
                        bframe = False
                        bCount = 0
                        for line in ins:
                            if 'FrameRange:' in line:
                                bframe = True
                                continue
                            if (bframe is False):
                                item = QtGui.QCheckBox(str(line).strip())
                                item.setChecked(True)
                                item.setFont(QtGui.QFont('meiryo', 9))
                                layout.addWidget(item)
                            elif (bframe is True):
                                self.NBR_createEditTextItemTableWidget(rowPosition, 2 + bCount, int(str(line).strip()))
                                bCount += 1

                    cellWidget = QtGui.QWidget()
                    cellWidget.setLayout(layout)
                    self.Queue_TW.setCellWidget(rowPosition, 1, cellWidget)
        self.Queue_TW.resizeRowsToContents()
        self.Queue_TW.scrollToBottom()
        QtGui.QApplication.processEvents()

    def createCmdArg(self, nk):  # nk = url
        return ["-ti", CHECKING_NK, nk]

    def createCmdArg2(self, nk, start, end, wnode=[]):
        return ["-ti", RENDER_NK, nk, wnode, start, end]

    def NBR_debug(self):
        while (self.nukeProcess.canReadLine()):
            print (str(self.nukeProcess.readLine()))

    def NBR_createCheckBoxItemTableWidget(self, row, col, text, color='#4c4c4c'):
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        item = QtGui.QCheckBox(text)
        item.setChecked(True)
        item.setFont(QtGui.QFont('meiryo', 9))

        layout.addWidget(item)
        cellWidget = QtGui.QWidget()
        cellWidget.setStyleSheet('color:white; background-color:' + color)

        cellWidget.setLayout(layout)
        self.Queue_TW.setCellWidget(row, col, cellWidget)
        # self.Queue_TW.setItem(row, 0, QtGui.QTableWidgetItem(str(text)))

    def NBR_createEditTextItemTableWidget(self, row, col, text, color='#4c4c4c'):
        layout = QtGui.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        item = QtGui.QSpinBox()
        item.setMaximum(9999)
        item.setValue(text)
        item.setFont(QtGui.QFont('meiryo', 9))

        layout.addWidget(item)
        cellWidget = QtGui.QWidget()
        cellWidget.setStyleSheet('color:white; background-color:' + color)

        cellWidget.setLayout(layout)
        self.Queue_TW.setCellWidget(row, col, cellWidget)

    def NBR_getCellData(self, row, col, key):
        cellDict = {}
        target = self.Queue_TW.cellWidget(row, col)
        if target:
            lay = target.layout()
            if lay:
                for k in xrange(lay.count()):
                    w = lay.itemAt(k).widget()

                    if isinstance(w, QtGui.QCheckBox):
                        cellDict[key] = w.checkState()  # 0 false, > 0 true
                    elif isinstance(w, QtGui.QSpinBox):
                        cellDict[key] = w.value()
        return cellDict

    def NBR_getCellNodeData(self, row, col):
        target = self.Queue_TW.cellWidget(row, col)
        cellUserInputList = []
        if target:
            lay = target.layout()
            if lay:
                for k in xrange(lay.count()):
                    w = lay.itemAt(k).widget()

                    if isinstance(w, QtGui.QCheckBox):
                        cellUserInputList.append([str(w.text()), w.checkState()])
                    else:
                        cellUserInputList.append(-1)
        return cellUserInputList

    def NBR_render(self):
        global folderQueue
        for nk in xrange(len(folderQueue)):
            renderNode = []
            # proj = os.path.splitext(os.path.basename(folderQueue[nk]))[0]
            projDict = self.NBR_getCellData(nk, 0, 'Project')
            if int(projDict['Project']) > 0:
                nodeArr = self.NBR_getCellNodeData(nk, 1)
                startDict = self.NBR_getCellData(nk, 2, 'Start')
                endDict = self.NBR_getCellData(nk, 3, 'End')
                # Write nodes loop
                for node in xrange(len(nodeArr)):
                    if nodeArr[node][1] > 0:  # get each node check state (0/2), selected write node (render)
                        renderNode.append(nodeArr[node][0].split(":")[0])
                # Debug
                print str(renderNode)
                # print nodeArr
                self.nukeProcess = QProcess(self)    # QProcess for nuke
                print nodeArr[node][0].split(":")[0]  # get each node from array
                self.nukeProcess.setProcessChannelMode(QProcess.MergedChannels)
                args = self.createCmdArg2(str(folderQueue[nk]), renderNode, startDict['Start'], endDict['End'])
                self.nukeProcess.start(NUKE_EXE, str(args))
                self.nukeProcess.readyRead.connect(self.NBR_debug)
                self.nukeProcess.waitForFinished()
                self.nukeProcess.close()
                # print nodeArr
                # print startDict
                # print endDict
            # if runDict[nk][proj] > 0:
            #     print self.NBR_getCellData(nk, 1)
            #     print self.NBR_getCellData(0, 1)
            # self.Queue_TW.removeRow(0)
# -------------------------------------------------------------------------------------------------------------------------------------


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    app.setStyleSheet
    ('''
        QWidget
        {
            color: #b1b1b1;
            background-color: #323232;
        }
        QWidget:item:hover
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fcb055, stop: 1 #ffa438);
            color: #000000;
        }

        QWidget:item:selected
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
        }
        QPushButton:pressed
        {
             background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
        }
        QComboBox:hover,QPushButton:hover
        {
            border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f7af59, stop: 1 #f7af59);
        }
        QProgressBar
        {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }

        QProgressBar::chunk
        {
            background-color: #d7801a;
            width: 3px;
            margin: 1.5px;
        }
        '''
     )
    MainWin = FrD_NukeBatchRender()
    MainWin.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
