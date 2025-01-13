category_list_eng = ['accommodation',
                 'amenity',
                 'amenity.toilet',
                 'commercial',
                 'childcare',
                 'entertainment',
                 'healthcare',
                 'national_park',
                 'parking',
                 'tourism',
                 'camping',
                 'beach',
                 'airport',
                 'ski',
                 'sport',
                 'public_transport',
                 'populated_place'
                 ]
category_list_str_eng = ''
count = 0
for i in category_list_eng:
    count = count + 1
    category_list_str_eng = category_list_str_eng + str(count) + " " + str(i) + '\n'

category_list = [['entertainment.museum', 'Музеи'],
                    ['national_park', 'Парки'],
                    ['entertainment', 'Развлечения'],
                    ['catering.restaurant', 'Рестораны'],
                    ['catering.food_court', 'Фудкорты'],
                    ['leisure.picnic', 'Места для пикника'],
                    ['accommodation','Гостинницы'],
                    ['parking', 'Парковки'],
                    ['public_transport', 'Транспорт'],
                    ['beach','Пляжи'],
                    ['amenity.toilet','Туалет']]

category_list_str = ''
count = 0
for i in category_list:
    count = count + 1
    category_list_str = category_list_str + str(count) + " " + str(i[1]) + '\n'