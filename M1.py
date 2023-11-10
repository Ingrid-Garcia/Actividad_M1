from typing import Any
from mesa import Agent, Model


# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np


def results(model):
    agent_steps = [agent.steps for agent in model.schedule.agents]
    x = (agent_steps)
    return x

class agenteLimpieza(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.position = None
        self.state = None
        self.steps = 0

    def move(self):
        possible = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        newPos = self.random.choice(possible)
        self.model.grid.move_agent(self, newPos)
        self.steps += 1

    def step(self):
        x, y = self.pos
        value = self.model.grid.get_cell_list_contents((x,y))
        if len(value) > 1:
            for ag in value:
                if ag != self:  # Verificar si el agente actual no es el agente que estamos revisando
                    if ag.state == 0:
                        ag.state = 2
                        self.model.clean += 1
                        self.move()
        self.move()

class LimpiezaModelo(Model):
    def __init__(self, width, height, N, percentage, t):
        self.num_agents = N
        self.total = width * height
        self.quantityDirty = int((percentage * width * height)/ 100)
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.maxT = t
        self.count = 0
        self.clean = (width * height) - self.quantityDirty
        self.running = True #Para la visualizacion usando navegador

        for i in range(self.quantityDirty):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            newPos = (x,y)
            while self.grid.is_cell_empty(newPos) == False:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                newPos = (x,y)
            m = agenteLimpieza(i, self)
            m.position = newPos
            m.state = 0
            self.grid.place_agent(m, newPos)
            
        for i in range (self.quantityDirty, (self.num_agents + self.quantityDirty),1):
            a = agenteLimpieza(i, self)
            a.position = (0,0)
            a.state = 1
            self.grid.place_agent(a, (0, 0))
            self.schedule.add(a)
        
    def step(self):
        if self.count < self.maxT and (self.clean != self.total):
            self.schedule.step()
            self.count += 1
        else:
            self.running = False
            print ("Cuenta con " + str(self.num_agents) 
                   + " robots limpiadores, termino con un tiempo de " + str(self.count) 
                   + " el porcentaje de celdas fue de " + str(round(((self.clean * 100)/ self.total), 2)) 
                   + "% y los movimiento realizados por cada agente fueron " + str(results(self)) 
                   + " teniendo un total de " + str(sum(results(self))) + " movimientos en total" )
            # print(self.count)
            # print((self.clean * 100)/ self.total)
            # print(results(self))
            
