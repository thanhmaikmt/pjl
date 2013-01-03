from defs import *

import array
import random


back_colour = 'grey'
track_colour = 'grey38'

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
        
        x01 = xl + x0 + dx * (0.5 - wid)
        y01 = yt + y0 + dy * (0.5 - wid)
        
        x11 = xl + x1 - dx * (0.5 - wid)
        y11 = yt + y1 - dy * (0.5 - wid)
        
        x2 = (x01 + x11) * 0.5 + dy * leng * d
        
        y2 = (y01 + y11) * 0.5 - dx * leng * d
    
        canvas.create_polygon(((x01, y01), (x11, y11), (x2, y2)), fill=color)
    
     

class Gene:
    
    def clone(self):
        g=Gene()
        g.str=self.str[:]
        return g
    
    
class Piece:
    
    def __init__(self, cell):
        
        self.cell = cell
        cell.piece = self
        
    def  process_train(self, train):
        self.cell.world.handle_crash(train)

        
    def draw(self, context):
        pass
    
    def reset(self):
        
        pass
    

    
class Cell:
    
    def __init__(self, pos, world, edges):
    
        self.pos = pos
        self.piece = None       # Default to blank
        self.world = world
        
        self.cellAt = [None, None, None, None]
        
        self.edgeAt = edges
        
    def edge_pos(self,edge):
        return self.pos.x+midside[edge][0],self.pos.y+midside[edge][1]
                   
            
class Edge:
    
    def __init__(self):
        self.cells = []
        
    
class TrainCrash(Exception):
    
    def __init__(self, train):
            self.train = train

    def __str__(self):
        return " Train crash "

class Pos:
    
    def __init__(self, posC, w):
        self.i = posC
        self.x = posC % w
        self.y = posC / w
    
class World:
    
    
    def __init__(self, width, height):
        
       
        self.width = width
        self.height = height
        self.cells =  []
        self.nulls = []
        self.goals = []
        self.outlets=[]
        self.trains =[]
        
        # TODO move else where
        self.gene_length = width*height
        self.maxTok = len(segments_from_type)
        
        
        node_ref = 0       
        
        for i in range(height):
        
            for j in range(width):
                
                posC = i * width + j
                pos = Pos(posC, width)
        
                n_top = node_ref + j
                n_bot = n_top + 2 * width + 1
                
                n_left = n_top + width
                n_right = n_left + 1
                
                self.cells.append(Cell(pos, self, (n_top, n_right, n_bot, n_left)))
            node_ref = n_right + 1
        
        cnt = 0
        
        for i in range(height):
        
            for j in range(width):
                
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
 
       
 
                
    def rebuild_from_gene(self,gene):
        
            
        # reset any existing tracks
        for cell in self.cells:
            if isinstance(cell.piece,Track):
                cell.piece=None 
                
        for i in range(self.gene_length):
            if self.cells[i].piece != None:
                continue
            
            id=gene.str[i]
            
            if id >0:
                Track(self.cells[i],segments_by_id[id],char_from_id[id])
        
            
        self.reset()
                
            
    def draw(self, context):
        
        self.draw_grid(context)
        
        for c in self.cells:
            if c .piece != None:
                c.piece.draw(context)
 
        for outlet in self.outlets:
            outlet.draw(context)
            
        
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
        
        
    def reset(self):
        
        self.done = False
        
        for outlet in self.outlets:
            outlet.reset()
 
        for cell in self.cells:
            if cell.piece:
                cell.piece.reset()
        
        self.running = True
      
        self.travels = []
        self.trains = []
        self.scrap = []
        self.queue = self.outlets[:]
        
        
        
      
      
    def step(self):
        
        
        self.travels = []
        self.newtrains = []
        
        try:
            for train in self.trains:
                train.step()
                
        except TrainCrash as e:
            print " Exception :", e
            return
        
        
        self.trains.extend(self.newtrains)
            
        done = []
        for outlet in self.queue:
            outlet.step()
            if not outlet.queue:
                done.append(outlet)
                
        for outlet in done:
            self.queue.remove(outlet)    
            
        # process crashes mid segment
        
        for track in self.travels:
            
            if len(track.trains) == 2:
                
                # Check for a crossover mid segment

                seg1 = track.trains[0][1]
                seg2 = track.trains[1][1]
                
                if (seg1 == 1 and seg2 == 4) or (seg1 == 1 and seg2 == 4) or (seg1 == seg2): 
                    colour = mix_colours[track.trains[0][0].colour][track.trains[1][0].colour]
                    track.trains[0][0].colour = colour
                    track.trains[1][0].colour = colour
                    print " CROSSOVER SEG"
                    
                    
                    
                # check for a merger
                if track.trains[0][0].side == track.trains[1][0].side:
                    print " MERGER "
                    track.trains[0][0].colour = mix_colours[track.trains[0][0].colour][track.trains[1][0].colour]
                    track.trains[1][0].merged = True
                    
                    
               
            seg = track.segments
            track.trains = []
             
            if len(seg) == 1:
                continue
            
            segTmp = seg[0]
            seg[0] = seg[1]
            seg[1] = segTmp
            

        # check for crossovers on edges
        edge_to_train = {}
 
        for train in self.trains:    
 
            if not train.active():
                continue
            
            e = train.cell.edgeAt[train.side]
            #print e
            
            train2 = edge_to_train.get(e)
 
            if train2 != None:
                print " CROSSOVER  EDGE"
                colour = mix_colours[train.colour][train2.colour]
                train.colour = colour
                train2.colour = colour
            else:
                edge_to_train[e] = train
 
 
 
        
        scraps = []
        for train in self.trains:    
            if not train.active():
                scraps.append(train)
                
                
        for train in scraps:
            self.scrap.append(train)
            self.trains.remove(train)
       

               
        if self.trains or self.queue:
            return
       
        self.success()
       
    
    def handle_crash(self,train):
        
        self.done = True
        
        print "FINISHED FAIL ------------------------"
        
        print " Trains:",
        for train in self.trains:
            print train.debug(),
            
        print

        
        for goal in self.goals:
            goal.debug()
        
        raise TrainCrash(train)
        
        
    def success(self):

        self.done = True
        
        print "FINISHED SUCCESS ------------------------"
        
        print " Trains:",
        for train in self.scrap:
            print train.debug(),
            
        print

        
        for goal in self.goals:
            goal.debug()
            
            
     
    # ----------------------------------------------------------
    def blank_gene(self):
        g=Gene()  
        g.str=array.array('B',[0] * self.gene_length)
        return g
    
    def random_gene(self):
        g=self.blank_gene()
        for i in range(self.gene_length):
            g.str[i]=self.random_token()
        return g
        
    def mate(self,a,b):
            length=len(a.str)
            i=random.randint(1,length-1)
            g=Gene()        
            g.str=array.array('B',a.str[0:i]+b.str[i:length])
            return g
    
    def random_token(self):
            return random.randint(0,self.maxTok)
    
    def mutate(self,g): # randomly replace a character
        length=len(g.str)
        i=random.randint(0,length-1)
        #g2=g.clone()
        g.str[i]=self.random_token()
   
        
 
class Track(Piece):       

    def __init__(self, cell, segs, typ ):
        Piece.__init__(self, cell)
        
        self.segment_init = segs    # segments_from_type[typ]
     
        self.typ = typ
        self.reset()
     
    def reset(self):
        
        self.segments=list(self.segment_init)
        self.trains = []
        
        
    def  process_train(self, train):
             
        for segId in self.segments:
            
            seg = seg_sides[segId]
            
            if seg[0] == train.side:
                train.side = seg[1]
                self.cell.world.travels.append(self)
                self.trains.append((train, segId))
                return
            
            elif seg[1] == train.side:
                train.side = seg[0]
                self.cell.world.travels.append(self)
                self.trains.append((train, segId))
                return
            
            
        self.cell.world.handle_crash(self)
  
       
    def draw(self, context):
        
        canvas = context.canvas
        h = context.h
        pos = self.cell.pos
        xl = context.x + pos.x * h
        yt = context.y + pos.y * h
        
       
        #return
        
        segments = self.segments # track_from_type[self.typ]
        
        wid2 = h / 6
        #wid=2*wid2
        
        for iseg in reversed(segments):
            if iseg == None:
                print " TODO "
                continue
            
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
                
                
                canvas.create_rectangle(x0 - dx, y0 - dy, x1 + dx, y1 + dy, fill=track_colour)
                
            else:
                iv = seg[2]
                x = xl + vert[iv][0] * h
                y = yt + vert[iv][1] * h
                
                
                canvas.create_arc(x - h / 2 - wid2, y - h / 2 - wid2, x + h / 2 + wid2, y + h / 2 + wid2, start=seglim[iv][0], extent=seglim[iv][1], fill=track_colour)
                canvas.create_arc(x - h / 2 + wid2, y - h / 2 + wid2, x + h / 2 - wid2, y + h / 2 - wid2, start=seglim[iv][0], extent=seglim[iv][1], fill=back_colour)
                
                
        
        context.canvas.create_text(xl + 6 , yt + 12, text=self.typ)
        
class Goal(Piece):

    def __init__(self, cell, sides, colours):
        Piece.__init__(self, cell)
        self.sides = sides
        self.colours = colours
        cell.world.goals.append(self)
        self.reset()
     
    def process_train(self, train):
        
        
        #print " Goal: process "
        
        if train.side in self.sides:
            if train.colour in self.queue:
                self.queue.remove(train.colour)
                train.terminated = True
                return
    
        self.cell.world.handle_crash(train)    
        
    def reset(self):
        self.queue = self.colours[:]
        
            
    
    def debug(self):#
        
        print "Goal: ",
        for c in self.queue:
            print colour_name[c],
            
        print
    
    
    def draw(self, context):
     
     
        pos = self.cell.pos
        fill_cell(pos, "black", context)   
        
        for side in self.sides:
            mark_side(pos, side, "white", -1, context, .1, .2)
       
        
        dxx = dyy = context.h / 8
        
        cnt = 0
        n = len(self.queue)
        
        for i in range(3):
            x = context.h * (pos.x + i / 4.0 + 0.25) + dxx
            for j in range(3):
                if cnt == n:
                    return
                
                y = context.h * (pos.y + j / 4.0 + 0.25) + dyy
                context.canvas.create_oval(x - dxx, y - dyy, x + dxx, y + dyy, fill=colour_name[self.queue[cnt]])  
                cnt += 1
               
               
         
                
       
class OutLet(Piece):

    def __init__(self, cell, side, colours):
        Piece.__init__(self, cell)
        self.side = side
        self.colours = colours
        cell.world.outlets.append(self)
        self.reset()
        
    def reset(self):
        self.queue = self.colours[:]
        self.trains = []
        self.done = False
        
    def draw(self, context):
        
        dxx = dyy = context.h / 8
        pos = self.cell.pos
        mark_side(pos, self.side, "black", -1, context, .2, .2)
        
        cnt = 0
        n = len(self.queue)
        
        for i in range(3):
            x = context.h * (pos.x + i / 4.0 + 0.25) + dxx
            for j in range(3):
                if cnt == n:
                    return
                y = context.h * (pos.y + j / 4.0 + 0.25) + dyy
                context.canvas.create_oval(x - dxx, y - dyy, x + dxx, y + dyy, fill=colour_name[self.queue[cnt]])
                cnt += 1
             

    def step(self):
        
        if not self.queue:
            return
        
        colour = self.queue.pop()
        self.cell.world.trains.append(Train(self.cell, self.side, colour))
        
        
    def debug(self):
        print self.pos.x, self.pos.y, self.side, self.colours
        
        
  
class Painter(Piece):
    
    def __init__(self, cell, sideA, sideB, colour):
        Piece.__init__(self, cell)
        
        self.sideA = sideA
        self.sideB = sideB
        self.colour = colour
        self.debug()
       
           
    def  process_train(self, train):
             
            sideIn = train.side
            if self.sideA == sideIn:
                train.side = self.sideB
        
            elif self.sideB == sideIn:
                train.side = self.sideA
            else:
                self.cell.world.handle_crash(train," In Painter")
                return
            
            train.colour = self.colour
           
            
  
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
                
          
      
class Splitter(Piece):

    def __init__(self, cell, side):
        Piece.__init__(self, cell)
        
        self.side = side
      
    def  process_train(self, train):
             
            if self.side != self.side:    
                self.cell.world.handle_crash(train)
                return
                
            colours = split_colour[train.colour]
            
        
            side = self.side 
            sideA = (side + 3) % 4
            sideB = (side + 1) % 4
      
            train.colour = colours[0]
            train.side = sideA
            
            self.cell.world.newtrains.append(Train(self.cell, sideB, colours[1]))

       
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
        
        context.canvas.create_line(xIn, yIn, xClock, yClock, fill=track_colour)
        context.canvas.create_line(xIn, yIn, xAnti, yAnti, fill=track_colour)
                
             

  
class Train:
    
    def __init__(self, cell, side, color):
        self.colour = color
        self.side = side
        self.cell = cell    
      
        self.crashed = False
        self.terminated = False
        self.merged = False
        
    def active(self):    
        return not (self.crashed or self.terminated or self.merged)
    
    def draw(self, context):
        
        #print " HELLO FROM TRAIN DRAW "
        if not self.active():
            return
        
        canvas = context.canvas
        h = context.h
        
    
        mark_side(self.cell.pos, self.side, colour_name[self.colour], 1, context, .2, .4)
            #context.canvas.create_string(x, y,text="T")
    
    def step(self):
        
                
        #print " STEP TRAIN ",self
        
        if not self.active():
            return
        
        cell = self.cell.cellAt[self.side]
        
        if cell == None:
            self.cell.world.handle_crash(self)

        """ 
         If the world raises an exception we might not get here
        """        
        
        self.cell=cell   
        self.side = (self.side + 2) % 4
        self.cell.piece.process_train(self)

    def debug(self):
        
        str=colour_name[self.colour]
        
        if self.crashed:
            str+=" Crashed"

        if self.merged:
            str+=" Merged"
            
        if self.terminated:
            str+=" Terminated"

        str+=" {0} {1} ".format(self.cell.edge_pos(self.side)[0],self.cell.edge_pos(self.side)[1])
        
        return str
    
class Rock:

    def __init__(self, pos):
        self.pos = pos
        
    def draw(self, context):
        x = context.h * (self.pos.x + 0.5)
        y = context.h * (self.pos.y + 0.5)
        
        context.canvas.create_string(x, y, text="R")
        
                
                            
