class Command(object):
    def __init__(self, context):
        self.ctx = context

    def exec(self, args):
        pass


class SetCommand(Command):
    def exec(self, args):
        index = args[0]
        value = args[1:].join(" ")
        self.ctx.value[index] = value
        return
