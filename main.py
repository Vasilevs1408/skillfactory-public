price = 0
discount = 10
tickets = input("Введите кол-во билетов: ")

for i in range(int(tickets)):
    age = input("Укажите возраст посетителя: ")
    if int(age) < 18:
        price = price + 0
    elif 18 <= int(age) < 25:
        price = price + 990
    elif int(age) >= 25:
        price = price + 1390
if int(tickets) > 3:
    price = price - price * discount / 100
print("общая стоимость билетов: ", price)
