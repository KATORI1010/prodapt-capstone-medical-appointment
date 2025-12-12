import pandas as pd

from ai import review_application

df = pd.read_csv("test/job_rewriting_tests.csv")

review_description = []
overall_summary = []
revised_description = []

for row in df.itertuples():
    description = row[1]
    review_description.append(description)
    result = review_application(job_description=description)

    overall_summary.append(result.overall_summary)
    revised_description.append(result.revised_description)

df["Summary"] = overall_summary
df["Fixed Description"] = revised_description

df.to_csv("eval_output.csv", index=False)
