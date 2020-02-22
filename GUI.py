import wx


class TitleWindow(wx.StaticText):
    def __init__(self, parent):
        wx.StaticText.__init__(self, parent, label="Open Source Search Engine",
                             style=wx.ALIGN_CENTRE_HORIZONTAL,
                             size=(400, 400))

        self.SetFont(wx.Font(30, wx.FONTFAMILY_ROMAN,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                             
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Open Source Search Engine'
        kwargs['size'] = (300, 200)
        wx.Frame.__init__(self, *args, **kwargs)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.AddSpacer(20)

        self.titleWindow = TitleWindow(self)
        self.sizer.Add(self.titleWindow, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None,  wx.ID_ANY)

    app.MainLoop()
