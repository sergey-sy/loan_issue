from allpairspy import AllPairs


def get_pairwise_object():
    """
        return [
            [150, 'F', 'employee', 1000, 1, 10, 20, 'mortgage'],
            [150, 'M', 'businessman', 1000, 0, 0.1, 20, 'business'],
            [1, 'F', 'businessman', 0, 2, 10, 20, 'car'],
            [150, 'M', 'employee', 0, 1, 0.1, 1, 'car'],
            [1, 'F', 'passive', 1000, 0, 10, 20, 'consumer'],
            [150, 'M', 'passive', 0, 1, 10, 1, 'business'],
            [150, 'F', 'businessman', 1000, 1, 10, 1, 'mortgage'],
            [1, 'F', 'businessman', 0, 1, 0.1, 1, 'consumer'],
            [150, 'F', 'passive', 0, 1, 10, 20, 'consumer'],
            [150, 'F', 'employee', 0, 2, 10, 1, 'mortgage'],
            [150, 'F', 'employee', 0, 0, 10, 1, 'consumer'],
            [150, 'F', 'passive', 0, 2, 10, 1, 'business'],
            [150, 'F', 'passive', 0, 0, 10, 1, 'car'],
            [150, 'F', 'businessman', 0, -2, 10, 1, 'consumer'],
            [150, 'F', 'unemployed', 0, 1, 10, 1, 'car'],
            [1, 'M', 'passive', 0, -2, 0.1, 1, 'mortgage'],
            [1, 'F', 'unemployed', 0, 1, 10, 1, 'business'],
            [150, 'M', 'unemployed', 1000, 2, 0.1, 1, 'consumer'],
            [1, 'F', 'employee', 1000, -2, 10, 20, 'business'],
            [150, 'F', 'unemployed', 0, 0, 0.1, 1, 'mortgage'],
            [150, 'F', 'unemployed', 1000, -2, 10, 20, 'car']
        ]
    """
    parameters = [
        [1, 150],
        ["M", "F"],
        ["passive", "employee", "businessman", "unemployed"],
        [0, 1000],
        [-2, 1, 0, 1, 2],
        [0.1, 10],
        [1, 20],
        ["mortgage", "business", "car", "consumer"]
    ]

    return AllPairs(parameters)



if __name__ == '__main__':
    # If client parameters are changed use this script to generate pairwise coverage
    print("PAIRWISE:")
    for pairs in get_pairwise_object():
        print(f"{pairs}")