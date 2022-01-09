

class my_pokemon:
    
    def __init__(self, type :int, value: int, src: int, dest: int, x: float, y: float, z: float):
        self.type = type
        self.value = value
        self.src = src
        self.dest = dest
        self.pos = {'x': x, 'y': y, 'z': z}


    # return the type of the pokemon
    def get_type(self) -> int:
        if self.type > 0:
            return 1
        else:
            return -1

    # return the src of the adge
    def get_src(self) -> int:
        return self.src

    # return the dest of the adge
    def get_dest(self) -> int:
        return self.dest

    # return the location of the pokemon
    def get_location(self) -> dict:
        return f"{','.join(str(x) for x in self.pos.values())}"

    # return the value of the pokemon
    def get_value(self) -> int:
        return self.value

    def __str__(self):
        return f"[value:{self.value}, src:{self.src}, dest:{self.dest}, type:{self.type}, pos: {','.join(str(x) for x in self.pos.values())}]"

    def __repr__(self):
        return f"[value:{self.value}, src:{self.src}, dest:{self.dest}, type:{self.type}, pos: {','.join(str(x) for x in self.pos.values())}]"




