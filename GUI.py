import wx
import wx.adv
import wx.lib.newevent
import os

import loader
import search


LoadDirectoryCommandEvent, EVT_LOAD_DIRECTORY_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()
RemoveDirectoryCommandEvent, EVT_REMOVE_DIRECTORY_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()


class TitleWindow(wx.StaticText):
    def __init__(self, parent):
        wx.StaticText.__init__(self, parent, label="Open Source Search Engine",
                               style=wx.ALIGN_CENTRE_HORIZONTAL,
                               size=(350, 100))

        self.SetMinSize(wx.Size(350, 100))

        self.SetFont(wx.Font(30, wx.FONTFAMILY_ROMAN,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


class SearchBar(wx.SearchCtrl):
    def __init__(self, parent, **kwargs):
        kwargs['size'] = (200, 200)
        wx.SearchCtrl.__init__(self, parent, **kwargs)

        self.SetMinSize(wx.Size(300, 30))
        self.SetMaxSize(wx.Size(400, -1))

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)

    def OnEnter(self, e):
        # create the event
        evt = wx.PyCommandEvent(
            wx.EVT_SEARCHCTRL_SEARCH_BTN.typeId, self.GetId())
        evt.SetString(self.GetValue())
        # post the event
        wx.PostEvent(self, evt)


class FileList(wx.ListBox):
    def __init__(self, parent, **kwargs):
        kwargs['size'] = (100, 200)
        kwargs['style'] = wx.ALIGN_RIGHT
        wx.ListBox.__init__(self, parent, **kwargs)

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleClick)

    def OnDoubleClick(self, e):
        selection = self.GetSelection()
        assert(selection != wx.NOT_FOUND), "Nothing is selected"

        path = self.GetString(selection)
        os.system('xdg-open ' + path)

    def AddFileEntry(self, filename):
        self.Append(filename)

    def GetSelectedString(self):
        selection = self.GetSelection()
        if selection == wx.NOT_FOUND:
            return None

        return self.GetString(selection)

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
        # , style=wx.BORDER_NONE)
        self.fileList = FileList(self, choices=dirnames)
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

        # If the directory was already added to the fileList, don't do anything
        if path in self.fileList.GetItems():
            return

        self.fileList.AddFileEntry(dialog.GetPath())

    def OnRemove(self, e):
        directory = self.fileList.GetSelectedString()
        self.fileList.DeleteSelection()

        if directory == None:
            return

        # create the event
        evt = RemoveDirectoryCommandEvent(-1, directory=directory)
        # post the event
        wx.PostEvent(self, evt)


class FileManager(wx.Window):
    def __init__(self, parent, dirIndex):
        wx.Window.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer.AddSpacer(20)
        self.fileList = FileList(self, choices=['ana', 'are', 'mere'])
        self.sizer.Add(self.fileList)

        self.sizer.AddSpacer(20)
        self.sizer.Add(DirectoryChooser(self, dirIndex))

        self.SetSizerAndFit(self.sizer)
        self.sizer.Fit(self)

    def UpdateResults(self, choices):
        self.fileList.Set(choices)


class MyFrame(wx.Frame):
    def __init__(self, parent, dirIndex):
        self.dirIndex = dirIndex

        wx.Frame.__init__(
            self, parent, title='Open Source Search Engine', size=(300, 200))

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.AddSpacer(20)

        self.titleWindow = TitleWindow(self)
        self.sizer.Add(self.titleWindow, 1, wx.EXPAND)

        self.searchBar = SearchBar(self, style=wx.TE_PROCESS_ENTER)
        self.sizer.Add(self.searchBar, 0, wx.EXPAND | wx.ALIGN_CENTER)
        self.sizer.AddSpacer(10)

        self.fileManager = FileManager(self, self.dirIndex)
        self.sizer.Add(self.fileManager)
        self.sizer.AddSpacer(20)

        self.Bind(EVT_LOAD_DIRECTORY_COMMAND_EVENT, self.OnLoadDir)
        self.Bind(EVT_REMOVE_DIRECTORY_COMMAND_EVENT, self.OnRemoveDir)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch)

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

    def OnRemoveDir(self, e):
        directory = e.directory
        dir_id = loader.get_path_id(directory)
        assert(dir_id in self.dirIndex), 'dir_id is not in self.dirIndex'

        del self.dirIndex[dir_id]
        os.remove(loader.DATA_DIRECTORY + dir_id)

    def OnSearch(self, e):
        query = e.GetString()
        
        files = []
        for wordsIndex in self.dirIndex.values():
            files.extend(search.search(query, wordsIndex))
        
        print(files)
        self.fileManager.UpdateResults(files)

if __name__ == '__main__':
    dirIndex = loader.load_words_index()

    app = wx.App(False)
    frame = MyFrame(None, dirIndex=dirIndex)

    app.MainLoop()
