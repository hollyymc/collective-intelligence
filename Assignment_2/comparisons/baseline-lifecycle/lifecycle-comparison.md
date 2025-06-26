# Comparative Analysis of Baseline vs. Life-Cycle Predator–Prey Simulations

## Hypotheses

- **H₀:** Introducing a life-cycle (aging, sexual reproduction, max_age) into the Lotka–Volterra model does **not** significantly change population dynamics compared to the baseline model.  
- **H₁:** Introducing a life-cycle (aging, sexual reproduction, max_age) into the Lotka–Volterra model **does** significantly change population dynamics compared to the baseline model.

---

## Metrics for Comparison

- **steps_survived:** How long the population persisted  
- **final_rabbits:** Population size at termination  
- **final_foxes:** Population size at termination  
- **min_rabbits:** Minimum rabbit count reached during a run  
- **min_foxes:** Minimum fox count reached during a run  
- **max_rabbits:** Maximum rabbit count reached during a run  
- **max_foxes:** Maximum fox count reached during a run  

---

## Parameters

### Baseline model
duration: 15 000 steps
movement_speed: 2.0
fox_hunt_radius: 10
rabbit_reproduction_prob: 0.005
fox_death_prob: 0.01
fox_start_energy: 0
fox_energy_gain_on_eat: 0


### Life-Cycle model
duration: 15 000 steps
movement_speed: 2.0
fox_hunt_radius: 50.0
rabbit_reproduction_prob: 0.01 * age-based value
    - Age < 10: 0
    - Age 10–80: 0.5
    - Age > 80: 0.25
fox_death_prob: 0.0005 * age_death_prob
    - age_death_prob = min(0.002, age/max_age * 0.02)
fox_start_energy: 0
fox_energy_gain_on_eat: 0
max_age: 200
mating_radius: 40
fox_reproduction_prob: 0.05 * age-based value
    - Age < 10: 0
    - Age 10–100: 0.5
    - Age > 100: 0.25
aging_frequency: ~0.10 chance per tick to age 1 year (≈1 year every 10 ticks)


## Results

### Statistical analysis

**steps_survived**
BASELINE: mean = 2995.2, SD = 12.3, 95% CI = [2980.1, 3010.3]
LIFE-CYCLE: mean = 3001.5, SD = 10.8, 95% CI = [2987.4, 3015.6]
t-test p-value = 0.4231
Mann–Whitney p-value = 0.4150


**final_rabbits**
BASELINE: mean = 5.2, SD = 7.8, 95% CI = [2.1, 8.3]
LIFE-CYCLE: mean = 6.5, SD = 8.1, 95% CI = [3.3, 9.7]
t-test p-value = 0.6125
Mann–Whitney p-value = 0.5782


**final_foxes**
BASELINE: mean = 4.8, SD = 6.5, 95% CI = [1.9, 7.7]
LIFE-CYCLE: mean = 3.9, SD = 6.9, 95% CI = [1.0, 6.8]
t-test p-value = 0.7320
Mann–Whitney p-value = 0.6891


**max_rabbits**
BASELINE: mean = 98.7, SD = 2.5, 95% CI = [97.8, 99.6]
LIFE-CYCLE: mean = 100.2, SD = 1.9, 95% CI = [99.6, 100.8]
t-test p-value = 0.0145
Mann–Whitney p-value = 0.0162


**max_foxes**
BASELINE: mean = 26.8, SD = 4.5, 95% CI = [24.3, 29.3]
LIFE-CYCLE: mean = 22.1, SD = 3.8, 95% CI = [20.1, 24.1]
t-test p-value = 0.0018
Mann–Whitney p-value = 0.0021


**min_rabbits**
BASELINE: mean = 0.8, SD = 1.1, 95% CI = [–0.1, 1.7]
LIFE-CYCLE: mean = 1.2, SD = 1.4, 95% CI = [0.1, 2.3]
t-test p-value = 0.3287
Mann–Whitney p-value = 0.3452


**min_foxes**
BASELINE: mean = 0.6, SD = 0.9, 95% CI = [–0.1, 1.3]
LIFE-CYCLE: mean = 0.3, SD = 0.7, 95% CI = [–0.2, 0.8]
t-test p-value = 0.2543
Mann–Whitney p-value = 0.2690


## Interpretation

**steps_survived**
Both models exhibited virtually identical survival times (Baseline: 2 995 ± 12 steps; Life-Cycle: 3 002 ± 11 steps), and neither the t-test (p = 0.42) nor the Mann–Whitney test (p = 0.42) found a statistically significant difference.

Biological implication: Introducing age structure and sexual reproduction does not significantly alter the overall duration before one or both populations collapse under these parameter sets.


**final_rabbits, final_foxes**
On average, both models ended with only a handful of survivors: roughly 5–6 rabbits and 4–5 foxes per run. Statistical tests confirm no meaningful difference (all p-values > 0.5), indicating that neither model reliably produces larger remnant populations at collapse.

Biological implication:  Even when you add aging, enforced mating, and a fixed lifespan, those life-history traits don’t significantly alter the number of animals left when the cycle finally crashes. Under our settings, these processes neither shield the populations against extinction nor push them toward a higher final count.

**min_rabbits, min_foxes**
In both simulations, rabbits dipped to about 1 or fewer on average (baseline ~0.8, life-cycle ~1.2; p ≈ 0.33), and foxes similarly sank to around half an individual (baseline ~0.6, life-cycle ~0.3; p ≈ 0.25). These small differences aren’t statistically significant, meaning both runs hit almost zero just as often. Such deep crashes are typical of predator–prey cycles, periods when prey are scarce and predators starve. They show up regardless of added lifecycle rules.

Biological implication:  Delays in reproduction, built-in aging and capped lifespan do not stop the populations from going extinct.


**max_rabbits, max_foxes**
in the baseline model, the highest rabbit count averaged 98.7 ± 2.5, whereas the life-cycle model reached 100.2 ± 1.9. This increase is statistically significant (p ≈ 0.015). Peak fox numbers dropped from 26.8 ± 4.5 in the baseline to 22.1 ± 3.8 with life-cycle rules, a highly significant decrease (p ≈ 0.002).

Biological implication:  Because rabbits in the life-cycle model must wait until they’re older to reproduce and lose breeding potential as they age, they don’t churn out offspring as steadily in the middle of a cycle. That delay lets their numbers build to a slightly higher “boom” before crashing.
Foxes face a different constraint: they must age, hunt successfully, and find a mate before they can have young. Those added steps slow down their numerical response to rising rabbit numbers, so their population doesn’t spike as sharply.


## Conclusion

By adding aging, mating rules, and a fixed lifespan to the predator-prey model, we saw only one real change: rabbit booms got a bit bigger and fox booms got smaller. Everything else stayed about the same. How long the populations lasted and how many animals were left at the end didn’t change. In other words, life-history details tweak the size of the ups and downs but don’t affect the overall survival time or extinction chances under our settings.

Our data show no significant differences in survival time, final population sizes, or minimum counts (all p > 0.25), but clear, statistically significant shifts in the peak populations of both species (rabbit p ≈ 0.015; fox p ≈ 0.002). Therefore, we reject H₀ in favor of H₁ lifecycle  traits do alter the dynamics, specifically by boosting prey booms and dampening predator peaks, even though overall persistence and end‐point abundances stay the same.