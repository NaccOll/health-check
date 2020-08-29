import time
from app.properties import HealthProperties
from app.core import HealthActor
def run():
    actor = HealthActor(HealthProperties())
    actor.start()

    def task():
        actor.send(1)
    while True:
        task()
        time.sleep(1)