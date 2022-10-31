
import pygame
import cv2
import imutils
import numpy as np


filename="stylized.jpg"
x_size=800
y_size=600
image=cv2.imread(filename)
image=cv2.resize(image, (x_size, y_size))
image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
data=""
lines=[]


def convert_arc(pt1, pt2, sagitta):
    # extract point coordinates
    x1, y1 = pt1
    x2, y2 = pt2

    # find normal from midpoint, follow by length sagitta
    n = np.array([y2 - y1, x1 - x2])
    n_dist = np.sqrt(np.sum(n ** 2))

    if np.isclose(n_dist, 0):
        # catch error here, d(pt1, pt2) ~ 0
        print('Error: The distance between pt1 and pt2 is too small.')

    n = n / n_dist
    x3, y3 = (np.array(pt1) + np.array(pt2)) / 2 + sagitta * n

    # calculate the circle from three points
    # see https://math.stackexchange.com/a/1460096/246399
    A = np.array([
        [x1 ** 2 + y1 ** 2, x1, y1, 1],
        [x2 ** 2 + y2 ** 2, x2, y2, 1],
        [x3 ** 2 + y3 ** 2, x3, y3, 1]])
    M11 = np.linalg.det(A[:, (1, 2, 3)])
    M12 = np.linalg.det(A[:, (0, 2, 3)])
    M13 = np.linalg.det(A[:, (0, 1, 3)])
    M14 = np.linalg.det(A[:, (0, 1, 2)])

    if np.isclose(M11, 0):
        # catch error here, the points are collinear (sagitta ~ 0)
        print('Error: The third point is collinear.')

    cx = 0.5 * M12 / M11
    cy = -0.5 * M13 / M11
    radius = np.sqrt(cx ** 2 + cy ** 2 + M14 / M11)

    # calculate angles of pt1 and pt2 from center of circle
    pt1_angle = 180 * np.arctan2(y1 - cy, x1 - cx) / np.pi
    pt2_angle = 180 * np.arctan2(y2 - cy, x2 - cx) / np.pi

    return (cx, cy), radius, pt1_angle, pt2_angle


def draw_ellipse(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness=1, lineType=cv2.LINE_AA, shift=10):
    # uses the shift to accurately get sub-pixel resolution for arc
    # taken from https://stackoverflow.com/a/44892317/5087436
    center = (
        int(round(center[0] * 2 ** shift)),
        int(round(center[1] * 2 ** shift))
    )
    axes = (
        int(round(axes[0] * 2 ** shift)),
        int(round(axes[1] * 2 ** shift))
    )
    cv2.ellipse(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness, lineType, shift)
    return img


def draw(img, p1, p2, sag, thick, colour):
    if sag == 0:
        img = cv2.line(img, p1, p2, color=colour, thickness=thick)
        return img
    else:

        center, radius, start_angle, end_angle = convert_arc(p1, p2, sag)
        axes = (radius, radius)
        img = draw_ellipse(img, center, axes, 0, start_angle, end_angle, color=colour, thickness=thick)

        return img
with open("data.txt", 'r') as op:
    data=op.read()
data=data.split('\n')
lines=[eval(i) for i in data]
for obj in lines:
    temp_sag = 0
    pointarray = []
    for param in obj:
        if type(param)==list:
            pointarray=param
        if type(param)==int:
            temp_sag=param
    draw(image, pointarray[0], pointarray[1], temp_sag, 1, (255, 0, 0))
while True:
    pgimg=imutils.rotate_bound(image, -90)
    gameDisplay = pygame.display.set_mode((x_size,y_size))
    points=[]
    Sag=0
    strSag=""
    surf = pygame.surfarray.make_surface(pgimg)

    run=True
    temp:np.ndarray





    while run:

        #gameDisplay.blit(textinput.surface, (10, 10))
        gameDisplay.blit(surf, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN and len(points)!=2:
                temp=np.copy(image)
                points.append(pygame. mouse. get_pos())
                points[-1]=(x_size-points[-1][0], points[-1][1])
                temp=cv2.circle(temp, points[-1], 5, (255, 0, 0), -1)
                gameDisplay = pygame.display.set_mode((x_size, y_size))
                pgimg = imutils.rotate_bound(temp, -90)
                surf = pygame.surfarray.make_surface(pgimg)
                #pygame.draw.circle(surf, pygame.Color("Green"), pygame. mouse. get_pos(), 5, 0)
                if len(points)==2:
                    #pygame.draw.line(surf, pygame.Color("Green"), points[0], points[1], 2)
                    temp=np.copy(image)
                    temp=draw(temp, points[0], points[1], 0, 1, (255, 0, 0))
                    gameDisplay = pygame.display.set_mode((x_size, y_size))
                    pgimg = imutils.rotate_bound(temp, -90)
                    surf = pygame.surfarray.make_surface(pgimg)

                #if len(points) == 3:
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key)=="e":
                    run=False
                a=0
                try:
                    a=int(strSag)
                except:
                    if strSag!='-' :
                        strSag=""
                if(a==Sag):
                    strSag=""
                strSag+=pygame.key.name(event.key)[1:-1] if pygame.key.name(event.key)[1:-1]!="etur" else ""
                if pygame.key.name(event.key)[1:-1]=="etur":
                    temp = np.copy(image)
                    temp = draw(temp, points[0], points[1], int(strSag), 1, (255, 0, 0))
                    Sag=int(strSag)
                    gameDisplay = pygame.display.set_mode((x_size, y_size))
                    pgimg = imutils.rotate_bound(temp, -90)
                    surf = pygame.surfarray.make_surface(pgimg)

                #surf.set_at(pygame. mouse. get_pos(), (255, 0, 255))
        pygame.display.flip()
    with open("data.txt", 'a') as op:
        if(points!=[]):
            op.write(str([points, Sag]))
            op.write('\n')
    print(points, Sag)
    pygame.quit()
    try:
        image=draw(image, points[0], points[1], Sag, 1, (255, 0, 0))
    except:
        pass
