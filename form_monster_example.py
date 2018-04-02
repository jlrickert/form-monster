import form_monster as Fm

def get_first_name():
    return input("First name: ")

form = {
    'first_name': {
        'get': get_first_name,
        'type': str,
        'validate': lambda x: True,
        'error_msg': "Invalid name"
    },
    'last_name': {
        'get': get_first_name,
        'type': str,
        'validate': lambda x: True,
        'error_msg': "Inval id name"
    },
    'over_18': {
        #get: lambda: input("over 18?: "),
        'type': bool,

        #example that will default to making sure it is a bool
        #validate: lambda x: x is bool
        #calculate: lambda: calculate();
        #depencies: ["date_of_birth"]
    }
}

console = Fm.FormMonster(form)

console.gui()

print(console.get("first_name"))
