from datetime import datetime, date
import csv
import re  
        
class User:
    def __init__(self,Name,Birthday,Email,State,ZipCode):
            self.Name=Name
            self.Birthday=Birthday
            self.Email=Email
            self.State=State
            self.ZipCode=ZipCode
    
    def is_valid_state(self):
        return self.State not in ['NJ', 'CT', 'PA', 'MA', 'IL', 'ID', 'OR']


    def is_valid_age(self):
        Birthday_obj = datetime.strptime(self.Birthday, '%m/%d/%Y')
        today = date.today()
        age = today.year-Birthday_obj.year
        if (today.month < Birthday_obj.month or (today.month == Birthday_obj.month and today.day < Birthday_obj.day)):
            age -= 1
        return age >= 21


    def is_valid_mail(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, self.Email)):
            return True


    def is_valid_zipcode(self):
        for i in range(len(self.ZipCode)-1):
            if (abs(int(self.ZipCode[i])-int(self.ZipCode[i+1])) == 1):
                return False
        return True


    def first_monday_born(self):
        Birthday_obj = datetime.strptime(self.Birthday, '%m/%d/%Y')
        return Birthday_obj.weekday() != 0 or Birthday_obj.day > 7

            
class Order:
    def __init__(self,Order_ID,Name,Birthday,Email,State,ZipCode):
        self.Order_ID=Order_ID
        self.user=User(Name,Birthday,Email,State,ZipCode)
        
    def validate_orders(self):
        return self.user.is_valid_state() and self.user.is_valid_zipcode() and self.user.is_valid_age() and self.user.is_valid_age() and self.user.is_valid_mail() and self.user.first_monday_born()           
        

    
    
class Acme:
    def __init__(self):
        self.valid_orders=[]
        self.invalid_orders=[]
    
    
    def process(self):
        with open('orders.csv', 'r') as file:
            csvreader = csv.reader(file)
            headers = next(csvreader)

            ID_index = headers.index('ID')
            Name_index = headers.index('Name')
            Birthday_index = headers.index('Birthday')
            Email_index = headers.index('Email')
            State_index = headers.index('State')
            ZipCode_index = headers.index('ZipCode')

            for row in csvreader:
                Order_ID = row[ID_index]
                Name = row[Name_index]
                Birthday = row[Birthday_index]
                Email = row[Email_index]
                State = row[State_index]
                ZipCode = row[ZipCode_index]
                
                order=Order(Order_ID, Name, Birthday, Email, State, ZipCode)

                if (order.validate_orders()):
                    self.valid_orders.append(order)
                else:
                    self.invalid_orders.append(order)
                    
                    
    def write(self):
        with open('valid.csv', 'w', newline='') as valid_file: 
            writer = csv.writer(valid_file) 
            writer.writerows([[order.Order_ID]] for order in self.valid_orders)
            
        with open('invalid.csv', 'w', newline='') as invalid_file: 
            writer = csv.writer(invalid_file) 
            writer.writerows([[order.Order_ID]] for order in self.invalid_orders)
            
            
if __name__ == '__main__':
    acme = Acme()
    acme.process()
    acme.write()
            