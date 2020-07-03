import pandas as pd
import os

# Converts the t-test results to LaTeX table format
AUDIO_FEATURES = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness", "speechiness", "tempo", "valence"]
DIR_PATH = "ttest/"
directory = os.fsencode(DIR_PATH)

i = 2
for file in os.listdir(directory):
    if i%2==0:
        print('\\begin{minipage}[b]{.45\\textwidth} \n \\centering')

    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
         contexts = filename[:-4]
         dat = pd.read_csv(f'{DIR_PATH}{filename}')
         dat.columns = [f'textbf{{{contexts}}}', 't', 'p', 'dof']
         dat = dat.drop(columns=['dof'])
         dat = dat.round({'t':2,'p':4})
         caption = '\\captionof{table}{' + f'T-test result for all audio features when comparing {contexts} songs.}}'
         label = '\n \\label{' + f'table:{contexts}}}'
         latex_table = dat.to_latex(index=False).replace("textbf\\", "\\textbf")
         latex_table = latex_table.replace("\\}", "}")
         print(latex_table + caption + label)
         print('\n')

    if i%2==0:
        print('\\end{minipage}\\qquad \n \\begin{minipage}[b]{.45\\textwidth} \n \centering')

    if i%2==1:
        print('\\end{minipage}')

    i = i + 1