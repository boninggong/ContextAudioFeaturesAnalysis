import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# Visualizes each average audio feature for the activity dimensions
n_groups = 11
AUDIO_FEATURES = ["#songs", "acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness", "speechiness", "tempo", "valence"]
activites = ["running", "walking", "sleeping", "relaxing"]
wanted_features = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence"]
feature_values = [[] for _ in range(9)]
time_of_day_values = [[] for _ in range(4)]

for j, act in enumerate(activites):
    dat = pd.read_csv(f"audio_features/audio_features_{act}.csv")[:1].values[0]
    for i, feat in enumerate(wanted_features):
        time_of_day_values[j].append(dat[AUDIO_FEATURES.index(feat)])
        feature_values[i].append(dat[AUDIO_FEATURES.index(feat)])

def radar_plot():
    # Set data
    df = pd.DataFrame({
        'group': activites,
        'accousticness': feature_values[0],
        'danceability': feature_values[1],
        'energy': feature_values[2],
        'instrumentalness': feature_values[3],
        'liveness': feature_values[4],
        'loudness': feature_values[5],
        'speechiness': feature_values[6],
        'tempo': feature_values[7],
        'valence': feature_values[8]
    })

    print(feature_values)
    # ------- PART 1: Create background

    # number of variable
    categories = list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["0.25", "0.5", "0.75"], color="grey", size=7)
    plt.ylim(0, 1)

    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Ind1
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Running")
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Walking")
    ax.fill(angles, values, 'r', alpha=0.1)

    # Ind1
    values = df.loc[2].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Sleeping")
    ax.fill(angles, values, 'g', alpha=0.1)

    # Ind2
    values = df.loc[3].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Relaxing")
    ax.fill(angles, values, 'm', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.show()

# 0 = morning, 1 = afternoon, 2 = evening, 3 = night
def line_plot():
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], time_of_day_values[0], 'b', label='Running')
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], time_of_day_values[1], 'r', label='Walking')
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], time_of_day_values[2], 'g', label='Sleeping')
    plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9], time_of_day_values[3], 'm', label='Relaxing')
    plt.axis([1, 9, 0, 1])
    plt.ylabel('Values')
    plt.text(1.6, -0.085, "1 = acousticness | 2 = danceability | 3 = energy | 4 = instrumentalness | 5 = liveness | 6 = loudness | 7 = speechiness | 8 = tempo | 9 = valence")
    plt.legend()
    plt.show()

radar_plot()

# line_plot()



