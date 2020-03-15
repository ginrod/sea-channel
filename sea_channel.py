import numpy, math

# EYE: t most be passed sumed with offset
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

# Simulating a sea channel with 5 dikes since 8AM to 8PM
def simulate_sea_channel():
    standingTime = []
    offset = 8 # offset time

    return standingTime
    
if __name__ == '__main__':
    standingTime = simulate_sea_channel()
    print(sum(standingTime))