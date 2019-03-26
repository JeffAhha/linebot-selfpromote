import threading
import time
from reponse_template import response_challenge

def gamefunction(user_id):
    counter = 0
    while (counter < 10):
        counter = counter + 1
        print(counter)
        time.sleep(1)


question = response_challenge.genQuestion(10)
print(question[0])
print('\n====================================\n')
print(question[1])
print('\n====================================\n')
print(question[2])
print('\n====================================\n')
