def theme(p):
    purp = '#1a1a23'
    purp_grid = '#1e1e25'
    purp_axes = '#252532'
    purp_font = '#bfbfc0'
    purpd_ = dict(paper_bgcolor=purp, plot_bgcolor=purp, font_color=purp_font,
                  title_font_size=30, margin=dict(t=90, l=90, b=90, r=15))
    axes_set = dict(showline=True, linewidth=2, linecolor=purp_axes, gridcolor=purp_grid)

    return p.update_layout(purpd_)\
        .update_xaxes(axes_set, showgrid=False)\
        .update_yaxes(axes_set)




def conf_matrix_vis(y_true, y_pred, title, acc, f1, figsize=(12,8)):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from sklearn.metrics import confusion_matrix
    import pandas as pd
    
    sns.set(font='serif', font_scale=1.5)
    font_colour = 'white'
    face_color = 'black'

    plt.rcParams['text.color'] = font_colour
    plt.rcParams['axes.labelcolor'] = font_colour
    plt.rcParams['xtick.color'] = font_colour
    plt.rcParams['ytick.color'] = font_colour
    mpl.rcParams['figure.facecolor'] = 'black'
    labels = sorted(y_true.unique())
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    df_cm = pd.DataFrame(cm, index=labels, columns=labels)

    plt.figure(figsize=(figsize))
    heatmap = sns.heatmap(df_cm, cmap=sns.dark_palette("#40DBC6", as_cmap=True),
                          fmt="d", linewidths=1.5, linecolor='#111111',
                          annot=True, annot_kws={"size": 12, "color": "white", 'family': 'serif'},
                          cbar=False, square=True)

    plt.setp(heatmap.get_yticklabels(),
             rotation=0, ha="right",
             rotation_mode="anchor")

    heatmap.set(ylabel='True Label', xlabel='Predicted Label')
    heatmap.set_title(title, fontsize=35)
    heatmap.text(x=0.75, y=1.006, s=f'Acc: {acc}, F1: {f1}', fontsize=15, alpha=0.9,
                 ha='center', va='bottom', transform=heatmap.transAxes)
    
    plt.show()