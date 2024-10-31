class Miau:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def delete(self):
        del self    
        
    
ls = [Miau(10), Miau(20), Miau(30), Miau(40)]

s = set(ls)
d = {str(i): v for i, v in enumerate(ls)}

print(s)
print(d)

d["1"].value += 700

print(s)
print(d)