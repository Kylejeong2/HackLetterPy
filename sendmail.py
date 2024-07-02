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

#only query this once per day 
info = main()
summaries, titles, urls = info[0], info[1], info[2]

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
                    "Name": "Your Daily Hackletter"
                },
                "To": [
                    {
                        "Email": "{}".format(email),
                        "Name": ""
                    }
                ],
                "Subject": "Hack Letter {}".format(current_date),
                "TextPart": "HackLetter v1",
                "HTMLPart": '<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Newsletter</title><style>body {font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;}.container {width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);}.header {text-align: center; padding: 20px 0;}.header img {max-width: 150px;}.headline {font-size: 24px; font-weight: bold; margin: 20px 0;}.article {margin-bottom: 20px;}.article img {max-width: 100%; height: auto;}.article h2 {font-size: 20px; margin: 10px 0;}.article p {font-size: 16px; line-height: 1.5;}.footer {text-align: center; padding: 20px 0; font-size: 14px; color: #888888;}.footer a {color: #888888; text-decoration: none;}</style><script src="index.js"></script></head><body><div class="container"><div class="header"></div><div class="headline">Your Daily HackerNews Brief</div><div class="article"><h2><a href="' + urls[0] + '">'+ titles[0] +'</a></h2><p id="article1">' + summaries[0] + '</p></div><div class="article"><h2><a href="' + urls[1] + '">' + titles[1]+ '</a></h2><p id="article2">' + summaries[1] + '</p></div><div class="article"><h2><a href="' + urls[2] + '">' + titles[2] + '</a></h2><p id="article3">' + summaries[2] + '</p></div><div class="article"><h2><a href="' + urls[3] + '">' + titles[3] + '</a></h2><p id="article4">' + summaries[3] + '</p></div><div class="article"><h2><a href="' + urls[4] + '">' + titles[4] + '</h2><p id="article5">' + summaries[4] + '</p></div><div class="footer"><p>&copy; 2024 Hack Letter. All rights reserved.</p><p><a href="www.hackletter.co/unsubscribe.html">Unsubscribe</a> | <a href="">Privacy Policy</a> | <a href="">Report Bugs to @Kylejeong21 on X</a></p></div></div></body></html>',
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