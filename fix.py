from mailjet_rest import Client
from app import main
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

secret = os.getenv("MAILJET_SECRET_KEY")
api = os.getenv('MAILJET_API_KEY')

mailjet = Client(auth=(api, secret), version='v3.1')

current_date = datetime.now().strftime("%B %d, %Y")

#pull list of emails from mongodb 
client = MongoClient(os.getenv("MONGODB_CONNECTION"))
db = client['Hackletter']
collection = db['emails']

emails = [doc['email'] for doc in collection.find({}, {'email': 1})] #list of all emails in the database
#print(emails)

#for loop send emails to all of the emails in the list 
for email in emails:
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "Kyle@hackletter.co",
                    "Name": "Hackletter Support"
                },
                "To": [
                    {
                        "Email": "{}".format(email),
                        "Name": ""
                    }
                ],
                "Subject": "Support {}".format(current_date),
                "TextPart": "HackLetter v1",
                "HTMLPart": '<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Newsletter</title><link rel="icon" type="image/x-icon" href="https://upload.wikimedia.org/wikipedia/commons/b/b2/Y_Combinator_logo.svg"><style>body {font-family: Arial, sans-serif;background-color: #f4f4f4;margin: 0;padding: 0;}.container {width: 100%;max-width: 600px;margin: 0 auto;background-color: #ffffff;padding: 20px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);}.header {text-align: center;padding: 20px 0;}.header img {max-width: 150px;}.headline {font-size: 24px;font-weight: bold;margin: 20px 0;}.article {margin-bottom: 20px;}.article img {max-width: 100%;height: auto;}.article h2 {font-size: 20px;margin: 10px 0;}.article p {font-size: 16px;line-height: 1.5;}.footer {text-align: center;padding: 20px 0;font-size: 14px;color: #888888;}.footer a {color: #888888;text-decoration: none;}</style><script src="index.js"></script></head><body><div class="container"><div class="headline">Hackletter Update</div><div class="article"><h2>Issue with scraping</h2><p id="article1">Hey everyone, Kyle here. </p><p id="article1">Running into some bugs while scraping certain websites that I am currently working on now. </p><p id="article1">Please be patient as this is a super early version of the product, and I am making it better everyday. </p><p id="article1">If you are reading this, thanks for your support! I appreciate all of you!</p><div class="footer"><p>&copy; 2024 Hack Letter. All rights reserved.</p><p><a href="">Unsubscribe</a> | <a href="">Privacy Policy</a> | <a href="">Report Bugs to @Kylejeong21 on X</a></p></div></div></body>',
                "CustomID": "Hackletter V1",
            }
        ]
    }

    result = mailjet.send.create(data=data)

# testing
# print (result.status_code)
# print (result.json())

print("Sent emails to: ")
print(emails)