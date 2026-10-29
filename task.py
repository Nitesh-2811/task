
import pandas as pd

data = {
"Roll No": [1, 1, 2, 2, 1, 2],
"Subject": ["DS", "Java", "DS", "Java", "DS", "Java"],
"Marks": [25, 40, 30, 26, 40, 50],
"Date": [
"01-01-23",
"02-01-23",
"01-01-23",
"02-01-23",
"15-01-23",
"15-01-23"
]
}

df = pd.DataFrame(data)


df["Date"] = pd.to_datetime(
df["Date"], format="%d-%m-%y"
)

df = df.sort_values(
["Roll No", "Subject", "Date"],
ascending=[True, True, False]
)

df["Attempt"] = (
df.groupby(["Roll No", "Subject"])
.cumcount() + 1
)


latest_three = df[df["Attempt"] <= 3].copy()


latest_three["Metric"] = (
"M" + latest_three["Attempt"].astype(str)
)


marks = latest_three.pivot(
index=["Roll No", "Subject"],
columns="Metric",
values="Marks"
)

marks = marks.reindex(
columns=["M1", "M2", "M3"]
).fillna(0).astype(int)


latest_date = (
df.groupby(["Roll No", "Subject"])["Date"]
.first()
.rename("Date")
)

result = latest_date.to_frame().join(marks).reset_index()

result["Date"] = result["Date"].dt.strftime("%d-%m-%y")


print(result.to_string(index=False))
