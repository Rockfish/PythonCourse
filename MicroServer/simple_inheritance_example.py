from datetime import datetime


class Foo(object):

    def __init__(self):
        print("Foo init called! ")
        print(self.value)

    def name(self):
        print("Name is Foo.")

    def time(self):
        print(datetime.now())


class Bar(Foo):

    def __init__(self):
        print("Bar init called!")
        self.value = "hi!"
        super().__init__()

    def name(self):
        print("Name is bar.")


bar = Bar()
bar.name()
bar.time()


