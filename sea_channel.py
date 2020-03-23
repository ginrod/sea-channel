import numpy, math, heapq

# EYE: t most be passed sumed with offset and in hours
def big_ship_arrival(t):
    miu, sigma = 45, math.sqrt(3)

    if 11 <= t and t < 17:
        miu, sigma = 35, math.sqrt(7)
    elif 17 <= t and t <= 20:
        miu, sigma = 60, math.sqrt(9)

    return numpy.random.normal(miu, sigma)

def medium_ship_arrival(t):
    miu, sigma = 15, math.sqrt(3)

    if 11 <= t and t < 17:
        miu, sigma = 10, math.sqrt(5)
    elif 17 <= t and t <= 20:
        miu, sigma = 20, math.sqrt(5)

    return numpy.random.normal(miu, sigma)

def small_ship_arrival(t):
    miu, sigma = 5, math.sqrt(2)

    if 11 <= t and t < 17:
        miu, sigma = 3, math.sqrt(1)
    elif 17 <= t and t <= 20:
        miu, sigma = 10, math.sqrt(2)

    return numpy.random.normal(miu, sigma)

def space_in_dike_line(line):
    return 6 - line[0] - line[1] - line[2]

def simulate_ships_arrival(eventsQueue, currTimeInHours):
    ssa = small_ship_arrival(currTimeInHours)
    msa = medium_ship_arrival(currTimeInHours)
    bsa = big_ship_arrival(currTimeInHours)

    heapq.heappush(eventsQueue, (ssa, {'type': 'Ship Arrival', 'size': 'small'}) )
    heapq.heappush(eventsQueue, (msa, {'type': 'Ship Arrival', 'size': 'medium'}))
    heapq.heappush(eventsQueue, (bsa, {'type': 'Ship Arrival', 'size': 'big'}))

def simulate_departure_from_dike(dike):
    t = 0
    for _ in dike[0]:
        t += numpy.random.

# Simulating a sea channel with 5 dikes since 8AM to 8PM
def simulate_sea_channel():
    standingTime = []
    offset = 8 * 60 # offset time in minutes
    maxSimTime = 12 * 60 # 12 hours (from 8AM to 8PM) = 720 minutes

    currentSimTime = numArrives = numDepartures = 0
    total = 0 # total of ships
    
    dikes = [
        ([], []), # each list represents a line in the dike
        ([], []),
        ([], []),
        ([], []),
        ([], [])
    ]

    # arrival time of n-th ship to the i-th dike 
    A = [[] for _ in range(5)]
    D = [] # departure of the n-th ship
    eventsQueue = [] # arrival times

    currTimeInHours = (currentSimTime + offset) / 60
    simulate_ships_arrival(eventsQueue, currTimeInHours)

    # Ta = heapq.heappop(eventsQueue) # time for the next arrival
    # T = [Ta + 1 for _ in range(5)] # time for the departure fron i-th dike

    while currentSimTime <= maxSimTime:
        nextEventTime, nextEvent = heapq.heappop(eventsQueue)
        currentSimTime = nextEventTime
        
        if nextEvent['type'] == 'Ship Arrival':
            pass

        if nextEvent['type'] == 'Entry Phase':
            pass
        if nextEvent['type'] == 'Transportation Phase':
            pass
        if nextEvent['type'] == 'Exit Phase':
            pass

    return [D[n] - A[0][n] for n in range(total)]
    

# Simulating a sea channel with 5 dikes since 8AM to 8PM
def __simulate_sea_channel():
    standingTime = []
    offset = 8 * 60 # offset time in minutes
    maxSimTime = 12 * 60 # 12 hours (from 8AM to 8PM) = 720 minutes

    currentSimTime = numArrives = numDepartures = 0
    total = 0 # total of ships
    
    dikes = [
        ([], []), # each list represents a line in the dike
        ([], []),
        ([], []),
        ([], []),
        ([], [])
    ]

    # arrival time of n-th ship to the i-th dike 
    A = [[] for _ in range(5)]
    D = [] # departure of the n-th ship
    pending = [] # arrival times

    currTimeInHours = (currentSimTime + offset) / 60
    simulate_ships_arrival(pending, currTimeInHours)

    Ta = heapq.heappop(pending) # time for the next arrival
    T = [Ta + 1 for _ in range(5)] # time for the departure fron i-th dike

    while currentSimTime <= maxSimTime:
        if Ta == min(Ta, *[T]) and Ta <= maxSimTime:
            currentSimTime = Ta
            numArrives += 1
            total += 1
            currTimeInHours = (currentSimTime + offset) / 60
            simulate_ships_arrival(pending)

            line1, line2 = dikes[0][0], dikes[0][1]
            if space_in_dike_line(line1) < 6 or space_in_dike_line(line2) < 6:
                pass

    return [D[n] - A[0][n] for n in range(total)]
    
if __name__ == '__main__':
    standingTime = simulate_sea_channel()
    print(sum(standingTime))