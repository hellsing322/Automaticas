import pandas as pd

data = {
    'id': [1, 2, 3],
    'nombre': ['Juan', 'María', 'Pedro'],
    'edad': [25, 30, 27],
    'nombre': ['Ana', 'Luis', 'Sara']
}

df = pd.DataFrame(data)
print(df)