import wx
import wx.adv
from .base_view import BaseView


class FieldWidget(object):
    pass


class FieldValueWidget(FieldWidget):
    def __init__(self, parent=None, field=None, sizer=None):
        self._field = field
        self.static_text = self.init_static_text(parent, sizer)
        self.controller = self.init_controller(parent, sizer)
        self.set_value(field.value)

    def init_static_text(self, parent, sizer):
        static_text = wx.StaticText(parent, wx.ID_ANY, self._field.text,
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        static_text.Wrap(-1)
        sizer.Add(static_text, 0, wx.EXPAND, 5)
        return static_text

    def init_controller(self, parent, sizer):
        if self._field:
            pass


# wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
        controller = wx.TextCtrl(parent, wx.ID_ANY, "", wx.DefaultPosition,
                                 wx.Size(-1, -1), 0)

        controller.Bind(wx.EVT_TEXT, self.on_text_update)
        sizer.Add(controller, 1, wx.EXPAND, 5)
        return controller

    def on_text_update(self, event):
        self._field.value = event.GetString()
        if self._field.is_valid():
            self.controller.SetBackgroundColour(wx.Colour(127, 127, 0))
        else:
            self.controller.SetBackgroundColour(wx.Colour(255, 0, 0))

    def set_value(self, value):
        value = self._field.value
        if value is None:
            value = ""
        self.controller.SetValue(value)


class FrameMonster(wx.Frame):
    def __init__(self, form, parent=None):
        super().__init__(
            parent,
            title="Frame Monster",
        )
        self.form = form
        main_layout = self._init_main_layout()
        self._init_field_panel(form, main_layout)
        self._add_submit_button(main_layout)
        self.Centre()
        self.Show()

    def _init_main_layout(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(layout)
        return layout

    def _add_submit_button(self, layout):
        button = wx.Button(self, wx.ID_ANY, "Submit", wx.DefaultPosition,
                           wx.DefaultSize, 0)
        layout.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        button.Bind(wx.EVT_BUTTON, self.on_submit)

    def _init_field_panel(self, form, layout):
        sizer = wx.FlexGridSizer(0, 2, 10, 10)
        sizer.AddGrowableCol(1, 0)
        panel = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition,
                                  wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        panel.SetScrollRate(5, 5)
        panel.SetSizer(sizer)

        for field in form.fields:
            FieldValueWidget(parent=panel, field=field, sizer=sizer)

        layout.Add(panel, 1, wx.EXPAND | wx.ALL, 5)

    def on_submit(self, event):
        event.Skip()
        self.Close()

    def __del__(self):
        pass


class WxView(BaseView):
    def __init__(self, form):
        super().__init__(form)

    def run(self):
        app = wx.App()
        # frame = FMFrame(self.form)
        frame = FrameMonster(self.form)
        app.MainLoop()
        return {field.name: field.value for field in self.form.fields}
