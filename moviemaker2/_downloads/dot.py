import Tkinter
import os.path
import numpy
from moviemaker2 import *
from moviemaker2.rasterisers.distance import Distance
import moviemaker2.ext.tk
import moviemaker2.ext.PIL_from_argb
import moviemaker2.ext.render

tk = Tkinter.Tk()
render_frame = moviemaker2.ext.tk.RenderFrame(tk, nbins=100)
render_frame.pack()

shape = (300, 400)
(shapey, shapex) = shape

zeros = numpy.zeros(shape)
ones = numpy.ones(shape)

Y = numpy.linspace(-3, 3, shapey)[:, numpy.newaxis].repeat(shapex, axis=1)
X = numpy.linspace(-4, 4, shapex)[numpy.newaxis, :].repeat(shapey, axis=0)
mesh_array = numpy.asarray([Y.T, X.T]).T

point_position = asmatharray([-numpy.sin(p('time/real')), 
                              numpy.cos(p('time/real'))]) * 2
mesh = Extension(p=p('mesh'), value=mesh_array)
point_mask = mesh | numpy.exp(-Distance(p('mesh') - point_position) ** 2 / \
    0.1 ** 2)
point = asmatharray([point_mask,
                     point_mask,
                     0.2 * point_mask,
                     zeros])

white = numpy.asarray([ones, ones, ones, ones])
alpha = AlphaBlendRasterStack(background=white)
alpha ^ point

pil = moviemaker2.ext.PIL_from_argb.PILfromARGB()
render = moviemaker2.ext.render.Render(fn=(alpha | pil))

render(framerate=25, directory='Frames', extension='jpg', 
    startrealtime=0, stoprealtime=6.5,
    render_queue=render_frame.render_queue)

tk.mainloop()
