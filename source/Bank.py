#MUST PIP INSTALL simplejson

import decimal
from os import name
import sys
import simplejson as json

from decimal import Decimal

from datetime import datetime


class Customer:
    def __init__(self):
        self.username = None  #A unique username that is set by the user on creation of their “user”. This is used as unique ID for each customer
        self.pin = None #A unique 4 digit string that is used to verify the user
        self.name = None  #the user's name
        self.age = None  #the user's age

    def getAccountDict(self):
        """Will return a “sub dictionary” of the dictionary 'AccountDict', containing just the accounts the belong to the customer"""
        UserAccountsDict = {}  #create empty dictionary
        for account in AccountDict.values():  #loop through each account in the main account dictionary
            if account.ownerUsername == self.username:
                #any item that is owned by the active user, add this account to the user dictionary
                id = account.uniqueID

                UserAccountsDict[id] = account #add account to the user dictionary
        return UserAccountsDict

    def menu(self):
        """Displays a menu which allows the user to select a method to run"""
        while True:
            #display menu
            print("Logged in as", self.name)

            print("1. Select Account")
            print("2. Create New Account")
            print("3. Logout")
            print("\n")

            try:
                menuoption = int(input("Please enter a number corresponding to the options above: ")) #get user input
                print("\n")
            except ValueError:
                print("Invalid Input!\n")
            else:
                if menuoption == 1:
                    self.selectAccount()
                elif menuoption == 2:
                    self.createNewAccount()
                elif menuoption == 3:
                    self.logout()                    
                else:
                    print("Invalid Input")
    
    def selectAccount(self):
        """Displays a list of the user's accounts where the user can then select one to enter the account menu of."""
        accounts = self.getAccountDict() #gets a dictionary of all accounts partaining to the current customer

        if len(accounts) != 0: #if the user has at least one account created

            print("Please input the number corresponding to the account you wish to use: ")
        
            menuDict = {} #create empty dictionary for menu

            #create and display a dictionary with numbers counting up from 0 as the keys and names of the accounts as the values
            for number, account in enumerate(accounts.values()):
                menuDict[number+1] = account
                print("{} : {} ({})".format(number+1, account.name, account.type))  #display menu entry
        
            #add a final option to go back to the menu
            exitNumber = len(menuDict) + 1 

            print("{} : Go Back".format(exitNumber)) #print the final menu option
            print("\n")
            
            try:
                userSelection = int(input("Input number: ")) #user menu item selection
                print("\n")
            except ValueError:
                print("Invalid Input!\n")
            else:

                if userSelection == exitNumber:
                    #if the exit number was chosen
                    return #exit

                if userSelection < 0 or userSelection > len(menuDict):
                     #if the user's selection is out of bounds
                    print("Invalid Selection\n")
                    return #exot

                chosenAccount = menuDict[userSelection] 

                chosenAccount.menu() #enter the menu of the chosen account

                return
        
        else: #if the user has no accounts
            print("You have no accounts created!\n")
            return

    def createNewAccount(self):
        """facilitates the creation of a new account"""
        print("Creating new account for", self.name, ":\n")

        #display menu
        print("What type of account would you like to create:\n1. Savings Account\n2. Checking Account\n")

        try:
            typeInput = int(input("Please enter 1 or 2: ")) #user input
            print("\n")
        except ValueError:
            print("Invalid Input!\n")
        else:
            if typeInput == 1:
                account = SavingAccount() #create a savings account
            elif typeInput == 2:
                account = CheckingAccount()  #create a checking account
            
            account.ownerUsername = self.username #stores the users username in account

            #if account creation requirements are not met, it will not be added to the dictionary
            if account.viableCheck() == True:
                
                account.name = uniqueNameEntry(self.getAccountDict(), "name") #user can create unique name for their account

                AccountDict[account.uniqueID] = account #add new account to the Account dictionary
                
                print("Account Created\n")
            else:
                print("Account Requirements Not Met\n")
                
    def logout(self):
        """return user to the login screen"""
        loginMenu()

    def __str__(self):
        return "Username = {}, PIN = {}, Name = {}, Age = {}".format(self.username, self.pin, self.name, self.age)

class Account:
    """A bank account belonging to a customer"""
    #class attributes
    minAge = 18
    minBalance = 0

    def __init__(self):
        #instance attributes
        self.uniqueID = uniqueDictID(AccountDict, "uniqueID")  #create unique id for account and store it in the object and use it as dictionary key
        
        self.ownerUsername = None #stores the customer object that created the account
        self.balance = Decimal(0)  #the money balance stored in the account
        self.name = None  #the name of the account

    #This finds the customer object that created the class using username and stores it as self.owner
    def getOwnerObject(self, customerDict):
        """Uses the ‘ownerUsername’ attribute of the account to return the Customer object that created the account."""
        for customer in customerDict.values():
            if customer.username == self.ownerUsername:
                return customer

    def viableCheck(self):
        """Checks if the age of the owner customer matches the allowed age to create the account"""
        if (self.getOwnerObject(CustomersDict)).age >= self.minAge:
            return True
        else:
            return False

    def delete(self):
        """Will remove the dictionary entry containing this object, essentially deleting the object as it will not be saved when the program closes"""
        del AccountDict[self.uniqueID] #removes account from dictionary

        print(self.name, "deleted!\n")

    def recordTransaction(self, description):
        """Will create a new ‘Transaction’ object with the description that is passed in, and store it in the 'TransactionDict' dictionary"""
        newTransaction = Transaction(description, self.uniqueID)

        TransactionDict[newTransaction.uniqueID] = newTransaction
        
    def checkIfEnoughFunds(self, amount):
        """Checks if amount subtracted from balance will be less than the minimum balance allowed by the account"""
        
        potentialBalance = Decimal(self.balance) - Decimal(amount) #find what remaining balance would be

        if potentialBalance < self.minBalance: #if the potential balance is less than the min balance:
            return False
        else:
            return True

    def menu(self):
        """Display a persistent menu that allows the user to choose which to run from a list of methods:"""
        
        while True:  #keep looping until the menu is exited
            #print menu
            print("In account: {}, ID: {}".format(self.name, self.uniqueID))

            print("1. View Balance")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Transfer Money")
            print("5. Show Transaction History")
            print("6. Delete Account")
            print("7. Exit Account")

            print("\n")

            try:
                menuoption = int(input("Please enter a number corresponding to the options above: ")) #user enters menu option
                print("\n")
            except ValueError:
                print("Invalid Input!\n")
            else:
                if menuoption == 1:
                    self.viewBalance()
                elif menuoption == 2:
                    self.withdraw()
                elif menuoption == 3:
                    self.deposit()
                elif menuoption == 4:
                    self.transfer()
                elif menuoption == 5:
                    self.showTransactions()
                elif menuoption == 6:
                    self.deleteConfirmation()
                elif menuoption == 7:
                    self.goToPreviousMenu()
                else:
                    print("Invalid Input")

    def viewBalance(self):
        """Prints the current balance of the account"""
        print("Your current balance is €{}".format(self.balance))
        print("\n")

    def withdraw(self):
        """If they have sufficient funds, user withdraws a selected amount from account. A transaction log is created."""
        
        try:
            amount = Decimal(input("Please enter an amount to withdraw: "))  #user enters amonunt they wish to withdraw
            print("\n")
        except ValueError:
            print("Invalid Input!\n")
            return

        if self.checkIfEnoughFunds(amount) == False:  #if there are not sufficient funds in the account
            print("Not ennough funds to complete transaction\n")
            return  #exit function

        self.balance -= amount  #remove funds from account

        #create transaction description
        description = "€{} withdrawed from account ID {} by Account Owner {}. New Account Balance: €{}".format(amount, self.uniqueID, self.ownerUsername, self.balance)

        self.recordTransaction(description)  #create log of transaction

        print(description)  #disaply confirmation of transaction to the user

        print("\n")

    def deposit(self):
        """The user enters an amount to be deposited, which is then added to their account. A transaction log is created."""
        try:
            amount = Decimal(input("Please enter an amount to deposit: "))  #user inputs desired amount to be deposited
            print("\n")
        except ValueError:
            print("Invalid Input!\n")
            return
        
        self.balance = Decimal(self.balance) + Decimal(amount)  #amount is added to balance

        #create transaction description
        description = "€{} deposited into account ID {} by Account Owner {}. New Account Balance: €{}".format(amount, self.uniqueID, self.ownerUsername, self.balance)
        
        self.recordTransaction(description)  #create log of transaction

        print(description)  #display confirmation of transaction to the user

        print("\n")

    def transfer(self):
        """Facilitates the transfer of money from one account to another"""
        
        try:
            recipientID = int(input("Please enter the account ID of the account you wish to transfer funds to: ")) #user enters ID of account to transfer money into
            print("\n")
        except ValueError:
            print("Invalid Input!\n")
            return        

        accountFound = False #initiate flag variable
        #find account
        for account in AccountDict.values(): #loop through each account
            if account.uniqueID == recipientID:  #if account is found, return true
                accountFound = True

        if accountFound == True:
            #if the account does exist
            try:
                amount = Decimal(input("Please enter the amount you would like to transfer into the account: "))
                print("\n")
            except ValueError:
                print("Invalid Input!\n")
                return        
            
            if self.checkIfEnoughFunds(amount) == False: #check if the user has enough funds to complete their desired transaction
                print("Not ennough funds to complete transaction\n")
                return
            
            recipientAccount = AccountDict[recipientID]  #recipient account that will be recieving the money

            recipientAccount.balance += amount  #add the funds to recipient account balance
            self.balance -= amount  #remove the funds from giving account

            #create log for author of transaction (this account)
            authorDescription = "€{} transferred into Account ID {}. New Account Balance: €{}".format(amount, recipientID, self.balance)  #create log description

            print(authorDescription+"\n")  #display feedback to the user that the transactoin was succesful

            self.recordTransaction(authorDescription)  #create log of transaction

            #create log for recipient of transaction
            recipeintDescription = "€{} recieved from Account ID {}. New Account Balance: €{}".format(amount,self.uniqueID, recipientAccount.balance)  #create log description

            recipientAccount.recordTransaction(recipeintDescription)  #create log of transaction

        else:
            #display feedback to the user if the account ID they entered is not valid
            print("Account not found!")
        
    def showTransactions(self):
        """Prints each transaction related to to the account object"""
        print("Showing Transaction History for account {}:\n".format(self.name))

        for transaction in TransactionDict.values():  #loop through each transaction in the transaction dictionary
            if transaction.accountID == self.uniqueID: 
                print(transaction)
        
        print("\n")

    def deleteConfirmation(self):
        print("Are you sure you wish to delete the account {}?\n".format(self.uniqueID))

        print("1. Delete")
        print("2. Go back")

        try:
            menuoption = int(input("Please enter a number corresponding to the options above: "))
            print("\n")
        except ValueError:
            print("Invalid Input!\n")
        else:
            if menuoption == 1:
                self.delete() #delete account
                self.goToPreviousMenu() #returnt to the previous accountmanagement menu
            elif menuoption == 2:
                return
            else:
                print("Invalid input, returning...\n")

    def goToPreviousMenu(self):
        (self.getOwnerObject(CustomersDict)).menu()

    def __str__(self):
        return "UniqueId = {}, Account name = {}, owner = {},  type = {}, Balance = {}".format(self.uniqueID,self.name, self.ownerUsername, self.type, self.balance)

class SavingAccount(Account):
    """This is a subclass of Account'.\n
    Unique Traits:\n
    Must be 14 years old or older to create\n
    Can only make one transfer/withdrawal per year
    """
    minAge = 14 #constant age

    def __init__(self):
        super().__init__()
        self.type = "SavingsAccount" #account type
        self.lastWithdrawMonth = None #when account is first made, withdraw month should be none because no withdraws have been made yet

    def menu(self):
        """Displays menu where the user can run various functions for the SavinsAccount\n
        Note that the user can only withdraw or transfer once a month"""
        while True:
            
            currentMonth = datetime.today().month #get the current month
            
            #check if the last month a withdraw was made is not equal to the current month or none
            if self.lastWithdrawMonth != currentMonth or self.lastWithdrawMonth == None: 
                canWithdraw = True #the user can withdraw/transfer
            else:
                canWithdraw = False  #the user cannot withdraw/transfer

            #display menu
            print("In", self.type,"account:", self.name)

            print("1. View Balance")
            print("2. Deposit Money")
            print("3. Show Transaction History")

            if canWithdraw == True:
                print("4. Withdraw or Transfer Money")
            else:
                print("4. Withdraw or Transfer Money (Already had one withdraw/transfer this month, cannot withdraw more)")
            
            print("5. Delete Account")
            print("6. Exit Account")

            print("\n")

            try:
                menuoption = int(input("Please enter a number corresponding to the options above: ")) #user menu selection
                print("\n")
            except ValueError:
                print("Invalid Input!\n")
            else:
                if menuoption == 1:
                    self.viewBalance()
                elif menuoption == 2:
                    self.deposit()
                elif menuoption == 3:
                    self.showTransactions()
                elif menuoption == 4:                
                    self.savingsWithdrawTransfer(canWithdraw)
                elif menuoption == 5:
                    self.deleteConfirmation()
                elif menuoption == 6:
                    self.goToPreviousMenu()
                else:
                    print("Invalid Input")

    def savingsWithdrawTransfer(self, canWithdraw):
        """If the user can withdraw/transfer, a menu is displayed where the user can choose to run either the withdraw() or transfer() methods"""
        if canWithdraw == True:  #if the user can withdraw/make a transaction
            self.lastWithdrawMonth = datetime.today().month  #sets the month last withdrawed attribute to the current month
            
            #display menu
            print("Please select an option (NOTE: You can only perform one of these actions per month):\n")
            
            print("1. Withdraw")
            print("2. Transfer")

            try:
                menuoption = int(input("Please enter a number corresponding to the options above: "))  #user option entry
                print("\n")
            except ValueError:
                print("Invalid Input!\n")
            else:
                if menuoption == 1:
                    self.withdraw()
                elif menuoption == 2:
                    self.transfer()
                else:
                    print("Invalid Option Selected")              

    
class CheckingAccount(Account):
    """This is a subclass of Account'.\n
    Unique Traits:\n
    Must be 18 years old or older to create\n
    Balance can go into the minus up to a specified credit
    """
    minAge = 18 #constant age
    minBalance = -100 #constant credit limit

    def __init__(self):
        super().__init__()
        self.type = "CheckingAccount"
    

class Transaction():
    """This represents a transaction that occured"""
    def __init__(self, description, accountID):
        self.uniqueID = uniqueDictID(TransactionDict, "uniqueID") #will create a unique id within the dictionary
        self.description = description  #description of the transaction
        self.accountID = accountID  #the ID of the account the made the transaction
        
        #set current Date and Time
        now = datetime.now()
        self.date = now.strftime("%d/%m/%Y %H:%M") #create date and time

    def __str__(self):
        return "[Transaction ID: {}] [Account ID: {}] {} : {}".format(self.uniqueID, self.accountID, self.date, self.description)


#globals
CustomersDict = {}
AccountDict = {}
TransactionDict = {}

#UTILITY FUNCTIONS
def uniqueNameEntry(dictionary, attribute):
    """function will continuously prompty user to enter a string until it is not equal to any 'attribute parameter' of a class from 'dictionary parameter'
    and wil return the unique name"""
    
    while True:  #continuous loop
        
        userEnteredName = str(input("Please enter a unique name: "))

        nameFound = False #initilaise name found flag
        for item in dictionary.values():  #loop through each item in the dictionary
            if getattr(item, attribute) == userEnteredName:  #if the attribute of the current item matches the name the user entered
                    nameFound = True  #the name is found

        if nameFound != True:  #if the name is not found in the dictionary
            return userEnteredName  #return the unique name
        else:
            print("Name not unique!\n")  #else tell the user that the name is not unique and loop again

def uniqueDictID(dictionary, attribute):
    """This function will loop through the specified dictionary and find a unique numerical id that does not match the specified attribute"""

    if not dictionary:
        #if dictionary is empty, return 0
        return 0

    id = 0  #initialse id at 0
    while True:  #continuous loop
        
        idFound = False  #initialise id found flag
        for item in dictionary.values():  #loop through each item in the dictionary
            if getattr(item, attribute) == id:  #if the specified attribute of that item matches the id
                idFound = True  #change id found to True
                pass
        
        if idFound != True:  #if the id not found in the dictionary
            return id  #return the unique id
        else:
            id += 1  #else, increment the id value by 1 and loop again

def saveDictToFile(dictionary, filename):
    """will open the specified text file and write the contents of a dictionary full of objects into it, with each item being turned into json format and saved on one line each"""
    f = open(filename, "w")  #open file
    
    for id in dictionary:
        jsonString = json.dumps(dictionary[id].__dict__) #will create a json string containing all items from the object that the user can input as parameters
        f.write(jsonString + "\n")  #write line to file and then go to next line

    f.close()  #close file

def pinEntry():
    """Will prompt the user to enter a 4 digit pin"""
    pin = ""  #initialise empty pin string
    print("Please enter a 4 digit PIN: ")
    for i in range(4):  #loop 4 times
        print("Enter digit", i+1)
        try:
            newDigit = int(input())  #user enters new digit
        except ValueError:
            print("Invalid Input!\n")
            return False
        else:
            pin += str(newDigit)  #if there are no errors, that new digit is added to the pin string
    
    return pin  #return completed pin string
        

#LOADING FROM FILE FUNCTIONS
def createCustomerDictFromFile():
        """This loads the data from the customer file, and turns each json string line into an object which then gets stored in the customer dictionary"""
        
        f = open("customers.txt", "r")
        fileLines = f.readlines() #puts every line from file in array
        f.close()

        #return if file is empty
        if not fileLines:
            return

        #for each line
        for line in fileLines:

            attributeDict = json.loads(line) #stores the data from the json string into a dictionary

            id = attributeDict["username"] #retrieve ID value

            CustomersDict[id] = Customer() #create new object and add it to dictionary

            #add each attribute that must be added to the object from the attribute array
            for attribute,value in attributeDict.items(): 
                setattr(CustomersDict[id], attribute, value)

def createTransactionDictFromFIle():
    """This loads the data from the transaction file, and turns each json string line into an object which then gets stored in the transaction dictionary"""
    f = open("accountTransactions.txt", "r")
    fileLines = f.readlines() #puts every line from file in array
    f.close()

    #return if file is empty
    if not fileLines:
        return

    #for each line
    for line in fileLines:

        attributeDict = json.loads(line) #stores the data from the json string into a dictionary

        id = attributeDict["uniqueID"]
        
        TransactionDict[id] = Transaction(None, None)

        #add each attribute that must be added to the object from the attribute array
        for attribute,value in attributeDict.items(): 
            setattr(TransactionDict[id], attribute, value)


def createAccountsDictFromFile():
    """This loads the data from the accounts file, and turns each json string line into an object which then gets stored in the accounts dictionary"""
    f = open("accounts.txt", "r")
    fileLines = f.readlines() #puts every line from file in array
    f.close()
    
    #return if file is empty
    if not fileLines:
        return
    
    #for each line
    for line in fileLines:       

        attributeDict = json.loads(line) #stores the data from the json string into a dictionary
        
        id = attributeDict["uniqueID"] #retrieve the id from the object, which will be used as the key for the objects place in the dictionary

        #check what type account is 
        if attributeDict["type"] == "SavingsAccount":
            AccountDict[id] = SavingAccount()  #create savings account
        if attributeDict["type"] == "CheckingAccount":
            AccountDict[id] = CheckingAccount()  #create checking account

        #add each attribute that must be added to the object from the attribute array
        for attribute,value in attributeDict.items(): 
            setattr(AccountDict[id], attribute, value)


#LOGIN MENU
def loginMenu():
    """The first thing that the user sees, gives the user options to run a function related to logging in"""
    while(True):
        #Dispaly menu
        print("Welcome to Rob's Bank!")

        print("1. Login")
        print("2. Register as a New User")
        print("3. Exit")
        print("\n")

        try:
            menuoption = int(input("Please enter a number corresponding to the options above: ")) #user inputs menu option
        except ValueError:
            print("Invalid Input!\n")
        else:
            if menuoption == 1:
                customerLogin()
            elif menuoption == 2:
                customerCreate()
            elif menuoption == 3:
                saveExit()
            else:
                print("Invalid Selection!\n")

def customerLogin():
    """Login in function for customer"""
    username = str(input("Please enter your Username: ")) #user inputs username

    #check if username exists
    for customerID in CustomersDict: #loop through each customer in the customer dictionary
        customer = CustomersDict[customerID]

        if username == customer.username:
            #username is found, check if pin matches
            pin = str(input("Please enter your pin: ")) #prompt user to enter their pin
            print("\n")

            if pin == customer.pin:  #if pin matches
                print("Successful Login")
                successfulLogin(customer)
            else:
                print("Pin incorrect")

    print("Username not found\n") #display feedback if the user is not found

def successfulLogin(customer):
    """Run after a successful login attempt"""
    customer.menu() #redirects user to the customer menu

def customerCreate():
        print("Please enter a unique username") 

        username = uniqueNameEntry(CustomersDict, "username")  #prompt user to enter a unique username

        pin = pinEntry()  #prompt user to enter a 4 digit pin

        if pin == False:  #if pin entry fails, exit
            return

        #user enters their first name and last name, which get combined into one field
        firstname = str(input("Please enter your first name: "))
        lastname = str(input("Please enter your last name: "))
        name = firstname + " " + lastname
        
        try:
            age = int(input("Please enter your age: ")) #prompt user to enter their age
        except ValueError:
            print("Invalid Input!\n")
            return

        customer = Customer() #create customer object

        #populate user object with the entered data
        customer.username = username
        customer.pin = pin
        customer.name = name
        customer.age = age

        #add newly created customer to the customer dictionary
        customerId = len(CustomersDict)

        CustomersDict[customerId] = customer

        print("Account Created Successfully!\n")

def saveExit():
        """Run when function is being exited, saves all data and then exits"""

        saveDictToFile(AccountDict, "accounts.txt")
        
        saveDictToFile(TransactionDict, "accountTransactions.txt")

        saveDictToFile(CustomersDict, "customers.txt")
       
        sys.exit()



#INIT FUNCTION
def init():
    """Function that is ran to initialise the program"""
    createAccountsDictFromFile()
    createCustomerDictFromFile()
    createTransactionDictFromFIle()

    loginMenu()


#MAIN
init() #start program
