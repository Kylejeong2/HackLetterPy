from mailjet_rest import Client
from app import main
import os
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv("MAILJET_SECRET_KEY")
api = os.getenv('MAILJET_API_KEY')

mailjet = Client(auth=(api, secret), version='v3.1')

# info = main()
# summaries, titles = info[0], info[1]

data = {
  'Messages': [
    {
      "From": {
        "Email": "kylejeong21@gmail.com",
        "Name": "Kyle"
      },
      "To": [
        {
          "Email": "kylejeong21@gmail.com",
          "Name": "Kyle"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      #"HTMLPart": '<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Newsletter</title><link rel="icon" type="image/x-icon" href="logo.png"><link rel="stylesheet" href="styles.css"><script src="index.js"></script></head><body><div class="container"><div class="header"><img src="logo.png" alt="Newsletter Logo"></div><div class="headline">Your Daily HackerNews Brief</div><div class="article"><h2>{}</h2><p id="article1">{}</p> </div><div class="article"><h2>{}</h2><p id="article2">{}</p></div><div class="article"><h2>{}</h2><p id="article3">{}</p></div><div class="article"><h2>{}</h2><p id="article4">{}</p></div><div class="article"><h2>{}</h2><p id="article5">{}</p></div><div class="footer"><p>&copy; 2024 Your Company. All rights reserved.</p><p><a href="">Unsubscribe</a> | <a href="">Privacy Policy</a></p></div></div></body></html>'.format(titles[0], summaries[0], titles[1], summaries[1], titles[2], summaries[2], titles[3], summaries[3], titles[4], summaries[4]),
      "CustomID": "AppGettingStartedTest",
    }
  ]
}

result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())