import rich 
from rich.progress import track
import rich.traceback
import time
import random

rich.traceback.install()  # make errors pretty!

#1/0

rich.get_console().clear()
rich.get_console().rule("Hello, World!", style="bold magenta")
rich.get_console().print("Hello, [bold magenta]World[/bold magenta]!", style="green")


for i in track(range(100), description='Processing...'):
    time.sleep(random.random())