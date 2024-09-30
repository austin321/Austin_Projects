#send an email with content from an API

#implement some form of logging

#make sure that the email credentials are not in the script hehe

#properly handle all exceptions!


import requests
import json
import smtplib
import logging

URL = 'https://v2.jokeapi.dev/joke/Any'

#reference our credentials file with our creds in json
with open('creds.json', "r") as f:
    #save to variable "creds"
    creds = json.load(f)
    f.close()

#establish our creds from our JSON file
EMAIL = creds['email']
PASSWORD = creds['password']
RECIPIENT = EMAIL

LOGFILE = 'email_send.log'

logging.basicConfig(filemode='a', filename=LOGFILE, level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

def send_email(joke):
    #we define a function "send_email"
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587) #specific to gmail
        s.starttls()
    except smtplib.SMTPConnectError:
        logging.error("Couldn't connect to mail server")
        exit()

    try:
        s.login(EMAIL, PASSWORD)
    except smtplib.SMTPAuthenticationError:
        logging.error("Auth failure, error occurred during establishment of a connection with the server ")
        exit()

    try:
        s.sendmail(EMAIL, RECIPIENT, f'\n{joke}')
    except smtplib.SMTPException:
        logging.error('Unable to send email due to error')
        exit()
    s.quit()

def get_the_joke_content():
    response = requests.get(URL)
    result = response.json()

    #error handling
    if result['error']:
        logging.error('something went wrong with the request to the API')
        return None
    
    #twopart
    if result['type'] == 'twopart':
        #extract a setup and delivery
        setup = result['setup']
        delivery = result['delivery']
        return f'Setup: \n\n{setup}\n\nDelivery: {delivery}\n\n'

    #one-liners
    else:
        #extract a normal one line joke
        one_liner = result['joke']
        return f'\n\n{one_liner}\n\n'
    
joke = get_the_joke_content()
logging.info('Joke retrieved successfully!')
send_email(joke)
logging.info('Email successfully sent!')
