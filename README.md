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

[ ] - better profiling
[ ] - level dictionary
[ ] - accuracy


## ⚙️ TO DO
Given the projects department's important and quite useful remarks, I decided to create a TO-DO list to properly know where this project is going. \
- [X] Profiling game's performance to identify bottlenecks
- [ ] Adjustable Enemy's bullets' accuracy for a more fair gameplay
- [ ] Level descriptions via dictionary per level that contains relevant information (enemy types, bullet patterns, timers, etc...)
