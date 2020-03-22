from allpairspy import AllPairs

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
# If client parameters are changed use this script to generate pairwise coverage
print("PAIRWISE:")
for i, pairs in enumerate(AllPairs(parameters)):
    # print("{:2d}: {}".format(i, pairs))
    print(f"{pairs}")
