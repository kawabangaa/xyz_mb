import pandas as pd
from bokeh.palettes import inferno,viridis
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                          LinearColorMapper, PrintfTickFormatter,Label, Title)
from bokeh.plotting import figure, save
from bokeh.io import output_file
from bokeh.transform import transform
from Game import Game
from Probability import Probability
from constants import animal_cnt, num_of_animal, verbose, b_value, r_value, d_value

def run_games(special_prob_dist,selected_animal_prob, draw_max_weight, draw_resulotion, plays_per_comb):
    special_prob = Probability(2,special_prob_dist)
     # in this mode we are not exploring the draw probabilities
    animal_prob = Probability(num_of_animal, selected_animal_prob)
    idx = 0
    data = []
    for draw_weight in range(1, draw_max_weight,draw_resulotion):
        # Generating the games
        res = {b_value: 0, d_value: 0, r_value: 0}
        draw_prob = Probability(2, [draw_max_weight - draw_weight, draw_weight])
        game = Game(special_prob, animal_prob, draw_prob)
        for i in range(plays_per_comb):
            if verbose:
                print("starting game " + str(i))
            res[game.play_game()] += 1
            if verbose:
                print('result stake: ' + str(res))
            game.reset()
        # Converting results into percentages
        factor = 100.0 / sum(res.values())
        for k in res:
            res[k] = res[k] * factor
        if verbose:
            print("finished params, result: "+ str(res))
        # Inserting the data into the data list
        data.append([draw_weight,draw_max_weight, res[b_value], res[r_value], res[d_value], special_prob_dist[1]/sum(special_prob_dist)])
        idx += 1
    df = pd.DataFrame(data, columns=['draw_weight','draw_max_weight', 'black per', 'red per', 'draw_per', 'special prob'])
    return df

def run_and_plot_draw_prob(special_prob_dist,selected_animal_prob):
    df = run_games(special_prob_dist,selected_animal_prob, 100, 10, 1000)
    df.to_csv('draw_prob.csv')
    plot_draw_prob(df,"draw_prob")

def plot_draw_prob(df,  output_file_name):

    df['draw_prob'] = (df['draw_weight'] / df['draw_max_weight'])
    df = df.sort_values('draw_prob')
    df['index'] = df.index.astype(str)


    source = ColumnDataSource(df)
    output_file_name_with_ext = str(output_file_name) + ".html"
    output_file(output_file_name_with_ext)

    colors = ["#7fc6a4", "#EF767A", "#FFE347", "#0091AD"]
    tooltips = [("draw prob", "@draw_prob"), ("draw per", "@draw_per")]
    p = figure(plot_height=max(df.shape[0]*5,700), title=None,
               toolbar_location="right", tools="pan, box_select, zoom_in, zoom_out, save, reset, hover", tooltips=tooltips)

    label_opts = dict(x=0, y=0,x_units='screen', y_units='screen')
    msg2 = "black - red win (in percentage, over X games) difference"
    msg1 = "as a function of the probability of each animal to appear in the game"
    caption1 = Label(text=msg1, **label_opts)
    p.add_layout(caption1, 'above')
    caption2 = Label(text=msg2, **label_opts)
    p.add_layout(caption2, 'above')

    p.axis.visible = True
    # p.hbar_stack(animal_col, y='index', height=1, color=colors, source=source,
    #              legend_label=animal_col)
    # p.add_layout(p.legend[0], 'right')
    p.circle('draw_prob', 'draw_per', size=20, color="navy", alpha=0.5, source = source)

    # colors = viridis(df['black_red_diff'].nunique())
    # mapper = LinearColorMapper(palette=colors, low=df['black_red_diff'].min(), high=df['black_red_diff'].max())
    #
    # p.rect(x=1.07, y='index', width=0.1, height=0.9, source=source,
    #        line_color=None, fill_color=transform('black_red_diff', mapper))
    # color_bar = ColorBar(color_mapper=mapper,
    #                      ticker=BasicTicker(desired_num_ticks=30),
    #                      formatter=PrintfTickFormatter(format="%d"),
    #                      title="red - black win % diff",
    #                      location='center',
    #                      orientation='horizontal', )
    #
    # p.add_layout(color_bar, 'below')

    p.ygrid.grid_line_color = None

    save(p)

if __name__ == '__main__':
    run_and_plot_draw_prob([2,1],[0.273, 0.364, 0.273, 0.09])