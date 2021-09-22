import pandas as pd
from os import listdir, path, environ
from measures import measures_kwargs
import itertools
import numpy as np


def load_data():
    # Load input files
    first = True
    for f, d in [
        (
            path.join("output", "measures", f),
            f.replace("input_", "").replace(".csv.gz", ""),
        )
        for f in listdir(path.join("output", "measures"))
        if f.startswith("input")
    ]:
        if first:
            df = pd.read_csv(f).assign(date=d)
            first = False
        else:
            df = pd.concat([df, pd.read_csv(f).assign(date=d)])
    df.date = df.date = pd.to_datetime(df.date)
    return df


def calculate_antibiotic_infection_intersection(df):
    # get infection and antibiotic prescription date columns
    infection_antibiotic_measures = ["infection", "antibiotic_prescription"]
    infection_antibiotic_cols = {}
    for a, b in itertools.product(infection_antibiotic_measures, ["date", "code"]):
        infection_antibiotic_cols[(a, b)] = sorted(
            [c for c in df.columns if c.startswith(f"{a}_{b}_")]
        )

    date_cols = sorted(
        [v for k, v in infection_antibiotic_cols.items() if k[1] == "date"]
    )

    # count intersections of infection and antibiotic prescription dates
    A = df[date_cols[0]].to_numpy(dtype=str)
    I = df[date_cols[1]].to_numpy(dtype=str)
    intersection_count = lambda x: np.count_nonzero(np.intersect1d(x[0], x[1]) != "nan")
    df["infection_antibiotic_intersection"] = [
        intersection_count(r) for r in np.stack((A, I), axis=1)
    ]

    # Check pivot n is adequate
    pivot_n = max(
        [
            int(a.split("_")[-1])
            for a in list(
                itertools.chain(*[v for _, v in infection_antibiotic_cols.items()])
            )
        ]
    )
    print(f"n for pivot operations: {pivot_n}")
    print("Max record counts for pivoted columns:")
    print(df[[m + "s" for m in infection_antibiotic_measures]].max())


def calculate_grouped_measure(df, group, measure):
    group = None if group == "practice" else group
    groups = ["practice", group, "date"] if group else ["practice", "date"]
    df_grouped_measure = (
        df.groupby(groups)[[measure["numerator"], measure["denominator"]]]
        .sum()
        .reset_index()
    )
    df_grouped_measure[measure["id"]] = df_grouped_measure.apply(
        lambda x: x[measure["numerator"]] / x[measure["denominator"]]
        if x[measure["denominator"]] > 0
        else 0,
        axis=1,
    )

    if (
        "OPENSAFELY_BACKEND" not in environ
        or environ["OPENSAFELY_BACKEND"] == "expectations"
    ):
        df_grouped_measure[measure["id"]] = df_grouped_measure[measure["id"]].fillna(0)
        df_grouped_measure[measure["id"]] = df_grouped_measure.apply(
            lambda x: x[measure["id"]]
            if x[measure["id"]] <= 1
            else 1 / x[measure["id"]],
            axis=1,
        )

    df_grouped_measure.to_csv(
        path.join("output", "measures", f'measure_{measure["id"]}_{group}.csv.gz'),
        index=False,
        compression="gzip",
    )


def main():
    df = load_data()
    calculate_antibiotic_infection_intersection(df)

    for measure in measures_kwargs:
        for group in measure["group_by"]:
            calculate_grouped_measure(df=df, measure=measure, group=group)


if __name__ == "__main__":
    main()
