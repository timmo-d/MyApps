from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from django.http import HttpResponse
from django.urls import reverse
from bokeh.resources import CDN
from bokeh.embed import components
import math
# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, 'plotter/index.html')
        #return HttpResponse(reverse('plotter:index'))

    elif request.method == "POST":
        domain  = request.POST['domain'].split()
        eqn     = request.POST['equation']
        domain = range( int(domain[0]), int(domain[1]) )
        y = [ eval(eqn) for x in domain ]
        title = 'y = ' + eqn

        plot = figure(title= title , x_axis_label= 'X-Axis', y_axis_label= 'Y- Axis', plot_width =400, plot_height =400)
        plot.line(domain, y, legend= 'f(x)', line_width = 2)
        script, div = components(plot)

        return render(request, 'plotter/index.html', {'script' : script , 'div' : div} )


    else:
        pass