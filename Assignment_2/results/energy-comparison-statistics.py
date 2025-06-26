import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu, sem ,t
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

baseline_df = pd.read_csv("baseline/baseline_results.csv")
energy_df = pd.read_csv("energy/energy_results.csv")
metrics = [
    "steps_survived",
    "final_rabbits",
    "final_foxes",
    "max_rabbits",
    "max_foxes",
    "min_rabbits",
    "min_foxes"
]

def confidence_interval(data):
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    n = len(data)
    margin_error = t.ppf(0.975, df=n-1) * sem(data)
    return mean, std, (mean - margin_error, mean + margin_error)

def compare_metric(metric):
    base = baseline_df[metric]
    energy = energy_df[metric]
    base_mean, base_std, base_ci = confidence_interval(base)
    energy_mean, energy_std, energy_ci = confidence_interval(energy)

    # tests
    t_stat, t_p = ttest_ind(base, energy, equal_var=False)
    u_stat, u_p = mannwhitneyu(base, energy, alternative='two-sided')

    print(f"\n**{metric}**")
    print(f"BASELINE: mean = {base_mean:.2f}, SD = {base_std:.2f}, 95% con inter = [{base_ci[0]:.2f}, {base_ci[1]:.2f}]")
    print(f"ENERGY: mean = {energy_mean:.2f}, SD = {energy_std:.2f}, 95% con inter = [{energy_ci[0]:.2f}, {energy_ci[1]:.2f}]")
    print(f"T-test p-value = {t_p:.4f}")
    print(f"Mann-Whitney p-value = {u_p:.4f}")

for metric in metrics:
    compare_metric(metric)

    sns.boxplot(data=[baseline_df[metric], energy_df[metric]], palette="Set2")
    plt.xticks([0, 1], ['Baseline', 'Energy Model'])
    plt.title(f"{metric} Comparison")
    plt.ylabel(metric)
    plt.show()
