import main
import importlib
print(main.str1)
main.str1 = 20
print(main.str1)
importlib.reload(main)
print(main.str1)