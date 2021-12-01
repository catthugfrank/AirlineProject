from __future__ import annotations
from datetime import date
import json
from streamlit.elements.button import ButtonMixin
from streamlit.type_util import Key
import json
from collections import OrderedDict
import pandas as pd
from bs4 import BeautifulSoup
import random
from abc import ABC, abstractmethod
from typing import Any, Optional
import random
from abc import ABC, abstractmethod
from typing import Any, Optional
import time as time2


with open('final_search_list2.json', 'r') as myfile: #import the search list used for flights
    pstate=myfile.read()
fstate = json.loads(pstate) 
myfile.close()
with open('final_flights_output.json', 'r') as myfile: #import flights found
    pstate=myfile.read()
flights = json.loads(pstate) 
myfile.close()

def cutdown(dict_list, search_item, search_type): #search function that cuts down flights
    faux_flights=dict_list
    cut_flight=[d for d in faux_flights if d[search_type] == search_item]
    return cut_flight

class Component(ABC): #abstract component in decorater

    @abstractmethod
    def operation(self) -> str:
        pass


class ConcreteComponent(Component): #concrete component in decorater
    def __init__(self, value) :
        self._value = value
    def operation(self):
        return self._value


class Decorator(ABC): #abstract decorator 

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> str:
        return self._component

    def operation(self) -> str:
        return self._component.operation()


class DateDecorator(Decorator): #decorates date
    def operation(self):
        return [self.component.operation()[0], cutdown(self.component.operation()[1],self.component.operation()[0][1] ,'date')] 

class ObDecorator(Decorator): #decorates outbound flight hub
    def operation(self):
        return [self.component.operation()[0], cutdown(self.component.operation()[1],self.component.operation()[0][2],'ob')]
    
class IbDecorator(Decorator): #decorates inbound flight hub

    def operation(self):
        print()
        return [self.component.operation()[0],cutdown(self.component.operation()[1],self.component.operation()[0][3],ClientHandler.convert(self.component.operation()[0][3]))]
    

class Handler(ABC): #abstract handler 

    def __init__(self, successor=None):
        self._successor = successor

    @abstractmethod
    def handle(self):
        pass


class FAA_Handler(Handler): #FAA code handler
    def handle(self, request):
        if any(request in d['FAA'] for d in fstate['data']):
            return 'ib'
        elif self._successor is not None:
            return self._successor.handle(request)


class Country_Handler(Handler): #Country Handler
    def handle(self, request: Any):
        if any(request in d['Country'] for d in fstate['data']):
            return 'Country'
        elif self._successor is not None:
            return self._successor.handle(request)
        
class City_Handler(Handler): #City Handler
    def handle(self, request: Any):
        if any(request in d['City'] for d in fstate['data']):
            return 'City'
        elif self._successor is not None:
            return self._successor.handle(request)


class Continent_Handler(Handler): #Continent Handler
    def handle(self, request: Any):
        if any(request in d['Continent'] for d in fstate['data']):
            return 'Continent'
        elif self._successor is not None:
            return self._successor.handle(request)
    
class ClientHandler(): #Client Class for Handler
    def convert(conv_input):
        FAA = FAA_Handler()
        Country = Country_Handler(FAA)
        City = City_Handler(Country)
        FOOT = Continent_Handler(City)
        result = FOOT.handle(conv_input)
        return result
    
def cheapest25(flight_dict): #reduces dictionary to cheapest 25 
    output = sorted(flight_dict, key=lambda z: z['price'])[:25] 
    return output

