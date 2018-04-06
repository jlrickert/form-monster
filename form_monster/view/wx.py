import wx
from .base_view import BaseView


class FieldValueWidget(object):
    def __init__(self, parent=None, field=None, sizer=None):
        self._field = field
        self.static_text = wx.StaticText(parent, wx.ID_ANY, self._field.text,
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap(-1)
        self.is_valid = field.is_valid
        value = field.value
        if value is None:
            value = ""
        self.text_controller = wx.TextCtrl(parent, wx.ID_ANY,
                                           value, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        sizer.Add(self.static_text, 0, wx.ALL, 5)
        sizer.Add(self.text_controller, 1, wx.ALL | wx.EXPAND, 5)
        self.text_controller.Bind(wx.EVT_TEXT, self.on_text_update)

    def on_text_update(self, event):
        self._field.value = event.GetString()
        self.is_valid = self._field.is_valid
        if self._field.is_valid:
            self.text_controller.SetBackgroundColour(wx.Colour(127, 127, 0))
        else:
            self.text_controller.SetBackgroundColour(wx.Colour(255, 0, 0))


class FMFrame(wx.Frame):
    def __init__(self, form, parent=None):
        super().__init__(
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(500, 300),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        gridSizer = self._init_grid_sizer()
        self.grid = self._init_grid(gridSizer)

        for field in form.fields:
            FieldValueWidget(parent=self.grid, field=field, sizer=gridSizer)

        self.submit_button = wx.Button(self, wx.ID_ANY, "Submit",
                                       wx.DefaultPosition, wx.DefaultSize, 0)

        gridWrapper = wx.BoxSizer(wx.VERTICAL)
        gridWrapper.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        gridWrapper.Add(self.submit_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetSizer(gridWrapper)
        self.Layout()
        self.Centre(wx.BOTH)
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)

    def __del__(self):
        pass

    def _init_grid_sizer(self):
        sizer = wx.FlexGridSizer(0, 2, 5, 0)
        sizer.SetFlexibleDirection(wx.BOTH)
        sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        return sizer

    def _init_grid(self, sizer):
        grid = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        grid.SetScrollRate(5, 5)
        grid.SetSizer(sizer)
        grid.Layout()
        sizer.Fit(grid)
        return grid

    # Virtual event handlers, overide them in your derived class
    def onTextUpdate(self, event):
        event.Skip()

    def on_submit(self, event):
        event.Skip()
        self.Close()


class WxView(BaseView):
    def __init__(self, form):
        super().__init__(form)

    def run(self):
        app = wx.App()
        frame = FMFrame(self.form)
        frame.Show()
        app.MainLoop()
        return {field.name: field.value for field in self.form.fields}
