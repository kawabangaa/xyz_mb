import pandas as pd
from bokeh.palettes import inferno, viridis
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                          LinearColorMapper, PrintfTickFormatter, Label, Title)
from bokeh.plotting import figure, save
from bokeh.io import output_file
from bokeh.transform import transform
from Game import Game
from Probability import Probability
from constants import animal_cnt, num_of_animal, VERBOSE, BLACK_VALUE, RED_VALUE, DRAW_VALUE


def run_games(special_prob_dist, top_configurations, plays_per_comb):
    special_prob = Probability(2, special_prob_dist)
    draw_prob = Probability(2, [1, 0])  # in this mode we are not exploring the draw probabilities
    idx = 0
    data = []
    for animal_prob_dist in top_configurations:
        # Generating the games
        res = {BLACK_VALUE: 0, DRAW_VALUE: 0, RED_VALUE: 0}
        animal_prob = Probability(num_of_animal, animal_prob_dist)
        game = Game(special_prob, animal_prob, draw_prob)
        for i in range(plays_per_comb):
            if VERBOSE:
                print("starting game " + str(i))
            res[game.play_game()] += 1
            if VERBOSE:
                print('result stake: ' + str(res))
            game.reset()
        # Converting results into percentages
        factor = 100.0 / sum(res.values())
        for k in res:
            res[k] = res[k] * factor
        if VERBOSE:
            print("finished params, result: " + str(res))
        # Inserting the data into the data list
        data.append([animal_prob_dist[0], animal_prob_dist[1], animal_prob_dist[2], animal_prob_dist[3], res[BLACK_VALUE],
                     res[RED_VALUE], res[DRAW_VALUE], special_prob_dist[1] / sum(special_prob_dist)])
        idx += 1
    df = pd.DataFrame(data, columns=['wasp', 'chameleon', 'snake', 'cheetah', 'black per', 'red per', 'draw per',
                                     'special prob'])
    return df


def run_and_plot_top_animal_prob(top_configurations):
    df = run_games([2, 1], top_configurations, 100000)
    df.to_csv('top_animal_prob_ranked.csv')
    plot_animal_prob_explor(df, df.shape[0], "top_animal_prob_ranked")


def get_top_animal_prob(df):
    plot_animal_prob_explor(df, 5, "animal_prob_exploration_top")
    df['black_red_diff'] = (df['red per'] - df['black per']).abs()
    df = df.sort_values(['black_red_diff'])
    top_animal_prob = df[:5]
    print(top_animal_prob)


def plot_animal_prob_explor(df, num_of_rows_to_plot, output_file_name):
    df['black_red_diff'] = (df['red per'] - df['black per']).abs()
    df = df.sort_values('black_red_diff')
    df = df.head(num_of_rows_to_plot)
    df['index'] = df.index.astype(str)
    animal_col = ['wasp', 'chameleon', 'snake', 'cheetah']
    df[animal_col] = df[animal_col].div(df[animal_col].sum(axis=1), axis=0).fillna(0)
    df = df.sort_values(animal_col)

    source = ColumnDataSource(df)
    output_file_name_with_ext = str(output_file_name) + ".html"
    output_file(output_file_name_with_ext)

    colors = ["#7fc6a4", "#EF767A", "#FFE347", "#0091AD"]
    tooltips = [("wasp", "@wasp"), ("chameleon", "@chameleon"), ("snake", "@snake"), ("cheetah", "@cheetah"),
                ("black red diff", "@black_red_diff")]
    p = figure(y_range=list(df["index"].unique()), plot_height=max(df.shape[0] * 5, 700), title=None,
               toolbar_location=None, tools="pan, box_select, zoom_in, zoom_out, save, reset, hover", tooltips=tooltips)

    label_opts = dict(x=0, y=0, x_units='screen', y_units='screen')
    msg2 = "black - red win (in percentage, over X games) difference"
    msg1 = "as a function of the probability of each animal to appear in the game"
    caption1 = Label(text=msg1, **label_opts)
    p.add_layout(caption1, 'above')
    caption2 = Label(text=msg2, **label_opts)
    p.add_layout(caption2, 'above')

    p.axis.visible = False
    p.hbar_stack(animal_col, y='index', height=1, color=colors, source=source,
                 legend_label=animal_col)
    p.add_layout(p.legend[0], 'right')

    colors = viridis(df['black_red_diff'].nunique())
    mapper = LinearColorMapper(palette=colors, low=df['black_red_diff'].min(), high=df['black_red_diff'].max())

    p.rect(x=1.07, y='index', width=0.1, height=0.9, source=source,
           line_color=None, fill_color=transform('black_red_diff', mapper))
    color_bar = ColorBar(color_mapper=mapper,
                         ticker=BasicTicker(desired_num_ticks=30),
                         formatter=PrintfTickFormatter(format="%d"),
                         title="red - black win % diff",
                         location='center',
                         orientation='horizontal', )

    p.add_layout(color_bar, 'below')

    p.ygrid.grid_line_color = None

    save(p)


def get_top_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    print(list(df))
    df['black_red_diff'] = (df['red per'] - df['black per']).abs()
    df = df.sort_values('black_red_diff')
    print(list(df))
    return df[['wasp', 'chameleon', 'snake', 'cheetah']][:5].copy()


if __name__ == '__main__':
    run_and_plot_top_animal_prob([[0.375, 0.125, 0.375, 0.125],
                                  [0.364, 0.273, 0.273, 0.09],
                                  [0.3, 0.2, 0.4, 0.01],
                                  [0.273, 0.364, 0.273, 0.09],
                                  [0.182, 0.364, 0.364, 0.09]])
