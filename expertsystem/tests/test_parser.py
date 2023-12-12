import pandas as pd

try:
    from expertsystem.expertsystem.myparser import DataProcessor, MostValuedConsumer, MostValuedProducer
except ImportError:
    from expertsystem.myparser import DataProcessor, MostValuedConsumer, MostValuedProducer


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
    proc.get_base_value_0()
