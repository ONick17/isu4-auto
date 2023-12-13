import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import TypeAlias, Literal, DefaultDict
from collections import defaultdict
from dataclasses import dataclass


CONSUMER_MAX_VALUE = 10
PRODUCER_MAX_VALUE = 20

MIN_THRESHOLD = 0.17
MAX_THRESHOLD = 0.25

DISCONT = 0.02

ProducerName: TypeAlias = Literal['Ветер', 'Солнце']
ConsumerName: TypeAlias = Literal['Больницы', 'Дома', 'Заводы']
Tariff: TypeAlias = float

"""
Чистая приведенная стоимость потребляемой энергии
"""
NPVConsumerList: TypeAlias = list[tuple[ConsumerName, float]]

NPVProducerList: TypeAlias = list[tuple[ProducerName, float]]

AllObjects: TypeAlias = dict[ProducerName | ConsumerName, int]


@dataclass
class MostValuedConsumer():
    name: str
    value: float


@dataclass
class MostValuedProducer():
    name: str
    value: float


@dataclass
class Consumer():
    name: str


@dataclass
class Producer():
    name: str


@dataclass
class GameObject():
    object_type: ProducerName | ConsumerName
    tariff: int


class DataProcessor():
    def __init__(self) -> None:
        self.data = pd.DataFrame()
        self.producers_sums: list[float] = []
        self.consumers_sums: list[float] = []
        self.consumers_names = ('Больницы', 'Дома', 'Заводы')
        self.producers_names = ('Ветер', 'Солнце')
        self.consumers = [Consumer(name) for name in self.consumers_names]
        self.producers = [Producer(name) for name in self.producers_names]
        self.consumer_objects: DefaultDict[
            ConsumerName, list[Tariff]] = defaultdict(lambda: [])
        self.producer_objects: DefaultDict[
            ProducerName, list[Tariff]] = defaultdict(lambda: [])
        self.consumer_enemy_objects: DefaultDict[
            ConsumerName, list[Tariff]] = defaultdict(lambda: [])
        self.producer_enemy_objects: DefaultDict[ProducerName, list[Tariff]] = defaultdict(
            lambda: [])
        self.objects_count = 0
        self.enemy_objects_count = 0
        self.bought_objects_count = 0
        self.mns = 0
        self.ALL_OBJECTS_COUNT = None
        # self.ALL_OBJECTS_COUNT: AllObjects = {"Солнце": 0, "Ветер": 0,
        #                                       "Дома": 0, "Заводы": 0, "Больницы": 0}

        # self.prices = {"Солнце": 1, "Ветер": 1,
        #                "Дома": 1, "Заводы": 1, "Больницы": 1}
        # self.mods = {"Солнце": [], "Ветер": [],
        #              "Дома": [], "Заводы": [], "Больницы": []}

    def set_all_objects_count(self, ALL_OBJECTS_COUNT: AllObjects):
        self.ALL_OBJECTS_COUNT = ALL_OBJECTS_COUNT

    def parse(self, path: str) -> pd.DataFrame:
        data = pd.read_csv(path,
                           delimiter='\t',
                           dtype=float,
                           usecols=(1, 2, 3, 4, 5))

        for building in list(data.keys()):
            data[f'{building}17'] = np.array(
                data[building]) * (1 - MIN_THRESHOLD)
            data[f'{building}25'] = np.array(
                data[building]) * (1 + MAX_THRESHOLD)
        self.data = data
        return data

    def prepare_data(self, data: pd.DataFrame) -> None:
        self.producers_sums = list(
            map(lambda key: sum(data[key.name]), self.producers))
        self.consumers_sums = list(
            map(lambda key: sum(data[key.name]), self.consumers))
        self.data = data

    def getMostValued(self) -> tuple[MostValuedConsumer, MostValuedProducer]:
        # npv_consumers: NPVConsumerList = []
        # npv_producers: NPVProducerList = []
        # for k in list(self.data.keys()):
        #     data = self.data[k]
        #     npv = 0
        #     for i in range(len(self.data[k])):
        #         npv += data[i] * ((1 - DISCONT) ** i)
        #     if k in self.consumers_names:
        #         npv_consumers.append((k, npv))
        #     else:
        #         npv_producers.append((k, npv))
        # npv_consumers = sorted(npv_consumers, key=lambda x: x[1], reverse=True)
        # npv_producers = sorted(npv_producers, key=lambda x: x[1], reverse=True)
        max_producer_idx = np.argmax(self.producers_sums)
        max_consumer_idx = np.argmax(self.consumers_sums)
        most_valued_producer = MostValuedProducer(
            self.producers_names[max_producer_idx],
            self.producers_sums[max_producer_idx])
        most_valued_consumer = MostValuedConsumer(
            self.consumers_names[max_consumer_idx],
            self.consumers_sums[max_consumer_idx])

        return (most_valued_consumer, most_valued_producer)

    def get_mod2(self, objects_count: int):
        return 1 - ((objects_count + self.objects_count - self.bought_objects_count) / objects_count)

    def get_mod3(self, mes: float) -> float:
        if mes != 0:
            return mes / abs(mes)
        else:
            return 0

    def get_base_value4(self, object_name: ProducerName | ConsumerName, enemy_bet: float):
        bs4 = (self.bs3[object_name] + enemy_bet) / 2
        return {
            'Солнце': bs4['Солнце'][0],
            'Ветер': bs4['Ветер'][0],
            'Больницы': bs4['Больницы'][0],
            'Дома': bs4['Дома'][0],
            'Заводы': bs4['Заводы'][0]
        }

    def get_base_value3(self) -> pd.DataFrame:
        mes = self.get_mean_energy_store()
        print(mes)
        mod3 = self.get_mod3(mes)
        self.bs3 = {}

        for k in list(self.bs2.keys()):
            if k in self.consumers_names:
                self.bs3[k] = self.bs2[k] * (1 + mod3)
            else:
                self.bs3[k] = self.bs2[k] * (1 - mod3)

        return pd.DataFrame.from_dict(self.bs3, 'columns')

    def get_base_value2(self):
        loss = 0
        for k in list(self.consumer_objects.keys()):
            loss += len(self.consumer_objects[k]) * self.data[k].values

        store = 0

        for k in list(self.producer_objects.keys()):
            store += len(self.producer_objects[k]) * self.data[k].values

        self.bs2 = {}
        for k in list(self.data.keys()):
            if k in self.consumers_names:
                cf = store + loss
                if loss == 0 and store == 0:
                    cf = 1
                self.bs2[k] = self.bs1[k].values * \
                    (1 - (store - loss) / cf)
            else:
                cf = store + loss
                if store == 0 and loss == 0:
                    cf = 1
                self.bs2[k] = self.bs1[k].values * (1 - (loss - store) / cf)
        return pd.DataFrame.from_dict(self.bs2, orient='columns')

    # def get_mod2n(self):
    #     mods = {}
    #     mods['Солнце'] = len(self.producer_enemy_objects['Солнце']
    #                          ) / self.ALL_OBJECTS_COUNT['Солнце']
    #     mods['Ветер'] = len(self.producer_enemy_objects['Ветер']
    #                         ) / self.ALL_OBJECTS_COUNT["Солнце"]
    #     mods['Дома'] = len(self.consumer_enemy_objects['Дома']
    #                        ) / self.ALL_OBJECTS_COUNT["Дома"]
    #     mods['Больницы'] = len(self.consumer_enemy_objects['Больницы']
    #                            ) / self.ALL_OBJECTS_COUNT["Больницы"]
    #     mods['Заводы'] = len(self.consumer_enemy_objects['Заводы']
    #                          ) / self.ALL_OBJECTS_COUNT['Заводы']

    #     return mods

    def get_base_value_1(self, objects_count: int) -> pd.DataFrame:
        mod2 = self.get_mod2(objects_count)
        self.bs1 = self.bs0 * (1 + mod2)
        return self.bs1

    def get_base_value_0(self) -> pd.DataFrame:
        producer_sum = sum(self.producers_sums)
        consumer_sum = sum(self.consumers_sums)

        result = {}

        for i in range(len(self.consumers)):
            base_value_0 = (self.consumers_sums[i] /
                            consumer_sum) * CONSUMER_MAX_VALUE
            result[f'{self.consumers_names[i]}'] = [base_value_0]
            result[f'{self.consumers_names[i]}17'] = [base_value_0 *
                                                      (1 - MIN_THRESHOLD)]
            result[f'{self.consumers_names[i]}25'] = [base_value_0 *
                                                      (1 + MAX_THRESHOLD)]
        for i in range(len(self.producers)):
            base_value_0 = (self.producers_sums[i] /
                            producer_sum) * PRODUCER_MAX_VALUE
            result[f'{self.producers_names[i]}'] = [base_value_0]
            result[f'{self.producers_names[i]}17'] = [base_value_0 *
                                                      (1 - MIN_THRESHOLD)]
            result[f'{self.producers_names[i]}25'] = [base_value_0 *
                                                      (1 + MAX_THRESHOLD)]

        self.bs0 = pd.DataFrame.from_dict(result, orient='columns')
        return self.bs0

    def add_object(self, object: GameObject, enemy: bool) -> None:
        isConsumer = object.object_type in self.consumers_names

        if enemy:
            if isConsumer:
                self.consumer_enemy_objects[object.object_type].append(
                    object.tariff)
            else:
                self.producer_enemy_objects[object.object_type].append(
                    object.tariff)

            self.enemy_objects_count += 1
        else:
            if isConsumer:
                self.consumer_objects[object.object_type].append(object.tariff)
            else:
                self.producer_objects[object.object_type].append(object.tariff)
            self.objects_count += 1
            self.get_mean_energy_store()

        self.bought_objects_count += 1

    def reset(self) -> None:
        self.consumer_enemy_objects: DefaultDict[
            ConsumerName, list[Tariff]] = defaultdict(lambda: [])
        self.producer_enemy_objects: DefaultDict[ProducerName, list[Tariff]] = defaultdict(
            lambda: [])
        self.objects_count = 0
        self.enemy_objects_count = 0
        self.bought_objects_count = self.objects_count

    def remove(self, object_name: ProducerName | ConsumerName, tariff: Tariff, enemy: bool) -> None:
        if enemy:
            if object_name in self.consumers_names:
                self.consumer_enemy_objects[object_name].remove(tariff)
            else:
                self.producer_enemy_objects[object_name].remove(tariff)
        else:
            if object_name in self.consumers_names:
                self.consumer_objects[object_name].remove(tariff)
            else:
                self.producer_objects[object_name].remove(tariff)

    # def get_values(self, objects_count: int):
    #     self.get_base_value_0()
    #     self.get_base_value_1(objects_count)
    #     self.get_base_value2()
    #     bs = self.get_base_value3()
    #     return {
    #         'Солнце': bs['Солнце'][0],
    #         'Ветер': bs['Ветер'][0],
    #         'Больницы': bs['Больницы'][0],
    #         'Дома': bs['Дома'][0],
    #         'Заводы': bs['Заводы'][0]
    #     }

    def get_data_for_graphics(self) -> dict[ProducerName | ConsumerName, float]:
        result: dict[ProducerName | ConsumerName, float] = {}
        for k in list(self.data.keys()):
            if k.startswith('Ветер'):
                result[k] = self.data[k].values * \
                    len(self.producer_objects['Ветер'])
            elif k.startswith('Солнце'):
                result[k] = self.data[k].values * \
                    len(self.producer_objects['Солнце'])
            elif k.startswith('Дома'):
                result[k] = self.data[k].values * \
                    len(self.consumer_objects['Дома'])
            elif k.startswith('Заводы'):
                result[k] = self.data[k].values * \
                    len(self.consumer_objects['Заводы'])
            elif k.startswith('Больницы'):
                result[k] = self.data[k].values * \
                    len(self.consumer_objects['Больницы'])
        return result

    def get_mean_energy_store(self):
        if not self.data.empty:
            mean_wind = np.mean(self.data['Ветер'])
            mean_sun = np.mean(self.data['Солнце'])
            mean_house = np.mean(self.data['Дома'])
            mean_factory = np.mean(self.data['Заводы'])
            mean_hospital = np.mean(self.data['Больницы'])
            hospital_count = len(self.consumer_objects['Больницы'])
            factory_count = len(self.consumer_objects['Заводы'])
            house_count = len(self.consumer_objects['Дома'])
            sun_count = len(self.producer_objects['Солнце'])
            wind_count = len(self.producer_objects['Ветер'])
            self.mns = (wind_count * mean_wind) +\
                (sun_count * mean_sun) -\
                (house_count * mean_house) -\
                (factory_count * mean_factory) -\
                (hospital_count * mean_hospital)
            return self.mns
        else:
            return 0


    def show(self, data: pd.DataFrame):
        for building in list(data.keys()):
            plt.plot(data[building], label=building)
            plt.legend()
            plt.draw()

    def get_values(self, enemy_objects_count, my_objects_count):
        objects_count = self.ALL_OBJECTS_COUNT
        enemy_objects_count = {"Солнце": enemy_objects_count["СЭС"], "Ветер": enemy_objects_count["ВЭС"], "Дома": enemy_objects_count["Микрорайон"], "Заводы": enemy_objects_count["Завод"], "Больницы": enemy_objects_count["Больница"]}
        my_objects_count = {"Солнце": my_objects_count["СЭС"], "Ветер": my_objects_count["ВЭС"], "Дома": my_objects_count["Микрорайон"], "Заводы": my_objects_count["Завод"], "Больницы": my_objects_count["Больница"]}
        # enemy_objects_count = {"Солнце": 1, "Ветер": 1,
        #                        "Дома": 5, "Заводы": 2, "Больницы": 0}
        # my_objects_count = {"Солнце": 2, "Ветер": 0,
        #                     "Дома": 2, "Заводы": 2, "Больницы": 2}
        # last_prices = {"Солнце": None, "Ветер": 15.5,
        #                "Дома": None, "Заводы": 4, "Больницы": None}

        # потребители: от 10 до 1, чем больше цена, тем больше денег
        # производители: от 1 до 20, чем больше цена, тем меньше денег

        prices = {"Солнце": 1, "Ветер": 1,
                  "Дома": 1, "Заводы": 1, "Больницы": 1}
        mods = []
        for building in prices.keys():
            mods.append([])
            prices[building] = self.data[building].sum()
        sum_plus = prices["Солнце"] + prices["Ветер"]
        sum_min = prices["Дома"] + prices["Заводы"] + prices["Больницы"]

        # Создаю первый модификатор: сумма энергии объекта / сумма энергии категории = 0-1
        mods[0].append(prices["Солнце"] / sum_plus)
        mods[1].append(prices["Ветер"] / sum_plus)
        mods[2].append(prices["Дома"] / sum_min)
        mods[3].append(prices["Заводы"] / sum_min)
        mods[4].append(prices["Больницы"] / sum_min)

        # Создаю второй модификатор: купленные противником объекты / всего данных объектов = 0-1
        mods[0].append(enemy_objects_count["Солнце"] / objects_count["Солнце"])
        mods[1].append(enemy_objects_count["Ветер"] / objects_count["Ветер"])
        mods[2].append(enemy_objects_count["Дома"] / objects_count["Дома"])
        mods[3].append(enemy_objects_count["Заводы"] / objects_count["Заводы"])
        mods[4].append(enemy_objects_count["Больницы"] /
                       objects_count["Больницы"])

        # Нахожу средний показатель энергии за ход для каждого объекта
        prices["Солнце"] = self.data["Солнце"].sum() / \
            len(self.data["Солнце"])
        prices["Ветер"] = self.data["Ветер"].sum() / len(self.data["Ветер"])
        prices["Дома"] = self.data["Дома"].sum() / len(self.data["Дома"])
        prices["Заводы"] = self.data["Заводы"].sum() / \
            len(self.data["Заводы"])
        prices["Больницы"] = self.data["Больницы"].sum() / \
            len(self.data["Больницы"])
        # Нахожу сколько энергии в данный момент добывается моими объектами
        sum_plus = prices["Солнце"]*my_objects_count["Солнце"] + \
            prices["Ветер"]*my_objects_count["Ветер"]
        sum_min = prices["Дома"]*my_objects_count["Дома"] + prices["Заводы"] * \
            my_objects_count["Заводы"] + prices["Больницы"] * \
            my_objects_count["Больницы"]
        # Выясняю кто в приоритете и на сколько, присваиваю проигрывающей стороне надбавку в проценте отстования, а выигрывающей стороне ничего не даю
        if (sum_plus == 0) and (sum_min != 0):
            sum_plus = 1
            sum_min = 0
        elif (sum_plus != 0) and (sum_min == 0):
            sum_plus = 0
            sum_min = 1
        elif (sum_plus == sum_min):
            sum_plus = 0.5
            sum_min = 0.5
        elif sum_plus > sum_min:
            sum_min = 0.5 + (sum_min / sum_plus)/2
            sum_plus = 1 - sum_min
        elif sum_plus < sum_min:
            sum_plus = 0.5 + (sum_plus / sum_min)/2
            sum_min = 1 - sum_plus
        # Создаю третий модификатор: отношение накопления энергии к тратам энергии = 0-1
        mods[0].append(sum_plus)
        mods[1].append(sum_plus)
        mods[2].append(sum_min)
        mods[3].append(sum_min)
        mods[4].append(sum_min)

        # Определяю суммарное производство энергии в первые n ходов
        n = int(len(self.data["Солнце"]) * 0.25)
        keke = self.data.head(n)
        keke = keke['Солнце'] + keke['Ветер']
        keke = keke.sum()
        # Создаю четвёртый модификатор: определение лучших производителей (производят больше энергии) первых ходов = 0-1
        mods[0].append(self.data.head(n)["Солнце"].sum()/keke)
        mods[1].append(self.data.head(n)["Ветер"].sum()/keke)

        # Определение ценности
        prices["Солнце"] = (mods[0][0]+mods[0][1]+mods[0][2]+mods[0][3]) / 4
        prices["Ветер"] = (mods[1][0]+mods[1][1]+mods[1][2]+mods[1][3]) / 4
        prices["Дома"] = (mods[2][0]+mods[2][1]+mods[2][2]) / 3
        prices["Заводы"] = (mods[3][0]+mods[3][1]+mods[3][2]) / 3
        prices["Больницы"] = (mods[4][0]+mods[4][1]+mods[4][2]) / 3

        # Определение цены
        prices["Солнце"] = 20*prices["Солнце"]
        prices["Ветер"] = 20*prices["Ветер"]
        prices["Дома"] = 10*(1-prices["Дома"])
        prices["Заводы"] = 10*(1-prices["Заводы"])
        prices["Больницы"] = 10*(1-prices["Больницы"])

        return prices
