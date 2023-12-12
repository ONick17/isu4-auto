from myparser import DataProcessor

data_processor = DataProcessor()
data_processor = data_processor.parse('./forecast.csv')

objects_count = {"Солнце": 4, "Ветер": 2, "Дома": 8, "Заводы": 4, "Больницы": 3}
enemy_objects_count = {"Солнце": 1, "Ветер": 1, "Дома": 5, "Заводы": 2, "Больницы": 0}
my_objects_count = {"Солнце": 2, "Ветер": 0, "Дома": 2, "Заводы": 2, "Больницы": 2}
last_prices = {"Солнце": None, "Ветер": 15.5, "Дома": None, "Заводы": 4, "Больницы": None}
# потребители: от 10 до 1, чем больше цена, тем больше денег
# производители: от 1 до 20, чем больше цена, тем меньше денег

prices = {"Солнце": 1, "Ветер": 1, "Дома": 1, "Заводы": 1, "Больницы": 1}
mods = []
for building in prices.keys():
    mods.append([])
    prices[building] = data_processor[building].sum()
sum_plus = prices["Солнце"] + prices["Ветер"]
sum_min = prices["Дома"] + prices["Заводы"] + prices["Больницы"]

#Создаю первый модификатор: сумма энергии объекта / сумма энергии категории = 0-1
mods[0].append(prices["Солнце"]   / sum_plus)
mods[1].append(prices["Ветер"]    / sum_plus)
mods[2].append(prices["Дома"]     / sum_min)
mods[3].append(prices["Заводы"]   / sum_min)
mods[4].append(prices["Больницы"] / sum_min)

#Создаю второй модификатор: купленные противником объекты / всего данных объектов = 0-1
mods[0].append(enemy_objects_count["Солнце"]    /   objects_count["Солнце"])
mods[1].append(enemy_objects_count["Ветер"]     /   objects_count["Ветер"])
mods[2].append(enemy_objects_count["Дома"]      /   objects_count["Дома"])
mods[3].append(enemy_objects_count["Заводы"]    /   objects_count["Заводы"])
mods[4].append(enemy_objects_count["Больницы"]  /   objects_count["Больницы"])

#Нахожу средний показатель энергии за ход для каждого объекта
prices["Солнце"]   = data_processor["Солнце"].sum()   / len(data_processor["Солнце"])
prices["Ветер"]    = data_processor["Ветер"].sum()    / len(data_processor["Ветер"])
prices["Дома"]     = data_processor["Дома"].sum()     / len(data_processor["Дома"])
prices["Заводы"]   = data_processor["Заводы"].sum()   / len(data_processor["Заводы"])
prices["Больницы"] = data_processor["Больницы"].sum() / len(data_processor["Больницы"])
#Нахожу сколько энергии в данный момент добывается моими объектами
sum_plus = prices["Солнце"]*my_objects_count["Солнце"] + prices["Ветер"]*my_objects_count["Ветер"]
sum_min = prices["Дома"]*my_objects_count["Дома"] + prices["Заводы"]*my_objects_count["Заводы"] + prices["Больницы"]*my_objects_count["Больницы"]
#Выясняю кто в приоритете и на сколько, присваиваю проигрывающей стороне надбавку в проценте отстования, а выигрывающей стороне ничего не даю
if sum_plus == 0:
    sum_plus = 1
    sum_min = 0
elif sum_min == 0:
    sum_plus = 0
    sum_min = 1
elif sum_plus > sum_min:
    sum_plus = 0
    sum_min /= sum_plus
elif sum_plus < sum_min:
    sum_plus /= sum_min
    sum_min = 0
else:
    sum_plus = 0
    sum_min = 0
#Создаю третий модификатор: отношение накопления энергии к тратам энергии = 0-1
mods[0].append(sum_plus)
mods[1].append(sum_plus)
mods[2].append(sum_min)
mods[3].append(sum_min)
mods[4].append(sum_min)

#Определяю суммарное производство энергии в первые n ходов
n = int(len(data_processor["Солнце"]) * 0.25)
keke = data_processor.head(n)
keke = keke['Солнце'] + keke['Ветер']
keke = keke.sum()
#Создаю четвёртый модификатор: определение лучших производителей (производят больше энергии) первых ходов = 0-1
mods[0].append(data_processor.head(n)["Солнце"].sum()/keke)
mods[1].append(data_processor.head(n)["Ветер"].sum()/keke)

#Определение ценности
prices["Солнце"] =      (mods[0][0]+mods[0][1]+mods[0][2]+mods[0][3]) / 4
prices["Ветер"] =       (mods[1][0]+mods[1][1]+mods[1][2]+mods[1][3]) / 4
prices["Дома"] =        (mods[2][0]+mods[2][1]+mods[2][2]) / 3
prices["Заводы"] =      (mods[3][0]+mods[3][1]+mods[3][2]) / 3
prices["Больницы"] =    (mods[4][0]+mods[4][1]+mods[4][2]) / 3

print(prices)

#Определение цены
prices["Солнце"] =      20*prices["Солнце"]
prices["Ветер"] =       20*prices["Ветер"]
prices["Дома"] =        10*(1-prices["Дома"])
prices["Заводы"] =      10*(1-prices["Заводы"])
prices["Больницы"] =    10*(1-prices["Больницы"])

print(prices)

#Корректировка цены по сделкам противников
for building in last_prices.keys():
    if last_prices[building]:
        prices[building] = (prices[building] + last_prices[building]) / 2
        last_prices[building] = None

print(prices)