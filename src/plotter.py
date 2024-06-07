from typing import List, Union
import matplotlib.pyplot as plt

from .plot_styles import *


def _plot_markers(x, y, points, marker, m_clr, m_lbl):
    if points is None:
        return

    x = x[points]
    y = y[points]

    if marker is None or not marker:
        marker = [None] * len(x)
    if m_clr is None or not m_clr:
        m_clr = [None] * len(x)
    if m_lbl is None or not m_lbl:
        m_lbl = [None] * len(x)

    for xp, yp, m, clr, lbl, in zip(x, y, marker, m_clr, m_lbl):
        plt.scatter(xp, yp, marker=m,
                    s=marker_size, c=clr, edgecolors="k", label=lbl)


def plot_spo(
    x: Union[List[float], List[List[float]]],
    y: Union[List[float], List[List[float]]],
    labels: List[str],
    xlabel: str,
    ylabel: str,
    color: Union[str, List[str]] = None,
    points: Union[List[int], List[List[int]]] = None,
    xlim: List[float] = None,
    ylim: List[float] = None,
    legend: bool = False,
    grid: bool = False,
    visible_top_right_border: bool = False,
    markers: Union[List[str], List[List[str]]] = None,
    marker_colors: Union[List[str], List[List[str]]] = None,
    marker_labels: Union[List[str], List[List[str]]] = None,
):
    """Plots static pushover curves

    Parameters
    ----------
    x : Union[List[float], List[List[float]]]
        X values, typically base shear
    y : Union[List[float], List[List[float]]]
        Y values, typically drift
    labels : List[str]
        Labels of x and y axis
    xlabel : str
        X label
    ylabel : str
        Y label
    color : Union[str, List[str]], optional
        Colors for pushover curve(s) provided, by default None
    points : Union[List[int], List[List[int]]], optional
        Marker point indexes matching the pushover curves to show,
        by default None
    xlim : List[float], optional
        X axis limits, by default None
    ylim : List[float], optional
        Y axis limits, by default None
    legend : bool, optional
        Show legend, by default False
    grid : bool, optional
        Show gridlines, by default False
    visible_top_right_border : bool, optional
        Show top and right borders of the figure, by default False
    markers : Union[List[str], List[List[str]]], optional
        Marker types corresponding to points, by default None
    marker_colors : Union[List[str], List[List[str]]], optional
        Marker colors corresponding to points, by default None
    marker_labels : Union[List[str], List[List[str]]], optional
        Marker labels corresponding to points, by default None

    Returns
    -------
    fig : `.Figure`
    ax : `~.axes.Axes` or array of Axes

    Raises
    ------
    ValueError
        if more than 10 pushover curves are provided, i.e., length of X is 10
    ValueError
        if length of x, y, points, markers, marker_colors, marker_labels
        do not match
    """
    fig, ax = plt.subplots(figsize=(3, 3), dpi=200)

    if isinstance(x[0], float):
        if color is None:
            color = "k"

        plt.plot(x, y, color=color, label=labels, zorder=0)

        if markers is not None and isinstance(markers, list):
            markers = markers[i]

        _plot_markers(x, y, points, markers)

    else:
        if color is None:
            color = color_grid

        if len(x) > 4:
            ls = None
        if len(x) > 10:
            raise ValueError("Does not support more than 10 pushover curves!")
        else:
            ls = linestyles

        for i in range(len(x)):
            if len(x) != len(y) != len(points):
                raise ValueError(
                    "x, y, and points must have the same dimension"
                    " along 0 axis")

            if ls is None:
                plt.plot(x[i], y[i], color=color[i], label=labels[i], zorder=0)
            else:
                plt.plot(x[i], y[i], color=color[i],
                         label=labels[i], ls=ls[i], zorder=0)

            mrk, mrk_clrs, mrk_labels = None, None, None

            if markers is not None:
                if len(markers) != len(x):
                    raise ValueError(
                        "x, y, markers, and points must have the same"
                        " dimension along 0 axis")

                mrk = markers[i]

            if marker_colors is not None:
                if len(markers) != len(marker_colors):
                    raise ValueError(
                        "marker_colors and markers must have the same"
                        " dimension along 0 axis")

                mrk_clrs = marker_colors[i]

            if marker_labels is not None:
                if len(markers) != len(marker_labels):
                    raise ValueError(
                        "marker_labels and markers must have the same "
                        "dimension along 0 axis")

                mrk_labels = marker_labels[i]

            _plot_markers(x[i], y[i], points[i], marker=mrk,
                          m_clr=mrk_clrs, m_lbl=mrk_labels)

    # X and Y axis labels
    plt.xlabel(xlabel, fontsize=FONTSIZE)
    plt.ylabel(ylabel, fontsize=FONTSIZE)

    # X and Y axis limits
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    if grid:
        plt.grid(True, which="major", axis='both', lw=0.5)
        plt.grid(True, which="minor", axis='both', lw=0.5)

    if legend:
        plt.legend(frameon=False, loc='center left',
                   bbox_to_anchor=(1, 0.5), fontsize=FONTSIZE)

    ax.spines[['right', 'top']].set_visible(visible_top_right_border)
    ax.tick_params(axis='both', labelsize=FONTSIZE)

    plt.show()

    return fig, ax


def cloud_im_vs_edp(
    im: List,
    edp: List,
    scale: str = "linear",
    xlim: List = None,
    ylim: List = None,
    marker: str = "o",
    color: str = "r",
    grid: bool = False,
    xlabel: str = "IML",
    ylabel: str = "EDP",
):
    """Plots cloud (scatter) distribution of IM vs EDPs

    Parameters
    ----------
    im : List
        Intensity measure levels
    edp : List
        Engineering demand parameters (EDPs)
    scale : str, optional
        Axis scale, by default "linear"
    xlim : List, optional
        Limits of X (IM) axis, by default None
    ylim : List, optional
        Limits on Y (EDP) axis, by default None
    marker : str, optional
        Marker type, by default "o"
    color : str, optional
        Marker color, by default "r"
    grid : bool, optional
        Show both grids, by default False
    xlabel : str, optional
        IM axis label, by default "IML"
    ylabel : str, optional
        EDP axis label, by default "EDP"

    Returns
    -------
    fig : `.Figure`
    ax : `~.axes.Axes` or array of Axes
    """
    if xlim is None:
        xlim = [min(im), max(im)]
    if ylim is None:
        ylim = [min(edp), max(edp)]

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

    plt.scatter(im, edp, marker=marker, color=color)

    plt.grid(grid, which="both", axis="both", ls="--", lw=1.0)

    plt.xscale(scale)
    plt.yscale(scale)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()

    return fig, ax
