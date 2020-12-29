'''

    This script watches newegg until restock and then
    purchases selected card. Make sure to remove nordvpn
    code if you do not use nordvpn.

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

import random, time, os, hashlib, base64, six, datetime
from nordvpn_connect import initialize_vpn, get_current_ip, connect_to_server, close_vpn_connection, rotate_VPN
from nerodia.browser import Browser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

#globals
options = Options()
driver = ""
browserNewEgg = ""
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
settings = ""
#rtxCardLink = "https://www.newegg.com/asus-geforce-rtx-3060-ti-dual-rtx3060ti-o8g/p/N82E16814126468?Description=3060%20ti&cm_re=3060_ti-_-14-126-468-_-Product"
rtxCardLink = "https://www.newegg.com/asus-radeon-rx-570-rog-strix-rx570-o8g-gaming/p/N82E16814126427?Item=N82E16814126427"

def main():

    #globals
    global browserTwitter, browserNewEgg, username, password, driver, options, rtxCardLink

    options.add_argument("--log-level=3")

    time.sleep(2)

    print("...")

    time.sleep(3)

    #start up text
    clear_console(5)
    print("Welcome to the RTX Bot Script!")
    clear_console(1)
    print("To begin, enter your username and password")
    print("to access your personal information")
    clear_console(5)

    #logs user in to retrieve personal information
    login()

    time.sleep(2)

    print("...")

    time.sleep(3)

    print("User successfully logged in!")

    #loads personal infrormation using password as key for decryption
    loadPersonalInformation()

    time.sleep(2)
    print("...")
    time.sleep(1)
    print("Personal Information Loaded!")

    time.sleep(2)

    print("...")

    time.sleep(3)

    print("Loading vpn...")
    vpnStart()

    time.sleep(12)

    print("Connected to VPN!")

    print("...")

    time.sleep(3)

    print("Loading browser to newegg...")

    time.sleep(2)

    driver = webdriver.Chrome(options=options)
    browserNewEgg = Browser(browser=driver)
    browserNewEgg.goto(rtxCardLink)

    wait(9)

    #closes pop up
    if (browserNewEgg.link(id = 'popup-close').exists):
        browserNewEgg.link(id = 'popup-close').click()

    print("All set! Refreshing newegg until they restock")

    x = datetime.datetime.now()
    y = x + datetime.timedelta(seconds=120)

    #checks new egg until restock
    restocked = False
    count = 0
    while restocked == False:

        if (count > 40):
            count = 0

            time.sleep(1)

            print("Restarting browser with new IP...")

            #clears browser cache
            browserNewEgg.cookies.clear()

            time.sleep(1)

            #closes browser
            browserNewEgg.close()

            time.sleep(1)

            #disconnect from vpn
            vpnEnd()

            time.sleep(10)

            #reconnects to vpn
            vpnStart()

            time.sleep(12)

            driver = webdriver.Chrome(options=options)
            browserNewEgg = Browser(browser=driver)
            time.sleep(1)
            browserNewEgg.goto(rtxCardLink)

            time.sleep(12)

            #closes pop up
            if (browserNewEgg.link(id = 'popup-close').exists):
                browserNewEgg.link(id = 'popup-close').click()

            wait(2)

        else:
            pass

        browserNewEgg.refresh()
        wait(3)

        locator = {"class": "nav-col", "index": 1}
        condition = (browserNewEgg.div(class_name = "product-buy").div().div(**locator).button()).exists

        '''
        x = datetime.datetime.now()
        condition = x > y
        '''

        if (condition):
            restocked = True
        else:
            pass

        count += 1

    clear_console(100)

    print("Cards restocked!")

    time.sleep(1)

    #clicks add to cart
    browserNewEgg.div(class_name = "product-buy").div().div(**locator).button().click()

    time.sleep(2)

    #declines warrenty if it is presented
    if (not (browserNewEgg.div(class_name = "item-summary").exists)):
        locator = {"index": 0}
        browserNewEgg.div(class_name = "modal-footer").button(**locator).click()

    time.sleep(2)

    #clicks view cart and checkout
    browserNewEgg.button(title = "View Cart & Checkout").click()

    wait(5)

    #says no to masks if asked
    if (browserNewEgg.button(id = "Masks_addtocart").exists):
        locator = {"index": 0}
        locator2 = {"index": 1}
        browserNewEgg.div(class_name = "modal-footer").div(**locator2).button(**locator).click()

    time.sleep(2)

    #goes to secure checkout
    browserNewEgg.div(class_name = "summary-actions").button().click()


#-----------------------------------------------------------------------

def login():

    global username, password

    #logs user in to retrieve information
    goodLogin = False
    while (goodLogin == False):

        #asks user for username until a good one is entered
        goodUsername = False
        while (goodUsername == False):

            username = input("Username: ")

            #if username's file does not exist, user will be prompted again
            if (not os.path.exists("credentials/" + username + ".txt")):
                print("ERROR: Username does not exist.")
            else:
                goodUsername = True

        #once good username is found, associated encryted password is retrieved
        file = open("credentials/" + username + ".txt", "r")
        encryptedPassword = (file.readline()).rstrip()
        file.close()

        #asks user for password until a good one is entered
        goodPassword = False
        while (goodPassword == False):

            password = input("Password: ")

            #if password does not match, user will be prompted to enter another one
            if not (sha256(password) == encryptedPassword):
                print("ERROR: Password does not match username.")
            else:
                goodPassword = True

        #if a good username and password have been found, then the login is complete
        if (goodUsername == True and goodPassword == True):
            goodLogin = True
        else:
            goodLogin = False

#-----------------------------------------------------------------------

def loadPersonalInformation():

    global username, password, firstName, lastName, address, city, state, zip, phone, email, cardHolderName, cardNumber, expMonth, expYear, vpnEmail, vpnPass

    #opens credential file
    file = open("credentials/" + username + ".txt", "r")

    throwoutline = file.readline()

    #reads each line and saves the decrypted version to each variable
    encryptedFirstName = (file.readline().rstrip())
    firstName = (decode(password, encryptedFirstName.encode("utf-8")))

    encryptedLastName = (file.readline().rstrip())
    lastName = (decode(password, encryptedLastName.encode("utf-8")))

    encryptedAddress = (file.readline().rstrip())
    address = (decode(password, encryptedAddress.encode("utf-8")))

    encryptedCity = (file.readline().rstrip())
    city = (decode(password, encryptedCity.encode("utf-8")))

    encryptedState = (file.readline().rstrip())
    state = (decode(password, encryptedState.encode("utf-8")))

    encryptedZip = (file.readline().rstrip())
    zip = (decode(password, encryptedZip.encode("utf-8")))

    encryptedPhone = (file.readline().rstrip())
    phone = (decode(password, encryptedPhone.encode("utf-8")))

    encryptedEmail = (file.readline().rstrip())
    email = (decode(password, encryptedEmail.encode("utf-8")))

    encryptedCardHolderName = (file.readline().rstrip())
    cardHolderName = (decode(password, encryptedCardHolderName.encode("utf-8")))

    encryptedCardNumber = (file.readline().rstrip())
    cardNumber = (decode(password, encryptedCardNumber.encode("utf-8")))

    encryptedExpMonth = (file.readline().rstrip())
    expMonth = (decode(password, encryptedExpMonth.encode("utf-8")))

    encryptedExpYear = (file.readline().rstrip())
    expYear = (decode(password, encryptedExpYear.encode("utf-8")))

    encryptedVpnEmail = (file.readline().rstrip())
    vpnEmail = (decode(password, encryptedVpnEmail.encode("utf-8")))

    encryptedVpnPass = (file.readline().rstrip())
    vpnPass = (decode(password, encryptedVpnPass.encode("utf-8")))

    file.close()

#-----------------------------------------------------------------------

def sha256(var):

	#Return the SHA-256 hash of the string var

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

def printPersonalInfo():

    global firstName, lastName, address, city, state, zip, phone, email, cardHolderName, cardNumber, expMonth, expYear

    print("First Name: " + firstName)
    print("Last Name: " + lastName)
    print("Address: " + address)
    print("City: " + city)
    print("State: " + state)
    print("Zip: " + zip)
    print("Phone: " + phone)
    print("Email: " + email)
    print("Card Holder Name: " + cardHolderName)
    print("Card Number: " + cardNumber)
    print("Experation Month: " + expMonth)
    print("Experation Year: " + expYear)

#-----------------------------------------------------------------------

def wait(seconds):
    if seconds < 2:
        time.sleep(1)
    else:
        time.sleep(random.randint(seconds-1, seconds+1))

#-----------------------------------------------------------------------

def vpnStart():

    #globals
    global vpnEmail, vpnPass

    #initializes vpn
    settings = initialize_vpn("United States", vpnEmail, vpnPass)

    #connects to vpn
    rotate_VPN(settings)

#-----------------------------------------------------------------------

def vpnEnd():

    #globals
    global vpnEmail, vpnPass

    #initializes vpn
    settings = initialize_vpn("United States", vpnEmail, vpnPass)

    #disconnects from vpn
    close_vpn_connection(settings)

#-----------------------------------------------------------------------

main()
