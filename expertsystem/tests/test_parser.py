import pandas as pd
from pprint import pprint
try:
    from expertsystem.expertsystem.myparser import DataProcessor, MostValuedConsumer, GameObject, MostValuedProducer, CONSUMER_MAX_VALUE, PRODUCER_MAX_VALUE
except ImportError:
    from expertsystem.myparser import DataProcessor, MostValuedConsumer, MostValuedProducer, GameObject, CONSUMER_MAX_VALUE, PRODUCER_MAX_VALUE


def test_parse():
    proc = DataProcessor()
    proc.parse('./expertsystem/forecast.csv')


def test_getMostValued():
    data = pd.DataFrame({
        'Солнце': [5.5, 5.5],
        'Ветер': [3.4, 2.3],
        'Дома': [4.0, 5.0],
        'Заводы': [2.0, 5.0],
        'Больницы': [3.0, 1.0]
    })
    most_valued_consumer = MostValuedConsumer('Дома', 9.0)
    most_valued_producer = MostValuedProducer('Солнце', 11.0
                                              )
    proc = DataProcessor()
    proc.prepare_data(data)
    assert proc.getMostValued() == (
        most_valued_consumer, most_valued_producer)


def test_base_value_0():
    data = pd.DataFrame({
        'Солнце': [5.5, 5.5],
        'Ветер': [3.4, 2.3],
        'Дома': [4.0, 5.0],
        'Заводы': [2.0, 5.0],
        'Больницы': [3.0, 1.0]
    })
    proc = DataProcessor()
    proc.prepare_data(data)
    answer = {
        'Солнце': [11. / 16.7 * PRODUCER_MAX_VALUE],
        'Ветер': [5.7 / 16.7 * PRODUCER_MAX_VALUE],
        'Дома': [9.0 / 20.0 * CONSUMER_MAX_VALUE],
        'Заводы': [7.0 / 20.0 * CONSUMER_MAX_VALUE],
        'Больницы': [4.0 / 20.0 * CONSUMER_MAX_VALUE]
        # Еще тут Больница17, Больница25 и тд.
    }

    print(proc.get_base_value_0())


def test_add_object():
    proc = DataProcessor()
    proc.add_object(GameObject('Солнце', 4), False)
    assert proc.producer_objects == {
        'Солнце': [4]
    }
    proc.add_object(GameObject('Солнце', 5), True)
    assert proc.producer_enemy_objects == {
        'Солнце': [5]
    }


def test_get_mean_energy_store():
    proc = DataProcessor()
    data = pd.DataFrame({
        'Солнце': [5.5, 5.5],
        'Ветер': [3.4, 2.3],
        'Дома': [4.0, 5.0],
        'Заводы': [2.0, 5.0],
        'Больницы': [3.0, 1.0]
    })
    proc.prepare_data(data)
    proc.add_object(GameObject('Солнце', 4), False)
    proc.add_object(GameObject('Больницы', 4), False)
    proc.add_object(GameObject('Дома', 4), False)

    assert proc.get_mean_energy_store() == -1


def test_get_mod2():
    proc = DataProcessor()
    data = pd.DataFrame({
        'Солнце': [5.5, 5.5],
        'Ветер': [3.4, 2.3],
        'Дома': [4.0, 5.0],
        'Заводы': [2.0, 5.0],
        'Больницы': [3.0, 1.0]
    })
    proc.prepare_data(data)
    bs0 = proc.get_base_value_0()
    proc.add_object(GameObject('Солнце', 4), False)
    proc.add_object(GameObject('Больницы', 4), False)
    proc.add_object(GameObject('Дома', 4), True)

    assert round(proc.get_mod2(6), 2) == round(1 - ((6 + 2 - 3) / 6), 2)
    assert proc.enemy_objects_count == 1
    assert proc.bought_objects_count == 3
    assert proc.objects_count == 2

# С остальными base_value алгоритм взаимодействия такой же
def test_base_value_1():
    proc = DataProcessor()
    data = pd.DataFrame({
        'Солнце': [5.5, 5.5],
        'Ветер': [3.4, 2.3],
        'Дома': [4.0, 5.0],
        'Заводы': [2.0, 5.0],
        'Больницы': [3.0, 1.0]
    })
    proc.prepare_data(data)
    bs0 = proc.get_base_value_0()
    pprint(bs0['Больницы'])
    proc.add_object(GameObject('Солнце', 4), False)
    proc.add_object(GameObject('Больницы', 4), False)
    proc.add_object(GameObject('Дома', 4), True)
    # print(proc.get_base_value_1(5)['Больницы'])
    # Приходится использовать [0], так как это лист
    assert round(proc.get_base_value_1(5)['Больницы'][0], 2) == round(
        2.0 * (1 + proc.get_mod2(5)), 2)
