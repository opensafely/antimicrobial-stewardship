from typing import List
import pandas as pd
from os import listdir, path, environ
from measures import measures_kwargs
import itertools
import numpy as np
from datetime import datetime


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
    pivot_stats = {"pivot_n": pivot_n}
    df_ps = df[[m + "s" for m in infection_antibiotic_measures]].max()
    pivot_stats.update(df_ps.to_dict())

    return pivot_stats


def calculate_grouped_measure(df, group, measure, date):
    group = None if group == "practice" else group
    groups = ["practice", group] if group else ["practice"]
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

    out_file_path = path.join(
        "output", "measures", f'{date}~{measure["id"]}~{group}.csv.gz'
    )

    df_grouped_measure.to_csv(
        out_file_path,
        index=False,
        compression="gzip",
    )
    return out_file_path


def calculate(df, date):
    pivot_stats = calculate_antibiotic_infection_intersection(df)
    out_files = []
    for measure in measures_kwargs:
        for group in measure["group_by"]:
            out_files.append(
                calculate_grouped_measure(
                    df=df, measure=measure, group=group, date=date
                )
            )
    return (out_files, pivot_stats)


def combine(measure_files):
    fmgd = {
        x[0]: {"measure": x[2], "group": x[3], "date": x[1]}
        for x in [[mf] + mf.replace(".csv.gz", "").split("~") for mf in measure_files]
    }
    measures = set([v["measure"] for v in fmgd.values()])
    groups = set([v["group"] for v in fmgd.values()])
    for m in measures:
        for g in groups:
            input_files = {
                k: v["date"]
                for k, v in fmgd.items()
                if v["measure"] == m and v["group"] == g
            }

            df = ""
            first = True
            for f, d in input_files.items():
                if first:
                    df = pd.read_csv(f).assign(date=d)
                    first = False
                else:
                    df = pd.concat([df, pd.read_csv(f).assign(date=d)])
            df.to_csv(
                path.join("output", "measures", f"measure_{m}_{g}.csv.gz"),
                index=False,
                compression="gzip",
            )


def write_pivot_stats(pivot_stats):
    df = pd.DataFrame.from_dict(pivot_stats)
    df.to_csv(
        path.join("output", "measures", f"pivotstats_{datetime.now().isoformat()}.csv")
    )


def main():
    out_files = []
    pivot_stats = {}
    for f, d in [
        (
            path.join("output", "measures", f),
            f.replace("input_", "").replace(".csv.gz", ""),
        )
        for f in listdir(path.join("output", "measures"))
        if f.startswith("input")
    ]:
        df = pd.read_csv(f)
        c = calculate(df, d)
        out_files = out_files + c[0]
        pivot_stats[d] = c[1]
    combine(out_files)
    write_pivot_stats(pivot_stats)


if __name__ == "__main__":
    main()
