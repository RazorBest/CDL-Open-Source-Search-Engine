import wx
import wx.adv
import wx.lib.newevent
import os

import loader
import search


LoadDirectoryCommandEvent, EVT_LOAD_DIRECTORY_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()


class TitleWindow(wx.StaticText):
    def __init__(self, parent):
        wx.StaticText.__init__(self, parent, label="Open Source Search Engine",
                               style=wx.ALIGN_CENTRE_HORIZONTAL,
                               size=(350, 100))

        self.SetMinSize(wx.Size(350, 100))

        self.SetFont(wx.Font(30, wx.FONTFAMILY_ROMAN,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


class SearchBar(wx.SearchCtrl):
    def __init__(self, parent):
        wx.SearchCtrl.__init__(self, parent, size=(200, 200))

        self.SetMinSize(wx.Size(30, 30))
        self.SetMaxSize(wx.Size(100, -1))


class FileList(wx.ListBox):
    def __init__(self, parent, **kwargs):
        kwargs['size'] = (100, 200)
        kwargs['style'] = wx.ALIGN_RIGHT
        wx.ListBox.__init__(self, parent, **kwargs)

    def AddFileEntry(self, filename):
        self.Append(filename)

    def DeleteSelection(self):
        selection = self.GetSelection()
        if selection != wx.NOT_FOUND:
            self.Delete(selection)

        return selection


class RemoveButton(wx.Button):
    def __init__(self, parent):
        wx.Button.__init__(self, parent, label='x')

        self.Fit()
        self.SetMinSize(wx.Size(30, 30))


class FileEntry(wx.Window):
    def __init__(self, parent, label=""):
        wx.Window.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(wx.StaticText(self, label=label), 0, wx.ALIGN_LEFT)
        self.sizer.AddStretchSpacer(1)
        self.sizer.Add(RemoveButton(self), 0, wx.ALIGN_RIGHT)

        self.SetSizer(self.sizer)


class EditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.addButton = wx.Button(self, label='Add')
        self.sizer.Add(self.addButton)

        self.removeButton = wx.Button(self, label='Remove')
        self.sizer.Add(self.removeButton)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)


class DirectoryChooser(wx.Panel):
    def __init__(self, parent, dirIndex):
        wx.Panel.__init__(self, parent, size=(300, 300))

        self.SetBackgroundColour(wx.WHITE)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        dirnames = [wIndex.directoryPath for wIndex in dirIndex.values()]
        self.fileList = FileList(self, choices=dirnames)  # , style=wx.BORDER_NONE)
        self.sizer.Add(self.fileList, 1, flag=wx.EXPAND)

        self.editPanel = EditPanel(self)
        self.sizer.Add(self.editPanel)

        self.editPanel.addButton.Bind(wx.EVT_BUTTON, self.OnAdd)
        self.editPanel.removeButton.Bind(wx.EVT_BUTTON, self.OnRemove)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def OnAdd(self, e):
        dialog = wx.DirDialog(self, "Choose a directory")

        if dialog.ShowModal() != wx.ID_OK:
            return

        path = dialog.GetPath()

        # create the event
        evt = LoadDirectoryCommandEvent(-1, directory=dialog.GetPath())
        # post the event
        wx.PostEvent(self, evt)

        # If the directory was already addede to the fileList, don't do anything
        if path in self.fileList.GetItems():
            return

        self.fileList.AddFileEntry(dialog.GetPath())

    def OnRemove(self, e):
        self.fileList.DeleteSelection()


class FileManager(wx.Window):
    def __init__(self, parent, dirIndex):
        wx.Window.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer.AddSpacer(20)
        self.sizer.Add(DirectoryChooser(self, dirIndex))
        self.sizer.AddSpacer(20)
        self.sizer.Add(FileList(self, choices=['ana', 'are', 'mere']))

        self.SetSizerAndFit(self.sizer)
        self.sizer.Fit(self)


class MyFrame(wx.Frame):
    def __init__(self, parent, dirIndex):
        self.dirIndex = dirIndex

        wx.Frame.__init__(
            self, parent, title='Open Source Search Engine', size=(300, 200))

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.AddSpacer(20)

        self.titleWindow = TitleWindow(self)
        self.sizer.Add(self.titleWindow, 1, wx.EXPAND)

        self.searchBar = SearchBar(self)
        self.sizer.Add(self.searchBar, 0, wx.EXPAND | wx.ALIGN_CENTER)
        self.sizer.AddSpacer(10)

        self.fileManager = FileManager(self, self.dirIndex)
        self.sizer.Add(self.fileManager)
        self.sizer.AddSpacer(20)

        self.Bind(EVT_LOAD_DIRECTORY_COMMAND_EVENT, self.OnLoadDir)

        self.SetSizerAndFit(self.sizer)
        self.sizer.Fit(self)
        self.Centre()
        self.Show(True)

    def OnLoadDir(self, e):
        directory = e.directory

        assert (os.path.isdir(directory)
                ), 'argument is not a directory or does not exist'

        dir_id = loader.get_path_id(directory)

        wordsIndex = loader.load_words_index_from_directory(directory)
        self.dirIndex[dir_id] = wordsIndex
        print(wordsIndex)


if __name__ == '__main__':
    dirIndex = loader.load_words_index()

    app = wx.App(False)
    frame = MyFrame(None, dirIndex=dirIndex)

    app.MainLoop()
