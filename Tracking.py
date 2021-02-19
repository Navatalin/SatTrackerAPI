from datetime import datetime, tzinfo
from skyfield.api import load
from skyfield.positionlib import Geocentric
import pytz
import numpy as np
import json

class Tracking:
    def __init__(self) -> None:
        self.stations_url = 'https://celestrak.com/NORAD/elements/starlink.txt'
        self.satellites = load.tle_file(self.stations_url)
    
    def get_pos(self):
        positions = []
        for sat in self.satellites:
            ts = load.timescale()
            gpo = sat.at(ts.now())
            velocity = gpo.velocity.km_per_s
            position = [sat.name, gpo.position.km[0], gpo.position.km[1],gpo.position.km[2], velocity[0], velocity[1],velocity[2]]
            
            positions.append(position)
        return positions
