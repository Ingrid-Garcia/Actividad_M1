import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from M1 import *

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }
    if agent.state == 0: 
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0

    if agent.state == 2: 
        portrayal["Color"] = "white"
        portrayal["Layer"] = 0
    
    return portrayal
    
ancho = 30
alto = 30
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(LimpiezaModelo, [grid], "Modelo Limpieza", 
                       {"width": ancho, "height": alto, "N":90, "percentage": 10, "t": 500})
server.port = 8521
server.launch()

