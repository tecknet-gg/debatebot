from gpt4all import  GPT4All
import requests
import random
import nltk
from nltk.corpus import wordnet as wn
import random
import re
import faker
import json

def generatePersonas(debateTopic,special,name):
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    personas = [{},{}]
    name2 = None
    for i in range(2):
        if i == 1:
            stance = "against"
        else:
            stance = "for"
        if name == None:
            name = generateName()
        if name == True:
            name = input("Enter name: ")
            name2 = True
        personaPrompt = getPersonaPrompt(debateTopic, stance, name, special)
        print(f"Generating person that is {stance} the motion:")
        print(personaPrompt)
        with model.chat_session():
            persona = model.generate(personaPrompt, max_tokens=1024)
            print(persona)
        match = re.search(r'"([^"]*)"', persona)
        if match:
            quotedText = match.group(1)
            print(quotedText)
            personas[i][0] = quotedText
            personas[i][1] = name
        else:
            print("No quoted text found.")
        if name2:
            name = True
        else:
            name = None
    return personas


def generateDebate(topic):
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    if topic == None:
        topic = randomWord("n")
    print(f"Generating debate topic for {topic}:")
    debatePrompt = f"""
    You are tasked with generating a fun, quirky, and unconventional debate topic for a lively and humorous discussion. The topic should be something that invites creative arguments, and the tone should be lighthearted and playful, but still worthy of a spirited back-and-forth.
    The question should be a simple for/against statement.
    The topic should be something that could have two distinct and interesting sides. It could be something slightly absurd, or something deeply philosophical. 
    The debate topic must incorporate the noun {topic} into it.
    Here is the format:
    debate_topic: "Debate topic goes here, something creative and unusual that will generate amusing arguments on both sides."
    In your response, only the debate topic should be put in double quotes.
    """
    with model.chat_session():
        text = model.generate(debatePrompt, max_tokens=1024)
        print(text)

    match = re.search(r'"([^"]*)"', text)
    if match:
        quotedText = match.group(1)
        print(quotedText)
        return quotedText
    else:
        print("No quoted text found.")


def getPersonaPrompt(debateTopic, stance, name, special):
    if special == None:
        special = ""
    else:
        special = f"Special prompt: {special}"
    personaPrompt = f"""
        You are tasked with creating one completely unique personas for a lively and funny debate about {debateTopic}"
        Their quirky persona should be unique and intersting, and should incorporate the verb: {randomWord("v")}
        The persona should be named {name} and their job title should be {generateJob()}, aged {generateAge()}.
        Each persona should have a distinct background, personality, tone, quirks, and speaking style.
        This persona should argue {stance} the motion.
        The persona should also emobdy this special prompt: {special}

        For each persona, include:
        - A brief description of their background.
        - A quirky habit or odd trait.
        - Their stance on the debate (For or Against).
        - A unique way of speaking or phrasing things.

        Here is the format to follow:
        persona1: "Persona 1 description goes here, including their background, quirks, stance, and speaking style, and their arguement {stance} the motion."
        The persona and their description, along with their arguement should be put into one sentence, in double quotes. No other sentences should be in double quotes.
        """
    return personaPrompt

def generateName():
    fake = faker.Faker()
    name = fake.name()
    print(name)
    return name

def generateJob():
    fake = faker.Faker()
    job = fake.job()
    print(job)
    return job

def generateAge():
    age = random.randint(10, 70)
    print(age)
    return age

def randomWord(type):
    words = [word.name() for word in wn.all_synsets(f'{type}')]
    word = random.choice(words)
    word = word.split('.')[0]
    print(word)
    return word


def generateFile(specialTopic, specialPersonas,name):
    debateTopic = generateDebate(specialTopic)
    personas = generatePersonas(debateTopic,specialPersonas,name)
    debateData = {
        "topic": debateTopic,
        "persona1": personas[0][0],
        "persona1name": personas[0][1],
        "persona2": personas[1][0],
        "persona2name": personas[1][1],
    }
    with open('debateData.json', 'w') as outfile:
        json.dump(debateData, outfile, indent=4)
    print("Debate data saved to debateData.json")
