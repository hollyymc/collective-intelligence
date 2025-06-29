import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu, sem ,t
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

baseline_df = pd.read_csv("baseline/baseline_results.csv")
lifecycle_and_energy_df = pd.read_csv("lifecycle+energy/lifecycle+energy_results.csv")
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
    lifecycle_and_energy = lifecycle_and_energy_df[metric]
    base_mean, base_std, base_ci = confidence_interval(base)
    lifecycle_and_energy_mean, lifecycle_and_energy_std, lifecycle_and_energy_ci = confidence_interval(lifecycle_and_energy)

    # tests
    t_stat, t_p = ttest_ind(base, lifecycle_and_energy, equal_var=False)
    u_stat, u_p = mannwhitneyu(base, lifecycle_and_energy, alternative='two-sided')

    print(f"\n**{metric}**")
    print(f"BASELINE: mean = {base_mean:.2f}, SD = {base_std:.2f}, 95% con inter = [{base_ci[0]:.2f}, {base_ci[1]:.2f}]")
    print(f"LIFECYCLE AND ENERGY: mean = {lifecycle_and_energy_mean:.2f}, SD = {lifecycle_and_energy_std:.2f}, 95% con inter = [{lifecycle_and_energy_ci[0]:.2f}, {lifecycle_and_energy_ci[1]:.2f}]")
    print(f"T-test p-value = {t_p:.4f}")
    print(f"Mann-Whitney p-value = {u_p:.4f}")

for metric in metrics:
    compare_metric(metric)

    sns.boxplot(data=[baseline_df[metric], lifecycle_and_energy_df[metric]], palette="Set2")
    plt.xticks([0, 1], ['Baseline', 'lifecycle and energy Model'])
    plt.title(f"{metric} Comparison")
    plt.ylabel(metric)
    plt.show()
