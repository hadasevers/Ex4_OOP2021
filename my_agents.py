
class my_agent:

    def __init__(self, id: int, value: float, src :int, dest :int, speed: float, x: float, y: float, z: float):
        self.id = id
        self.pos = {'x': x, 'y': y, 'z': z}
        self.src = src
        self.dest = dest
        self.value = value
        self.speed = speed

    # return the number of the agent
    def get_id(self) -> int:
        return self.id

    # return the src of the agent
    def get_src(self) -> int:
        return self.src

    # return the dest of the agent
    def get_dest(self) -> int:
        return self.dest

    # return the location of the agent
    def get_location(self) -> dict:
        return f"{','.join(str(x) for x in self.pos.values())}"

    # return the value of the agent
    def get_value(self) -> float:
        return self.value

    # return the speed of the agent
    def get_speed(self) -> float:
        return self.speed


    def __str__(self):
        return f"[id:{self.id}, value:{self.value}, src:{self.src}, dest:{self.dest}, speed:{self.speed}, pos:{','.join(str(x) for x in self.pos.values())}]"

    def __repr__(self):
        return f"[id:{self.id}, value:{self.value}, src:{self.src}, dest:{self.dest}, speed:{self.speed}, pos:{','.join(str(x) for x in self.pos.values())}]"




