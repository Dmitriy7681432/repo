import pandas as pd
a = pd.Series([5,6,7],index=["a","b","c"])
print(a)
df = pd.DataFrame({
'№ п.п.':'a',
'country': ['Kazakhstan', 'Russia', 'Belarus', 'Ukraine'],
'population': [17.04, 143.5, 9.5, 45.5],
'square': [2724902, 17125191, 207600, 603628]
})
print(df)
b = []
c='-'
b.append(c)
print(b)