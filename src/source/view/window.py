"""This module is responsible for rendering the
root window and enforcing its associated attributes and items

    State Variables:
    root: the application window

    Environment Variables:
    system display: array of pixels used for graphical output

    **Exported Access Programs**

    ==================   =====================================  ============
    Routine                  In                                     Out
    ==================   =====================================  ============
    setBackground()         root
    create_card             canvas, stackID, cards, num, hide
    draw_card               label, x, y
    bind_card               label, bindings
    ==================   =====================================  ============

    **Semantics**

    setBackground(root) :
    * transition: renders the background for the main window

    create_card(canvas, stackID, cards, num, hide)
    * transition: creates a card in the proper location and predefined attributes

    draw_card(label, x, y):
    * transition: renders the card to the main window

    bind_card(label, bindings):
    * transition: binds the mouse actions to the card

"""

import Tkinter
import ttk
import os


def setBackground(root, path=None):
    """Draw the window background"""
    height = root.winfo_height()
    width = root.winfo_width()
    if hasattr(root, 'canvas'):
        root.canvas.destroy()
    root.canvas = Tkinter.Canvas(root, height=height, width=width)

    if path is None:
        tile = Tkinter.PhotoImage(file=os.path.join(os.getcwd(), "tiles/Nostalgy.gif"))
    else:
        tile = Tkinter.PhotoImage(file=path)
    root.back = tile
    for x in range(0, width, tile.width()):
        for y in range(0, height, tile.height()):
            label = Tkinter.Label(root.canvas, image=tile, borderwidth=0)
            label.place(x=x,y=y)
    root.canvas.pack(fill=Tkinter.BOTH, expand=Tkinter.YES)
    root.canvas.update()


def create_card(canvas, stackID, cards, num, hide):
    """Creates a card with the desired properties"""
    if hide:
        img = cards[num].back_image()
    else:
        img = cards[num].get_image()

    label = ttk.Label(canvas, image=img, borderwidth=0)
    setattr(label, "rank", cards[num].rank)
    setattr(label, "suit", cards[num].suit)
    setattr(label, "color", cards[num].color)
    setattr(label, "stackID", stackID)
    setattr(label, "cardNum", num)
    return label


def draw_card(label, x, y):
    """Renders the card to the main window"""
    label.place(x = x, y = y)


def bind_card(label, bindings):
    if bindings is not None:
        for binding, callback in bindings.iteritems():
            label.bind(binding, callback)