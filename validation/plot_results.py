import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("validation/evaluation_metrics.csv")

# Prepare data by averaging scores grouped by model, prompt_mode, and metric
mean_df = df.groupby(["model", "prompt_mode"])\
    [["faithfulness", "context_recall", "answer_correctness"]].mean().reset_index()

# Melt data for seaborn-friendly long format
melted = mean_df.melt(id_vars=["model", "prompt_mode"],
                      var_name="Metric", value_name="Score")

# Create a faceted bar plot with seaborn.catplot for multiple metrics separately
g = sns.catplot(
    data=melted,
    x="prompt_mode",
    y="Score",
    hue="model",
    col="Metric",
    kind="bar",
    height=4,
    aspect=1,
    errorbar=None  # disables confidence intervals, replacing ci=None
)

g.set_axis_labels("Prompt Engineering Technique", "Average Score")
g.set_titles("{col_name}")
g.set_xticklabels(rotation=30)
plt.tight_layout()
plt.show()
