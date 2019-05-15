import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    for command in commands:
        if command["op"] == "push":
            stack.append( [x[:] for x in stack[-1]])
        elif command["op"] == "pop":
            stack.pop()
        elif command["op"] == "move":
            t = make_translate(command["args"][0],\
                           command["args"][1],\
                           command["args"][2],)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command["op"] == "rotate":
            theta = command["args"][1] * (math.pi / 180)
            if command["args"][0] == 'x':
                t = make_rotX(theta)
            elif command["args"][0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command["op"] == "scale":
            t = make_scale(command["args"][0],\
                           command["args"][1],\
                           command["args"][2],)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command["op"] == "box":
            add_box(tmp,\
                        command["args"][0],\
                        command["args"][1],\
                        command["args"][2],\
                        command["args"][3],\
                        command["args"][4],\
                        command["args"][5])
            matrix_mult( stack[-1], tmp )
            if command["constants"] != None:
                draw_polygons(tmp, screen,\
                            zbuffer, view,\
                            ambient, light,\
                            symbols, command["constants"])
            else:
                draw_polygons(tmp, screen,\
                            zbuffer, view,\
                            ambient, light,\
                            symbols, reflect)
            tmp = []
        elif command["op"] == "sphere":
            add_sphere(tmp,\
                        command["args"][0],\
                        command["args"][1],\
                        command["args"][2],\
                        command["args"][3],\
                        step_3d)
            matrix_mult( stack[-1], tmp )
            if command["constants"] != None:
                draw_polygons(tmp, screen,\
                            zbuffer, view,\
                            ambient, light,\
                            symbols, command["constants"])
            else:
                draw_polygons(tmp, screen,\
                            zbuffer, view,\
                            ambient, light,\
                            symbols, reflect)
            tmp = []

        elif command["op"] == "torus":
            add_torus(tmp,\
                        command["args"][0],\
                        command["args"][1],\
                        command["args"][2],\
                        command["args"][3],\
                        command["args"][4],\
                        step_3d)
            matrix_mult( stack[-1], tmp )
            if command["constants"] != None:
                draw_polygons(tmp, screen,\
                            zbuffer, view,\
                            ambient, light,\
                            symbols, command["constants"])
            else:
                draw_polygons(tmp, screen,\
                            zbuffer, view,\
                            ambient, light,\
                            symbols, reflect)
            tmp = []
        elif command["op"] == "line":
            add_edge( edges,\
                      command["args"][0],\
                      command["args"][1],\
                      command["args"][2],\
                      command["args"][3],\
                      command["args"][4],\
                      command["args"][5])
            matrix_mult( systems[-1], edges )
            draw_lines(eges, screen, zbuffer, color)
            edges = []

        elif command["op"] == "constants":
            pass
        elif command["op"] == "save":
            save_extension(screen, command["args"][0] + ".png")
        elif command["op"] == "display":
            display(screen)
        else:
            print command
