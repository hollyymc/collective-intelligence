from dataclasses import dataclass
from vi import Agent, Config, Simulation
from pygame.math import Vector2
import random
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid Tkinter issues
import matplotlib.pyplot as plt
import pandas as pd

@dataclass
class LotkaVolterraConfig(Config):
    fox_death_prob: float = 0.01
    fox_hunt_radius: float = 10
    movement_speed: float = 2.0
    rabbit_reproduction_prob: float = 0.005
    fox_reproduction_prob: float = 0.5  
    fox_start_energy: int = 100
    fox_energy_gain_on_eat: int = 100
    mating_radius: float = 30.0  # Add mating radius
    max_age: int = 200  # Maximum age before natural death
    # Disable metrics to avoid polars error
    enable_logging: bool = False
    enable_recording: bool = False
    duration: int = 15000  # Simulation duration in steps


class PopulationTracker:
    def __init__(self):
        self.data = []
        self.step = 0

    def record(self, simulation):
        """Record current population counts"""
        rabbit_count = sum(1 for agent in simulation._agents if hasattr(agent, 'species') and agent.species == "rabbit")
        fox_count = sum(1 for agent in simulation._agents if hasattr(agent, 'species') and agent.species == "fox")

        # Calculate average ages
        rabbit_ages = [agent.age for agent in simulation._agents if hasattr(agent, 'species') and agent.species == "rabbit" and hasattr(agent, 'age')]
        fox_ages = [agent.age for agent in simulation._agents if hasattr(agent, 'species') and agent.species == "fox" and hasattr(agent, 'age')]
        
        avg_rabbit_age = sum(rabbit_ages) / len(rabbit_ages) if rabbit_ages else 0
        avg_fox_age = sum(fox_ages) / len(fox_ages) if fox_ages else 0

        self.data.append({
            'step': self.step,
            'rabbits': rabbit_count,
            'foxes': fox_count,
            'avg_rabbit_age': avg_rabbit_age,
            'avg_fox_age': avg_fox_age
        })
        self.step += 1

        # Print every 20 steps to monitor progress
        if self.step % 20 == 0:
            print(f"Step {self.step}: Rabbits={rabbit_count} (avg age: {avg_rabbit_age:.1f}), Foxes={fox_count} (avg age: {avg_fox_age:.1f})")

        # Check if population is extinct
        if rabbit_count == 0 and fox_count == 0:
            print("Both populations extinct!")
            return True
        elif rabbit_count == 0:
            print("All rabbits extinct!")
            return True
        elif fox_count == 0:
            print("All foxes extinct!")
            return True
        return False

    def plot(self):
        """Create simple population dynamics plot"""
        if not self.data:
            print("No data to plot!")
            return

        df = pd.DataFrame(self.data)
        print(f"Plotting {len(df)} data points...")

        # Create single plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['rabbits'], label='Rabbits', color='blue', linewidth=2)
        plt.plot(df['step'], df['foxes'], label='Foxes', color='red', linewidth=2)
        plt.xlabel('Time Steps')
        plt.ylabel('Population Count')
        plt.title('Lotka-Volterra Population Dynamics with Sexual Reproduction & Aging')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('population_dynamics_lifecycle.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'population_dynamics_lifecycle.png'")
        plt.close()

        # Print basic statistics
        print(f"\n=== Population Statistics ===")
        print(f"Duration: {len(df)} time steps")
        print(f"Rabbits - Max: {df['rabbits'].max()}, Min: {df['rabbits'].min()}, Final: {df['rabbits'].iloc[-1]}")
        print(f"Foxes - Max: {df['foxes'].max()}, Min: {df['foxes'].min()}, Final: {df['foxes'].iloc[-1]}")


class Rabbit(Agent):
    def __init__(self, images, simulation, pos=None, move=None):
        super().__init__(images, simulation, pos, move)
        self.species = "rabbit"
        self.sex = random.choice(["male", "female"])
        self.age = 0  # Add age tracking

    def starting(self):
        self.species = "rabbit"
        self.sex = random.choice(["male", "female"])
        self.age = 0
        angle = random.uniform(0, 360)
        self.move = Vector2(1, 0).rotate(angle) * self.config.movement_speed

    def change_position(self):
        # Age the rabbit much slower
        if random.random() < 0.1:  # Age every 10 ticks instead of 2
            self.age += 1

        # Much lower age-based death probability
        age_death_prob = min(0.001, self.age / self.config.max_age * 0.01)  # Reduced from 0.01 and 0.05
        if random.random() < age_death_prob:
            self.kill()
            return

        # Age-based movement speed (less penalty for aging)
        age_factor = max(0.2, 1 - (self.age / self.config.max_age) * 0.8)  # 20% to 100% efficiency
        current_speed = self.config.movement_speed * age_factor

        # Move randomly
        if random.random() < 0.1:
            self.move = self.move.rotate(random.uniform(-30, 30))

        # Update movement with age-adjusted speed
        self.move = self.move.normalize() * current_speed
        self.pos += self.move
        self.there_is_no_escape()

        # Age-based reproduction probability (more forgiving age ranges)
        if self.age < 10:  # Too young 
            reproduction_prob = 0
        elif self.age > 80:  # Too old
            reproduction_prob = self.config.rabbit_reproduction_prob * 0.5
        else:  # Prime reproductive age
            reproduction_prob = self.config.rabbit_reproduction_prob * 1.2

        # Sexual reproduction - look for opposite sex mate
        if random.random() < reproduction_prob:
            neighbours = list(self.in_proximity_accuracy())
            for agent, distance in neighbours:
                if (hasattr(agent, 'species') and agent.species == "rabbit" and 
                    hasattr(agent, 'sex') and agent.sex != self.sex and
                    distance <= self.config.mating_radius):
                    # Found a mate! Reproduce
                    print(f"{self.species} (age {self.age}) found a mate and reproduced!")
                    offspring = self.reproduce()
                    if offspring:
                        offspring.age = 0  # Offspring starts at age 0
                    break

class Fox(Agent):
    def __init__(self, images, simulation, pos=None, move=None):
        super().__init__(images, simulation, pos, move)
        self.species = "fox"
        self.sex = random.choice(["male", "female"])
        self.energy = self.config.fox_start_energy
        self.age = 0  # Add age tracking
        self.has_hunted = False  # Persistent hunting status

    def starting(self):
        self.species = "fox"
        self.sex = random.choice(["male", "female"])
        self.energy = self.config.fox_start_energy
        self.age = 0
        self.has_hunted = False  # Initialize hunting status
        angle = random.uniform(0, 360)
        self.move = Vector2(1, 0).rotate(angle) * self.config.movement_speed

    def change_position(self):
        # Age the fox much slower
        if random.random() < 0.1:  # Age every 10 ticks instead of 2
            self.age += 1

        # Much lower age-based death probability
        age_death_prob = min(0.002, self.age / self.config.max_age * 0.02)  # Reduced from 0.02 and 0.08
        base_death_prob = self.config.fox_death_prob + age_death_prob

        if random.random() < base_death_prob:
            self.kill()
            return

        # Age-based movement speed and hunting ability (less penalty)
        age_factor = max(0.2, 1 - (self.age / self.config.max_age) * 0.8)  # 20% to 100% efficiency
        current_speed = self.config.movement_speed * age_factor
        current_hunt_radius = self.config.fox_hunt_radius * age_factor

        # Hunt rabbits
        neighbours = list(self.in_proximity_accuracy())

        for agent, distance in neighbours:
            if hasattr(agent, 'species') and agent.species == "rabbit":
                if distance <= current_hunt_radius:
                    agent.kill()
                    print(f"{self.species} (age {self.age}) hunted a rabbit!")
                    self.energy += self.config.fox_energy_gain_on_eat
                    self.has_hunted = True  # Set persistent hunting status
                    break

        # Age-based reproduction probability 
        if self.age < 10:  # Too young
            reproduction_prob = 0
        elif self.age > 100:  # Too old
            reproduction_prob = self.config.fox_reproduction_prob * 0.5
        else:  # Prime reproductive age
            reproduction_prob = self.config.fox_reproduction_prob

        # Sexual reproduction - now uses persistent has_hunted status
        if self.has_hunted == True:  # fox has hunted at least once in their lifetime
            if random.random() < reproduction_prob:
                for agent, distance in neighbours:
                    if (hasattr(agent, 'species') and agent.species == "fox" and 
                        hasattr(agent, 'sex') and agent.sex != self.sex and
                        distance <= self.config.mating_radius):
                        # Found a mate! Reproduce
                        offspring = self.reproduce()
                        if offspring:
                            offspring.age = 0  # Offspring starts at age 0
                            offspring.has_hunted = False  # Offspring hasn't hunted yet
                        print(f"{self.species} (age {self.age}) found a mate and reproduced!")
                        break

        # Random movement with age-adjusted speed
        if random.random() < 0.15:
            self.move = self.move.rotate(random.uniform(-45, 45))

        self.move = self.move.normalize() * current_speed
        self.pos += self.move
        self.there_is_no_escape()

        # Energy loss and starvation
        if self.config.fox_start_energy > 0:
            self.energy -= 1
            if self.energy <= 0:
                self.kill()


class LotkaVolterraSimulation(Simulation):
    def __init__(self, config):
        super().__init__(config)
        self.tracker = PopulationTracker()
        self.current_step = 0
        self.simulation_ended = False

    def tick(self):
        # Record population every 5 steps
        if self.current_step % 5 == 0:
            extinct = self.tracker.record(self)
            if extinct and not self.simulation_ended:
                print("Population extinct! Generating plot...")
                self.tracker.plot()
                self.simulation_ended = True

        # Call parent tick but skip metrics if they cause issues
        try:
            super().tick()
        except Exception as e:
            if "polars" in str(e).lower() or "dataframe" in str(e).lower():
                # Skip metrics-related errors and continue simulation
                pass
            else:
                raise e
            
        self.current_step += 1

    def end(self):
        super().end()
        if not self.simulation_ended:
            print("\nSimulation ended normally. Generating plot...")
            self.tracker.plot()


# Run simulation with sexual reproduction and aging
if __name__ == "__main__":
    print("Starting Lotka-Volterra simulations with sexual reproduction and aging...")

    all_stats = []

    for run in range(1, 26):  # run 25 simulations
        print(f"\n=== Starting Simulation {run} ===")

        config = LotkaVolterraConfig(
            movement_speed=2.0,
            fox_death_prob=0.0005,  # Reduced death probability
            fox_hunt_radius=50,
            rabbit_reproduction_prob=0.01,  # Reduced
            fox_reproduction_prob=0.05,    # Reduced
            mating_radius=40.0,  # Larger mating radius
            fox_start_energy=0,
            fox_energy_gain_on_eat=0,
            max_age=200,
            enable_logging=False,  # Disable metrics
            enable_recording=False
        )

        simulation = LotkaVolterraSimulation(config)
        simulation.batch_spawn_agents(100, Rabbit, images=["images/rabbit.png"])
        simulation.batch_spawn_agents(20, Fox, images=["images/fox.png"])
        simulation.run()

        df = pd.DataFrame(simulation.tracker.data)
        if df.empty:
            print(f"Run {run}: No data collected, skipping.")
            continue

        stats = {
            "run": run,
            "steps_survived": len(df),
            "final_rabbits": df['rabbits'].iloc[-1],
            "final_foxes": df['foxes'].iloc[-1],
            "max_rabbits": df['rabbits'].max(),
            "max_foxes": df['foxes'].max(),
            "min_rabbits": df['rabbits'].min(),
            "min_foxes": df['foxes'].min(),
        }
        all_stats.append(stats)

    stats_df = pd.DataFrame(all_stats)
    print("\n=== Summary Statistics ===")
    print(stats_df.describe())
    stats_df.to_csv("life_cycle_results.csv", index=False)
    print("Saved summary to 'life_cycle_results.csv'")
