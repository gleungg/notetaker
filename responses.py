"""Handle all messages sent to the Discord to perform an action and respond"""
from datetime import date
from db import Database


def handleResponses(message, text):
    """Handle responses to messages sent to the Discord channel"""
    if text.startswith('!noted'):
        return handleNoted(message, text)
    if text.startswith('!register'):
        return handleRegister(text)
    if text.startswith('!help'):
        return "JUST !NOTE SOMETHING MAN"
    if text.startswith('!review'):
        return handlePlayerReview(text)


def handleNoted(message, text):
    """
    Noted takes the form of !noted <user> <event>. Tokenize string and build a record to be inserted into the database.
    """
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
        response = db.addNote(record)
        db.shutdownDb()
        return response
    except Exception as e:
        print("Malformed use of !noted probably does not contain a note.")
        print(e)


def handleRegister(message):
    """Register one user with !register <user>"""
    tokens = message.split(" ")
    try:
        db = Database()
        record = {"name": tokens[1]}
        response = db.registerUser(record)
        db.shutdownDb()
        return response
    except Exception:
        return str(f"{record['luckerdog']} is already registered or otherwise ineligible.")


def handlePlayerReview(message):
    """
    Review a player's notes with !review <user>. Returns a list of notes in the form of:
    <index>. <event> - <ref url>
    """
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
