from unicodedata import name
from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, value = None):
        if value is None: 
            super().__init__(value)
        else: 
            try:
                date_value = datetime.strptime(value, '%d.%m.%Y').date()
                date_value = value
                super().__init__(date_value)
                
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
        # #Check Name is not empty 
        # def __init__(self, value):
        #     try:
        #         if not value or not value.strip():
        #             super().__init__(value)
        #     except ValueError:
        #         print("Name cannot be empty")
        

class Phone(Field):

    # Phone instance initialising
    def __init__(self, number):
        if number == '' or number is None or not number.isdigit() or len(number) != 10:
            raise ValueError("Please provide a valid phone number")
        super().__init__(number)
            
class Record:

    # Record instance initialising
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    # pretty representation of Record object data
    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"
    

    #Add Record object to the list of objects
    def add_phone(self, phone_val: str) -> object:
        for phone_obj in self.phones:
            if phone_obj.value == phone_val:
                raise ValueError("Phone already exists")
        self.phones.append(Phone(phone_val))
        return self
                
    # Remove Record instance from the list of objects
    def remove_phone(self, phone_val: str) -> None:
        found_phone = self.find_phone(phone_val)
        return self.phones.remove(found_phone)


    # Change phone number to the new one keeping rest of applicable numbers as is
    def edit_phone(self, old_phone: str, new_phone: str) -> True:
        found_phone = self.find_phone(old_phone)
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
        return True


    # Search the User info by phone number(str)
    def find_phone(self, phone_val: str) -> object:
        for phone in self.phones:
            if phone.value == phone_val:
                return phone
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return self.birthday

class AddressBook(UserDict):
    def __str__(self):
        return f"AddressBook with records: \n{'\n'.join(str(value) for key, value in self.data.items())}"

    # Adding Record object to the AddressBook dictionary
    def add_record(self, user: object) -> str:
        name = user.name.value
        if name not in self.data:
            self.data[name] = user
        return name
          
    # Search Record object by name in the AddressBook dictionary
    def find(self, name: str) -> object:
        return self.data.get(name)


    # Remove Record found by name from the AddressBook dictionary
    def delete(self, name: str) -> str:
        record = self.find(name)
        del self.data[name]
        return name
    

    #Getting upcomming birthdays for the next 7 days from the current date
    
    # transform date object to string in the format DD.MM.YYYY
    def date_to_string(self, date):
        return date.strftime("%d.%m.%Y")

    # Find the next weekday for a given date and weekday
    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
            congratulation_date = start_date + timedelta(days=days_ahead)
        return congratulation_date

    # Adjust the birthday date if it falls on a weekend (Saturday or Sunday)
    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    # Get upcoming birthdays within a specified number of days
    def get_upcoming_birthdays(self, book, days=7):
        congrats_list = []
        upcoming_birthday = None
        today = date.today()

        # Adjust the birthday year to the current year for comparison
        for record in book.data.values():
            dt = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            if dt is None:
                continue

            birthday_this_year = dt.replace(year=today.year)

            # Check if the birthday is within the specified range of days
            if birthday_this_year >= today:

                if 0 <= (birthday_this_year - today).days <= days:
                    upcoming_birthday = self.adjust_for_weekend(birthday_this_year)
            congrats_list.append({
            'name' : record.name.value,
            'birthday' :self.date_to_string(upcoming_birthday)
            })
        
        return congrats_list



#------------------------------------------------
def input_error(func):
    def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Enter correct arguments for the command"
            except KeyError:
                return "Give me a valid value."
            except IndexError:
                return "Enter a valid value."
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
    
    if phone:
        record.add_phone(phone)
    
    return f"Contact added."

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    rec = book.find(name)
    if rec is None:
        return "Contact not found."
    else:
        rec.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return f"{'\n'.join(phone.value for phone in record.phones)}"

def show_all(book):
    return book

# Related to Birthday functionality
@input_error
def add_birthday(args, book):
    name, birth_date, *_ = args
    if book.find(name) is None:
        return "Contact not found."
    record = book.find(name)
    record.add_birthday(birth_date)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if book.find(name) == None:
        return "Contact not found."
    
    if record.birthday.value is None:
        return "Birthday is not set."
    
    return record.birthday.value

@input_error
def birthdays(args, book):
    for record in book.data.values():
        if record.birthday.value is None:
            continue
        return book.get_upcoming_birthdays(book)





def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))
                    
        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()



