import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

questions = [
    "What is the Italian word for Pie? \n a. Pasty \n b. Patty \n c. Pizza",
    "Water boils at 212 Units at which scale? \n a. Fahrenheit \n b. Celsius \n c. Kelvin",
    "Which sea creature has three hearts? \n a. Octopus \n b. Seahorse \n c. Mandarin Fish ",
    "How many bones are present in the human body? \n a. 205 \n b. 206 \n c. 306",
    "Hg stands for? \n a. Mercury \n b. Hafnium \n c. Germanium"
]

answers = ['c','a','a','b','a']

print("This server has started")

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def clientThread(conn):
    score = 0
    conn.send("Welcome to this quiz!".encode('utf-8'))
    conn.send("You will receive a question. Please answer as a, b, c or d only.".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your current score is {score}!".encode('utf-8'))
                else:
                    conn.send(f"Incorrect! Better luck next time!".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue 

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + ' is connected')
    new_thread = Thread(target=clientThread, args=(conn, addr))
    new_thread.start()
