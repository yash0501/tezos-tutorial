import smartpy as sp

class Cryptobot(sp.Contract):
    def __init__(self, life_state, manager_address):
        self.init(
            name = "terminator", 
            is_alive = life_state, 
            coordinate_x = sp.int(0), 
            coordinate_y = sp.int(0), 
            plasma_bullet_count = 5, 
            record_alien_kills = sp.map({
                "simple_alien": sp.nat(0), 
                "boss_alien": sp.nat(0)
            }),
            bot_manager = manager_address
            )
    
    @sp.entry_point()
    def change_name(self, new_name):
        sp.verify(self.data.bot_manager == sp.sender, message = "Error: Sender is not contract owner")
        self.data.name = new_name

    @sp.entry_point()
    def move_horizontally(self, update_to):
        sp.verify(self.data.bot_manager == sp.sender, message = "Error: Sender is not contract owner")
        sp.if (update_to >= -10) & (update_to <= 10):
            self.data.coordinate_x = update_to
        sp.else :
            sp.failwith("Error: Out of bound movement!")

    @sp.entry_point()
    def move_vertically(self, update_to):
        sp.verify(self.data.bot_manager == sp.sender, message = "Error: Sender is not contract owner")
        sp.if (update_to >= -10) & (update_to <= 10):
            self.data.coordinate_y = update_to
        sp.else:
            sp.failwith("Error: Out of bound movement!")


    @sp.entry_point()
    def shoot_alien(self, alien_type):
        sp.verify(self.data.bot_manager == sp.sender, message = "Error: Sender is not contract owner")
        sp.if (self.data.plasma_bullet_count >=1):
            self.data.plasma_bullet_count -= 1
            self.data.record_alien_kills[alien_type] += 1
        sp.else:
            sp.failwith("Error: Cryptobot run out of bullets!")

@sp.add_test(name = "Test Cryptobot Contract")
def test():
    scenario = sp.test_scenario()
    my_address = sp.address("tz1Syu3KacZ8cy4286a4vaCeoMtwqVKHkaoj")
    test_bot = Cryptobot(life_state = True, manager_address = my_address)
    scenario += test_bot
    scenario += test_bot.change_name("punky terminator").run(sender = my_address)
    scenario.verify(test_bot.data.is_alive == True)
    scenario += test_bot.move_horizontally(2).run(sender = my_address)
    scenario += test_bot.move_vertically(1).run(sender = my_address)
    scenario += test_bot.shoot_alien("boss_alien").run(sender = my_address)
    scenario += test_bot.shoot_alien("simple_alien").run(sender = my_address)
