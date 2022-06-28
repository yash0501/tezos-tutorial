import smartpy as sp

class Test_Contract(sp.Contract):
    def __init__(self):
        self.init(storage=sp.nat(0))
    
    @sp.entry_point
    def repeat(self, params):
        self.data.storage = params

@sp.add_test(name = "Test")
def test():
    scenario = sp.test_scenario()
    test = Test_Contract()
    scenario += test
    test.repeat(2)
