import pygame as pg
import numpy as np
import usb
from sys import stdout

# Initialise pygame (also initialises pygame.joystick, ...).
pg.init()

# Get and intialise PS3 joystick.
js_max_val = 1.
js_scale_val = 100
for i in range(pg.joystick.get_count()):
    js = pg.joystick.Joystick(i)
    if 'playstation' in js.get_name().lower():
        print 'Found PS3 Joystick'
        ps3_js = js
        break
ps3_js.init()

done = False
clock = pg.time.Clock()
xl_o, xr_o, yl_o, yr_o = 0., 0., 0., 0.
tol = 1
while not done:
	for event in pg.event.get():
		if event.type == pg.JOYAXISMOTION:
			left_axis = [ ps3_js.get_axis(0), ps3_js.get_axis(1) ]
			right_axis = [ ps3_js.get_axis(2), ps3_js.get_axis(3) ]

			xl = int(js_scale_val * left_axis[0] / js_max_val / 2.)
			yl = int(-js_scale_val * left_axis[1] / js_max_val / 2.)
			xr = int(js_scale_val * right_axis[0] / js_max_val / 2.)
			yr = int(-js_scale_val * right_axis[1] / js_max_val / 2.)

			if(abs(xl-xl_o) > tol or abs(xr-xr_o) > tol or
					abs(yl-yl_o) > tol or abs(yr-yr_o) > tol):
				xl_o, xr_o, yl_o, yr_o = xl, xr, yl, yr
				print '%d, %d, %d, %d' % (xl, yl, xr, yr)
ps3_js.quit()
