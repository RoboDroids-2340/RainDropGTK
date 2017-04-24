#!/usr/bin/python3

from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
import matplotlib.cm as cm
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


class HistoricalGraph(object):
    def __init__(self, avg_ppm, _type, year):
        graph_window = Gtk.Window()
        graph_window.connect("delete-event", graph_window.destroy)
        graph_window.set_default_size(500, 500)

        fig = Figure(figsize=(5,5), dpi=100)
        ax = fig.add_subplot(111)

        
        ax.plot([i for i in range(1,13)], avg_ppm)

        ax.set_title("{0} PPM for the year of {1}".format('Virus' if _type == 'v' else 'Contaminant', str(year)))
        ax.set_xlabel('Month')
        ax.set_ylabel("{0} PPM".format('Virus' if _type == 'v' else 'Contaminant'))
        ax.xaxis.set_ticks([i for i in range(1,13)])
        sw = Gtk.ScrolledWindow()
        graph_window.add(sw)

        canvas = FigureCanvas(fig)
        canvas.set_size_request(400,400)
        sw.add_with_viewport(canvas)

        graph_window.show_all()
