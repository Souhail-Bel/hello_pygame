from pyinstrument import Profiler

from hello_pygame.main import main

def exec_profiler():
    prof = Profiler()
    prof.start()

    try:
        main()
    except SystemExit:
        pass

    prof.stop()
    prof.open_in_browser()
