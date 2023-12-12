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
Tariff: TypeAlias = int

"""
Чистая приведенная стоимость потребляемой энергии
"""
NPVConsumerList: TypeAlias = list[tuple[ConsumerName, float]]

NPVProducerList: TypeAlias = list[tuple[ProducerName, float]]


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

    def getMostValued(self) -> tuple[NPVConsumerList, NPVProducerList]:
        npv_consumers: NPVConsumerList = []
        npv_producers: NPVProducerList = []
        for k in list(self.data.keys()):
            data = self.data[k]
            npv = 0
            for i in range(len(self.data[k])):
                npv += data[i] * ((1 - DISCONT) ** i)
            if k in self.consumers_names:
                npv_consumers.append((k, npv))
            else:
                npv_producers.append((k, npv))
        npv_consumers = sorted(npv_consumers, key=lambda x: x[1], reverse=True)
        npv_producers = sorted(npv_producers, key=lambda x: x[1], reverse=True)
        # max_producer_idx = np.argmax(self.producers_sums)
        # max_consumer_idx = np.argmax(self.consumers_sums)
        # most_valued_producer = MostValuedProducer(
        # self.producers_names[max_producer_idx],
        # self.producers_sums[max_producer_idx])
        # most_valued_consumer = MostValuedConsumer(
        # self.consumers_names[max_consumer_idx],
        # self.consumers_sums[max_consumer_idx])
        print(npv_consumers, npv_producers)
        return (npv_consumers, npv_producers)

    def get_mod2(self, objects_count: int):
        return 1 - ((objects_count + self.objects_count - self.bought_objects_count) / objects_count)

    def get_base_value2(self):
        loss = 0
        for k in list(self.consumer_objects.keys()):
            loss += len(self.consumer_objects[k]) * self.data[k]

        store = 0

        for k in list(self.producer_objects.keys()):
            store += len(self.producer_objects[k]) * self.data[k]

        for k in list(self.data.keys()):
            if k in self.consumers_names:
                self.data[k] = self.data[k] * store / loss
            else:
                self.data[k] = self.data[k] * loss / store

        return self.data

    def get_base_value_1(self, mod2: float) -> pd.DataFrame:
        self.bs1 = self.bs0 * (1 + mod2)
        return self.bs1

    def get_base_value_0(self) -> pd.DataFrame:
        producer_sum = sum(self.producers_sums)
        consumer_sum = sum(self.consumers_sums)

        result = {}

        for i in range(len(self.consumers)):
            base_value_0 = (self.consumers_sums[i] /
                            consumer_sum) * CONSUMER_MAX_VALUE
            result[f'{self.consumers_names[i]}'] = base_value_0
            result[f'{self.consumers_names[i]}17'] = base_value_0 * \
                (1 - MIN_THRESHOLD)
            result[f'{self.consumers_names[i]}25'] = base_value_0 * \
                (1 + MAX_THRESHOLD)
        for i in range(len(self.producers)):
            base_value_0 = (self.producers_sums[i] /
                            producer_sum) * CONSUMER_MAX_VALUE
            result[f'{self.producers_names[i]}'] = base_value_0
            result[f'{self.producers_names[i]}17'] = base_value_0 * \
                (1 - MIN_THRESHOLD)
            result[f'{self.producers_names[i]}25'] = base_value_0 * \
                (1 + MAX_THRESHOLD)
        self.bs0 = pd.DataFrame([list(result.keys()), list(result.values())])
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

        self.bought_objects_count += 1

    def get_mean_energy_store(self) -> np.floating:
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

        return (wind_count * mean_wind) +\
               (sun_count * mean_sun) -\
               (house_count * mean_house) -\
               (factory_count * mean_factory) -\
               (hospital_count * mean_hospital)

    def show(self, data: pd.DataFrame):
        for building in list(data.keys()):
            plt.plot(data[building], label=building)
            plt.legend()
            plt.draw()
