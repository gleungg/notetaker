from db import Database
from datetime import date
def handle_responses(message, text):
    if text.startswith('!noted'):
        return handleNoted(message, text)
    if text.startswith('!register'):
        return handleRegister(text)
    if text.startswith('!help'):
        return "JUST !NOTE SOMETHING MAN"
    if text.startswith('!review'):
        return handlePlayerReview(text)
    
'''
Noted takes the form of !noted <user> <event>. Tokenize the string and build a record to be inserted into the database.
'''
def handleNoted(message, text):
    tokens = text.split(" ")
    try:
        db = Database()
        user = tokens[1]
        note = tokens[2:]
        record = {
            "name": user,
            "event": " ".join(note),
            "inputDate": str(date.today()),
            "author": message.author.name,
            "link": message.jump_url
        }
        db.addNote(record)
        db.shutdownDb()
        return str(f"Noted. {user} is clearly a luckerdog. \"{' '.join(note)}\"")
    except Exception as e:
        print("Unhandled: malformed use of !noted probably does not contain a note. " )
        print(e)

'''
Register one user with !register <user>
'''
def handleRegister(message):
    tokens = message.split(" ")
    try:
        db = Database()
        record = {"luckerdog": tokens[1]}
        db.registerUser(record)
        db.shutdownDb()
        return str(f"Luckerdog has been registered.")
    except Exception as e: 
        return str(f"{record['luckerdog']} is already registered or otherwise ineligible.")
    
'''
Review a player's notes with !review <user>. Returns a list of notes in the form of:
<index>. <event> - <ref url>
'''
def handlePlayerReview(message):
    tokens = message.split(" ")
    try:
        player = tokens[1]
        db = Database()
        collection = db.getNotes(player)
        strBuilder = ""
        for idx, record in enumerate(collection): 
            strBuilder += str(idx+1) + ". "
            strBuilder += record["event"] + " - " + record["link"]
            strBuilder += "\n"
        db.shutdownDb()

        return strBuilder
    except Exception as e: 
        print("Unhandled: malformed use of !review. Probably does not contain a player")
        print(e)