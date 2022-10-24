from CLI_classes import AddressBook, Record


def corrector(handler):
    def wrapper(*args, **kwargs):
        try:
            result = handler(*args, **kwargs)
            return result
        except KeyError:
            print('Enter user name.')
        except ValueError:
            print('Enter correct type.')
        except IndexError:
            print('Give me name and phone')
        except TypeError:
            print('Give me name and phone')
    return wrapper
    
@corrector
def hello():
    return "Hello! How can I help you?"

@corrector
def add_new_contact(data):
    name, phone = create_data(data)
    record_add = Record(name.lower())
    record_add.add(phone)
    addressbook.add_record(record_add)
    return f'New contact {name} : {phone}'


@corrector
def add_phone(data):
    name, phone = create_data(data)
    record_add_phone = addressbook.data[name]
    record_add_phone.add(phone)
    return f"{addressbook.data[name].name.value} : {list(map(lambda x: x.value, addressbook.data[name].phones))}"

@corrector
def change(data):
    name, phone = create_data(data)
    new_phone = data[2]
    record_change = addressbook.data[name]
    if record_change.change(old_phone= phone, new_phone=new_phone) is True:
        return f"{addressbook.data[name].name.value} : {list(map(lambda x: x.value, addressbook.data[name].phones))}"
    else:
        return 'The phone number not exist'

@corrector
def find_phone(name):
    name = name[0]
    return f"{addressbook.data[name].name.value} : {list(map(lambda x: x.value, addressbook.data[name].phones))}"


def show_all():
    return f'All contacts: {addressbook.data}'

@corrector
def delete(data):
    name, phone = create_data(data)
    record_delete = addressbook.data[name]

    if record_delete.delete(phone) is True:
        return f'{name} : {phone} has been deleted'
    else:
        return 'The phone number not exist'

def finish_work():
    return 'Good bye!'


INFORMATION = {
    'add': add_new_contact,
    'add_phone': add_phone,
    'change': change,
    'phone': find_phone,
    'hello': hello,
    'show all': show_all,
    'good bye': finish_work,
    'close': finish_work,
    'exit': finish_work,
    'delete': delete
}

information =['add', 'add_phone', 'change', 'phone', 'hello', 'show all', 'good bye', 'close', 'exit', 'delete']

def create_data(data):
    name = data[0]
    phone = data[1]
    if name.isnumeric():
        raise ValueError('Wrong name')
    if not phone.isnumeric():
        raise ValueError('Wrong phone')
    return name, phone



def main():
    while True:
        go = input('Enter command: ').lower()

        if go == 'help':
            print(f"All commands: {information}.")
            continue

        elif go == "":
            continue

        elif go in INFORMATION:
            print(INFORMATION[go]())
            if INFORMATION[go]() == "Good bye!":
                break

        elif go.split()[0] in INFORMATION:
            print(INFORMATION[go.split()[0]](go.split()[1:]))
            

        else:
            print(
                f"Sorry, i don't know, what is '{go}', please, try again.\nAll commands: {information}")


if __name__ == "__main__":
    addressbook = AddressBook()
    main()