from classes import Player, Item, Events, City, COEFFS
import random

ITEM_LIST = ['мясо', 'сухофрукты', 'зерно', 'мука', 'ткани', 'краска']
day_count = 1

player = Player(input("Введите максимальное кол-во единиц вместительности: "))
nextCity = City
# totalProfit = 0
while True:
    # profit = player.balance

    prices = {"мясо": random.randint(5, 15), "сухофрукты": random.randint(5, 15), 
              "зерно": random.randint(5, 15), "мука": random.randint(5, 15), 
              "ткани": random.randint(5, 15), "краска": random.randint(5, 15)}

    randomItem = Item(random.choice(ITEM_LIST))
    randomItem.price = prices.get(randomItem.item)

    while player.balance - randomItem.price > 0 and player.MAX_LOAD > 0:
        player.products.append(randomItem)
        player.balance -= randomItem.price
        player.MAX_LOAD -= 1

        print("Куплено {} за {}. Текущий баланс: {}, осталось места: {}".format(randomItem.item,
                randomItem.price, player.balance, player.MAX_LOAD))

        randomItem = Item(random.choice(ITEM_LIST))
        randomItem.price = prices.get(randomItem.item)
    
    print("\nБаланс: {}".format(player.balance))
    print("Места осталось: {}".format(player.MAX_LOAD))

    while nextCity.distance > 0:
        # print("Осталось пройти: {} лиг.".format(nextCity.distance))

        randomEventNumber = random.randint(0, 8)
        event = Events(randomEventNumber).name

        if event == "REGULAR_DAY":
            print("\n День {}".format(day_count))
            print("Обычный день.")
            player.speed = random.randint(3, 5)
            nextCity.distance -= player.speed
            print("Осталось пройти: {} лиг.".format(nextCity.distance))

            day_count += 1
        elif event == "RAIN":
            print("\n День {}".format(day_count))
            print("Пошёл дождь. Скорость была {}, стала {}".format(player.speed, player.speed - 2))
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
        
        else:
            #Прописать события
            print("\n День {}".format(day_count))
            player.speed = random.randint(3, 5)
            nextCity.distance -= player.speed
            print("Осталось пройти: {} лиг.".format(nextCity.distance))
            day_count += 1
    break
