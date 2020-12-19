import csv
import time
import pandas as pd
from bokeh.palettes import inferno
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                          LinearColorMapper, PrintfTickFormatter, Label, Title)
from bokeh.plotting import figure, save
from bokeh.io import output_file
from bokeh.transform import transform
from Game import Game
from Probability import Probability
from constants import animal_cnt, num_of_animal, VERBOSE, BLACK_VALUE, RED_VALUE, DRAW_VALUE


def run_games(special_prob_dist, draw_prob_dist, max_weight, weight_resulotion, plays_per_comb):
    special_prob = Probability(2, special_prob_dist)
    draw_prob = Probability(2, draw_prob_dist)
    idx = 0
    data = []
    for wasp_weight in range(0, max_weight, weight_resulotion):
        for chameleon_weight in range(0, max_weight, weight_resulotion):
            for snake_weight in range(0, max_weight, weight_resulotion):
                for cheetah_weight in range(0, max_weight, weight_resulotion):
                    # Generating the games
                    res = {BLACK_VALUE: 0, DRAW_VALUE: 0, RED_VALUE: 0}
                    if VERBOSE:
                        print("starting with new params: " + str(wasp_weight) + str(chameleon_weight) + str(
                            snake_weight) + str(cheetah_weight))
                    animal_prob = Probability(num_of_animal,
                                              [wasp_weight, chameleon_weight, snake_weight, cheetah_weight])
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
                    data.append(
                        [wasp_weight, chameleon_weight, snake_weight, cheetah_weight, res[BLACK_VALUE], res[RED_VALUE],
                         res[DRAW_VALUE], special_prob_dist[1] / sum(special_prob_dist),
                         draw_prob_dist[1] / sum(draw_prob_dist)])
                    idx += 1
    df = pd.DataFrame(data, columns=['wasp', 'chameleon', 'snake', 'cheetah', 'black per', 'red per', 'draw per',
                                     'special prob', 'draw prob'])
    return df


def plot_games():
    df = run_games([2, 1], [1, 0], 5, 1, 1000)
    df.to_csv('result.csv')
    print(df.shape[0])
    df['black_red_diff'] = (df['red per'] - df['black per']).abs()
    df['index'] = df.index.astype(str)
    animal_col = ['wasp', 'chameleon', 'snake', 'cheetah']
    df[animal_col] = df[animal_col].div(df[animal_col].sum(axis=1), axis=0).fillna(0)
    df = df.sort_values(animal_col)

    print(list(df.index))
    print(df.head(5))
    source = ColumnDataSource(df)

    # experiment_list = source.
    output_file("stacked.html")

    colors = ["#7fc6a4", "#EF767A", "#FFE347", "#0091AD"]
    tooltips = [("wasp", "@wasp"), ("chameleon", "@chameleon"), ("snake", "@snake"), ("cheetah", "@cheetah"),
                ("black red diff", "@black_red_diff")]
    p = figure(y_range=list(df["index"].unique()), plot_height=700, title=None,
               toolbar_location=None, tools="pan, box_select, zoom_in, zoom_out, save, reset, hover", tooltips=tooltips)

    label_opts = dict(

        x=0, y=0,

        x_units='screen', y_units='screen'

    )
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

    # colors = ['#e1dce3', '#ddd8e4', "#c8bdd2", "#a192b4", "#7a6691", "#624d7d", "#422e5d"]
    # colors.reverse()
    colors = inferno(df['black_red_diff'].nunique())
    mapper = LinearColorMapper(palette=colors, low=df['black_red_diff'].min(), high=df['black_red_diff'].max())

    p.rect(x=1.07, y='index', width=0.1, height=0.9, source=source,
           line_color=None, fill_color=transform('black_red_diff', mapper))
    color_bar = ColorBar(color_mapper=mapper,
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d"),
                         title="red - black win % diff",
                         location='center',
                         orientation='horizontal', )

    p.add_layout(color_bar, 'below')

    p.ygrid.grid_line_color = None

    save(p)


def run_one_game():
    start_time = time.time()
    res = {-1: 0, 0: 0, 1: 0}
    plays_per_comb = 100000
    normal_prob = Probability(2, [1, 0])
    animal_prob = Probability(num_of_animal, [0, 1, 0, 0])
    draw_prob = Probability(2, [1, 5])
    game = Game(normal_prob, animal_prob, draw_prob)
    for i in range(plays_per_comb):
        res[game.play_game()] += 1
        game.reset()
    print("--- %s seconds ---" % (time.time() - start_time))
    factor = 100.0 / sum(res.values())

    for k in res:
        res[k] = (res[k] * factor)
    print(res)


def test_probability():
    prob = Probability(3, [1, 0, 1])
    test = [0, 0, 0]
    for _ in range(1000):
        test[prob.draw_idx()] += 1
    print(test)


if __name__ == '__main__':
    # test_probability()
    run_one_game()
    # run_games([2,1], 8, 1, 5000)
    # plot_games()
