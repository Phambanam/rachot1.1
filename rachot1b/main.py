import codecs
import collections
import random
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

c_v = 'аеиоуыэюя'  # ГЛАСНЫЕ СТРОЧНЫЕ
u_v = 'АЕИОУЫЭЮЯ'  # ГЛАСНЫЕ ЗАГЛАВНЫЕ
u_signs = 'ЬЪ-_'  # БЕЗЗВУЧНЫЕ ЗАГЛАВНЫЕ
c_signs = 'ьъ-_'  # БЕЗЗВУЧНЫЕ СТРОЧНЫЕ
u_c_r = 'БВГДЖЗЛМНРЙ'  # СОГЛАСНЫЕ ЗВОНКИЕ ЗАГЛАВНЫЕ
u_c_d = 'ПФКТШСХЦЧЩ'  # СОГЛАСНЫЕ ГЛУХИЕ ЗАГЛАВНЫЕ
c_c_r = 'бвгджзлмнрй'  # СОГЛАСНЫЕ ЗВОНКИЕ СТРОЧНЫЕ
c_c_d = 'пфктшсхцчщ'  # СОГЛАСНЫЕ ГЛУХИЕ СТРОЧНЫЕ

evolution_dict = {}


def random_color():
    rgb_random = [255, 0, 0]
    random.shuffle(rgb_random)
    return tuple(rgb_random)


class Words:
    word_dict = {}

    def __init__(self):
        capitals_file = codecs.open('names_all.txt', 'r', encoding='utf-8')
        capitals_list = capitals_file.readlines()
        for line in capitals_list:
            self.word_dict[line.strip()] = 0.0

    def use_rule(self, rule):
        chars = rule.char
        if len(chars) == 1:
            self.use_1_rule(chars)
        else:
            self.use_type_rule(chars, rule.pos)

    def use_1_rule(self, char):
        words_to_pop = []
        for capital in self.word_dict.keys():
            if char in capital.lower():
                char_dict = collections.Counter(capital)
                count = char_dict[char]
                self.word_dict[capital] = self.word_dict[capital] + count * 1.0 / len(capital)
            else:
                words_to_pop.append(capital)
        for word in words_to_pop:
            self.word_dict.pop(word)

    def use_type_rule(self, chars, pos):
        words_to_pop = []
        for capital in self.word_dict.keys():
            position = int(pos)
            if len(capital) < position:
                words_to_pop.append(capital)
                continue
            char = capital[position - 1]
            if char not in chars:
                words_to_pop.append(capital)
        for word in words_to_pop:
            self.word_dict.pop(word)

    def calculate_prob(self):
        summa = sum(self.word_dict.values())

        prob_dict = {}
        for key in self.word_dict:
            prob_dict[key] = self.word_dict[key] / summa
        return prob_dict


class DefineChar:
    pos = 0
    char = ''

    def __init__(self, char, pos):
        self.char = char
        self.pos = pos


class RulesReader:
    rules = codecs.open('task_1_words.txt', 'r', encoding='utf-8')

    def __init__(self):
        self.rules.readline()
        self.rules.readline()

    def read_rule(self):
        line_rule = self.rules.readline().strip()
        find = re.match('# \d+: \"([а-я])\"', line_rule)
        if find is not None:
            return DefineChar(find.group(1), -1)

        pos = re.match("# \d+: (\d+)", line_rule).group(1)

        if line_rule.__contains__("строчная"):
            if line_rule.__contains__("согласная"):
                if line_rule.__contains__("звонкая"):
                    return DefineChar(c_c_r, pos)
                else:
                    return DefineChar(c_c_d, pos)
            else:
                return DefineChar(c_v, pos)
        else:
            if line_rule.__contains__("согласная"):
                if line_rule.__contains__("звонкая"):
                    return DefineChar(u_c_r, pos)
                else:
                    return DefineChar(u_c_d, pos)
            else:
                return DefineChar(u_v, pos)


# first task
def make_plot():
    x = Words()
    y = RulesReader()
    first = y.read_rule()
    x.use_rule(first)
    p = x.calculate_prob()
    for key in p.keys():
        evolution_dict[key] = []
        evolution_dict[key].append(p[key])
    for i in range(0, 8):
        new = y.read_rule()
        x.use_rule(new)
        p = x.calculate_prob()
        for j in evolution_dict.keys():
            if j in p.keys():
                evolution_dict[j].append(p[j])
            else:
                evolution_dict[j].append(0.0)

    frame = pd.DataFrame({'x': range(1, 10)})
    for key in evolution_dict:
        if evolution_dict[key][1] != 0.0:
            frame[key] = evolution_dict[key]

    df = frame

    plt.style.use('seaborn-darkgrid')

    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color=np.random.rand(3, ), linewidth=1, alpha=0.9, label=column)

    plt.legend(loc=6, bbox_to_anchor=(0.5, -0.15), ncol=3)

    plt.title("Ряд распределения гипотез (слова не прошедшие 1 и 2 проверку дропнуты)", loc='left', fontsize=12,
              fontweight=0, color='orange')
    plt.xlabel("k опыт")
    plt.ylabel("Вероятность")
    plt.show()


# second task
def make_plot2():
    x = Words()
    y = RulesReader()
    first = y.read_rule()
    x.use_rule(first)
    p = x.calculate_prob()
    for key in p.keys():
        evolution_dict[key] = []
        evolution_dict[key].append(p[key])
    for i in range(0, 8):
        new = y.read_rule()
        x.use_rule(new)
        p = x.calculate_prob()
        for j in evolution_dict.keys():
            if j in p.keys():
                evolution_dict[j].append(p[j])
            else:
                evolution_dict[j].append(0.0)

    frame = pd.DataFrame({'x': range(1, 10)})
    for key in evolution_dict:
        if key == 'Александр':
            frame[key] = evolution_dict[key]

    df = frame

    plt.style.use('seaborn-darkgrid')

    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color=np.random.rand(3, ), linewidth=1, alpha=0.9, label=column)

    plt.legend(loc=2, bbox_to_anchor=(0.5, -0.15), ncol=3)

    plt.title("Тирана", loc='left', fontsize=12,
              fontweight=0, color='orange')
    plt.xlabel("k опыт")
    plt.ylabel("Вероятность")
    plt.show()


def make_plot_3():
    x = Words()
    y = RulesReader()
    first = y.read_rule()
    x.use_rule(first)
    array = [len(x.word_dict)]
    for i in range(0, 10):
        new = y.read_rule()
        x.use_rule(new)
        array.append(len(x.word_dict))

    frame = pd.DataFrame({'x': range(1, 12), 'y': array})

    df = frame

    plt.style.use('seaborn-darkgrid')

    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color="red", linewidth=1, alpha=0.9, label=column)

    plt.legend(loc=6, bbox_to_anchor=(0.5, -0.15), ncol=3)

    plt.title("Число превалирующих гипотез", loc='center', fontsize=12,
              fontweight=0, color='red')
    plt.xlabel("k опыт")
    plt.ylabel("Кол-во гипотез")
    plt.show()


def make_plot_4(pos):
    reader = RulesReader()
    evolution_4 = {}
    deleted = {}

    for i in c_v + u_v + u_signs + c_signs + u_c_r + u_c_d + c_c_r + c_c_d:
        evolution_4[i] = [0.0]
        for j in range(1, 1000):
            evolution_4[i].append(0.0)

    for i in range(1, 1000):
        next_rule = reader.read_rule()
        chars = next_rule.char
        to_delete = []
        if len(chars) == 1:
            evolution_4[chars][i] = 1.0
            evolution_4[chars.upper()][i] = 1.0
        else:
            if int(next_rule.pos) == int(pos):
                for key in evolution_4.keys():
                    if key not in next_rule.char:
                        to_delete.append(key)
        for key in to_delete:
            if key not in deleted.keys():
                deleted[key] = i

    for j in evolution_4.keys():
        count = 0
        for i in range(1, 1000):
            if evolution_4[j][i] == 0.0:
                evolution_4[j][i] = count
            else:
                count = count + 1
                evolution_4[j][i] = count

    for i in range(1, 1000):
        for j in evolution_4.keys():
            if j in deleted.keys():
                if i >= deleted[j]:
                    evolution_4[j][i] = 0.0
    for i in range(1, 1000):
        summa = 0
        for j in evolution_4.keys():
            summa += evolution_4[j][i]
        if summa != 0.0:
            for j in evolution_4.keys():
                evolution_4[j][i] = evolution_4[j][i] / summa
        else:
            counter = 0
            for j in evolution_4.keys():
                if j not in deleted.keys():
                    counter = counter + 1
            for j in evolution_4.keys():
                if j not in deleted.keys():
                    evolution_4[j][i] = 1 / counter

    frame = pd.DataFrame({'x': range(1, 1001)})
    for key in evolution_4:
        if sum(evolution_4[key]) != 0.0:
            frame[key] = evolution_4[key]

    df = frame
    plt.style.use('seaborn-darkgrid')
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color=np.random.rand(3, ), linewidth=1, alpha=0.9, label=column)

    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=2, loc=4)
    plt.title("Шестой символ в слове (оставлены ненулевые шансы)", loc='left', fontsize=12,
              fontweight=0, color='orange')
    plt.xlabel("k опыт")
    plt.ylabel("Вероятность")
    plt.show()


def make_plot_5(pos):
    reader = RulesReader()
    evolution_5 = {}
    deleted = {}

    for i in c_v + u_v + u_signs + c_signs + u_c_r + u_c_d + c_c_r + c_c_d:
        evolution_5[i] = [0.0]
        for j in range(1, 10000):
            evolution_5[i].append(0.0)

    for i in range(1, 10000):
        next_rule = reader.read_rule()
        chars = next_rule.char
        to_delete = []
        if len(chars) == 1:
            evolution_5[chars][i] = 1.0
            evolution_5[chars.upper()][i] = 1.0
        else:
            if int(next_rule.pos) == int(pos):
                for key in evolution_5.keys():
                    if key not in next_rule.char:
                        to_delete.append(key)
        for key in to_delete:
            if key not in deleted.keys():
                deleted[key] = i

    for j in evolution_5.keys():
        count = 0
        for i in range(1, 10000):
            if evolution_5[j][i] == 0.0:
                evolution_5[j][i] = count
            else:
                count = count + 1
                evolution_5[j][i] = count

    for i in range(1, 10000):
        for j in evolution_5.keys():
            if j in deleted.keys():
                if i >= deleted[j]:
                    evolution_5[j][i] = 0.0
    for i in range(1, 10000):
        summa = 0
        for j in evolution_5.keys():
            summa += evolution_5[j][i]
        if summa != 0.0:
            for j in evolution_5.keys():
                evolution_5[j][i] = evolution_5[j][i] / summa
        else:
            counter = 0
            for j in evolution_5.keys():
                if j not in deleted.keys():
                    counter = counter + 1
            for j in evolution_5.keys():
                if j not in deleted.keys():
                    evolution_5[j][i] = 1 / counter

    data = []
    for j in range(1, 1000):
        max_now = -1
        max_key = '-'
        for key in evolution_5:
            now = evolution_5[key][j]
            if now > max_now:
                max_now = now
                max_key = key
        data.append(max_key)
    frame = pd.DataFrame({'x': range(1, 1000)})
    df = frame
    frame['Седьмая буква'] = data
    plt.style.use('seaborn-darkgrid')
    for column in df.drop('x', axis=1):
        plt.plot(df['x'], df[column], marker='', color=np.random.rand(3, ), linewidth=1, alpha=0.9, label=column)
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=2, loc=4)
    plt.title("", loc='left', fontsize=12,
              fontweight=0, color='orange')
    plt.xlabel("k опыт")
    plt.ylabel("Вероятность")
    plt.show()


def get_frequency():
    reader = RulesReader()
    count_dict = {}
    for i in range(1, 10001):
        check = reader.read_rule()
        if len(check.char) == 1:
            if check.char not in count_dict.keys():
                count_dict[check.char] = 0.0
            count_dict[check.char] = count_dict[check.char] + 1
    summa = sum(count_dict.values())
    for key in count_dict.keys():
        count_dict[key] = count_dict[key] / summa
    print(count_dict)
    plt.bar(range(len(count_dict)), list(count_dict.values()), align='center')
    plt.xticks(range(len(count_dict)), list(count_dict.keys()))
    plt.show()


def changing_profile():
    reader = RulesReader()
    evolution_chaining = {}
    for i in c_v + u_v + u_signs + c_signs + u_c_r + u_c_d + c_c_r + c_c_d:
        evolution_chaining[i] = [0]

    for i in range(1, 10001):
        rule = reader.read_rule().char
        for key in evolution_chaining.keys():
            if len(rule) == 1 and rule in key:
                evolution_chaining[key].append(evolution_chaining[key][i - 1] + 1)
            else:
                evolution_chaining[key].append(evolution_chaining[key][i - 1])

    frame = pd.DataFrame({'x': range(1, 10002)})

    def recalculateNow(column_to_remap):
        summa = 0
        for key_to_remap in evolution_chaining.keys():
            summa = summa + evolution_chaining[key_to_remap][column_to_remap]
        for key_to_remap in evolution_chaining.keys():
            evolution_chaining[key_to_remap][column_to_remap] \
                = evolution_chaining[key_to_remap][column_to_remap] / summa

    for i in range(1, 10001):
        recalculateNow(i)

    for key in evolution_chaining.keys():
        if evolution_chaining[key][9999] != 0.0:
            frame[key] = evolution_chaining[key]

    df = frame
    plt.style.use('seaborn-darkgrid')
    num = 0
    for column in df.drop('x', axis=1):
        num += 1
        plt.plot(df['x'], df[column], marker='', color=np.random.rand(3, ), linewidth=1, alpha=0.9, label=column)
    plt.legend(loc=3, bbox_to_anchor=(0.5, -0.15), ncol=3)

    plt.title("Изменение частоты встречи букв", loc='left', fontsize=12,
              fontweight=0, color='orange')
    plt.xlabel("k опыт")
    plt.ylabel("Вероятность")
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    make_plot_4(5)
