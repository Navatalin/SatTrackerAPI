from datetime import datetime, tzinfo
from skyfield.api import load
from skyfield.positionlib import Geocentric
import time
import pytz
import numpy as np
import json
import asyncio
from MQPublisher import MQPublisher

class Tracking:
    def __init__(self) -> None:
        self.stations_url = 'https://celestrak.com/NORAD/elements/starlink.txt'
        self.satellites = load.tle_file(self.stations_url)
        self.rabbit_mq_url = 'amqp://Worker:workerPassword@localhost:5672/%2F?connection_attempts=3&heartbeat=3600'


    def satelite_names_list(self):
        sat_names = []
        for item in self.satellites:
            sat_names.append(item.name)
        return sat_names

    def chunks(self,l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

    def send_to_queue(self, work):
        mq = MQPublisher(self.rabbit_mq_url)
        mq.connect()
        for chunk in work:
            mq.publish_message(chunk)
        mq.disconnect()
 

    def get_pos(self):
        positions = []
        #for sat in self.satellites:
         #   ts = load.timescale()
         #   gpo = sat.at(ts.now())
         #   velocity = gpo.velocity.km_per_s
         #   position = [sat.name, gpo.position.km[0], gpo.position.km[1],gpo.position.km[2], velocity[0], velocity[1],velocity[2]]
            
         #   positions.append(position)
        sat_names = self.satelite_names_list()
        work = list(self.chunks(sat_names, 10))
        self.send_to_queue(work)

        return positions