import wx


class TitleWindow(wx.StaticText):
    def __init__(self, parent):
        wx.StaticText.__init__(self, parent, label="Open Source Search Engine",
                               style=wx.ALIGN_CENTRE_HORIZONTAL,
                               size=(350, 70))

        self.SetMinSize(wx.Size(350, 70))

        self.SetFont(wx.Font(30, wx.FONTFAMILY_ROMAN,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


class SearchBar(wx.SearchCtrl):
    def __init__(self, parent):
        wx.SearchCtrl.__init__(self, parent, size=(200, 200))

        self.SetMinSize(wx.Size(30, 30))
        self.SetMaxSize(wx.Size(100, -1))


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Open Source Search Engine'
        kwargs['size'] = (300, 200)
        wx.Frame.__init__(self, *args, **kwargs)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.AddSpacer(20)

        self.titleWindow = TitleWindow(self)
        self.sizer.Add(self.titleWindow, 1, wx.EXPAND)

        self.searchBar = SearchBar(self)
        self.sizer.Add(self.searchBar, 0, wx.EXPAND)

        self.SetSizerAndFit(self.sizer)
        self.sizer.Fit(self)
        self.Show(True)


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None,  wx.ID_ANY)

    app.MainLoop()
