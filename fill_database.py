from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# session.rollback()
session = DBSession()

# Create User
testUser = User(email="testthetestytester@gmail.com")
session.add(testUser)
session.commit()

# Books Category and items
cat = Category(user_id=1, name="Books")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="Pointers in C",
    description="This is a book about the magical world of the pointer in c "
    " programming.  Enjoy the thrills of passing by reference, pointer "
    " arithmetic and dereferencing via this efficient and misunderstood "
    "creature.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Programming in C",
    description="K&R's famous introductory book on C programming. "
    " It's a bit heavy for a first programming book, but looked upon as the "
    "core reference for "
    "the language.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Python network programming",
    description="A fun book about... Python network programming. "
    "Includes sockets module as well as HTTP based modules.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Django Unleashed",
    description="No relation to the (probably) bad movie, this book outlines "
    " the django framework and is pretty awesome. It's Orange.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Algorithms Illustrated",
    description="A book by Stanford's head of computer science about "
    "algorithms.  Enjoy the wonders of sorting lists over and over using "
    "different methods. You will probably just use the default sort "
    "functionality of any language, but hey why not read an entire book "
    "about it.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Applied Cryptography",
    description="Find out that you are not good at math using this easy to"
    " follow guide on cryptography.",
    category=cat)
session.add(item)
session.commit()

# Computers / items
cat = Category(user_id=1, name="Computers")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="Mac Book Pro",
    description="The newest installation of the MBP from Apple. It's space"
    "grey, 15 and only has usb C ports for some reason. It comes with nothing "
    "that you need in order to use it",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Gaming Rig",
    description="Ohhhh ohhhh ohhh. This is a i7 4.2 ghz machine with a "
    "Geforce GTX 1080 and 64Gb of ram. It glows bright red on the inside."
    " Scary!",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Acer Brick Thingie",
    description="Acer's small computer thing. It currently functions as a "
    "book end on a shelf, but one day it will house a samba server that "
    "backs up to AWS. This will happen after this class is over. (hopefully)",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Xbox-S",
    description="It is a computer afterall... I never play it because I am "
    "always too busy doing things like writing descriptions for fictional"
    " projects.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Friends Machine",
    description="I have no idea what it is exactly, but there is an x64 "
    "machine sitting on the floor of my office. It was left there by a man "
    "named Derek. I hope he comes to get it soon.",
    category=cat)
session.add(item)
session.commit()

# Furniture / items
cat = Category(user_id=1, name="Furniture")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="UpDesk",
    description="It's a desk that goes up and down so I can pretend that I"
    " stand at my desk. It is made in Austin TX by very nice people.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="CB2 white shelf",
    description="Pretty much a white shelf from CB2. That's crate and barrel's"
    " more hip website for the uninitiated. It has all of my books, coffee "
    "cups and random trinkets on it. My wife informs me that I should say "
    "it has 4 shelves.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Mesh Chair of sitting + 2",
    description="A super comfortable chair that allows you to sit and code for"
    " a llllong time without feeling like you need to get up. It probably "
    "contributes to me never using my Updesk.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Nap Couch",
    description="Its a grey lovesac couch that I take naps on sometimes."
    " When I'm not there my cat sleeps on it.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="CB2 Rug",
    description="Rug from CB2. Its blue, 8x4 and pretty gross from the dog "
    "sleeping on it all the time. It has wavey white lines that look vaguely"
    " like the bacon icon in font awesome. My wife doesn't like it",
    category=cat)
session.add(item)
session.commit()

# Pens / items
cat = Category(user_id=1, name="Pens")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="Black Bic Pen",
    description="A Bic Pen that has black Ink.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Blue Bic Pen",
    description="Its a Bic Pen with Black Ink.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Sharpie",
    description="Black Marker that I seem to always find a way "
    "to write on myself with.",
    category=cat)
session.add(item)
session.commit()

# Notepads / items
cat = Category(user_id=1, name="Notepads")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="Mole Skin",
    description="A note book that seems to multiply. I have more of them "
    "than I ever remember buying.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Blackhat Notebook",
    description="A notebook from a security conference. It's from circa 2005.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Texas Grid",
    description="My favorite notebook. It contains grid paper and has "
    "something about texas on the front.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Mini Moleskin",
    description="A tiny Moleskin notebook. Good for very small thoughts.",
    category=cat)
session.add(item)
session.commit()

# Lights / items
cat = Category(user_id=1, name="Lights")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="Recessed Lights",
    description="Lights that are installed in my ceiling",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Desk Lamp",
    description="Curved neck spot light that is generally useless in this"
    " day and age.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Pen Light",
    description="A small light that can be used to open up a machine and help"
    " to locate the source of the burning smell.",
    category=cat)
session.add(item)
session.commit()

# Fitness Gear / items
cat = Category(user_id=1, name="Fitness Gear")
session.add(cat)
session.commit()

item = Item(
    user_id=1,
    name="35lb Kettle Bell",
    description="Sometimes its good to leave the chair and move the blood "
    "around. The kettle bell helps break up the day of staring at glowing "
    "rectangles.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="50lb Kettle Bell",
    description="Heavier version of the 35lb kettle bell. It does the same"
    " thing, but only heavier.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Resistance Band",
    description="Band for stretching",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Jiu Jitsu Dummy",
    description="I call him Dan. I beat him up when my code doesn't work.",
    category=cat)
session.add(item)
session.commit()

item = Item(
    user_id=1,
    name="Sand Bag",
    description="Bag of sand! You carry it around and it makes you burn more "
    "calories than just walking.",
    category=cat)
session.add(item)
session.commit()

print("added category items!")
