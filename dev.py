# @property test
class Shot():
    def __init__(self):
        self._effect = None
    @property
    def effect(self):
        return self._effect
    @effect.setter
    def effect(self, value):
        self._effect = value
    @effect.getter
    def effect(self):
        return self._effect
    @effect.deleter
    def effect(self):
        del self._effect

def shot_property_test():
    My_Shot = Shot()
    My_Shot.effect = "test"
    print(My_Shot.effect)
    print(My_Shot.effect)
    del My_Shot.effect
    print(My_Shot.effect)
        

# 