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