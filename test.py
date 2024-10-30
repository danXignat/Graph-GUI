class Miau:
    def __init__(self):
        self.value = 10

    def __str__(self):
        return str(self.value)
miau = Miau()

ls = [miau]

del miau

print(ls)