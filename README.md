# Space Shooters... Touhou'd
Much like the name suggests, this is a game that replicates space shooters... but more like Touhou's bullet hell :P \
My hello_pygame.

All assets here were drawn by me via LibreSprite (except for the sky, that's a real sky that's been palletized).


## 🚀 How do I run it?
First, install [`uv`](https://github.com/astral-sh/uv) which is an extremely fast and easy to use package and project manager. \
You can do so either from [PyPI](https://pypi.org/project/uv/):
```bash
# Using pip
pip install uv
# Using pipx
pipx install uv
```
or from AUR if you're using Arch, via `yay -S uv`. \
<i>or just follow the installation procedures mentioned [here](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).</i>


Clone the repository and navigate to the folder.

```bash
git clone https://github.com/Souhail-Bel/hello_pygame
cd hello_pygame
```

Next, we get the virtual environment set up by running:

```bash
uv sync
```

Then, whenever you want to run it, simply type:

```bash
uv run play
```

You can also profile the game to identify performance bottlenecks:
```bash
uv run profile
```
Keep in mind that **Clock.tick** makes the CPU wait.


## 💻 Creating your own level
It it incredibly simple to make your own level. \
Each level is described in a list of dictionaries. \
Each dictionary is considered an event. \
Each event is composed of:
* **time:** a float that describes **WHEN** does the enemy appear
* **type:** a string that describes **WHAT** the enemy is ("red", "green", "boss", by default blue)
* **pos:** a tuple that describes **WHERE** the enemy initially is (X, Y)
* **script:** a list of instructions describing **HOW** the enemy behaves

Enemy scripting is handled by a basic interpreter that can take any of the following instructions:
### Moving the enemy
```
move X Y SPEED
```
Move the enemy to an X, Y coordinate (note that the origin is the top left corner) with speed SPEED
### Waiting
```
wait SECONDS
```
Make the enemy wait SECONDS seconds.
### Dying
```
die
```
die.
### Attacking
```
pattern NAME PARAMS..
```
Make the enemy attack via a given pattern with some parameters. \
If the pattern name is unknown, it switches to not attacking. \
The patterns are, with their respective arguments and eventually default values:
* **StreamPattern:** "stream" {}
* **AimPattern:** "aim" {accuracy (0..1)}
* **CirclePattern:** "circle" {count}
* **ConvergePattern:** "converge" {rows=10, spread=80, ang_vel_0=30 (0..TAU)}
* **RainPattern:** "rain" {row_count=12, rain_width=750}
* **FishingPattern:** "fish" {radius=100, count=16}
* **BlossomPattern:** "blossom" {radius=100, count=32}
* **CircleConvergePattern:** "cc" {radius=100, count=32}


Example Enemy script:
```
move 400 300 20
pattern aim 0.8
wait 2.0
pattern none
wait 1.0
move -50 500 1
die
```

This moves the enemy to (400, 300) in speed 20. \
Make the enemy use the Aim pattern with accuracy 80% for 2 seconds. \
Stop shooting, wait for 1 second. \
Move the enemy to the bottom left side of the screen. \
Once it reaches there, kill it.


## ⚙️ TO DO
Given the projects department's important and quite useful remarks, I decided to create a TO-DO list to properly know where this project is going.
- [X] Profiling game's performance to identify bottlenecks
- [X] Adjustable Enemy's bullets' accuracy for a more fair gameplay
- [X] Make the bullets smarter, by adding acceleration, friction, angular velocity, etc...
- [X] Make more interesting bullet patterns
- [X] Level descriptions via dictionary per level that contains relevant information (enemy types, bullet patterns, timers, etc...)
- [ ] Create a full-fledged level
- [ ] Better documentation for patterns with pictures
