import pandas as pd

# Создаем DataFrame
data = {
    'Имя': ['Иван', 'Петр', 'Мария', 'Александр'],
    'Возраст': [25, 30, 28, 35],
    'Город': ['Москва', 'Санкт-Петербург', 'Москва', 'Киев']
}
df = pd.DataFrame(data)

# Экспортируем DataFrame в Excel
df.to_excel('output.xlsx', index=False)
