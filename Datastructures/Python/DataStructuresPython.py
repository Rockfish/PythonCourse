print('Hello World')
 
from linked_list_mod import Linked_list;

class Book(object):

    def __init__ (self):
        self.Title = "";
        self.Author = "";
        self.ISBN = "";

    def __init__(self, _title, _author, _isbn):
        self.Title = _title;
        self.Author = _author;
        self.ISBN = _isbn;

    def isFilled (self):
        return self.Title.isalnum and self.Author.isalnum and self.ISBN.isalnum;
        
    def To_String(self):
        return self.Author + " "+ self.Title;

    def Equals(self, obj):
        if obj is not None and obj.isFilled():
            return self.ISBN==(obj.ISBN)
        return False;
        
    Title = "";
    Author = "";
    ISBN =  "";

class Person(object):
    """description of class"""

    def __init__(self, _firstname, _lastname, _sex, _birthday, _max=1):
        self.Firstname = _firstname;
        self.Lastname = _lastname;
        self.Sex = _sex;
        self.Birthday = _birthday;
        self.max = _max;

    Firstname = "";
    Lastname = "";
    Sex = "";
    Birthday =  "";

    def Equals(self, object):
        
        return self.Firstname == object.Firstname and self.Lastname == object.Lastname;
        

    def To_String(self):
        return self.Firstname + " " +self.Lastname + " "+self.Sex + " "+ self.Birthday; 
    

    def __iter__(self):
        self.a = 0
        self.b = 1
        return self

    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib

class LibraryDict(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value;
        
    def AddLending(self, p, l):
        l2 = Book("","","");
        res,ba = self.TryGetValue(p,l );
        
        res  = l.Equals(ba)
        if  res is False:
            self.add(p, l);
            res = True;
        else:
            res = False
            return res;
    
    def AssingBook (self,p,b):
        str = ("Trying to assing the book "+b.To_String()+ " to the person "+p.To_String());
        if self.AddLending(p, b):
            str+=("\nThe book "+b.To_String() + " is assigned to the person "+ p.To_String());
        else:
            str+=("\nThe book "+b.To_String() + " is not assigned to the person "+ p.To_String());
        return (str);

    def TryGetValue(self, Person, Book):
        b = 0;
        ba =None;
        keys = self.keys();
        values = self.values();
        i=0;
        for p in keys:
            if p.Equals(Person):
                ba = self[p];
                i+=1;
                break;
        return b,ba;

personsLinkedList = Linked_list();
Library = dict()

b1 = Book("Kronikë në gur", "Ismail Kadare", "20132322");
b2 = Book("Klithmat e fundi", "Ahmet Murati", "34334334");

print (b1.Title);

p1 = Person("Ahmet", "Murati", "Male", "04/29/1979");
p2 = Person("Prarim", "Hoxha", "Male", "04/21/1980");
p3 = Person("Fitim", "Bejtullahu", "Male", "01/10/1980");
p4 = Person("Erzen", "Komoni", "Male", "05/13/1886");
p5 = Person("Ridvan", "Aliu", "Male", "06/24/1981");
p6 = Person("Ridvan", "Bunjaku", "Male", "03/15/1977");


personsArray = [p1,p2,p3,p4];
ldict = LibraryDict();



Library[p1]=b2;
Library[p1]=b2;
Library[p1]=b2;


print(ldict.AssingBook(p1,b1));
print(ldict.AssingBook(p1,b1));
print(ldict.AssingBook(p1,b1));


 
print("First element");
personsLinkedList.append(p1);
for p3a in personsLinkedList:
    print(p3a.To_String())

print()
print("Second element");
personsLinkedList.add( p3);
for p3a in personsLinkedList:
    print(p3a.To_String())
print();

print("Third element");
personsLinkedList.append(p2);
for p3a in personsLinkedList:
    print(p3a.To_String())

print() 
print("Fourth Element");
personsLinkedList.prepend(p1);

 
nodes = personsLinkedList.nodes();

for p in  nodes:
    print((p.data.To_String()));
