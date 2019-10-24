import matplotlib.pyplot as plt
import pandas as pd
plt.ioff()

def plot_results(week):
    # keeps the plot from popping out
    plt.ioff()
    totals = pd.read_csv('DATA/Results/totals.csv')
    fig, ax = plt.subplots(1,2, figsize=(20,7))

    # plot run chart of win perc and moving average
    ax[0].plot(totals.week, totals.win_perc, 'bo-', label='Weekly Percentage')
    ax[0].plot(totals.week, totals.overall_win_perc, 'go-', label='Overall Percentage')
    ax[0].set_xlabel('Week of Season', fontsize=16)
    ax[0].set_ylabel('Win Percentage', fontsize=16)
    ax[0].set_ylim(0, 1)
    ax[0].set_xlim(0.5, float(week)+0.5)
    ax[0].hlines(0.5, 0, float(week)+0.5, colors='red', linestyles='dashed')
    ax[0].legend()

    # plot bar chart with number of weekly bets/wins
    index = list(range(1, week+1))
    width = 0.75

    ax[1].bar(index, totals.total_bets, width=width, label='Total Bets')
    ax[1].bar(index, totals.wins, width=width, label='Wins')
    ax[1].set_ylabel('Number of Bets Each Week', fontsize=16)
    ax[1].set_xlabel('Week')
    ax[1].set_ylim(0,16)
    ax[1].legend()

    fig.suptitle(f'NFL Bets \n*Current Record '
                 f'{int(totals.wins.sum())} - {int(totals.total_bets.sum() - totals.wins.sum())}*',
                 fontsize=22)

    plt.savefig(f'fig/Week_{week}')

