# Format:
#     time: when does the enemy appear
#     type: red/green/blue/boss
#     pos : where does it spawn
#     script [instructions]:
#         move X Y SPEED
#         pattern PATTERN ARGS..
#         wait SECONDS
#         die

# for now, the events should be ordered by time!

from hello_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH

# "time": 1.0,
# "type": "red",
# "pos": (400, 50),
# "script": [
#   "move 100 100 100",
# ],

LEVEL_1 = [
    {
        "time": 1.0,
        "type": "blue",
        "pos": (400, 0),
        "script": [
            "move 400 100 120",
            "pattern circle 8",
            "wait 3.0",
            "move 400 650 200",
            "die",
        ],
    },
    {
        "time": 8.0,
        "type": "red",
        "pos": (50, 0),
        "script": [
            "move 300 200 200",
            "pattern aim 0.8",
            "wait 2.0",
            "pattern none",
            "move -50 500 100",
            "die",
        ],
    },
    {
        "time": 8.0,
        "type": "red",
        "pos": (850, 0),
        "script": [
            "move 500 200 200",
            "pattern aim 0.8",
            "wait 2.0",
            "pattern none",
            "move 850 500 100",
            "die",
        ],
    },
    {
        "time": 12.0,
        "type": "green",
        "pos": (400, 0),
        "script": [
            "move 400 100 200",
            "pattern converge 4 180 50",
            "wait 2.0",
            "pattern none",
            "move 400 -50 100",
            "die",
        ],
    },
    {
        "time": 12.0,
        "type": "green",
        "pos": (400, 0),
        "script": [
            "move 400 100 200",
            "pattern converge 6 120 70",
            "wait 2.0",
            "pattern none",
            "move 400 -50 100",
            "die",
        ],
    },
    {
        "time": 16.0,
        "type": "blue",
        "pos": (800, 0),
        "script": [
            "move 780 20 500",
            "pattern stream",
            "move 400 300 200",
            "move -50 580 200",
            "die",
        ],
    },
    {
        "time": 17.5,
        "type": "blue",
        "pos": (0, 0),
        "script": [
            "move 20 20 500",
            "pattern stream",
            "move 400 300 200",
            "move 850 580 200",
            "die",
        ],
    },
    {
        "time": 19.0,
        "type": "blue",
        "pos": (800, 0),
        "script": [
            "move 780 20 500",
            "pattern stream",
            "move 400 300 200",
            "move -50 580 200",
            "die",
        ],
    },
    {
        "time": 20.5,
        "type": "blue",
        "pos": (0, 0),
        "script": [
            "move 20 20 500",
            "pattern stream",
            "move 400 300 200",
            "move 850 580 200",
            "die",
        ],
    },
    {
        "time": 22.0,
        "type": "blue",
        "pos": (800, 0),
        "script": [
            "move 780 20 500",
            "pattern stream",
            "move 400 300 200",
            "move -50 580 200",
            "die",
        ],
    },
    {
        "time": 23.5,
        "type": "blue",
        "pos": (0, 0),
        "script": [
            "move 20 20 500",
            "pattern stream",
            "move 400 300 200",
            "move 850 580 200",
            "die",
        ],
    },
    {
        "time": 25,
        "type": "green",
        "pos": (400, 0),
        "script": [
            "move 400 50 100",
            "pattern rain",
            "wait 4.0",
            "pattern none",
            "move 400 650 200",
            "die",
        ],
    }, # 6
    {
        "time": 29,
        "type": "green",
        "pos": (400, 0),
        "script": [
            "move 400 50 100",
            "pattern fish 100 8",
            "wait 4.0",
            "pattern fish 100 16",
            "wait 4.0",
            "pattern none",
            "move 400 650 200",
            "die",
        ],
    },
    {
        "time": 30,
        "type": "red",
        "pos": (200, 0),
        "script": [
            "move 200 50 100",
            "pattern aim 0.75",
            "wait 4.0",
            "move 400 650 200",
            "die",
        ],
    },
    {
        "time": 30,
        "type": "red",
        "pos": (600, 0),
        "script": [
            "move 600 50 100",
            "pattern aim 0.75",
            "wait 4.0",
            "move 400 650 200",
            "die",
        ],
    }, # boss is at 32
    {
        "time": 32,
        "type": "boss",
        "pos": (400, 0),
        "script": [
            "move 200 100 100",
            "pattern aim 0.75",
            "move 600 100 60",
            "wait 1.0",
            "pattern none",
            "move 400 120 200",
            "pattern blossom 100 16",
            "wait 2.5",
            "pattern blossom 100 32",
            "wait 2.0",
            "pattern cc",
            "wait 5.0",
            "die",
        ],
    },
]
