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


LEVEL_1 = [
    {
        "time": 1.0,
        "type": "red",
        "pos": (400, 50),
        "script": [
            "move 400 300 20",
            # "pattern aim 0.8",
            "wait 2.0",
            "move -50 500 1",
            "die",
        ],
    }
]
