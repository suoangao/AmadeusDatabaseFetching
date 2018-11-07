import re
import numpy as np
import copy

inPutFile = open('round_trip.txt')    # I read a txt as an input directly, you could define your own input
np.set_printoptions(threshold=np.nan)


def sort_input(inpt):   # This function sort out all desired information and store them inside of 3 lists

    # This is the outbound class
    class Outbound(object):
        outboundID = -1
        airIATA = []
        airNumber = []
        arrival = []
        departure = []

        # The an initializer
        def __init__(self, id, iata, fltnumb, arrT, depTime):
            self.outboundID = id
            self.airIATA = iata
            self.airNumber = fltnumb
            self.arrival = arrT
            self.departure = depTime

    # This Function will create an outbound object
    def make_outbound(id, iata, fltnumb, arrT, depTime):
        outbound = Outbound(id, iata, fltnumb, arrT, depTime)
        return outbound

    # This is the inbound class
    class Inbound(object):
        InboundID = -1
        airIATA = []
        airNumber = []
        arrival = []
        departure = []

        # The an initializer
        def __init__(self, id, iata, fltnumb, arrT, depTime):
            self.InboundID = id
            self.airIATA = iata
            self.airNumber = fltnumb
            self.arrival = arrT
            self.departure = depTime

    # This function will create a inbound object
    def make_Inbound(id, iata, fltnumb, arrT, depTime):
        inbound = Outbound(id, iata, fltnumb, arrT, depTime)
        return inbound

    # System 1 variables

    # counters for inbound and outbound. They are used count what inbound/outbound they belong to
    outbound_counter = -1
    outbound_old = 0
    outbound_list = []

    inbound_counter = -1
    inbound_old = 0
    inbound_list = []

    # lists of content for inbound and outbound
    iata_list = []
    flight_list = []
    arr_time = []
    dep_time = []

    iata_list_ibd = []
    flight_list_ibd = []
    arr_time_ibd = []
    dep_time_ibd = []

    # System 2 variables(inbound and outbound shares same variable)
    price_list = []
    refund_list = []

    for line in inpt:

        if 'outbound' in line:
            outbound_counter += 1
            # print('the {} th outbound '.format(outbound_counter))

            if outbound_old != outbound_counter:
                # create outbound and append it in the outbound list
                outbounds = make_outbound(outbound_counter-1, iata_list, flight_list, arr_time, dep_time)
                outbound_list.append(copy.deepcopy(outbounds))

                outbound_old = outbound_counter
                # reset parameters
                iata_list.clear()
                flight_list.clear()
                arr_time.clear()
                dep_time.clear()

        if 'inbound' in line:
            inbound_counter += 1

            if inbound_old != inbound_counter:
                # create outbound and append it in the outbound list
                inbounds = make_Inbound(inbound_counter-1, iata_list_ibd, flight_list_ibd, arr_time_ibd, dep_time_ibd)
                inbound_list.append(copy.deepcopy(inbounds))

                inbound_old = inbound_counter
                # reset parameters
                iata_list_ibd.clear()
                flight_list_ibd.clear()
                arr_time_ibd.clear()
                dep_time_ibd.clear()

        if ('departs_at' in line) & (outbound_counter > inbound_counter):
            dep_time.append(re.search(r'\d+\-\d+\-\d+' + 'T' + r'\d+\:\d+', line).group(0))
            # print('departure time list', dep_time)

        if ('departs_at' in line) & (outbound_counter == inbound_counter):
            dep_time_ibd.append(re.search(r'\d+\-\d+\-\d+' + 'T' + r'\d+\:\d+', line).group(0))
            # print('departure time list', dep_time)

        if ('arrives_at' in line) & (outbound_counter > inbound_counter):
            arr_time.append(re.search(r'\d+\-\d+\-\d+' + 'T' + r'\d+\:\d+', line).group(0))
            # print('arrival time list', arr_time)

        if ('arrives_at' in line) & (outbound_counter == inbound_counter):
            arr_time_ibd.append(re.search(r'\d+\-\d+\-\d+' + 'T' + r'\d+\:\d+', line).group(0))
            # print('arrival time list', arr_time)

        # Airline IATA Sorting Logic
        if ('marketing_airline' in line) & (outbound_counter > inbound_counter):
            iata_list.append(line[-5:-3])
            # print('iata list', iata_list)

        if ('marketing_airline' in line) & (outbound_counter == inbound_counter):
            iata_list_ibd.append(line[-5:-3])

        # Airline Flight number Sorting Logic
        if ('flight_number' in line) & (outbound_counter > inbound_counter):
            flight_list.append(re.search(r'\d+', line).group(0))
            # print('flight number list', flight_list)

        if ('flight_number' in line) & (outbound_counter == inbound_counter):
            flight_list_ibd.append(re.search(r'\d+', line).group(0))

        # Total Price Sorting Logic
        if 'total_price' in line:  # we sort out total price information at this modle
            price_list.append(re.search(r'\d+\.\d+', line).group(0))

            if outbound_counter > len(price_list):  # make sure these information lines up with outbound number
                diff_price = outbound_counter - len(price_list)
                i = 0
                while i < diff_price:

                    price_list.append(price_list[-1])
                    i += 1

        # Refundable Sorting Logic
        if 'refundable' in line:
            refund_list.append(line[-7:-2])

            if outbound_counter > len(refund_list):
                diff_refund = outbound_counter - len(refund_list)
                j = 0
                while j < diff_refund:

                    refund_list.append(refund_list[-1])
                    j += 1

    return outbound_list, inbound_list, price_list, refund_list


def filter_and_output(outboundlist, inboundlist,  pricelist, refundablelist,
                      userinptrefundable='-1', userinptairline='-1',
                      userinptdptimebound1=-1, userinptdptimebound2=-1,
                      userinptarrtimebound1=-1, userinptarrtimebound2=-1,
                      userinptdptimebound1_ibd=-1, userinptdptimebound2_ibd=-1,
                      userinptarrtimebound1_ibd=-1, userinptarrtimebound2_ibd=-1,
                      userinptprice='lth'):

    '''
    !!!PLEASE READ CAREFULLY BEFORE INTEGRATE!!!
    Notice: expected user inputs are different from the default value
    example of user inputs, expect user inputs in format below:

    *if default value, all results will be returned
    userinptrefundable='true'
    userinptairline='NK'
    userinptdptimebound1=9
    userinptdptimebound2='14'
    userinptdptprice='htl'

    Everything with a ibd stands for inbound

    The display matrix(the desired data matrix) has a shape of (249, 10)
    ten columns stand for:
    1. outbound_flight_IATA,
    2. outbound_flight_air_number,
    3. outbound_flight_departure_info
    4. outbound_flight_arrival_info
    5. inbound_flight_IATA,
    6. inbound_flight_air_number,
    7. inbound_flight_departure_info
    8. inbound_flight_arrival_info
    9. total_price for an itineraries
    10. refundablility for an itineraries

    '''

    # reconstruct three lists and get a numpy array
    airline_list = []
    airflight_list = []
    arrival_data = []
    departure_data = []

    airline_list_ibd = []
    airflight_list_ibd = []
    arrival_data_ibd = []
    departure_data_ibd = []

    for item in outboundlist:
        airline_list.append(item.airIATA)
        airflight_list.append(item.airNumber)
        arrival_data.append(item.arrival)
        departure_data.append(item.departure)

    for item_ibd in inboundlist:
        airline_list_ibd.append(item_ibd.airIATA)
        airflight_list_ibd.append(item_ibd.airNumber)
        arrival_data_ibd.append(item_ibd.arrival)
        departure_data_ibd.append(item_ibd.departure)

    data_matrix = np.column_stack((airline_list, airflight_list, departure_data,
                                  arrival_data, airline_list_ibd, airflight_list_ibd, departure_data_ibd,
                                  arrival_data_ibd, pricelist, refundablelist))

    # now to display certain parts of the data matrix base on how users filter out stuffs
    display = data_matrix

    # We filter based on:
    # base on airline iata
    if userinptairline != '-1':
        # print('------------------test for IATA in airline-----------------------------')
        map_iata = []

        for iatas in data_matrix[:, 0]:
            map_iata.append(userinptairline in iatas)

        display = data_matrix[map_iata]

# ################################## OUTBOUND TIME ###############################################
    # base on time to depart bound1
    if userinptdptimebound1 != -1:
        # print('------------------test for dep time bound 1-----------------------------')
        map_deptimebound1 = []

        for deptime in display[:, 2]:

            numb_deptime = int(re.search('T' + r'\d+', deptime[0]).group(0).replace("T", ""))
            map_deptimebound1.append(userinptdptimebound1 < numb_deptime)

        display = display[map_deptimebound1]

    # base on time to depart bound2
    if userinptdptimebound2 != -1:

        map_deptimebound2 = []

        for deptime in display[:, 2]:
            numb_deptime = int(re.search('T' + r'\d+', deptime[0]).group(0).replace("T", ""))
            map_deptimebound2.append(userinptdptimebound2 > numb_deptime)

        display = display[map_deptimebound2]

    # base on time to arr bound1
    if userinptarrtimebound1 != -1:

        map_arrtimebound1 = []

        for arrtime in display[:, 3]:

            numb_arrtime = int(re.search('T' + r'\d+', arrtime[-1]).group(0).replace("T", ""))
            map_arrtimebound1.append(userinptarrtimebound1 < numb_arrtime)

        display = display[map_arrtimebound1]

    # base on time to arr bound2
    if userinptarrtimebound2 != -1:

        map_arrtimebound2 = []

        for arrtime in display[:, 3]:

            numb_arrtime = int(re.search('T' + r'\d+', arrtime[-1]).group(0).replace("T", ""))
            map_arrtimebound2.append(userinptarrtimebound2 > numb_arrtime)

        display = display[map_arrtimebound2]

# ###################################### INBOUND TIME ##############################################
    # base on time to depart bound1
    if userinptdptimebound1_ibd != -1:
        # print('------------------test for dep time bound 1-----------------------------')
        map_deptimebound1_ibd = []

        for deptime in display[:, 6]:

            numb_deptime = int(re.search('T' + r'\d+', deptime[0]).group(0).replace("T", ""))
            map_deptimebound1_ibd.append(userinptdptimebound1_ibd < numb_deptime)

        display = display[map_deptimebound1_ibd]

    # base on time to depart bound2
    if userinptdptimebound2_ibd != -1:

        map_deptimebound2_ibd = []

        for deptime in display[:, 6]:
            numb_deptime = int(re.search('T' + r'\d+', deptime[0]).group(0).replace("T", ""))
            map_deptimebound2_ibd.append(userinptdptimebound2_ibd > numb_deptime)

        display = display[map_deptimebound2_ibd]

    # base on time to arr bound1
    if userinptarrtimebound1_ibd != -1:

        map_arrtimebound1_ibd = []

        for arrtime in display[:, 7]:

            numb_arrtime = int(re.search('T' + r'\d+', arrtime[-1]).group(0).replace("T", ""))
            map_arrtimebound1_ibd.append(userinptarrtimebound1_ibd < numb_arrtime)

        display = display[map_arrtimebound1_ibd]

    # base on time to arr bound2
    if userinptarrtimebound2_ibd != -1:

        map_arrtimebound2_ibd = []

        for arrtime in display[:, 7]:

            numb_arrtime = int(re.search('T' + r'\d+', arrtime[-1]).group(0).replace("T", ""))
            map_arrtimebound2_ibd.append(userinptarrtimebound2_ibd > numb_arrtime)

        display = display[map_arrtimebound2_ibd]

    # base on refundable
    if userinptrefundable != '-1':

        if userinptrefundable == 'true':  # please keep this structure
            # print('------------------test for true in refund-----------------------------')
            display = display[display[:, 5] == ' ' + userinptrefundable]

        elif userinptrefundable == 'false':
            display = display[display[:, 5] == userinptrefundable]

    # High to low price laid out:
    if userinptprice != 'lth':

        display = display[::-1]

    print(display.shape)
    return display


# # Code Executions:
outboundslists, inboundlists, pricelists, refundlists = sort_input(inPutFile)
filter_and_output(outboundslists, inboundlists, pricelists, refundlists,
                  userinptrefundable='-1', userinptairline='-1', userinptdptimebound1=-1,
                  userinptdptimebound2=-1, userinptarrtimebound1=-1, userinptarrtimebound2=-1,
                  userinptdptimebound1_ibd=13, userinptdptimebound2_ibd=19,
                  userinptarrtimebound1_ibd=16, userinptarrtimebound2_ibd=19,
                  userinptprice='lth')

