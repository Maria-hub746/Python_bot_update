from collections import UserDict
from datetime import date
from re import search
import pickle

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    def iterator(self, n):
        records = []

        n = n if n else len(self.data)

        for record in self.data.values():

            if len(records) == n:
                yield records
                records = []

            records.append(record)

        if records:
            yield records

    def write_contacts_to_file(self):
        with open('pickle.contacts', 'wb') as file:
            pickle.dump(self.data, file)

    def read_contacts_from_file(self):
        try:
            with open('pickle.contacts', 'rb') as file:
                contacts = pickle.load(file)
                return contacts
        except FileNotFoundError:
            pass

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.value: str = value
       
    @Field.value.setter
    def value(self, value):
        self._value = self.check_phone(value)

    @staticmethod
    def check_phone(value):
        clean_phone = (
                        value.strip()
                        .removeprefix("+")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("-", "")
                        .replace(" ", "")
                    )

        value = search(r"(?:380|0)\d{9}", clean_phone)
        if not value:
            raise ValueError(f"Phone number {clean_phone} is not valid")

        value = value.group()
        value = '38' + value if value.startswith('0') else value

        return int(value)

class Birthday:
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, value):
        self._value = self.check_date(value)

    @staticmethod
    def check_date(value):
        value = value.strip()

        for separator in (".", ",", "-", ":", "/"):
            value, *args = value.split(separator)

            if args:
                break

        if not args or len(args) > 2:
            raise ValueError("Invalide date format. Date format should be YYYY.MM.DD or DD.MM.YYYY.")

        if int(value) > 31:
            return date(int(value), int(args[0]), int(args[1]))

        return date(int(args[1]), int(args[0]), int(value))

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else ''


    def add(self, phone):
        self.phones.append(Phone(phone))

    def change(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add(new_phone)
                self.phones.remove(phone)
                return True

    def delete(self, delete_phone):
        for phone in self.phones:
            if phone.value == delete_phone:
                self.phones.remove(phone)
                return True

    def days_to_birthday(self):
        if not self.birthday:
            return

        birthday = self.birthday.value
        today = date.today()

        if (birthday.month >= today.month) and (birthday.day >= today.day):
            birthday = birthday.replace(year=today.year)

        elif birthday.month <= today.month:
            birthday = birthday.replace(year=today.year + 1)

        return (birthday - today).days