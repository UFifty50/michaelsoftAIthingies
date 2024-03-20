import os
import json
import openai
import sqlite3

# OpenAI Config
openai.api_key = "62437466-c110-4947-a0bb-0c38c870cc95"
openai.api_base = "https://polite-ground-030dc3103.4.azurestaticapps.net/api/v1"
openai.api_type = "azure"
openai.api_version = "2023-05-15"
deployment_name = "gpt-35-hackathon"


# TODO: UI
# TODO: multiple DB formats


class doWeNeedAI:
    prompt: str
    messages: list
    
    def __init__(self):
        self.prompt = "You are an AI that determines if a prompt needs to query a database. If a query is needed, return \"true\". Otherwise, return \"false\". A query is only needed if items to find are specified in the prompt."
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        
    def send(self):
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=2048,
            messages=self.messages,
        )
        return response["choices"][0]["message"]["content"]

class dbAI:
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor
    prompt: str
    messages: list

    def __init__(self):
        self.conn = sqlite3.connect("chatbot.db")
        self.cursor = self.conn.cursor()
        self.prompt = r"""You are an AI assistant that extracts information from a database. You will return your data in the format \"{dataname: fetchcommand}\".

SQL Database Schema:
\"CREATE TABLE \"email_list\" (
	\"list_name\"	TEXT NOT NULL,
	\"subscribers\"	INTEGER,
	\"followers\"	INTEGER,
	\"contributors\"	INTEGER,
	PRIMARY KEY("list_name")
);\""""

        self.messages = [{"role": "system", "content": self.prompt}]
        

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def send(self):
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=2048,
            messages=self.messages,
        )
        return response["choices"][0]["message"]["content"]
    
    def parseSQL(self, SQLs: str) -> str:
        # data in format of {"data name": "SQLcommand"}
        print(SQLs)
        SQLcmdMap = json.loads(SQLs)
        dataMap = {}
        
        for dataName, SQLcmd in SQLcmdMap.items():
            dataMap[dataName] = self.cursor.execute(SQLcmd).fetchall()
            
        return json.dumps(dataMap)
            

class userAI:
    prompt: str
    messages: list

    def __init__(self):
        self.prompt = "You are an AI assistant."
        
        self.messages = [{"role": "system", "content": self.prompt}]

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def send(self):
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=2048,
            messages=self.messages,
        )
        return response["choices"][0]["message"]["content"]


isdbneededAI = doWeNeedAI()
dbai = dbAI()
userai = userAI()

while True:
    # Get input from user
    user_input = input("User: ")
    
    isdbneededAI.add_message("user", user_input)
    isdbneeded = isdbneededAI.send()
    
    if isdbneeded == "true":
        dbai.add_message("user", user_input)
        parsedData = dbai.parseSQL(dbai.send())
        user_input += "\n" + parsedData
        
    userai.add_message("user", user_input)
    azure_openai_response = userai.send()
    userai.add_message("assistant", azure_openai_response)
    dbai.add_message("assistant", azure_openai_response)
    print("Azure OpenAI Service: " + azure_openai_response)
