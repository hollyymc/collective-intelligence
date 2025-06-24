from dataclasses import dataclass
from vi import Agent, Config, Simulation
from pygame.math import Vector2
import random

@dataclass
class LotkaVolterraConfig(Config):
    fox_death_prob: float = 0.01
    fox_hunt_radius: float = 30
    movement_speed: float = 2.0

class Rabbit(Agent):
    def starting(self):
        self.species = "rabbit"
        angle = random.uniform(0, 360)
        self.move = Vector2(1, 0).rotate(angle) * self.config.movement_speed
        
    def change_position(self):
        # Move randomly
        if random.random() < 0.1:
            self.move = self.move.rotate(random.uniform(-30, 30))
        
        self.pos += self.move
        self.there_is_no_escape()

class Fox(Agent):
    def starting(self):
        self.species = "fox"
        self.energy = 100
        angle = random.uniform(0, 360)
        self.move = Vector2(1, 0).rotate(angle) * self.config.movement_speed
        
    def change_position(self):
        # Initialize energy if it doesn't exist (safety check)
        if not hasattr(self, 'energy'):
            self.energy = 100
            
        # Hunt rabbits
        for agent, distance in self.in_proximity_accuracy():
            if hasattr(agent, 'species') and agent.species == "rabbit" and distance < self.config.fox_hunt_radius:
                agent.kill()
                self.energy += 30
                break
        
        # Move randomly
        if random.random() < 0.15:
            self.move = self.move.rotate(random.uniform(-45, 45))
        
        self.pos += self.move
        self.there_is_no_escape()
        
        # Lose energy and die
        self.energy -= 1
        if self.energy <= 0 or random.random() < self.config.fox_death_prob:
            self.kill()

# Run simulation - simple version without metrics collection
if __name__ == "__main__":
    config = LotkaVolterraConfig(
        movement_speed=2.0,
        radius=30,
        fox_death_prob=0.01,
        fox_hunt_radius=30,
        duration=1000
    )
    
    sim = Simulation(config)
    
    print("Starting Lotka-Volterra simulation...")
    print("Spawning 50 rabbits and 20 foxes...")
    
    # Spawn agents
    sim.batch_spawn_agents(50, Rabbit, images=["images/rabbit.png"])
    sim.batch_spawn_agents(20, Fox, images=["images/fox.png"])
    
    print(f"Initial agent count: {len(sim._all.sprites())}")
    
    # Run simulation
    sim.run()
    
    print("Simulation completed!")
    print(f"Final agent count: {len(sim._all.sprites())}")
    
    # Count remaining agents by type
    rabbits = [agent for agent in sim._all.sprites() if hasattr(agent, 'species') and agent.species == "rabbit"]
    foxes = [agent for agent in sim._all.sprites() if hasattr(agent, 'species') and agent.species == "fox"]
    
    print(f"Final Statistics:")
    print(f"Rabbits remaining: {len(rabbits)}")
    print(f"Foxes remaining: {len(foxes)}")
    
    if foxes:
        avg_energy = sum(fox.energy for fox in foxes if hasattr(fox, 'energy')) / len(foxes)
        print(f"Average fox energy: {avg_energy:.1f}")