# import modules
import tkinter as tk
from tkinter import Tk
from tkinter import ttk


# create main application window
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Shopping Manager")
        self.container = ttk.Frame(self, height=300, width=400, padding=2)
        self.container.pack()
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        # setup navigation controller
        self.frames = {}
        for F in (MainPage, ActiveList, AllLists):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        # Data structures for lists and items
        self.lists = {}
        self.active_list = None

        # show Main Page on start
        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_home_page(self):
        self.show_frame("MainPage")

    def show_active_list(self):
        self.show_frame("ActiveList")

    def show_all_lists(self):
        self.show_frame("AllLists")

    def quit_app(self):
        self.quit()


# create main page
class MainPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # create top frame for nav and quit buttons
        self.topMenuFrame = ttk.Frame(self, height=50, width=400, padding=(10, 5))
        self.topMenuFrame.pack(fill="x")
        self.topMenuFrame.columnconfigure(0, weight=1)
        self.topMenuFrame.columnconfigure(1, weight=1)
        self.topMenuFrame.columnconfigure(2, weight=1)

        # top nav button
        self.topNavButton = ttk.Menubutton(
            self.topMenuFrame, text="Menu", direction="below"
        )
        self.menu = tk.Menu(self.topNavButton, tearoff=0)
        self.menu.add_command(
            label="Active List", command=lambda: self.controller.show_active_list()
        )
        self.menu.add_command(
            label="All Lists", command=lambda: self.controller.show_all_lists()
        )
        self.topNavButton["menu"] = self.menu
        self.topNavButton.grid(row=0, column=0, sticky="W")

        # top quit button
        self.topQuitButton = ttk.Button(
            self.topMenuFrame, text="Quit", command=lambda: self.controller.quit_app()
        )
        self.topQuitButton.grid(row=0, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create middle frame for entry box and add to list button
        self.middleMenuFrame = ttk.Frame(self, height=100, width=400, padding=(10, 30))
        self.middleMenuFrame.pack(fill="x")
        self.middleMenuFrame.columnconfigure(0, weight=1)
        self.middleMenuFrame.columnconfigure(1, weight=1)
        self.middleMenuFrame.columnconfigure(2, weight=1)
        self.middleMenuFrame.columnconfigure(3, weight=1)

        # middle-left info label
        self.infoLabel = ttk.Label(self.middleMenuFrame, text="Type in item name:")
        self.infoLabel.grid(row=1, column=0, sticky="E")

        # middle-left entry box
        self.inputItemBox = ttk.Entry(self.middleMenuFrame, width=15)
        self.inputItemBox.grid(row=1, column=1, sticky="W")

        # middle-right add to list button
        self.confirmItemButtonIcon = tk.PhotoImage(file="icons8-cart-16-white.png")
        self.confirmItemButton = ttk.Button(
            self.middleMenuFrame,
            text="Add",
            image=self.confirmItemButtonIcon,
            compound="right",
            width=2.2,
        )
        self.confirmItemButton.grid(row=1, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create bottom frame for displaying available lists
        self.bottomListFrame = ttk.Frame(self, height=350, width=500, padding=(10, 5))
        self.bottomListFrame.pack(fill="x")
        self.bottomListFrame.columnconfigure(0, weight=1)
        self.bottomListFrame.columnconfigure(1, weight=1)
        self.bottomListFrame.columnconfigure(2, weight=1)

        # Lists Title
        self.bottomListTitle = ttk.Label(
            self.bottomListFrame,
            text="All Lists",
            padding=(10, 10),
            font=("Arial", 16),
        )
        self.bottomListTitle.grid(row=0, column=1)

        # Icon button to navigate to All Lists window
        self.allListsIcon = tk.PhotoImage(file="icons8-documents-100.png")
        self.allListsLabel = tk.Label(self.bottomListFrame, image=self.allListsIcon)
        self.allListsLabel.grid(row=1, column=1, pady=10)
        self.allListsLabel.bind(
            "<Button-1>", lambda event: self.controller.show_all_lists()
        )


# create all lists page
class AllLists(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # create top frame for nav and quit buttons
        self.topMenuFrame = ttk.Frame(self, height=50, width=400, padding=(10, 5))
        self.topMenuFrame.pack(fill="x")
        self.topMenuFrame.columnconfigure(0, weight=1)
        self.topMenuFrame.columnconfigure(1, weight=1)
        self.topMenuFrame.columnconfigure(2, weight=1)

        # top nav button
        self.topNavButton = ttk.Menubutton(
            self.topMenuFrame, text="Menu", direction="below"
        )
        self.menu = tk.Menu(self.topNavButton, tearoff=0)
        self.menu.add_command(
            label="Active List", command=lambda: self.controller.show_active_list()
        )
        self.menu.add_command(
            label="Home", command=lambda: self.controller.show_home_page()
        )
        self.topNavButton["menu"] = self.menu
        self.topNavButton.grid(row=0, column=0, sticky="W")

        # top quit button
        self.topQuitButton = ttk.Button(
            self.topMenuFrame, text="Quit", command=lambda: self.controller.quit_app()
        )
        self.topQuitButton.grid(row=0, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")


# create active list page
class ActiveList(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # create top frame for nav and quit buttons
        self.topMenuFrame = ttk.Frame(self, height=50, width=400, padding=(10, 5))
        self.topMenuFrame.pack(fill="x")
        self.topMenuFrame.columnconfigure(0, weight=1)
        self.topMenuFrame.columnconfigure(1, weight=1)
        self.topMenuFrame.columnconfigure(2, weight=1)

        # top nav button
        self.topNavButton = ttk.Menubutton(
            self.topMenuFrame, text="Menu", direction="below"
        )
        self.menu = tk.Menu(self.topNavButton, tearoff=0)
        self.menu.add_command(
            label="All Lists", command=lambda: self.controller.show_all_lists()
        )
        self.menu.add_command(
            label="Home", command=lambda: self.controller.show_home_page()
        )
        self.topNavButton["menu"] = self.menu
        self.topNavButton.grid(row=0, column=0, sticky="W")

        # top quit button
        self.topQuitButton = ttk.Button(
            self.topMenuFrame, text="Quit", command=lambda: self.controller.quit_app()
        )
        self.topQuitButton.grid(row=0, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")


# call main
if __name__ == "__main__":
    app = Application()
    app.resizable(width=False, height=False)
    app.mainloop()
