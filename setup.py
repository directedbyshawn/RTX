'''

    This script creates an account to purchase
    your RTX card with. All of your personal
    and billing information will be encrypted and
    saved to later be accessed with a username
    and password you will create with this script.

    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------

                           v1.0
                     @dirctedbyshawn

    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------

'''

import time, random, os, hashlib, base64, six

#globals
username = ""
password = ""
firstName = ""
lastName = ""
address = ""
city = ""
state = ""
zip = ""
phone = ""
email = ""
cardHolderName = ""
cardNumber = ""
expMonth = ""
expYear = ""
vpnEmail = ""
vpnPass = ""

def main():

    #globals
    global username, password, firstName, lastName, address, city, state, zip, phone, email, cardHolderName, cardNumber, expMonth, expYear, vpnEmail, vpnPass

    time.sleep(2)

    print("...")

    time.sleep(3)

    #start up text
    clear_console(5)
    print("Welcome to the RTX Bot Setup!")
    clear_console(1)
    print("To begin, create a username and")
    print("password to keep your info safe")
    clear_console(5)

    #creates credentials directory as long as it doesnt already exist
    if not os.path.exists("credentials"):
        os.mkdir("credentials")

    #create new username that has not yet been taken
    goodUsername = False
    while (goodUsername == False):

        #gets new username
        username = input("New Username: ")

        #determines if it has been taken
        if (os.path.exists("credentials/" + username + ".txt")):
            print("ERROR: Username taken.")
        else:
            file = open("credentials/" + username + ".txt", "w")
            file.close()
            goodUsername = True

    #password creation with input validation
    goodPassword = False
    while (goodPassword == False):

        #gets username
        password = str(input("Password: "))

        #makes sure password isnt blank
        if (password == "" or password == " "):
            print("ERROR: Please enter a valid password")
        else:
            goodPassword = True

    print("...")

    time.sleep(2)

    #hashs password and writes it to credentials file
    passwordWrite = sha256(password)
    file = open("credentials/" + username + ".txt", "w")
    file.write(passwordWrite + "\n")
    file.close()

    print("Account successfully created!")

    time.sleep(2)

    print("...")

    time.sleep(1)

    print("Enter your personal information below")

    #collects personal & payment info
    firstName = str(input("First Name: "))
    lastName = str(input("Last Name: "))
    address = input("Address: ")
    city = str(input("City: "))
    state = str(input("State: "))
    zip = input("Zip Code: ")
    phone = input("Phone Number (no -'s): ")
    email = input("Email: ")
    cardHolderName = input("Card Holder Full Name: ")
    cardNumber = input("Card Number: ")
    expMonth = input("Expiration Month (number): ")
    expYear = input("Expiration Year (number): ")
    vpnEmail = input("NORDVPN Email: ")
    vpnPass = input("NORDVPN Password: ")


    time.sleep(2)

    print("...")

    #reopens credentials file and writes encrypted data to the file
    file = open("credentials/" + username + ".txt", "a")
    file.write((encode(password, firstName)).decode("utf-8") + "\n")
    file.write((encode(password, lastName)).decode("utf-8") + "\n")
    file.write((encode(password, address)).decode("utf-8") + "\n")
    file.write((encode(password, city)).decode("utf-8") + "\n")
    file.write((encode(password, state)).decode("utf-8") + "\n")
    file.write((encode(password, zip)).decode("utf-8") + "\n")
    file.write((encode(password, phone)).decode("utf-8") + "\n")
    file.write((encode(password, email)).decode("utf-8") + "\n")
    file.write((encode(password, cardHolderName)).decode("utf-8") + "\n")
    file.write((encode(password, cardNumber)).decode("utf-8") + "\n")
    file.write((encode(password, expMonth)).decode("utf-8") + "\n")
    file.write((encode(password, expYear)).decode("utf-8") + "\n")
    file.write((encode(password, vpnEmail)).decode("utf-8") + "\n")
    file.write((encode(password, vpnPass)).decode("utf-8") + "\n")

    file.close()

    time.sleep(2)

    print("Done! Your information is ready to be used. ")

    time.sleep(2)

    print("Come again!")

#-----------------------------------------------------------------------

def sha256(var):
	"""Return the SHA-256 hash of the string var."""

	if type(var) != str:
		raise TypeError('sha256() only accepts strings as input!')

	hash_obj = hashlib.sha256()
	hash_obj.update(var.encode('utf-8'))

	return hash_obj.hexdigest()

#-----------------------------------------------------------------------

def clear_console(n):
    print("")
    for i in range(n):
        print("-----------------------------------------------")
    print("")

#-----------------------------------------------------------------------

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin') if six.PY3 else encoded_string
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=')

#-----------------------------------------------------------------------

def decode(key, string):
    string = base64.urlsafe_b64decode(string + b'===')
    string = string.decode('latin') if six.PY3 else string
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

#-----------------------------------------------------------------------

def decryption_test():

    file = open("credentials/shawn.txt", "r")
    hashed_pass = (file.readline()).rstrip()

    password = input("Password: ")

    '''
    goodPass = False
    while (goodPass == False):
        password = input("Enter the password: ")
        if (sha256(password) != hashed_pass):
            print("ERROR: Wrong password entered")
        else:
            goodPass = True
    '''

    encryptedFirstName = (file.readline().rstrip())
    decryptedFirstName = (decode(password, encryptedFirstName.encode("utf-8")))

    print("First Name: " + decryptedFirstName)

    encryptedLastName = (file.readline().rstrip())
    decryptedLastName = (decode(password, encryptedLastName.encode("utf-8")))

    print("Last Name: " + decryptedLastName)

    encryptedAddress = (file.readline().rstrip())
    decryptedAddress = (decode(password, encryptedAddress.encode("utf-8")))

    print("Address: " + decryptedAddress)

    encryptedCity = (file.readline().rstrip())
    decryptedCity = (decode(password, encryptedCity.encode("utf-8")))

    print("City: " + decryptedCity)

#-----------------------------------------------------------------------

main()
