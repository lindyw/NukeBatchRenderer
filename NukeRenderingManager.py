import os
import wx


class mainWindow(wx.Frame):

    def __init__(self):

        # constructor
        wx.Frame.__init__(self, None, title="Nuke Rendering Manager", size=(600, 300), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        # it creates a status bar
        self.CreateStatusBar()

        # prepare the Nuke scripts list on screen
        self.NukeScriptsList = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.NukeScriptsList.SetEditable(False)
        self.NukeScriptsList.SetBackgroundColour((53, 53, 53))  # dark grey
        self.NukeScriptsList.SetForegroundColour((255, 255, 255))  # White
        self.NukeScriptsList.SetValue('Nuke scripts:\n')

        # it creates the render button
        self.RenderButton = wx.Button(self, label="Render", pos=(8, 8))

        # layout
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(self.NukeScriptsList, 1, wx.EXPAND)
        self.layout.Add(self.RenderButton, 0, wx.EXPAND)
        self.SetSizer(self.layout)

        # variables
        self.NukeScripts = []
        self.dirName = ""
        self.fileName = ""

        # it creates menu items
        menuBar = wx.MenuBar()

        filemenu = wx.Menu()
        addNukeScript = filemenu.Append(wx.ID_ANY, "Add Nuke script", "Add Nuke script")
        ClearList = filemenu.Append(wx.ID_ANY, "Clear list", "Clear list")
        exitEvt = filemenu.Append(wx.ID_EXIT, "Exit", "Exit")

        menuBar.Append(filemenu, "File")
        self.SetMenuBar(menuBar)

        # it binds elements to events
        self.Bind(wx.EVT_MENU, self.onAdd, addNukeScript)
        self.Bind(wx.EVT_MENU, self.onClearList, ClearList)
        self.Bind(wx.EVT_BUTTON, self.onRender, self.RenderButton)
        self.Bind(wx.EVT_MENU, self.onExit, exitEvt)

        # it shows the main window
        self.Show(True)

    # it adds Nuke scripts on the list
    def onAdd(self, event):
        wildcard = "Nuke scripts *.nk|*.nk"
        dlg = wx.FileDialog(self, message="Add Nuke Project", wildcard=wildcard, style=wx.OPEN | wx.MULTIPLE)
        # dlg = wx.FileDialog(self, message="Add Nuke script", wildcard=wildcard, style=wx.OPEN)
        # if dlg.ShowModal() == wx.ID_OK:
        #     self.dirName = dlg.GetDirectory()
        #     self.fileName = dlg.GetFilename()
        #     self.NukeScripts.append(self.dirName + "\\" + self.fileName)
        #     self.updateList()
        if dlg.ShowModal() == wx.ID_OK:  # when user pressed OK button
                self.fileNames = dlg.GetPaths()
                for i in self.fileNames:
                    # Check if the nuke project exists
                    self.extension = os.path.splitext(str(i))
                    if self.extension[1] == ".nk":
                        self.NukeScripts.append(str(i))
                self.updateList()
        dlg.Destroy()

    # it updates the Nuke scripts list on screen
    def updateList(self):
        self.NukeScriptsList.Clear()
        for i in self.NukeScripts:
            self.NukeScriptsList.AppendText(i + "\n")

    def onClearList(self, event):
        self.NukeScriptsList.Clear()
        self.NukeScripts = []

    # it starts the rendering process
    def onRender(self, event):
        for i in self.NukeScripts:
            os.system("D:\Python\NukeBatchRenderer\exeNuke.bat" + " " + i)

    # it closes the program
    def onExit(self, event):
        self.Close(True)


app = wx.App(False)
mainWindow = mainWindow()
app.MainLoop()
