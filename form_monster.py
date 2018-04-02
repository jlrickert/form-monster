import os

def clear_screan():
    os.system("cls")

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

class FormMonster(object):
    valid_tokens = {
        "set": {
            "arity": 2,
            "command": SetCommand
        },
        "get": {
            "arity": 2
        },
        "page": {
            "arity": 1
        },
        "complete": {
            "arity": 0
        },
        "DEFAULT": {
            "arity": 0
        }
    }

    def __init__(self, form_data):
        self.__raw = form_data
        self.values = ['' for x in list(form_data.keys())]
        self.complete = False

    def set_value(self, key, value):
        self.values[key] = value

    def gui(self):
        errors = []
        while not self.complete:
            clear_screan()
            self.__print_forms()

            if errors:
                print(errors)

            raw_string = self.__prompt()
            ast, errors = self.__parse(raw_string)

            if errors:
                print(errors)
                continue

            errors = self.__eval(ast)

            if errors:
                print(errors)

            clear_screan()

    def __prompt(self):
        return input(">>> ")

    def __parse(self, raw_str):
        tokens = [s for s in raw_str.strip().split(" ") if s != ""]
        errors = []

        if len(tokens) == 0:
            return ((), errors)

        command_name = tokens[0]

        try:
            command = self.valid_tokens[command_name]
            args = tokens[1:]
            if len(args) < command["arity"]:
                errors.append("Invalid arity")     
        except KeyError:
            errors.append("{} is not a valid command".format(command_name))

        return ([command] + args, errors)
    
    def __eval(self, tokens):
        if tokens:
            return []
        
        command = self.valid_tokens[tokens[0]]
        return command.exec(tokens[1:])

    def __print_forms(self):
        for i, key in enumerate(self.__raw):
            print("[{}] {} {}".format(i, key, self.values[i]))
