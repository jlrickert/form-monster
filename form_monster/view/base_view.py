class BaseView(object):
    def __init__(self, form):
        self.form = form

    def run(self):
        pass

    def data(self):
        return {key: field.value for key, field in self.form.fields}
