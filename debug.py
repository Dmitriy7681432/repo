import pandas as pd
a = pd.Series([5,6,7],index=["a","b","c"])
print(a)
ls = {'name':'Kazakhstan', 'name1':'Russia', 'name2':'Belarus', 'name3':'Ukraine'}
ls1 = ls.get('name2')
ls2 = '12'
df = pd.DataFrame({
    '№ п.п.':'a',
    'country':'12',
    'population': [17.04, 143.5, 9.5, 45.5],
    'square': [2724902, 17125191, 207600, 603628]
})
print(df)
b = []
c='-'
b.append(c)
print(b)