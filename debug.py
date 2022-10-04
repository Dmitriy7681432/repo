import pandas as pd
a = [[1,2,3,'a'],[4,5,6,'b'],[7,8,9,'c'],[10,11,12,'d']]
df =pd.DataFrame({
    'One': [i[0] for i in a],
    'Two': [i[1] for i in a],
    'Three': [i[2] for i in a],
    'Four': [i[3] for i in a]
})
print(df)

