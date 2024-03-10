import datetime

class Birthday(Field):
    
    def __init__(self, value):
        try:
            datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthday must be in the format DD.MM.YYYY.")
        super().__init__(value)

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
        except ValueError as e:
            print(e)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        print("Phone number not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                try:
                    phone.value = Phone(new_phone_number).value
                except ValueError as e:
                    print(e)
                return
        print("Phone number not found.")

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        print("Phone number not found.")

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(str(phone) for phone in self.phones)}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(str(phone) for phone in self.phones)}"
        
        
class AddressBook:
    
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            print("Contact not found.")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print("Contact not found.")

    def get_birthdays_per_week(self):
        current_date = datetime.datetime.now().date()
        next_week = current_date + datetime.timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                if current_date <= birthday_date < next_week:
                    birthdays.append(record)
        return birthdays
    
    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    @classmethod
    def load_from_file(cls, filename):
        address_book = cls()
        with open(filename, "rb") as file:
            address_book.data = pickle.load(file)
        return address_book
    
    def main():
        assistant = PhonebookAssistant()
        address_book = AddressBook()
        while True:
            command = input("Your command: ").lower()

            if command == "hello":
                print("How can I help you?")
            elif command.startswith("add"):
                _, name, phone_number = command.split(" ", 2)
                record = Record(name)
                record.add_phone(phone_number)
                address_book.add_record(record)
                print(assistant.add_contact(name, phone_number))
            elif command.startswith("change"):
                _, name, new_phone_number = command.split(" ", 2)
                record = address_book.find(name)
                if record:
                    record.edit_phone(record.phones[0].value, new_phone_number)
                    assistant.change_contact(name, new_phone_number)
            elif command.startswith("phone"):
                _, name = command.split(" ", 1)
                record = address_book.find(name)
                if record:
                    print(assistant.show_phone(name))
            elif command == "all":
                print(assistant.show_all())
            elif command.startswith("add-birthday"):
                _, name, birthday = command.split(" ", 2)
                record = address_book.find(name)
                if record:
                    record.add_birthday(birthday)
                    print(f"Birthday added for {name}.")
            elif command.startswith("show-birthday"):
                _, name = command.split(" ", 1)
                record = address_book.find(name)
                if record and record.birthday:
                    print(f"Birthday for {name}: {record.birthday.value}")
                else:
                    print(f"No birthday found for {name}.")
            elif command == "birthdays":
                birthdays = address_book.get_birthdays_per_week()
                if birthdays:
                    print("Birthdays for next week:")
                    for record in birthdays:
                        print(f"{record.name.value}: {record.birthday.value}")
                else:
                    print("No birthdays for next week.")
            elif command in ["close", "exit"]:
                print("Good bye!")
                break
            else:
                print("Invalid command.")

if __name__ == "__main__":
    main()
    
    