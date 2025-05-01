import debateGenerator
import subprocess
import random
import json
import time

from responseGenerator import generateInitial
from responseGenerator import generateResponse
from responseGenerator import generateFinal



def updateCounter(count):
    with open("messagesSent.json", "r") as file:
        data = json.load(file)
    data["messagesSent"] = count
    with open("messagesSent.json", "w") as file:
        json.dump(data, file, indent=2)

def formatContext(context):
    formattedContext = ""
    for i in range(len(context)):
        formattedContext += f"{context[i]['author']}: {context[i]['content']}\n"
    return formattedContext

def writeMessage(message,bot):
    with open("arguements.json", "r") as file:
        data = json.load(file)
    data[0][f"{bot}"] = message
    with open("arguements.json","w") as file:
        json.dump(data, file, indent=4)

def startBots():
    subprocess.Popen(["python", "debater1.py"])
    subprocess.Popen(["python", "debater2.py"])

def debate(newDebate):
    initial_data = [
        {
            "bot1": "",
            "bot2": ""
        }
    ]
    if newDebate:
        debateGenerator.generateFile(None,None,None)
    with open("arguements.json", "w") as file:
        json.dump(initial_data, file, indent=4)
    print("arguements.json has been initialized.")
    with open('debateData.json') as json_file:
        debateData = json.load(json_file)
    persona1 = debateData["persona1"]
    persona2 = debateData["persona2"]
    name1 = debateData["persona1name"]
    name2 = debateData["persona2name"]
    topic = debateData["topic"]
    updateCounter(0)
    i = 0
    starter = random.randint(1, 2)
    responder = 2 if starter == 1 else 1
    startBots()
    time.sleep(10)
    debateLength = random.randint(10, 14)
    closingDone = False
    while True:
        with open('context.json', 'r') as context_file:
            context = formatContext(json.load(context_file))

        if i == 0:
            if starter == 1:
                print("Bot 1 initiates the debate.")
                message = generateInitial(persona1, topic, name1)
                writeMessage(message, "bot1")
            else:
                print("Bot 2 initiates the debate.")
                message = generateInitial(persona2, topic, name2)
                writeMessage(message, "bot2")
            time.sleep(4)

        elif i >= debateLength and not closingDone:
            if (i % 2 == 1 and starter == 1) or (i % 2 == 0 and starter == 2):
                # Bot 2 gives final statement first
                print("Bot 2's closing statement")
                message = generateFinal(persona2, topic, context, name2)
                writeMessage(message, "bot2")
                time.sleep(4)

                print("Bot 1's closing statement")
                message = generateFinal(persona1, topic, context, name1)
                writeMessage(message, "bot1")
                time.sleep(4)
            else:
                # Bot 1 gives final statement first
                print("Bot 1's closing statement")
                message = generateFinal(persona1, topic, context, name1)
                writeMessage(message, "bot1")
                time.sleep(4)

                print("Bot 2's closing statement")
                message = generateFinal(persona2, topic, context, name2)
                writeMessage(message, "bot2")
                time.sleep(4)

            closingDone = True
            break  

        else:
            if (i % 2 == 1 and starter == 1) or (i % 2 == 0 and starter == 2):
                print("Bot 2's turn")
                message = generateResponse(persona2, topic, context, name2)
                writeMessage(message, "bot2")
            else:
                print("Bot 1's turn")
                message = generateResponse(persona1, topic, context, name1)
                writeMessage(message, "bot1")
            time.sleep(4)

        i += 1
    debate(True)
name = None
generate = input("Do you want to generate a new debate? (y/n): ")
if generate == "y":
    specialTopic = input("Do you want to generate a special topic? (y/n): ")
    if specialTopic == "y":
        specialTopic = input("Enter the special topic: ")
    else:
        specialTopic = None
    specialPersonas = input("Do you want to generate special personas? (y/n): ")
    if specialPersonas == "y":
        specialPersonas = input("Enter the special personas: ")
    else:
        specialPersonas = None
    if specialTopic != None or specialPersonas != None:
        name = input("Do you want to generate a name? (y/n): ")
        if name == "y":
            name = True
        else:
            name = None
        debateGenerator.generateFile(specialTopic,specialPersonas,True)
        debate(False)
    else:
        debate(True)
else:
    debate(False)