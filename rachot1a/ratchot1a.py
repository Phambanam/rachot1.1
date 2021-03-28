import math
import matplotlib.pyplot as plt
from scipy.special import comb, logsumexp
import codecs
class Box:
    def __init__(self,red = 0,white = 0,black = 0,green = 0,blue = 0):
        self.red = red
        self.white = white
        self.black = black
        self.green = green
        self.blue = blue
    def total(self):
        return self.red + self.white + self.black + self.green + self.blue
def parseData():
    f = codecs.open('task_1_ball_boxes_arrange.txt', encoding= 'utf-8')
    list = []
    f.readline()
    fline = f.readline()
    n_boxes = int(fline.split(',')[0].split(':')[1])
    m = int(fline.split(',')[1].split(':')[1])
    d =int(fline.split(',')[2].split(':')[1])
    n_Exp = int(fline.split(',')[3].split(':')[1])
    for line in f.readlines():
        if '#' in line:
            tmp = line.split(':')[1].strip().split(', ')
            list.append(tmp)
    print(len(list))
    return list
parseData()

def task1(iterations):
    exp = parseData()
    box1 = Box()

    
