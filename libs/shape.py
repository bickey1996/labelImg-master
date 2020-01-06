#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import distance
import sys

DEFAULT_LINE_COLOR = QColor(0, 255, 0, 128)
DEFAULT_FILL_COLOR = QColor(255, 0, 0, 128)
DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QColor(0, 128, 255, 155)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 0, 0)
MIN_Y_LABEL = 10

FIRST_VERTEX_COLOR = QColor(255, 255, 255, 255)

class Shape(object):
    P_SQUARE, P_ROUND = range(2)
    MAX_POINTS = 4

    MOVE_VERTEX, NEAR_VERTEX = range(2)

    # The following class variables influence the drawing
    # of _all_ shape objects.
    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
    point_type = P_SQUARE
    point_size = 24
    scale = 1.0

    def __init__(self, label=None, line_color=None, difficult=False,crew=False,fake=False,occluded=False,reflection=False,behindglass=False, paintLabel=False):
        self.label = label
        self.points = []
        self.cursor_points = []
        self.intersects = []
        self.fill = False
        self.selected = False
        self.difficult = difficult
        self.crew = crew
        self.fake = fake
        self.occluded = occluded
        self.reflection = reflection
        self.behindglass = behindglass
        self.paintLabel = paintLabel

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

    def close(self):
        self._closed = True

    def reachMaxPoints(self):
        if len(self.points) >= 40:
            return True
        return False

    def isLastPoint(self):
        if len(self.points) >= self.MAX_POINTS:
            return True
        return False

    def addPoint(self, point):
        if not self.reachMaxPoints():
            self.points.append(point)
            self.cursor_points.append(point)

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def paint(self, painter, curr):
        if self.points:
            color = self.select_line_color if self.selected else self.line_color
            # color = QColor(255, 255, 255, 255) if curr else color
            pen = QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.4 / self.scale))))
            pen.setStyle(Qt.DashDotLine)
            painter.setPen(pen)

            line_path = QPainterPath()
            vrtx_path = QPainterPath()
            first_vrtx_path = QPainterPath()

            line_path.moveTo(self.points[0])
            # Uncommenting the following line will draw 2 paths
            # for the 1st vertex, and make it non-filled, which
            # may be desirable.
            # self.drawVertex(vrtx_path, 0)
            for i, p in enumerate(self.points):
                line_path.lineTo(p)
                # print("i : {}, p : {}, curr : {}, len : {}".format(i, p, curr , len(self.points)))
                if curr and i ==0 :
                    self.drawVertex(first_vrtx_path, i)
                else:
                    self.drawVertex(vrtx_path, i)
                # self.drawVertex(vrtx_path, i)

            if self.isClosed():
                line_path.lineTo(self.points[0])

            # print("vrtx : ", vrtx_path.length())
            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)

            # painter.fillPath(vrtx_path, QColor(255, 255, 255, 255))
            painter.fillPath(vrtx_path, self.vertex_fill_color)
            painter.setPen(QPen(FIRST_VERTEX_COLOR))
            painter.fillPath(first_vrtx_path, QBrush(FIRST_VERTEX_COLOR))
            painter.drawPath(first_vrtx_path)

            # Draw text at the top-left
            if self.paintLabel:
                min_x = sys.maxsize
                min_y = sys.maxsize
                for point in self.points:
                    min_x = min(min_x, point.x())
                    min_y = min(min_y, point.y())
                if min_x != sys.maxsize and min_y != sys.maxsize:
                    font = QFont()
                    font.setPointSize(int(round(14.0/self.scale)))
                    font.setBold(True)
                    painter.setFont(font)
                    if(self.label == None):
                        self.label = ""
                    if(min_y < MIN_Y_LABEL):
                        min_y += MIN_Y_LABEL
                    # print("sdfgh: ", self.label, min_x, min_y)
                    painter.drawText(min_x, min_y, self.label)

            if self.fill:
                color = self.select_fill_color if self.selected else self.fill_color
                painter.fillPath(line_path, color)

    def drawVertex(self, path, i):
        # return
        d = self.point_size / self.scale
        shape = self.point_type
        if(i<len(self.cursor_points) and i>=0):
            point = self.cursor_points[i]

        
        if i == self._highlightIndex :
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = Shape.vertex_fill_color

        # if i == 0:
        #     self.vertex_fill_color = QColor(255, 255, 255, 255)
        if shape == self.P_SQUARE:
            #path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
            # path.addRect(point.x() - d/2, point.y() , 50,1)
            # path.addRect(point.x() , point.y() - d/2, 1,50)
            # Changed here
            path.addRect(point.x() - d/2, point.y(), d, 2)
            path.addRect(point.x(), point.y() - d/2, 2, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def nearestVertex(self, point, epsilon):
        for i, p in enumerate(self.points):
            if distance(p - point) <= epsilon:
                return i
        return None
    
    def nearestCursor(self, point, epsilon):
        for i, p in enumerate(self.cursor_points):
            if distance(p - point) <= epsilon:
                return i
        return None

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def makePath(self):
        path = QPainterPath(self.points[0])
        for p in self.points[1:]:
            path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.points = [p + offset for p in self.points]
        self.cursor_points = [p + offset for p in self.cursor_points]

    def moveVertexBy(self, i, offset):
        self.points[i] = self.points[i] + offset
    
    def moveCursorBy(self, i, offset):
        self.cursor_points[i] = self.cursor_points[i] + offset

    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        shape = Shape("%s" % self.label)
        shape.points = [p for p in self.points]
        shape.fill = self.fill
        shape.selected = self.selected
        shape._closed = self._closed
        if self.line_color != Shape.line_color:
            shape.line_color = self.line_color
        if self.fill_color != Shape.fill_color:
            shape.fill_color = self.fill_color
        shape.difficult = self.difficult
        shape.crew = self.crew
        shape.fake = self.fake
        shape.occluded = self.occluded
        shape.reflection = self.reflection
        shape.behindglass = self.behindglass
        return shape


    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
