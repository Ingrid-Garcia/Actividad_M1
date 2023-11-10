from typing import Any
from mesa import Agent, Model


from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np

#Regresa la cantidad de movimientos totales de cada agente que se han realizado dentro del tiempo especificado
def results(model):
    agent_steps = [agent.steps for agent in model.schedule.agents]
    x = (agent_steps)
    return x

#Implementación del agente limpieza, el cual necesita el modelo y el identificador único de estos
#Se debe de especificar su estado para conocer si es de tipo limpiador (1), está sucio(0) o ya ha sido limpiado(2)
class AgenteLimpieza(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.position = None
        self.state = None
        self.steps = 0

    #Se asegura de que se mueva a una posición dentro de los parametros establecidos
    def move(self):
        possible = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        
        newPos = self.random.choice(possible)
        self.model.grid.move_agent(self, newPos)
        self.steps += 1

    #Revisa que el moviemiento que realizo implica una limpieza o si no hace nada, además de que cambia el 
    #conteo de las celdas limpias
    def step(self):
        x, y = self.pos
        value = self.model.grid.get_cell_list_contents((x,y))
        if len(value) > 1:
            for ag in value:
                if ag != self: 
                    if ag.state == 0:
                        ag.state = 2
                        self.model.clean += 1
                        self.move()
        self.move()

#Se define el modelo a utilizar, se necesita el alto, ancho, cantidad de agentes, porcentaje de celdas sucias y el tiempo máximo
class LimpiezaModelo(Model):
    def __init__(self, width, height, N, percentage, t):
        self.num_agents = N
        self.total = width * height
        self.quantityDirty = int((percentage * width * height)/ 100)
        self.grid = MultiGrid(width, height, False) #Para que al princpio los agentes limpiadores puedan empezar en un mismo punto sin conflictos
        self.schedule = SimultaneousActivation(self)
        self.maxT = t
        self.count = 0
        self.clean = (width * height) - self.quantityDirty
        self.running = True #Para la visualizacion usando navegador

        for i in range(self.quantityDirty):#Se asegura de colocar la cantidad correcta de celdas sucias en posiciones aleatorias
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            newPos = (x,y)
            while self.grid.is_cell_empty(newPos) == False:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                newPos = (x,y)
            m = AgenteLimpieza(i, self)
            m.position = newPos
            m.state = 0
            self.grid.place_agent(m, newPos)

        #Crea los agentes limpiadores especificados y los coloca en la posición 0,0 que es en la esquina inferior izquierda 
        for i in range (self.quantityDirty, (self.num_agents + self.quantityDirty),1):
            
            a = AgenteLimpieza(i, self)
            a.position = (0,0)
            a.state = 1
            self.grid.place_agent(a, (0, 0))
            self.schedule.add(a)
    #Se asegura de que el modelo y agentes se sigan moviendo y revisa que la simulación no ha sobrepasado el tiempo especificado
    # Siempre hace dos de más   
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
            
