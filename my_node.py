

class my_node:
    def __init__(self, id: int, x: float, y: float, z: float):
        self.id = id
     #   self.x = x
      #  self.y = y
       # self.z = z
        self.weight = 0
        self.tag = 0
        self.pos = {'x': x, 'y': y, 'z': z}


    def get_id(self) -> int:
        return self.id

    def get_location(self) -> dict:
        return f"{','.join(str(x) for x in self.pos.values())}"
        #return self.pos.get('x'),self.pos.get('y'),self.pos.get('z')

    def set_location(self, x: float, y: float, z: float):
        self.pos.update({'x': x})
        self.pos.update({'y': y})
        self.pos.update({'z': z})

    def get_weight(self) -> float:
        return self.weight

    def set_weight(self, w: float):
        self.weight = w

    def get_tag(self) -> int:
        return self.tag

    def set_tag(self, tag: int):
        self.tag = tag

    def __str__(self):
        return f"[id:{self.id}, pos: {','.join(str(x) for x in self.pos.values())}]"

    def __repr__(self):
        return f"[id:{self.id}, pos: {','.join(str(x) for x in self.pos.values())}]"



