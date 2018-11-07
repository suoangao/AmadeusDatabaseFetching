import numpy as np
import json

with open('hotel.json') as file:
    data = json.loads(file.read())


def info_fetch_hotel(inpt):

    dataset = np.array(inpt['results'])

    property_name = []
    contacts = []
    room_info = []
    total_amount = []
    geo_location = []   # in lat/long format
    booking_code = []
    room_type_code = []
    rate_plan_code = []
    descriptions = []

    for item in dataset:

        property_name.append(item['property_name'])
        geo_location.append([item['location']['latitude'], item['location']['longitude']])
        total_amount.append(item['total_price']['amount'])
        contacts.append(item['contacts'][0]['detail'])
        room_info.append('info:  ' + str(item['rooms'][0]['room_type_info']).replace("{", "")
                                                                            .replace("}", "")
                                                                            .replace("'", ""))
        booking_code.append(item['rooms'][0]['booking_code'])
        room_type_code.append(item['rooms'][0]['room_type_code'])
        rate_plan_code.append(item['rooms'][0]['rate_plan_code'])
        descriptions.append(str(item['rooms'][0]['descriptions']).replace("[", "")
                                                                 .replace("]", "")
                                                                 .replace("'", ""))

    # print(len(property_name))
    # print(len(geo_location))
    # print(len(total_amount))
    # print(len(contacts))
    # print(len(room_info))
    # print(len(booking_code))
    # print(len(room_type_code))
    # print(len(rate_plan_code))
    # print(len(descriptions))

    data_arr = np.column_stack((property_name, contacts, room_info, total_amount, geo_location,
                                booking_code, room_type_code, rate_plan_code, descriptions))
    # print(data_arr)
    return data_arr


def hotel_sort(Data_ARR, userinptprice='lth'):

    display = Data_ARR

    if userinptprice == 'htl':
        display = display[::-1]

    print(display)
    return display


arr = info_fetch_hotel(data)
hotel_sort(arr, userinptprice='htl')
