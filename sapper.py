import random
from copy import copy, deepcopy
import rsa
import os
import shutil
class Sapper:
    def __init__(self, w=5, h=5, bombs=2) -> None:
        self.map = [[0 for _ in range(w)] for _ in range(h)]
        self.w = w
        self.h = h
        self.bombs = bombs
        self.was = [[0 for _ in range(w)] for _ in range(h)]
        self.current_state = [['@' for _ in range(w)] for _ in range(h)]
        self.flags = []
        self.init_map()
        self.bombs_count = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(h):
            for j in range(w):
                self.bombs_count[i][j] = self.check_bombs(j, i)
    
    def init_map(self):
        cnt = 0
        bombs = []
        while cnt != self.bombs:
            x = random.randint(0, self.w-1)
            y = random.randint(0, self.h-1)
            if (x, y) not in bombs:
                cnt += 1
                bombs.append((y, x))
                self.map[y][x] = 1
            
    def is_bomb(self, x, y):
        return self.map[y][x] == 1
    
    def check_bombs(self, x, y):
        cnt = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i + y >= 0 and j + x >= 0 and i + y < self.h and j + x < self.w:
                    cnt += self.map[i + y][j + x]
        return cnt
    def is_good_pos(self, x, y):
        return y >= 0 and x >= 0 and y < self.h and x < self.w
    
    def dfs(self, x, y):
        if self.was[y][x]:
            return
        self.was[y][x] = 1
        # self.current_state[y][x] = self.check_bombs(x, y)
        if self.bombs_count[y][x] > 0:
            return
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_good_pos(x + j, y + i) and abs(i) + abs(j) == 1 and self.was[y + i][x + j] == 0 and not self.is_bomb(x+j, y + i):
                    self.dfs(x + j, y + i)
    
    
    def clear_arrays(self):
        self.was = [[0 for _ in range(self.w)] for _ in range(self.h)]
        self.current_state = [[0 for _ in range(self.w)] for _ in range(self.h)]
    def turn(self, x, y, turn_type):
        # self.clear_arrays()
        
        if turn_type == 0:
            if self.is_bomb(x, y):
                return -1
            self.dfs(x, y)
        else:
            if (x, y) not in self.flags:
                self.flags.append((x, y))
            else:
                self.flags.remove((x, y))
        return 0
    
    
    def get_current_state(self):
        state = [['@' for _ in range(self.w)] for _ in range(self.h)]
        for i in range(self.h):
            for j in range(self.w):
                if (j, i) in self.flags:
                    state[i][j] = 'f'
                    continue
                if self.was[i][j] == 1:
                    state[i][j] = self.bombs_count[i][j]

        
        return state
    
    
    def print_current_state(self):
        state = self.get_current_state()
        for i in range(len(state)):
            for j in range(len(state[i])):
                print(state[i][j], end=' ')
            print()
            
    def get_bomb_map(self):
        return self.map
    
    def print_bomb_map(self):
        state = self.get_bomb_map()
        for i in range(len(state)):
            for j in range(len(state[i])):
                print(state[i][j], end=' ')
            print()
            
    def load_state(self, string:str):
        w, h, state = string.split('.')
        self.w = w
        self.h = h
        self.map = [[0 for _ in range(h)] for _ in range(w)]
    def make_state(self):
        return "123"

# сохранение состояния, не удалось

# files = os.listdir('.')
# if "key.pem" in files:
#     cls = Sapper()
#     with open('key.pem', mode='rb') as privatefile:
#         keydata = privatefile.read()
#     key = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')
#     with open('game.pem', mode='rb') as f:
#         state = f.read()
    
#     state = rsa.decrypt(state, key)
#     shutil.rmtree('key.pem')
#     shutil.rmtree('game.pem')
#     print(state)
#     cls.load_state(state)

# (bob_pub, bob_priv) = rsa.newkeys(512)
# message = 'hello Bob!'.encode('utf8')  
# crypto = rsa.encrypt(message, bob_pub)
# print(crypto)
# message = rsa.decrypt(crypto, bob_priv)
# print(message.decode('utf8'))
cls = Sapper(10, 10, 10)
# exit(0)
print("Введите высоту и ширину поля и кол-во бомб")
inp = input()
try:
    h, w, b= map(int, inp.split())
except:
    print('Неверные аргументы')
    exit(0)
if h * w < b:
    print('Неверное кол-во бомб')
    exit(0)
cls = Sapper(w, h, b)
while True:
    inp = input()
    if len(inp.split()) != 3:
        print("Неверное число аргументов")
        continue
    try:
        
        x, y, act = map(str, inp.split())
        
        x = int(x)
        y = int(y)
        # act = int(act)
        # act = 0 if act == "Open" else 1
        if act not in ["Open", "Flag"]:
            print('Неверная команда')
            continue
        act = 0 if act == "Open" else 1
        ret = cls.turn(x, y, act)
        if ret == -1:
            print('GAME OVER!!!!!!!!!!!!!!!')
            exit(0)
        cls.print_current_state()
        print()
        cls.print_bomb_map()
    except KeyboardInterrupt:
        # TODO encrypt with RSA
        (priv, pub) = rsa.newkeys(512)
        state = cls.make_state()
        state = state.encode('utf8')
        crypto = rsa.encrypt(state, pub)
        
        with open('game.pem', mode='wb') as f:
            f.write(crypto)
        with open('key.pem', mode='wb') as f:
            
            f.write(priv.save_pkcs1('PEM'))
        
        print('saved!')
        exit(0)
