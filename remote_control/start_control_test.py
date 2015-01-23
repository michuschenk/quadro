import pygame as pg
import usb

# Initialise pygame (also initialises pygame.joystick, ...).
pg.init()

# PS3 joystick.
# Parameters
js_max_val = 1.    # Max range of PS3 joystick values.
js_scale_val = 100 # Scaling of PS3 joystick values.
js_thr = 1         # Threshold to update joystick values.

# Get and intialise PS3 joystick.
for i in range(pg.joystick.get_count()):
    js = pg.joystick.Joystick(i)
    if 'playstation' in js.get_name().lower():
        ps3_js = js
        print('Found PS3 Joystick')
        break
xl_o, xr_o, yl_o, yr_o = 0., 0., 0., 0.

try:
    ps3_js.init()
except NameError as err:
    print('Problem with PS3 joystick initialisation. Error message:')
    print(err)
    print('Exiting...')
    exit(-101)

# Start main loop.
done = False
clock = pg.time.Clock()
while not done:
    for event in pg.event.get():
        if event.type == pg.JOYAXISMOTION:
            # Read out joystick axes. scale and cast to int for smaller
            # size (-> transmission via xbee). Maybe use signed short?!
            left_axis = [ ps3_js.get_axis(0), ps3_js.get_axis(1) ]
            right_axis = [ ps3_js.get_axis(2), ps3_js.get_axis(3) ]

            xl = int(js_scale_val * left_axis[0] / js_max_val / 2.)
            yl = int(-js_scale_val * left_axis[1] / js_max_val / 2.)
            xr = int(js_scale_val * right_axis[0] / js_max_val / 2.)
            yr = int(-js_scale_val * right_axis[1] / js_max_val / 2.)

            # Only print if there is a change of any of the joysticks.
            # Difference must be larger than 'tol'.
            if(abs(xl-xl_o) > js_thr or abs(xr-xr_o) > js_thr or
                    abs(yl-yl_o) > js_thr or abs(yr-yr_o) > js_thr):
                print('%d\t %d\t %d\t %d' % (xl, yl, xr, yr))
                xl_o, xr_o, yl_o, yr_o = xl, xr, yl, yr

        # Buttons 10 and 11 are L1 and R1 resp. Leave loop if both
        # are pressed.
        elif(ps3_js.get_button(10) and ps3_js.get_button(11)):
            done = True

ps3_js.quit()
