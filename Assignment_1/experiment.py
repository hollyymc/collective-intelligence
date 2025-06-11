# stage2.py
import argparse
from vi import Simulation
from aggregation import Cockroach
from aggregation import make_base_config

def run_experiment(site_images):
    cfg = make_base_config()
    sim = Simulation(cfg)

    w, h   = cfg.window.as_tuple()
    cx, cy = w // 2, h // 2

    sim.spawn_obstacle("images/frame.png", cx, cy)

    offsets = [-150, +150]

    for img, dx in zip(site_images, offsets):
        sim.spawn_site(img, cx + dx, cy)

    sim.batch_spawn_agents(50, Cockroach, images=["images/cockroach.png"])
    sim.run()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("experiment", type=int, choices=[1,2])
    args = p.parse_args()

    if args.experiment == 1:
        run_experiment(["images/site.png", "images/site.png"])
    else:
        run_experiment(["images/site-small.png", "images/site.png"])
