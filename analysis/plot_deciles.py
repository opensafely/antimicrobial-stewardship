from ebmdatalab import charts
import pandas as pd
from os import path
from measures import measures_kwargs
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def load_data(measure, group):
    return pd.read_csv(
        path.join("output", "measures", f'measure_{measure["id"]}_{group}.csv.gz'),
        parse_dates=['date']
    )


def plot_decile_group(df, group, measure):

    if group:
        group_values = df[group].drop_duplicates()
        n_groups = len(group_values)
    else:
        n_groups = 1
    fig = plt.figure(figsize=(12, 8 * n_groups))
    fig.autofmt_xdate()
    layout = gridspec.GridSpec(n_groups, 1, figure=fig)
    if group:
        for groupval, lax in zip(group_values, layout):
            ax = plt.subplot(lax)
            title = (
                f'{measure["id"].replace("_"," ").title()}'
                + f" - {group.title()}:{groupval}"
            )
            charts.deciles_chart(
                df=df[df[group] == groupval],
                period_column="date",
                column=measure["id"],
                title=title,
                ax=ax,
            )
    else:
        ax = plt.subplot(layout[0])
        title = f'{measure["id"].replace("_"," ").title()}'
        charts.deciles_chart(
            df=df,
            period_column="date",
            column=measure["id"],
            title=title,
            ax=ax,
        )
    return fig


def main():
    plt.ioff()
    plt.rcParams.update({"figure.max_open_warning": 0})
    for measure in measures_kwargs:
        df = load_data(measure=measure, group=None)
        fig = plot_decile_group(df=df, group=None, measure=measure)
        plt.savefig(path.join('output','figures',f'{measure["id"]}.png'))
        plt.close(fig)
        for group in [g for g in measure["group_by"] if g!="practice"]:
            df = load_data(measure=measure, group=group)
            fig = plot_decile_group(df=df, group=group, measure=measure)
            plt.savefig(path.join('output','figures',f'{measure["id"]}_{group}.png'))
            plt.close(fig)


if __name__ == "__main__":
    main()
