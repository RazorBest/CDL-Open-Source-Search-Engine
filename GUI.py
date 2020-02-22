import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['title'] = 'Open Source Search Engine'
        kwargs['size'] = (200, 100)
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None,  wx.ID_ANY)

    app.MainLoop()