from dataclasses import dataclass
import numpy as np
import re

from copy import deepcopy
from helpers import Agent, Llm

@dataclass
class Environment:
    location: np.ndarray
    llm: Llm
    description: str

    def update_loc(self, action):
        prompt = f"The agent is at {self.location} and has taken action {action}; what is their new location? Please respond with a tuple formatted as `(x,y,z)`."
        raw = self.llm.prompt(prompt)
        counter = 0
        try:
            loc = re.findall(r'\d+', raw)
            new_loc = np.array(loc)
            self.location = new_loc
        except:
            print("Invalid response; please try again.")
            counter += 1
            if counter < 3:
                self.update_loc(action)
            else:
                print("Too many invalid responses; exiting.")
                exit()

    def update_description(self, action):
        prompt = f"The agent is at {self.location} and has taken action {action}; what is the new description?"
        raw = self.llm.prompt(prompt)
        counter = 0
        try:
            self.description = raw
        except:
            print("Invalid response; please try again.")
            counter += 1
            if counter < 3:
                self.update_description(action)
            else:
                print("Too many invalid responses; exiting.")
                exit()
    
    def update(self, action):
        self.update_loc(action)
        self.update_description(action)
        
    def dump(self):
        return "You are at " + str(tuple(self.location)) + " and you observe " + self.description

@dataclass
class State:
    agent: Agent
    environment: Environment

    def transition(self):
        #agent observes environment
        self.agent.observe(self.environment.description)
        
        #check to see if the agent cogitates
        rng = np.random.randint(1,21):
        if rng < 17:
            self.agent.cogitate()

        #agent acts
        action = self.agent.prompt(f"{self.environment.dump()}\n what do you do?")
        # update the environment based on the action
        self.environment.update(action)

@dataclass
class trajectory:
    states:list[State] = None

    def intialize(self, agent, environment):
        self.states = [State(agent, environment)]

    def iterate(self, agent, environment):
        new_state = deepcopy(self.states[-1])
        new_state.transition()
        self.states.append(new_state)

#example usage
# declare an environment
myEnv = Environment(np.array([0,0,0]), Llm(), "You are in a small dark room with a table and a chair; there is a doorway into a dimly lit corridor in fron of you and a ladder in the corner behind you. The corridor leads back to the harem. It is too dark to see how far down the ladder goes.")
#declare an agent
myAgent = Agent("Alice", Llm(),"You are dressed in tight fitting leather armor; you are carrying a short sword and a buckler. You are adept swashbuckler who was captured in your sleep and taken to foreign land to be kept as a concubine. Through your rogue skills you have escaped and secured some basic gear but you have not escaped the castle. You also have paper and ink; you have been maintaining a three dimensional map; your current location is (0,0,0).", "As an escaped concubine adenturer, you are on a mission to advance your skills, gather equipment, and recruit allies in order to overthrow the patriarch who captured you.")
#declare a state
myState = State(myAgent, myEnv)
#declare a trajectory
myTrajectory = trajectory()
#initialize the trajectory
myTrajectory.intialize(myAgent, myEnv)

turns = 10
#iterate the trajectory
for i in range(turns):
    myTrajectory.iterate(myAgent, myEnv)
