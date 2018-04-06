class MainWindow(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, form, parent, *args, **kw):
        self.form = form
        # ensure the parent's __init__ is called
        super().__init__(parent, *args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello World!", pos=(0, 0))
        font = st.GetFont()
        font = font.Bold()
        st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(
            -1, "&Hello...\tCtrl-H",
            "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2", wx.OK | wx.ICON_INFORMATION)

    def Submit(self, event):
        if self.form.is_valid:
            self.Close(True)

    def AddField(self):
        pass


class FormPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.referrers = ['friends', 'advertising', 'websearch', 'yellowpages']
        self.colors = [
            'blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue',
            'black', 'gray'
        ]
        self.createControls()
        self.bindEvents()
        self.doLayout()

    def createControls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.submitButton = wx.Button(self, label="Submit")
        self.nameLabel = wx.StaticText(self, label="Your name:")
        self.nameTextCtrl = wx.TextCtrl(self, value="Enter here your name")
        self.referrerLabel = wx.StaticText(
            self, label="How did you hear from us?")
        self.referrerComboBox = wx.ComboBox(
            self, choices=self.referrers, style=wx.CB_DROPDOWN)
        self.insuranceCheckBox = wx.CheckBox(
            self, label="Do you want Insured Shipment?")
        self.colorRadioBox = wx.RadioBox(
            self,
            label="What color would you like?",
            choices=self.colors,
            majorDimension=3,
            style=wx.RA_SPECIFY_COLS)

    def bindEvents(self):
        for control, event, handler in \
            [(self.submitButton, wx.EVT_BUTTON, self.onSubmit),
             (self.nameTextCtrl, wx.EVT_TEXT, self.onNameEntered),
             (self.nameTextCtrl, wx.EVT_CHAR, self.onNameChanged),
             (self.referrerComboBox, wx.EVT_COMBOBOX, self.onReferrerEntered),
             (self.referrerComboBox, wx.EVT_TEXT, self.onReferrerEntered),
             (self.insuranceCheckBox, wx.EVT_CHECKBOX, self.onInsuranceChanged),
             (self.colorRadioBox, wx.EVT_RADIOBOX, self.onColorchanged)]:
            control.Bind(event, handler)

    def doLayout(self):
        """Layout the controls by means of sizers."""

        # A horizontal BoxSizer will contain the GridSizer (on the left)
        # and the logger text control (on the right):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        # A GridSizer will contain the other controls:
        gridSizer = wx.FlexGridSizer(rows=5, cols=2, vgap=10, hgap=10)

        # Prepare some reusable arguments for calling sizer.Add():
        expandOption = dict(flag=wx.EXPAND)
        noOptions = dict()
        emptySpace = ((0, 0), noOptions)

        # Add the controls to the sizers:
        for control, options in \
                [(self.nameLabel, noOptions),
                 (self.nameTextCtrl, expandOption),
                 (self.referrerLabel, noOptions),
                 (self.referrerComboBox, expandOption),
                  emptySpace,
                 (self.insuranceCheckBox, noOptions),
                  emptySpace,
                 (self.colorRadioBox, noOptions),
                  emptySpace,
                 (self.submitButton, dict(flag=wx.ALIGN_CENTER))]:
            gridSizer.Add(control, **options)

        for control, options in \
                [(gridSizer, dict(border=5, flag=wx.ALL)),
                 (self.logger, dict(border=5, flag=wx.ALL|wx.EXPAND,
                    proportion=1))]:
            boxSizer.Add(control, **options)

        self.SetSizerAndFit(boxSizer)

    # Callback methods:

    def onColorchanged(self, event):
        self.__log('User wants color: %s' % self.colors[event.GetInt()])

    def onReferrerEntered(self, event):
        self.__log('User entered referrer: %s' % event.GetString())

    def onSubmit(self, event):
        self.__log('User clicked on button with id %d' % event.GetId())
        self.Close()

    def onNameEntered(self, event):
        self.__log('User entered name: %s' % event.GetString())

    def onNameChanged(self, event):
        self.__log('User typed character: %d' % event.GetKeyCode())
        event.Skip()

    def onInsuranceChanged(self, event):
        self.__log('User wants insurance: %s' % bool(event.Checked()))

    # Helper method(s):

    def __log(self, message):
        ''' Private method to append a string to the logger text
            control. '''
        self.logger.AppendText('%s\n' % message)


class FieldWidget():
    def __init__(self, parent, field):
        self.field = field
        self._label = wx.StaticText(parent, label=field.text)
        value = ""
        if field.value:
            value = field.value
        self._textCtrl = wx.TextCtrl(parent, value=value)

    @property
    def value(self):
        return self.field.value

    @property
    def layout(self):
        return [(self._label, {}), (self._textCtrl, dict(flag=wx.EXPAND))]

    @property
    def controller(self):
        return self.textCtrl

class FormWindow(wx.Frame):
    def __init__(self, form):
        super().__init__(None, title="Form Monster")
        self._widgets = self._init_widgets(form)
        self._addSubmitBtn()
        self._doLayout()

    def _init_widgets(self, form):
        widgets = []
        for field in form.fields:
            widgets.append(FieldWidget(self, field))
        return widgets

    def _addField(self, field):
        fieldCtl = FieldWidget(self, field)
        self._widgets.append(FieldWidget, field)

    def _doLayout(self):
        boxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        gridSizer = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)

        expandOption = dict(flag=wx.EXPAND)
        noOptions = dict()
        emptySpace = ((0, 0), noOptions)

        for widget in self._widgets:
            for ctrl, options in widget.layout:
                gridSizer.Add(ctrl, **options)
            gridSizer.Add((0, 0), **noOptions)
            gridSizer.Add((0, 0), **noOptions)

        gridSizer.Add(self.submitButton, flag=wx.ALIGN_CENTER)

        self.SetSizerAndFit(gridSizer)

    def _addSubmitBtn(self):
        self.submitButton = wx.Button(self, label="Submit")
        self.submitButton.Bind(wx.EVT_BUTTON, self._onSubmit)

    def _onSubmit(self, event):
        self.Close(True)
