from defs import *

back_colour = 'grey'

def fill_cell(pos, color, context):
        canvas = context.canvas
        h = context.h
        xl = context.x + pos.x * h
        xr = xl + h
        yt = context.y + pos.y * h
        yb = yt + h
        canvas.create_rectangle(xl, yt, xr - 1, yb - 1, fill=color)
        
        #

def mark_side(pos, side, color, d, context, wid, leng):
    
        
        canvas = context.canvas
        h = context.h
        
        xl = context.x + pos.x * h
        yt = context.y + pos.y * h
        
        
        e = edge[side]
        
        v0 = vert[e[0]]
        v1 = vert[e[1]]
        
        x0 = v0[0] * h
        y0 = v0[1] * h
        
        x1 = v1[0] * h
        y1 = v1[1] * h
        
        dx = (x1 - x0)
        dy = (y1 - y0)
        
        x01 = xl + x0 + dx * wid
        y01 = yt + y0 + dy * wid
        
        x11 = xl + x1 - dx * wid
        y11 = yt + y1 - dy * wid
        
        x2 = (x01 + x11) * 0.5 + dy * leng * d
        
        y2 = (y01 + y11) * 0.5 - dx * leng * d
    
        canvas.create_polygon(((x01, y01), (x11, y11), (x2, y2)), fill=color)
    
     

class Piece:
    
    def __init__(self):
        self.segments = None
        self.colour = None
        
    def  process_train(self, train, sideIn):
        train.crashed = True
        return None
        
class Cell:
    
    def __init__(self, pos, node_list, nodes, world):
        
        self.nodes = node_list
        self.track = None
        self.painter = None
        self.pos = pos
        self.piece = Piece()
        self.world = world
        
        for n in node_list:
            nodes[n].cells.append(self)
            
        self.cellAt = [None, None, None, None]
        
        
    def getSegments(self):
        
        
        return self.piece.segments
        
        #if self.painter:
            
            
            
class Edge:
    
    def __init__(self):
        self.cells = []
        
    

class Pos:
    
    def __init__(self, posC, w):
        self.i = posC
        self.x = posC % w
        self.y = posC / w
    
    
    
class World:
    
    
    def __init__(self, width, height):
        self.goals = []
        self.outlets = []
        self.splitters = []
        self.painters = []
        self.rocks = []
        self.tracks = []
        self.trains = []
        self.piece = None
        
        self.width = width
        self.height = height
        
        self.gene_length = 10
        self.maxTok = 20
        
        self.cells = []
        self.global_sides = []
        
        self.flips = []
        
        node_ref = 0
        
        n_node = width * (height + 1) + height * (width + 1)
        
        
        self.global_edges = [Edge() for _ in range(n_node)]
        
        
        
        for i in range(height):
        
            for j in range(width):
                
                posC = i * width + j
                pos = Pos(posC, width)
                n_top = node_ref + j
                n_bot = n_top + width + 1
                n_left = i + width
                n_right = n_left + 1
                self.cells.append(Cell(pos, (n_top, n_right, n_bot, n_right), self.global_edges, self))
                
        
        cnt = 0
        
        for i in range(height):
        
            for j in range(width):
                n_top = node_ref + j
                n_bot = n_top + width + 1
                n_left = i + width
                n_right = n_left + 1
        
                c = self.cells[cnt]
                
                if i > 0 :
                    c.cellAt[0] = self.cells[(i - 1) * width + j]
               
                if j < (width - 1):
                    c.cellAt[1] = self.cells[i * width + j + 1]
                
                if i < (height - 1):
                    c.cellAt[2] = self.cells[(i + 1) * width + j]
            
                if j > 0 :
                    c.cellAt[3] = self.cells[i * width + j - 1]
                
                cnt += 1
                
        
            
    def draw(self, context):
        
        self.draw_grid(context)
        
        for g in self.goals:
            g.draw(context)
       
        for o in self.outlets:
            o.draw(context)
       
        for o in self.rocks:
            o.draw(context)
        
        
        for o in self.painters:
            o.draw(context)
       
       
        for o in self.splitters:
            o.draw(context)
       
        for o in self.tracks:
            o.draw(context)
       
        for t in self.trains:
            t.draw(context)
       
       
    def draw_grid(self, context):
        
        
        canvas = context.canvas
        xl = context.x
        xr = xl + context.h * self.width
        yt = context.y
        yb = yt + context.h * self.height
   
        canvas.create_rectangle(xl, yt, xr, yb, fill=back_colour)
   
        for i in range(self.width + 1):
            x = context.x + i * context.h
            canvas.create_line(x, yt, x, yb, fill="black")
        
        for j in range(self.height + 1):
            
            y = context.y + j * context.h
            canvas.create_line(xl, y, xr, y, fill="black")
        
    def init_run(self):
        for outlet in self.outlets:
            outlet.reset()
        
        self.running = True
      
    def step(self):
        
        self.flips = []
        
        for train in self.trains:
            train.step()
            
        for outlet in self.outlets:
            outlet.step()
            
            
        for seg in self.flips:
            if len(seg) == 1:
                continue
            
            segTmp = seg[0]
            seg[0] = seg[1]
            seg[1] = segTmp
            
        
        
        
        
 
class Track(Piece):       

    def __init__(self, cell, typ):
        Piece.__init__(self)
        
        self.segments = list(segments_from_type[typ])
        self.cell = cell
        self.typ = typ
        cell.piece = self
        
    def  process_train(self, train, sideIn):
             
        for segId in self.segments:
            seg = seg_sides[segId]
            if seg[0] == sideIn:
                train.side = seg[1]
                self.cell.world.flips.append(self.segments)
                train.cell = self.cell
                return
            elif seg[1] == sideIn:
                train.side = seg[0]
                self.cell.world.flips.append(self.segments)
                train.cell = self.cell
                return
        
        train.crashed = True
       
    def draw(self, context):
        
        canvas = context.canvas
        h = context.h
        pos = self.cell.pos
        xl = context.x + pos.x * h
        yt = context.y + pos.y * h
        
        context.canvas.create_text(xl + h / 3., yt + h / 3.0, text=self.typ)
        #return
        
        segments = self.segments # track_from_type[self.typ]
        
        wid2 = h / 6
        #wid=2*wid2
        
        for iseg in reversed(segments):
            seg = seg_sides[iseg]
            if len(seg) == 2:
                p0 = midside[seg[0]]
                p1 = midside[seg[1]]
                
                x0 = xl + p0[0] * h
                y0 = yt + p0[1] * h
                
                x1 = xl + p1[0] * h
                y1 = yt + p1[1] * h
                
                dy = abs(x1 - x0) / 6
                dx = abs(y1 - y0) / 6
                
                
                canvas.create_rectangle(x0 - dx, y0 - dy, x1 + dx, y1 + dy, fill="blue")
                
            else:
                iv = seg[2]
                x = xl + vert[iv][0] * h
                y = yt + vert[iv][1] * h
                
                
                canvas.create_arc(x - h / 2 - wid2, y - h / 2 - wid2, x + h / 2 + wid2, y + h / 2 + wid2, start=seglim[iv][0], extent=seglim[iv][1], fill='blue')
                canvas.create_arc(x - h / 2 + wid2, y - h / 2 + wid2, x + h / 2 - wid2, y + h / 2 - wid2, start=seglim[iv][0], extent=seglim[iv][1], fill=back_colour)
                
                
        

        
class Goal(Piece):

    def __init__(self, cell, sides, colours):
        self.cell = cell
        self.peice = self
        self.sides = sides
        self.colours = colours
        
    def draw(self, context):
     
     
        pos = self.cell.pos
        fill_cell(pos, "black", context)   
        
        for side in self.sides:
            mark_side(pos, side, "white", -1, context, .1, .2)
       
        
        dxx = dyy = context.h / 8
        
        cnt = 0
        n = len(self.colours)
        for i in range(3):
            x = context.h * (pos.x + i / 4.0 + 0.25) + dxx
            for j in range(3):
                y = context.h * (pos.y + j / 4.0 + 0.25) + dyy
                context.canvas.create_oval(x - dxx, y - dyy, x + dxx, y + dyy, fill=colour_name[self.colours[cnt]])  
                cnt += 1
                if cnt == n:
                    return
               
         
                
       
class OutLet(Piece):

    def __init__(self, cell, side, colours):
        self.cell = cell
        cell.peice = self
        self.side = side
        self.colours = colours
        self.queue = colours[:]
        self.done = False
        self.trains = []
        
    def reset(self):
        self.queue = self.colours[:]
        
    def draw(self, context):
        
        dxx = dyy = context.h / 8
        pos = self.cell.pos
        mark_side(pos, self.side, "white", 1, context, .1, .2)
        
        cnt = 0
        n = len(self.colours)
        for i in range(3):
            x = context.h * (pos.x + i / 4.0 + 0.25) + dxx
            for j in range(3):
                y = context.h * (pos.y + j / 4.0 + 0.25) + dyy
                context.canvas.create_oval(x - dxx, y - dyy, x + dxx, y + dyy, fill=colour_name[self.colours[cnt]])
                cnt += 1
                if cnt == n:
                    return

    def step(self):
        
        if not self.queue:
            return
        
        colour = self.queue.pop()
        self.cell.world.trains.append(Train(self.cell, self.side, colour))
        
        
    def debug(self):
        print self.pos.x, self.pos.y, self.side, self.colours
        
        
  
class Painter(Piece):
    
    def __init__(self, cell, sideA, sideB, color):
        Piece.__init__(self)
        
        self.cell = cell
        cell.piece = self
        self.sideA = sideA
        self.sideB = sideB
        self.colour = color
        self.debug()
       
           
    def  process_train(self, train, sideIn):
             
            if self.sideA == sideIn:
                train.side = self.sideB
        
            elif self.sideB == sideIn:
                train.side = self.sideA
            else:
                train.crashed = True
                return
            
            train.colour = self.colour
            train.cell = self.cell
            
  
    def draw(self, context):
        pos = self.cell.pos
        x = context.h * (pos.x + 0.5)
        y = context.h * (pos.y + 0.5)
        
        mark_side(pos, self.sideA, colour_name[self.colour], -1, context, .1, .2)
        mark_side(pos, self.sideB, colour_name[self.colour], -1, context, .1, .2)
       
        context.canvas.create_text(x, y, fill=colour_name[self.colour], text="P")
        
   
    
    def debug(self):
        pass
        #print self.pos.x,self.pos.y,self.side
                
          
      
class Splitter:

    def __init__(self, cell, side):
        self.cell = cell
        cell.piece = self
        self.side = side
        #self.debug()
        
    def draw(self, context):
        
        h = context.h
        pos = self.cell.pos
        x = pos.x * h + context.x
        y = pos.y * h + context.y
        pIn = midside[self.side]
     
           
        xIn = x + pIn[0] * h
        yIn = y + pIn[1] * h
     
        pClock = midside[nextClock(self.side)]
        xClock = x + pClock[0] * h
        yClock = y + pClock[1] * h
     
        pAnti = midside[nextAnti(self.side)]
        xAnti = x + pAnti[0] * h
        yAnti = y + pAnti[1] * h
        
        context.canvas.create_line(xIn, yIn, xClock, yClock, fill="white")
        context.canvas.create_line(xIn, yIn, xAnti, yAnti, fill="white")
                


  
class Train:
    
    def __init__(self, cell, side, color):
        #self.pos=pos
        self.colour = color
        self.side = side
      
        self.cell = cell    
        #self.node=self.cell.nodes[side]
        self.crashed = False
        
    def draw(self, context):
        
        #print " HELLO FROM TRAIN DRAW "
        
        canvas = context.canvas
        h = context.h
        
        mark_side(self.cell.pos, self.side, colour_name[self.colour], 1, context, .1, .3)
            #context.canvas.create_string(x, y,text="T")
    
    def step(self):
        
        #print " STEP TRAIN ",self
        if self.crashed:
            return
        
        cellNext = self.cell.cellAt[self.side]
        sideIn = (self.side + 2) % 4

        print cellNext.piece
        
        cellNext.piece.process_train(self, sideIn)

    
    
    
class Rock:

    def __init__(self, pos):
        self.pos = pos
        
    def draw(self, context):
        x = context.h * (self.pos.x + 0.5)
        y = context.h * (self.pos.y + 0.5)
        
        context.canvas.create_string(x, y, text="R")
        
                
                            