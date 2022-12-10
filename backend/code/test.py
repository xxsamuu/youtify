def sum(num1, num2):
    return num1 + num2

two_dim_array = [{'a': 20, 'c':30, 'function': sum, 'sum': ''}, ['b', 2]]

def change():
    two_dim_array[0]['sum'] = two_dim_array[0]['function'](20, 30)
    return two_dim_array

print(change())
print(two_dim_array)