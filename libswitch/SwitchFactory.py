class SwitchFactory:
    factories = {}

    def addFactory(id, switchFactory):
        SwitchFactory.factories[id] = switchFactory
    addFactory = staticmethod(addFactory)

    # Template method.
    def createSwitch(id):
        if key not in SwitchFactory.factories:
            SwitchFactory.factories[id] = eval(id + '.Factory()')
        return SwitchFactory.factories[id].create()
    createSwitch = staticmethod(createSwitch)

"""
List and generate the inherited Switch instances by
    types = Switch.__subclasses__()
    switches = [ SwitchFactory.createSwitch(i) for i in types.__name__ ]
"""
