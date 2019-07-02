import os
import wx


class mainWindow(wx.Frame):
    # Constructor
    def __init__(self):
        wx.Frame.__init__(self, None, title="Nuke Batch Renderer", size=(600, 300), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
    # Create Status Bar
        self.CreateStatusBar()
    # add text control to show which Nuke projects are going to processed:
        self.NukeScriptsList = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.NukeScriptsList.SetEditable(False)  # Read only
        self.NukeScriptsList.SetBackgroundColour((53, 53, 53))  # dark grey
        self.NukeScriptsList.SetForegroundColour((255, 255, 255))  # White
        self.NukeScriptsList.SetValue('Nuke Project(s):\n')

    # Create Render Button
        self.RenderButton = wx.Button(self, label="Render", pos=(8, 200))
    # BoxSizer: define a layout that places elements vertically
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(self.NukeScriptsList, 1, wx.EXPAND)  # number describes how much space each element occupied "1"
        self.layout.Add(self.RenderButton, 0, wx.EXPAND)
        self.SetSizer(self.layout)

    # Variables
        self.NukeScripts = []
        # self.dirName = ""
        # self.fileName = ""

    # Menu
        menuBar = wx.MenuBar()
        filemenu = wx.Menu()
        # Button ID elements (wx.ID_ANY: get an ID for the item, ID_EXIT: creates a special ID for the exit action)
        addNukeScript = filemenu.Append(wx.ID_ANY, "Add Nuke Project", "Add Nuke Project")
        ClearList = filemenu.Append(wx.ID_ANY, "Clear list", "Clear list")
        exitEvt = filemenu.Append(wx.ID_EXIT, "Exit", "Exit")
        # File -> Add Nuke Project + Clear list + Exit
        menuBar.Append(filemenu, "File")
        self.SetMenuBar(menuBar)

        # let the elements perform operations -> bind the element to a specific function
        self.Bind(wx.EVT_MENU, self.onAdd, addNukeScript)  # EVT_MENU:Menu event, onAdd:link function to element self, element self:addNukeScript
        self.Bind(wx.EVT_MENU, self.onClearList, ClearList)
        self.Bind(wx.EVT_MENU, self.onRender, self.RenderButton)
        self.Bind(wx.EVT_MENU, self.onExit, exitEvt)

        # Show MainWindow
        self.Show(True)

    # Functions
    # 1. adds Nuke scripts (project.nk) on the list
    def onAdd(self, event):
        wildcard = "Nuke Projects *.nk|*.nk"
        dlg = wx.FileDialog(self, message="Add Nuke Project", wildcard=wildcard, style=wx.OPEN | wx.MULTIPLE)  # Browser open

        try:
            if dlg.ShowModal() == wx.ID_OK:  # when user pressed OK button
                self.fileNames = dlg.GetPaths()
                for i in self.fileNames:
                    # Check if the nuke project exists
                    self.extension = os.path.splitext(str(i))
                    if self.extension[1] == ".nk":
                        self.NukeScripts.append(str(i))
                self.updateList()
        except:
            print "Unable to read files."
        dlg.Destroy()

    def updateList(self):
        self.NukeScriptsList.Clear()
        for i in self.NukeScripts:
            self.NukeScriptsList.AppendText(str(i) + "\n")
            print i

    # 2. Clear Nuke scripts on the list
    def onClearList(self, event):
        self.NukeScriptsList.Clear()
        self.NukeScripts = []
        print "Cleared."

    # 3. Start Render Process
    def onRender(self, event):
        print "Rendering..."
        # print self.NukeScripts
        # for i in self.NukeScripts:
        #     print self.NukeScripts[0]
        #     os.system("D:/Python/NukeBatchRenderer/exeNuke.bat" + " " + i)

    # 4. Exit (Close Program)
    def onExit(self, event):
        self.Close(True)


app = wx.App(False)
mainWindow = mainWindow()
app.MainLoop()
