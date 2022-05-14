from dataclasses import dataclass, field
from re import finditer, search
from typing import Dict, List

@dataclass
class RowSegment():
    row_no : int
    col_start : int
    col_end : int

    def __repr__(self):
        return f'{self.row_no}:{self.col_start}-{self.col_end}'

@dataclass
class Space():
    furn_count : Dict[str, int] = field(default_factory = dict)
    segs : List[RowSegment] = field(default_factory = list)
    complete : bool = False

    def __repr__(self):
        return f'{[s for s in self.segs]}'

plan = """
+---------------+-------------------+           +----------+
|               |                   |           |          |
|  (office)     |            C      |           |   C      |
|               |                   |           |          |
|           W   |                   +-----------+          |
|               |                   |           |          |
|   S           |   (bathroom)     S|      S    |          |
|           +---+--------+----------+           |          |
|          /P           S|                      |          |
|         /              |                      |          |
|        /   (kitchen)   |      (bedroom)       |  P       |
+-------+                |                      |          |
|        \               |                      |          |
|         \   SSWP       |   W              W   |          |
|          +-------------+----------------------+          |
|                                                          |
|             (hallway)                                    |
|    W                                                     |
+--------------+-------------+-------------+               |
               |             |              \              |
               |             |               \        C    |
               | P           |                \            |
               |             |                 \           |
        +------+           P |                  +----------+
        |S                   |                              
        |    (balcony)   C   |                              
        +--------------------+                              """

workspaces = []
rooms = []
rows = plan.split('\n')
rows.pop(0)

for no, row in enumerate(rows):
    found = list(finditer(r'[^/\\|+-]+', row))
    if found:
        rsegs = [RowSegment(no, rs.start(), rs.end()) for rs in found]
        for ws in workspaces:
            for rs in rsegs:
                if max(ws.segs[-1].col_start, rs.col_start) < min(ws.segs[-1].col_end, rs.col_end): #add rs to ws
                    ws.segs.append(rs)
                    rsegs.remove(rs)
                    break
            else: #no rs added => complete
                text = ''.join([rows[s.row_no][s.col_start:s.col_end] for s in ws.segs])
                name = search(r'\(\w+\)', text)
                if name:
                    rooms.append(ws)
                ws.complete = True
        #reset ws list to only not complete
        workspaces = [ws for ws in workspaces if ws.complete == False]
        #create new wss with remaining rss
        for rs in rsegs:
            newws = Space()
            newws.segs.append(rs)
            workspaces.append(newws)

def get_max(r,t):
    l = []
    if t == 'rn':
        for v in r:
            l.append(v.row_no)
    if t == 'cs':
        for v in r:
            l.append(v.col_start)
    if t == 'ce':
        for v in r:
            l.append(v.col_end)


    return max(l)

def get_min(r,t):
    l = []
    if t == 'rn':
        for v in r:
            l.append(v.row_no)
    if t == 'cs':
        for v in r:
            l.append(v.col_start)
    if t == 'ce':
        for v in r:
            l.append(v.col_end)


    return min(l)


for room in rooms:
    boundaries = []
    corners = []
    ini = room.segs[0].row_no
    for rowno in room.segs: 
        if rowno.row_no == room.segs[0].row_no:
            for i in range(rowno.col_start-1, rowno.col_end+1):
                boundaries.append([i, rowno.row_no-1])
        boundaries.append([rowno.col_start-1, rowno.row_no])
        if rowno.row_no == room.segs[-1].row_no:
            for i in range(rowno.col_start-1, rowno.col_end):
                boundaries.append([i, rowno.row_no+1])
            for i in range(rowno.row_no+1, ini-2, -1):
                boundaries.append([rowno.col_end, i])
    
    with open("floorplan01.txt") as f:
        ys = f.readlines()
    
    for coord in boundaries:
        if ys[coord[1]][coord[0]] == '+':
            corners.append(coord)
    print(corners)

    print('\n')