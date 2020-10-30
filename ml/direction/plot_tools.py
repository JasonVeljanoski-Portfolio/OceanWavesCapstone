import plotly.figure_factory as ff
def px_density(df, variables, custom_labs=None, standardise=False, lines=True, title=None, show_y=True):
    dff = df[variables].copy()
    labs = custom_labs if custom_labs is not None else variables

    if standardise:
        if len(variables) == 1:
            s = dff[variables]
            dff[variables] = (s - np.mean(s) / np.std(s))
        else:
            dff[variables] = dff[variables].apply(lambda s: (s - np.mean(s)) / np.std(s))

    kde = ff.create_distplot(
        [dff[var] for var in variables], group_labels=labs, show_hist=False, show_rug=False
    )

    mode = 'lines' if lines else 'none'
    p = px.area(title=title)
    for i, var in enumerate(variables):
        p.add_scatter(mode=mode, x=kde.data[i]['x'], y=kde.data[i]['y'], name=labs[i], fill='tozeroy')

    if show_y:
        return p
    else:
        return p.update_yaxes(showline=False, showticklabels=False)
    
    
def theme(p):
    purp = '#1a1a23'
    purp_grid = '#1e1e25'
    purp_axes = '#252532'
    purp_font = '#bfbfc0'
    theme_ = dict(paper_bgcolor=purp, plot_bgcolor=purp, font_color=purp_font,
                  title_font_size=30, margin=dict(t=90, l=90, b=90, r=15))
    axes_set = dict(showline=True, linewidth=2, linecolor=purp_axes, gridcolor=purp_grid)

    return p.update_layout(theme_)\
        .update_xaxes(axes_set, showgrid=False, zerolinewidth=1, zerolinecolor=purp_axes)\
        .update_yaxes(axes_set)