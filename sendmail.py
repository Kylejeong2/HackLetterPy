from mailjet_rest import Client
from app import main
import os
from dotenv import load_dotenv
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = os.getenv("MONGODB_CONNECTION")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

load_dotenv()

secret = os.getenv("MAILJET_SECRET_KEY")
api = os.getenv('MAILJET_API_KEY')

mailjet = Client(auth=(api, secret), version='v3.1')

#only query this once per day 
info = main()
summaries, titles = info[0], info[1]

current_date = datetime.now().strftime("%B %d, %Y")

data = {
  'Messages': [
    {
      "From": {
        "Email": "Kyle@hackletter.co",
        "Name": "Kyle"
      },
      "To": [
        {
          "Email": "kylejeong21@gmail.com",
          # "Name": "Kyle"
        }
      ],
      "Subject": "Hack Letter {}".format(current_date),
      # "TextPart": "HackLetter v1",
      "HTMLPart": '<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Newsletter</title><link rel="icon" type="image/x-icon" href="https://upload.wikimedia.org/wikipedia/commons/b/b2/Y_Combinator_logo.svg"><style>body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; } .container { width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); } .header { text-align: center; padding: 20px 0; } .header img { max-width: 150px; } .headline { font-size: 24px; font-weight: bold; margin: 20px 0; } .article { margin-bottom: 20px; } .article img { max-width: 100%; height: auto; } .article h2 { font-size: 20px; margin: 10px 0; } .article p { font-size: 16px; line-height: 1.5; } .footer { text-align: center; padding: 20px 0; font-size: 14px; color: #888888; } .footer a { color: #888888; text-decoration: none; }<style><script src="index.js"></script></head><body><div class="container"><div class="header"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b2/Y_Combinator_logo.svg" alt="Newsletter Logo"></div><div class="headline">Your Daily HackerNews Brief</div><div class="article"><h2>{}</h2><p id="article1">{}</p> </div><div class="article"><h2>{}</h2><p id="article2">{}</p></div><div class="article"><h2>{}</h2><p id="article3">{}</p></div><div class="article"><h2>{}</h2><p id="article4">{}</p></div><div class="article"><h2>{}</h2><p id="article5">{}</p></div><div class="footer"><p>&copy; 2024 Hack Letter. All rights reserved.</p><p><a href="">Unsubscribe</a> | <a href="">Privacy Policy</a> | <a href="">Report Bugs to @Kylejeong21 on X</a></p></div></div></body></html>'.format(titles[0], summaries[0], titles[1], summaries[1], titles[2], summaries[2], titles[3], summaries[3], titles[4], summaries[4]),
      "CustomID": "Hackletter V1",
    }
  ]
}

result = mailjet.send.create(data=data)

# testing
print (result.status_code)
print (result.json())