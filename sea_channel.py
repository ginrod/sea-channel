import numpy, math, heapq, uuid

def big_ship_arrival(t):
    t /= 60
    miu, sigma = 45, math.sqrt(3)

    if 11 <= t and t < 17:
        miu, sigma = 35, math.sqrt(7)
    elif 17 <= t and t <= 20:
        miu, sigma = 60, math.sqrt(9)

    return numpy.random.normal(miu, sigma)

def medium_ship_arrival(t):
    t /= 60
    miu, sigma = 15, math.sqrt(3)

    if 11 <= t and t < 17:
        miu, sigma = 10, math.sqrt(5)
    elif 17 <= t and t <= 20:
        miu, sigma = 20, math.sqrt(5)

    return numpy.random.normal(miu, sigma)

def small_ship_arrival(t):
    t /= 60
    miu, sigma = 5, math.sqrt(2)

    if 11 <= t and t < 17:
        miu, sigma = 3, math.sqrt(1)
    elif 17 <= t and t <= 20:
        miu, sigma = 10, math.sqrt(2)

    return abs(numpy.random.normal(miu, sigma))

def ship_arrival(event, eventsQueue, floodgate, dikes, queue, entringToDike, shipsInDikes, simulationTime, leavingFromDike):
    d = event['dike']
    ship = event['ship']

    pending = leavingFromDike[d]

    if not queue[d] and floodgate[d] == 'close' and not pending:
        floodgate[d] = 'opening'
        openTime = numpy.random.exponential(1/4) + simulationTime
        openEvent = {'type': 'Open Floodgate', 'dike': d}
        heapq.heappush(eventsQueue, (openTime, openEvent))
        queue[d].append(ship)
        return

    if not queue[d] and floodgate[d] == 'open':
        if  ship['size'] + dikes[d][0] <= 6:
            dikes[d][0] += ship['size']
            shipsInDikes[d].append(ship)
            timeToEnter = numpy.random.exponential(1/2) + simulationTime
            enterEvent = {'type': 'Ship Into Dike', 'dike': d, 'ship': ship}
            heapq.heappush(eventsQueue, (timeToEnter, enterEvent))
            entringToDike[d] += 1
        elif ship['size'] + dikes[d][1] <= 6:
            dikes[d][1] += ship['size']
            shipsInDikes[d].append(ship)
            timeToEnter = numpy.random.exponential(1/2)
            enterEvent = {'type': 'Ship Into Dike', 'dike': d, 'ship': ship}
            heapq.heappush(eventsQueue, (timeToEnter, enterEvent))
            entringToDike[d] += 1
        else:
            queue[d].append(ship)
        return
    
    queue[d].append(ship)

def open_floodgate(event, eventsQueue, floodgate, dikes, queue, entringToDike, shipsInDikes, simulationTime):
    d = event['dike']

    if floodgate[d] != 'opening':
        raise Exception(f'La puerta del dique {d} estaba {floodgate[d]} al mandarse a abrir')
    
    if not queue[d]:
        raise Exception(f'La puerta del dique {d} se está abriendo y no hay barcos en la cola del dique')
    
    shipsToRemove = []
    for ship in queue[d]:
        if  ship['size'] + dikes[d][0] <= 6:
            dikes[d][0] += ship['size']
            shipsInDikes[d].append(ship)
            timeToEnter = numpy.random.exponential(1/2) + simulationTime
            enterEvent = {'type': 'Ship Into Dike', 'dike': d, 'ship': ship}
            heapq.heappush(eventsQueue, (timeToEnter, enterEvent))
            shipsToRemove.append(ship)
            entringToDike[d] += 1
        elif ship['size'] + dikes[d][1]<= 6:
            dikes[d][1] += ship['size']
            shipsInDikes[d].append(ship)
            timeToEnter = numpy.random.exponential(1/2) + simulationTime
            enterEvent = {'type': 'Ship Into Dike', 'dike': d, 'ship': ship}
            heapq.heappush(eventsQueue, (timeToEnter, enterEvent))
            shipsToRemove.append(ship)
            entringToDike[d] += 1
        
        if dikes[d][0] == 6 and dikes[d][1] == 6:
            break
    
    for ship in shipsToRemove:
        queue[d].remove(ship)
    
    floodgate[d] = 'open'

def ship_into_dike(event, eventsQueue, floodgate, pendingToEnter, simulationTime):
    ship, d = event['ship'], event['dike']

    if floodgate[d] != 'open':
        raise Exception(f'El barco {ship} entró al dique y la puerta esta {floodgate[d]}')
    
    if not pendingToEnter[d]:
        floodgate[d] = 'closing'
        transportingTime = numpy.random.exponential(1/7) + simulationTime
        TransportingEvent = {'type': 'Transporting from Dike', 'dike': d}
        heapq.heappush(eventsQueue, (transportingTime, TransportingEvent))

def transporting_ships(event, eventsQueue, floodgate, shipsInDikes, leavingFromDike, simulationTime):
    d = event['dike']
    
    if floodgate[d] != 'closing':
        raise Exception(f'La fase de tranasporte del dique {d} comenzo y la puerta estaba {floodgate[d]}')
    
    if not shipsInDikes[d]:
        raise Exception(f'No hay barcos en el dique {d}')

    floodgate[d] = 'close'
    for ship in shipsInDikes[d]:
        exitTime = numpy.random.exponential(1/1.5) + simulationTime
        if d < 4:
            exitEvent = {'type': 'Ship Arrival to Dike',
                         'dike': d+1,
                         'ship': ship}
            heapq.heappush(eventsQueue, (exitTime, exitEvent))
        else:
            exitEvent = {'type': 'Ship Departure from Channel',
                         'ship': ship}
            heapq.heappush(eventsQueue, (exitTime, exitEvent))
        
        leavingFromDike[d] += 1

def create_ship_arrival_event(size):
    return {'type': 'Ship Arrival to Dike', 'ship': {'size': size, 'id': uuid.uuid4().hex}, 'dike': 0} 

def simulate_all_arrivals(simulationTime, maxSimulationTime):
    ssa = small_ship_arrival(simulationTime) + simulationTime
    msa = medium_ship_arrival(simulationTime) + simulationTime
    bsa = big_ship_arrival(simulationTime) + simulationTime

    small_ships = [(ssa, create_ship_arrival_event(1))]
    medium_ships = [(msa, create_ship_arrival_event(2))]
    big_ships = [(bsa, create_ship_arrival_event(4))]
    
    t = small_ships[0][0]
    while True:
        t += small_ship_arrival(t)
        if t > maxSimulationTime:
            break
        small_ships.append((t, create_ship_arrival_event(1)))

    t = medium_ships[0][0]
    while True:
        t += medium_ship_arrival(t)
        if t > maxSimulationTime:
            break
        medium_ships.append((t, create_ship_arrival_event(2)))
    
    t = big_ships[0][0]
    while True:
        t += big_ship_arrival(t)
        if t > maxSimulationTime:
            break
        big_ships.append((t, create_ship_arrival_event(4)))
    
    return small_ships, medium_ships, big_ships

# Simulating a sea channel with 5 dikes since 8AM to 8PM
def simulate_sea_channel():
    simulationTime = 8 * 60
    maxSimulationTime = 20 * 60

    queue = [[] for _ in range(5)]
    floodgate = ['close'] * 5
    transporting = [False] * 5
    arrivalTimeToDike = [{} for _ in range(5)]
    departureTime = {}
    dikes = [[0, 0] for _ in range(5)]
    shipsInDikes = [[] for _ in range(5)]

    ships = simulate_all_arrivals(simulationTime, maxSimulationTime)
    eventsQueue = ships[0] + ships[1] + ships[2]
    totalOfShips = len(eventsQueue)
    heapq.heapify(eventsQueue)

    entringToDike = [0] * 5
    leavingFromDike = [0] * 5

    while len(eventsQueue) > 0:
        eventTime, event = heapq.heappop(eventsQueue)
        simulationTime = eventTime

        if event['type'] == 'Ship Arrival to Dike':

            ship, d = event['ship'], event['dike']
            arrivalTimeToDike[d][ship['id']] = simulationTime

            if d > 0:
                leavingFromDike[d-1] -= 1
                if not leavingFromDike[d-1]:
                    shipsInDikes[d-1].clear()
                    dikes[d-1][0] = 0
                    dikes[d-1][1] = 0

                    if floodgate[d-1] != 'close':
                        raise Exception(f'Los barcos pasaron al dique {d} y la puerta del dique {d-1} estaba {floodgate[d-1]}')
                    
                    leavingFromDike[d-1] += 1
                    openFloodgateTime = numpy.random.exponential(1/4)
                    floodDikeTime = numpy.random.exponential(1/7) 
                    retoreToDeafultTime = openFloodgateTime + floodDikeTime + simulationTime
                    eventRestoreToDefault = {'type': 'Restore Default Dike State', 'dike': d-1}
                    heapq.heappush(eventsQueue, (retoreToDeafultTime, eventRestoreToDefault))

            ship_arrival(
                event = event, 
                floodgate = floodgate, 
                dikes = dikes, 
                queue = queue,
                eventsQueue = eventsQueue,
                entringToDike = entringToDike,
                shipsInDikes = shipsInDikes,
                simulationTime = simulationTime,
                leavingFromDike = leavingFromDike)
        
        if event['type'] == 'Restore Default Dike State':
            d = event['dike']

            leavingFromDike[d] -= 1
            if len(queue[d]) > 0:
                floodgate[d] = 'opening'
                openTime = numpy.random.exponential(1/4) + simulationTime
                openEvent = {'type': 'Open Floodgate', 'dike': d}
                heapq.heappush(eventsQueue, (openTime, openEvent))

        if event['type'] == 'Open Floodgate':
            open_floodgate(
                event = event, 
                floodgate = floodgate, 
                dikes = dikes, 
                queue = queue,
                eventsQueue = eventsQueue,
                entringToDike = entringToDike,
                shipsInDikes = shipsInDikes,
                simulationTime = simulationTime)
        
        if event['type'] == 'Ship Into Dike':
            d = event['dike']

            entringToDike[d] -= 1
            ship_into_dike(
                event = event, 
                floodgate = floodgate, 
                eventsQueue = eventsQueue,
                pendingToEnter = entringToDike,
                simulationTime = simulationTime)

        if event['type'] == 'Transporting from Dike':
            transporting_ships(
                event = event, 
                floodgate = floodgate, 
                eventsQueue = eventsQueue,
                leavingFromDike = leavingFromDike,
                shipsInDikes = shipsInDikes,
                simulationTime = simulationTime)

        if event['type'] == 'Ship Departure from Channel':
            ship = event['ship']
            departureTime[ship['id']] = simulationTime

            leavingFromDike[4] -= 1
            assert leavingFromDike[4] >= 0 
            if not leavingFromDike[4]:
                shipsInDikes[4].clear()
                dikes[4][0] = 0
                dikes[4][1] = 0

                leavingFromDike[4] += 1
                openFloodgateTime = numpy.random.exponential(1/4)
                floodDikeTime = numpy.random.exponential(1/7) 
                retoreToDeafultTime = openFloodgateTime + floodDikeTime + simulationTime
                eventRestoreToDefault = {'type': 'Restore Default Dike State', 'dike': 4}
                heapq.heappush(eventsQueue, (retoreToDeafultTime, eventRestoreToDefault))

    standingTimes = {}
    standingTimeSum = 0
    for id in arrivalTimeToDike[0]:
        standingTime = departureTime[id] - arrivalTimeToDike[0][id]
        standingTimes[id] = standingTime
        standingTimeSum += (standingTime)
    
    return standingTimeSum, totalOfShips, ships, standingTimes
   
if __name__ == '__main__':
    standingTimeSum, totalOfShips, ships, standingTimes = simulate_sea_channel()
    print(f'La suma del tiempo de espera de {totalOfShips} barcos es {standingTimeSum} minutos')
    print(f'Para un tiempo de espera aproximado de {standingTimeSum/totalOfShips} minutos por barco')
    print(f'De los {totalOfShips} barcos...')
    print(f'Hubo {len(ships[0])} barcos pequeños')
    print(f'Hubo {len(ships[1])} barcos medianos')
    print(f'Hubo {len(ships[2])} barcos grandes')