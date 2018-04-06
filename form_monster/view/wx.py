import wx
from .base_view import BaseView


class FMFrame(wx.Frame):
    def __init__(self, form, parent=None):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(500, 300),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gridWrapper = wx.BoxSizer(wx.VERTICAL)

        self.gridScroll = wx.ScrolledWindow(self, wx.ID_ANY,
                                            wx.DefaultPosition, wx.DefaultSize,
                                            wx.HSCROLL | wx.VSCROLL)
        self.gridScroll.SetScrollRate(5, 5)
        grid = wx.FlexGridSizer(0, 2, 5, 0)
        grid.SetFlexibleDirection(wx.BOTH)
        grid.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(
            self.gridScroll, wx.ID_ANY, u"MyLabel sadfdsafasdf ",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        grid.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(
            self.gridScroll, wx.ID_ANY,
            u"asdfsffsadfsd safd d fas dfdasfsadfsadfasf", wx.DefaultPosition,
            wx.Size(-1, -1), 0)
        self.m_textCtrl1.SetBackgroundColour(wx.Colour(255, 0, 0))

        grid.Add(self.m_textCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(self.gridScroll, wx.ID_ANY,
                                           u"MyLabel", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        grid.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self.gridScroll, wx.ID_ANY,
                                       wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        grid.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self.gridScroll, wx.ID_ANY,
                                           u"MyLabel", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        grid.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.m_checkBox1 = wx.CheckBox(self.gridScroll, wx.ID_ANY,
                                       u"Check Me!", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.m_checkBox1.Enable(False)

        grid.Add(self.m_checkBox1, 0, wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self.gridScroll, wx.ID_ANY,
                                           u"MyLabel", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        grid.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_checkBox2 = wx.CheckBox(self.gridScroll, wx.ID_ANY,
                                       u"Check Me!", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        grid.Add(self.m_checkBox2, 0, wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(self.gridScroll, wx.ID_ANY,
                                           u"MyLabel", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        grid.Add(self.m_staticText5, 0, wx.ALL, 5)

        m_choice1Choices = ["a", "b", "c"]
        self.m_choice1 = wx.Choice(self.gridScroll, wx.ID_ANY,
                                   wx.DefaultPosition, wx.DefaultSize,
                                   m_choice1Choices, 0)
        self.m_choice1.SetSelection(-1)
        grid.Add(self.m_choice1, 0, wx.ALL, 5)

        self.gridScroll.SetSizer(grid)
        self.gridScroll.Layout()
        grid.Fit(self.gridScroll)
        gridWrapper.Add(self.gridScroll, 1, wx.EXPAND | wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"MyButton",
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        gridWrapper.Add(self.m_button1, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(gridWrapper)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_textCtrl1.Bind(wx.EVT_TEXT, self.onTextUpdate)
        self.m_button1.Bind(wx.EVT_BUTTON, self.onSubmit)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def onTextUpdate(self, event):
        event.Skip()

    def onSubmit(self, event):
        event.Skip()


class WxView(BaseView):
    def __init__(self, form):
        super().__init__(form)

    def run(self):
        app = wx.App()
        frame = FMFrame(self.form)
        frame.Show()
        app.MainLoop()
        return {field.name: field.value for field in self.form.fields}
