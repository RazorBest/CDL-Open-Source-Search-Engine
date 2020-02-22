import wx

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, wx.ID_ANY, "Hello World")
    frame.Show(True)

    app.MainLoop()