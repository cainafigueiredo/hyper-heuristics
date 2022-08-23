availableLowLevelHeuristics = {
    "greedyRandConst": {
        "description": "Greedy Randomized Construction",
        "callback": ""
    },
    "greedyConst": {
        "description": "Greedy Construction",
        "callback": ""
    },
    "randomConst": {
        "description": "Random Constructive",
        "callback": ""
    },
}

def printAvailableLowLevelHeuristics():
    print("Available Low Level Heuristics:")
    print("==============================")
    for key, values in availableLowLevelHeuristics.items():
        name = key
        description = values['description']
        print(f"id: {name}\ndescription:{description}\n")