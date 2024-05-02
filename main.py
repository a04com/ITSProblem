from classes import Player, Item, Events, City, COEFFS
from db import insertItem, getItems, updateItem, deleteItems, deleteItem, makeItems
import random, math

ITEM_LIST = ['мясо', 'сухофрукты', 'зерно', 'мука', 'ткани', 'краска']
day_count = 1
isEmpty = False

player = Player(MAX_LOAD=input("Введите максимальное кол-во единиц вместительности: "), 
                MAX_SPEED=input("Введите максимальное кол-во единиц скорости: "))
nextCity = City

while True:
    profit = 0

    prices = {"мясо": random.randint(5, 15), "сухофрукты": random.randint(5, 15), 
              "зерно": random.randint(5, 15), "мука": random.randint(5, 15), 
              "ткани": random.randint(5, 15), "краска": random.randint(5, 15)}

    randomItem = Item(random.choice(ITEM_LIST))
    randomItem.price = prices.get(randomItem.item)

    while player.balance - randomItem.price > 0 and player.MAX_LOAD > 0:

        insertItem(randomItem)
        player.balance -= randomItem.price
        profit -= randomItem.price
        player.MAX_LOAD -= 1

        print("Куплено {} за {}. Текущий баланс: {}, осталось места: {}".format(randomItem.item,
                randomItem.price, player.balance, player.MAX_LOAD))

        randomItem = Item(random.choice(ITEM_LIST))
        randomItem.price = prices.get(randomItem.item)
    
    print("\nБаланс: {}".format(player.balance))
    print("Места осталось: {}".format(player.MAX_LOAD))

    print("Хотите изменить/добавить/удалить информацию о товаре?")
    isChange = input("Да(1) Нет(0): ")

    if isChange == "0":
            isChange = False

    while isChange:
        getItems()

        print("Изменить(0) / Добавить(1) / Удалить(2)")
        theChange = int(input())

        if theChange == 0:

            itemToChange = int(input("Выберите цифру какой товар изменить: "))
            newPrice = int(input("Новая цена: "))
            newQuality = float(input("Новое качество: "))
            
            updateItem(newPrice, newQuality, id=itemToChange)

        if theChange == 1:
            itemToAdd = input("Какой товар добавить: ")
            newPrice = int(input("Цена: "))
            newQuality = float(input("Качество: "))

            newItem = Item(itemToAdd)
            newItem.price = newPrice
            newItem.quality = newQuality

            insertItem(newItem)

        if theChange == 2:
            itemToDelete = input("Какой товар удалить(Введите ID): ")
            deleteItem(itemToDelete)

        isChange = input("Готово. Изменить ещё? (1, 0): ")

        if isChange == "0":
            isChange = False

    for i in makeItems():
        player.products.append(i)

    while nextCity.distance - player.speed > 0:
        if len(player.products) == 0:
            print("У вас украли все товары.")
            isEmpty = True
            break

        randomEventNumber = random.randint(0, 8)
        event = Events(randomEventNumber).name

        if event == "REGULAR_DAY":
            print("\n День {}".format(day_count))
            player.speed = random.randint(3, 5)
            print("Обычный день.")
            nextCity.distance -= player.speed
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1

        elif event == "RAIN":
            print("\n День {}".format(day_count))
            player.speed = random.randint(3, 5)
            if player.speed - 2 <= 0:
                print("Пошёл дождь. Скорость была {}, стала 0".format(player.speed))
                player.speed = 0
            else:
                print("Пошёл дождь. Скорость была {}, стала {}".format(player.speed, player.speed - 2))
                player.speed = player.speed - 2
                nextCity.distance -= player.speed

                player.speed = 0
            if random.random() < 0.2:
                lowerQualityItem = random.choice(player.products)

                if lowerQualityItem.quality == COEFFS.Normal.value:
                    oldQuality = lowerQualityItem.quality
                    lowerQualityItem.quality = COEFFS.SlightDamage.value

                elif lowerQualityItem.quality == COEFFS.SlightDamage.value:
                    oldQuality = lowerQualityItem.quality
                    lowerQualityItem.quality = COEFFS.HalfDamage.value

                elif lowerQualityItem.quality == COEFFS.HalfDamage.value:
                    oldQuality = lowerQualityItem.quality
                    lowerQualityItem.quality = COEFFS.AlmostAllDamage.value
                
                elif lowerQualityItem.quality == COEFFS.AlmostAllDamage.value:
                    oldQuality = lowerQualityItem.quality
                    lowerQualityItem.quality = COEFFS.Trash.value
                
                else:
                    print("Товар намок, но качество итак ужасное.")
                    continue

                print("Товар намок. Коэффицент товара {} снизился с {} до {}".format(lowerQualityItem.item, oldQuality, lowerQualityItem.quality))

            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1
        
        elif event == "SMOOTH_ROAD":
            print("\n День {}".format(day_count))
            print("Ровная дорога. Скорость увеличена на 2.")
            player.speed = random.randint(3, 5)

            if player.speed + 2 > player.MAX_SPEED:
                player.speed = player.MAX_SPEED
                print("Скорость не может превысить максимальное, поэтому скорость {}".format(player.MAX_SPEED))

            nextCity.distance -= player.speed
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1
        
        elif event == "BROKEN_CART":
            print("\n День {}".format(day_count))
            player.speed = 0
            print("Телега сломалась. Стоим на месте.")
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1

        elif event == "RIVER":
            print("\n День {}".format(day_count))
            rn = random.randint(1, 2)
            print("Река. Весь день ушел на поиск тропы. Проехано {}".format(rn))
            nextCity.distance -= rn
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1

        elif event == "LOCAL":
            print("\n День {}".format(day_count))
            player.speed = random.randint(3, 5)
            rn = random.randint(3, 6)
            print("Встретил местного. Проехано на {} больше.".format(rn))
            nextCity.distance -= player.speed + rn
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1
        
        elif event == "ROBBER":
            print("\n День {}".format(day_count))
            player.speed = random.randint(3, 5)

            if player.balance > 50:
                oldBalance = player.balance
                robbed_money = random.randint(50, player.balance)
                player.balance -= robbed_money
                print("Встретил разбойника. У вас забрали {}. Новый баланс: {}".format(robbed_money, player.balance))
            else:
                highestQuality = max([i.quality for i in player.products])
                highestQualityProducts = [i for i in player.products if i.quality == highestQuality]
                rnProducts = random.randint(1, math.ceil(len(highestQualityProducts) / 2))

                for i in range(rnProducts):
                    player.products.remove(highestQualityProducts[i])
                print('''Встретил разбойника. У вас было недостаточно денег, поэтому у вас забрали {} товаров с качеством {} каждая.'''.format(rnProducts, highestQuality))
            day_count += 1
        
        elif event == "TAVERN":
            print("\n День {}".format(day_count))
            print("Вы встретили таверну. Остановиться?")
            isStop = bool(int(input("Введите 1 если хотите остановиться и 0 если продолжить путь. ")))
            
            if isStop == True:
                if player.balance > 50:
                    print("Ночлег обошелся в 50 монет.")
                    if random.random() > 0.5:
                        lowestQuality = min([i.quality for i in player.products])
                        lowestQualityProducts = [i for i in player.products if i.quality == lowestQuality]
                        rnProducts = random.randint(1, len(lowestQualityProducts))
                        print("Вы обменяли {} товара с качеством {} на качество c коэффом 1.2.".format(rnProducts,
                            lowestQuality))
                        
                        for i in lowestQualityProducts:
                            i.quality = 1.2
                    else:
                        print("Вам не удалось ничего обменять")
            day_count += 1
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
        
        else:
            print("\n День {}".format(day_count))
            player.speed = random.randint(3, 5)
            lowerQualityItem = random.choice(player.products)

            if lowerQualityItem.quality == COEFFS.Normal.value:
                oldQuality = lowerQualityItem.quality
                lowerQualityItem.quality = COEFFS.SlightDamage.value

            elif lowerQualityItem.quality == COEFFS.SlightDamage.value:
                oldQuality = lowerQualityItem.quality
                lowerQualityItem.quality = COEFFS.HalfDamage.value

            elif lowerQualityItem.quality == COEFFS.HalfDamage.value:
                oldQuality = lowerQualityItem.quality
                lowerQualityItem.quality = COEFFS.AlmostAllDamage.value
            
            elif lowerQualityItem.quality == COEFFS.AlmostAllDamage.value:
                oldQuality = lowerQualityItem.quality
                lowerQualityItem.quality = COEFFS.Trash.value
            
            else:
                print("Товар уменьшился в качестве, но качество итак ужасное.")
                continue

            print("Товар уменьшился в качестве. Коэффицент товара {} снизился с {} до {}".format(lowerQualityItem.item, oldQuality, lowerQualityItem.quality))
            day_count += 1
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
    
    if not isEmpty:
        print("\n День {}".format(day_count))
        print("Доехали.")

        for i in player.products:
            print("Продано {} за {}".format(i.item, i.price * i.quality))
            profit += i.price * i.quality
        
        print("Профит: {}".format(profit))

    deleteItems()
    break
