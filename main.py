"""
Author: Andrei Benea
Date written: 7/24/24
Assignment: Final Project - "Shopping Manager"
This program allow its user to create multiple shopping lists, adding
various items and their respective quantities to the lists, while also
offering the possibility to manipulate the items and/or lists. The
program offers a clear navigation between pages, uses a dashboard to
quickly add items to the current active list (creating one if none exists),
and allows for quick navigation to the "All Lists" view for further action.
"""

# import modules
import tkinter as tk
from tkinter import ttk


# create main application window
class Application(tk.Tk):
    """Main application window in which all other frames are nested.
    Uses a controller setup for navigation and the function to add new items"""

    # define constructor method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setup main container title and size
        self.title("Shopping Manager")
        self.container = ttk.Frame(self, height=300, width=300, padding=2)
        self.container.pack()
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(
            False
        )  # prevent changing of size based on children

        # setup navigation controller
        self.frames = {}  # create empty dictionary to store all frames(pages)
        for F in (MainPage, ActiveListPage, AllListsPage):
            page_name = F.__name__  # store page name inside variable
            frame = F(
                parent=self.container, controller=self
            )  # initialize frame from its class
            self.frames[page_name] = frame  # populate dictionary
            frame.grid(row=0, column=0, sticky="NSEW")  # position page inside container

        # Data structures for lists and items
        self.lists = {}  # initialize empty dictionary for storing lists
        self.active_list = None  # active list flag

        # show Main Page on start
        self.show_frame("MainPage")

    # define class methods
    # method selecting between frames (used by navigation controller)
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # function that brings (raises) frame into view
        if page_name == "ActiveListPage":
            self.frames[page_name].show_active_list_contents()  # refresh page contents
        if page_name == "AllListsPage":
            self.frames[page_name].show_all_lists_contents()  # refresh page contents

    # pass page name to show_frame function
    def show_home_page(self):
        self.show_frame("MainPage")

    # pass page name to show_frame function
    def show_active_list_page(self):
        self.show_frame("ActiveListPage")

    # pass page name to show_frame function
    def show_all_lists_page(self):
        self.show_frame("AllListsPage")

    # quit application function
    def quit_app(self):
        self.quit()

    # function to add a new item to active list
    def add_item(self, item):
        if self.active_list:  # if active list exists, add item to it
            self.lists[self.active_list].append(item)
            print(self.lists)
            print(self.active_list)
        else:  # else create new list named "Default" and set as active_list
            self.lists["Default"] = [item]
            self.active_list = "Default"
            print(self.lists)
            print(self.active_list)


# create main page
class MainPage(tk.Frame):
    """Main page of the application. Contains functions to manage the adding of a new item"""

    # define constructor method
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # create top frame for nav and quit buttons
        self.topMenuFrame = ttk.Frame(self, height=50, width=300, padding=(10, 5))
        self.topMenuFrame.pack(fill="x")
        self.topMenuFrame.columnconfigure(0, weight=1)
        self.topMenuFrame.columnconfigure(1, weight=1)
        self.topMenuFrame.columnconfigure(2, weight=1)
        self.topMenuFrame.grid_propagate(False)

        # top nav button
        self.topNavButton = ttk.Menubutton(
            self.topMenuFrame, text="Menu", direction="below"
        )
        self.menu = tk.Menu(
            self.topNavButton, tearoff=0
        )  # create special "menu" button for navigation
        self.menu.add_command(
            label="Active List", command=lambda: self.controller.show_active_list_page()
        )
        self.menu.add_command(
            label="All Lists", command=lambda: self.controller.show_all_lists_page()
        )
        self.topNavButton["menu"] = self.menu
        self.topNavButton.grid(row=0, column=0, sticky="W")

        # top page name label
        self.topPageName = ttk.Label(
            self.topMenuFrame, text="Home", font=("PT Mono", 16)
        )
        self.topPageName.grid(row=0, column=1)

        # top quit button
        self.topQuitButton = ttk.Button(
            self.topMenuFrame, text="Quit", command=lambda: self.controller.quit_app()
        )
        self.topQuitButton.grid(row=0, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create middle frame for entry box and add to list button
        self.middleMenuFrame = ttk.Frame(self, height=100, width=300, padding=(10, 30))
        self.middleMenuFrame.pack(fill="x")
        self.middleMenuFrame.columnconfigure(0, weight=1)
        self.middleMenuFrame.columnconfigure(1, weight=1)
        self.middleMenuFrame.columnconfigure(2, weight=1)
        self.middleMenuFrame.columnconfigure(3, weight=1)
        self.middleMenuFrame.grid_propagate(False)

        # middle-left info label
        self.infoLabel = ttk.Label(
            self.middleMenuFrame, text="Item name:", font=("PT Mono", 14)
        )
        self.infoLabel.grid(row=1, column=0, sticky="W")

        # middle-left entry box
        self.inputItemBox = ttk.Entry(self.middleMenuFrame, width=10)
        self.inputItemBox.grid(row=1, column=1, sticky="W")

        # middle-right add to list button
        self.confirmItemButtonIcon = tk.PhotoImage(file="icons8-cart-16-white.png")
        self.confirmItemButton = ttk.Button(
            self.middleMenuFrame,
            text="Add",
            image=self.confirmItemButtonIcon,
            compound="right",
            width=2.2,
            command=lambda: self.prepare_item(),
        )
        self.confirmItemButton.grid(row=1, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create bottom frame for displaying available lists
        self.bottomListFrame = ttk.Frame(self, height=300, width=300, padding=(10, 5))
        self.bottomListFrame.pack(fill="x")
        self.bottomListFrame.columnconfigure(0, weight=1)
        self.bottomListFrame.columnconfigure(1, weight=1)
        self.bottomListFrame.columnconfigure(2, weight=1)

        # lists title / label
        self.bottomListTitle = ttk.Label(
            self.bottomListFrame,
            text="All Lists",
            padding=(10, 10),
            font=("PT Mono", 16),
        )
        self.bottomListTitle.grid(row=0, column=1)

        # icon button to navigate to All Lists page
        self.allListsIcon = tk.PhotoImage(file="icons8-documents-100.png")
        self.allListsLabel = tk.Label(self.bottomListFrame, image=self.allListsIcon)
        self.allListsLabel.grid(row=1, column=1, pady=10)
        self.allListsLabel.bind(
            "<Button-1>", lambda event: self.controller.show_all_lists_page()
        )

    # function for adding a new item
    def prepare_item(self):
        item_name = self.inputItemBox.get()  # get entry box value
        if item_name.isalpha():  # check for value to be "alpha"
            for widget in self.middleMenuFrame.winfo_children():
                widget.destroy()  # destroy widgets prior to creating new view

            # middle-left info label (quantity)
            self.infoLabel = ttk.Label(
                self.middleMenuFrame, text="How many items? ", font=("PT Mono", 14)
            )
            self.infoLabel.grid(row=1, column=0, sticky="W")

            # middle-left entry box (quantity)
            self.inputQuantityBox = ttk.Entry(self.middleMenuFrame, width=5)
            self.inputQuantityBox.grid(row=1, column=1, sticky="W")

            # middle-right add to list button (confirm)
            self.confirmItemButton = ttk.Button(
                self.middleMenuFrame,
                text="Confirm",
                compound="right",
                width=6,
                command=lambda: self.confirm_item(item_name),
            )
            self.confirmItemButton.grid(row=1, column=2, sticky="E")

    # function confirming item quantity, adding to active list
    def confirm_item(self, item_name):
        item_quantity = self.inputQuantityBox.get()  # get entry box value
        if item_quantity.isnumeric():  # check for value to be "numeric"
            item = (item_name, item_quantity)  # create item tuple
            print(item)
            self.controller.add_item(item)  # call function from controller
            for widget in self.middleMenuFrame.winfo_children():
                widget.destroy()

            # display success message
            self.successLabel = ttk.Label(
                self.middleMenuFrame, text="Added successfully!", font=("PT Mono", 14)
            )
            self.successLabel.grid(row=1, column=0, sticky="E")

            # reset widgets button
            self.successButton = ttk.Button(
                self.middleMenuFrame, text="OK", command=lambda: self.reset_view()
            )
            self.successButton.grid(row=1, column=1, sticky="E")

    # function resetting view to initial state after item was added
    def reset_view(self):
        for widget in self.middleMenuFrame.winfo_children():
            widget.destroy()

        # middle-left info label
        self.infoLabel = ttk.Label(
            self.middleMenuFrame, text="Item name:", font=("PT Mono", 14)
        )
        self.infoLabel.grid(row=1, column=0, sticky="W")

        # middle-left entry box
        self.inputItemBox = ttk.Entry(self.middleMenuFrame, width=10)
        self.inputItemBox.grid(row=1, column=1, sticky="W")

        # middle-right add to list button
        self.confirmItemButtonIcon = tk.PhotoImage(file="icons8-cart-16-white.png")
        self.confirmItemButton = ttk.Button(
            self.middleMenuFrame,
            text="Add",
            image=self.confirmItemButtonIcon,
            compound="right",
            width=2.2,
            command=lambda: self.prepare_item(),
        )
        self.confirmItemButton.grid(row=1, column=2, sticky="E")


# create all lists page
class AllListsPage(tk.Frame):
    """All Lists page of the application. Contains functions to manage lists like add, delete and set as active"""

    # define constructor method
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # create top frame for nav and quit buttons
        self.topMenuFrame = ttk.Frame(self, height=50, width=300, padding=(10, 5))
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
            label="Active List", command=lambda: self.controller.show_active_list_page()
        )
        self.menu.add_command(
            label="Home", command=lambda: self.controller.show_home_page()
        )
        self.topNavButton["menu"] = self.menu
        self.topNavButton.grid(row=0, column=0, sticky="W")

        # top page name label
        self.topPageName = ttk.Label(
            self.topMenuFrame, text="All Lists", font=("PT Mono", 16)
        )
        self.topPageName.grid(row=0, column=1)

        # top quit button
        self.topQuitButton = ttk.Button(
            self.topMenuFrame, text="Quit", command=lambda: self.controller.quit_app()
        )
        self.topQuitButton.grid(row=0, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create frame for canvas and scroll
        self.canvasFrame = ttk.Frame(self, padding=(2, 10))
        self.canvasFrame.pack(fill="x")

        # create canvas for scrolling functionality
        self.canvas = tk.Canvas(self.canvasFrame)
        self.scrollbar = ttk.Scrollbar(
            self.canvasFrame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # separator
        self.buttonSeparator = ttk.Separator(self)
        self.buttonSeparator.pack(fill="x")

        # bottom button frame
        self.bottomButtonsFrame = ttk.Frame(self)
        self.bottomButtonsFrame.pack(fill="x")
        self.bottomButtonsFrame.columnconfigure(0, weight=1)
        self.bottomButtonsFrame.columnconfigure(1, weight=1)
        self.bottomButtonsFrame.columnconfigure(2, weight=1)
        self.bottomButtonsFrame.columnconfigure(3, weight=1)

        # bottom button for creating new list
        self.bottomNewListButton = ttk.Button(
            self.bottomButtonsFrame,
            text="New List",
            command=lambda: self.prepare_create_list(),
        )
        self.bottomNewListButton.grid(row=0, column=1, columnspan=2)

    # function used to display all available lists
    def show_all_lists_contents(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # store all lists and active list inside separate variables
        all_lists = self.controller.lists  # all available lists
        active_list = self.controller.active_list  # active list flag
        print(all_lists)
        if len(all_lists) == 0:  # display label if empty
            label = ttk.Label(
                self.scrollable_frame, text="No entries", font=("PT Mono", 14)
            )
            label.pack()

        else:
            for list_name in all_lists:
                self.create_list_widget(
                    list_name, list_name == active_list
                )  # populate list

    # create widgets for each list in active list
    def create_list_widget(self, list_name, is_active):
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill="x", pady=5)

        print(f"Creating widget for: {list_name}")

        item_label = ttk.Label(item_frame, text=list_name, font=("PT Mono", 14))
        item_label.pack(side="left", padx=5)

        # display different buttons depending on list being active or not
        if is_active:
            action_text = "Open"
            action_command = lambda: self.controller.show_active_list_page()
        else:
            action_text = "Set Active"
            action_command = lambda: self.mark_as_active(list_name)

        action_button = ttk.Button(
            item_frame, text=action_text, command=action_command, width=7
        )
        action_button.pack(side="right", padx=5)

        remove_button = ttk.Button(
            item_frame, text="Remove", command=lambda: self.remove_list(list_name)
        )
        remove_button.pack(side="right", padx=5)

    # mark list as active
    def mark_as_active(self, list_name):
        self.controller.active_list = list_name
        print(f"Item marked as active: {list_name}")
        self.show_all_lists_contents()

    # function to remove list from all lists
    def remove_list(self, list_name):
        # check if the list exists in the controller
        if list_name in self.controller.lists:
            # if the list is the active list, reset the active list to None
            if list_name == self.controller.active_list:
                self.controller.active_list = None
            self.controller.lists.pop(list_name)  # remove the list from the controller
            self.show_all_lists_contents()  # refresh the list contents display
            print(f"List removed: {list_name}")

    # function preparing data required to create a new list
    def prepare_create_list(self):
        """When triggered adds a label and two buttons (Add and Cancel) to the bottom section"""
        for widget in self.bottomButtonsFrame.winfo_children():
            widget.destroy()

        self.listNameLabel = ttk.Label(self.bottomButtonsFrame, text="List name:")
        self.listNameLabel.grid(row=0, column=0)

        self.listNameInput = ttk.Entry(self.bottomButtonsFrame, width=8)
        self.listNameInput.grid(row=0, column=1)

        self.confirmCreateList = ttk.Button(
            self.bottomButtonsFrame,
            text="OK",
            width=3,
            command=lambda: self.create_list(),
        )
        self.confirmCreateList.grid(row=0, column=2)

        self.confirmCreateList = ttk.Button(
            self.bottomButtonsFrame,
            text="Cancel",
            width=5,
            command=lambda: self.cancel_list_creation(),
        )
        self.confirmCreateList.grid(row=0, column=3)

    # function creating the actual list entry inside all lists
    def create_list(self):
        list_name = self.listNameInput.get()
        print(list_name)
        if list_name.isalpha():
            self.controller.lists[list_name] = []
            self.show_all_lists_contents()
        else:
            print("Invalid list name")

    # recreate bottom row after clicking "Cancel"
    def cancel_list_creation(self):
        for widget in self.bottomButtonsFrame.winfo_children():
            widget.destroy()

        # bottom button for creating new list
        self.bottomNewListButton = ttk.Button(
            self.bottomButtonsFrame,
            text="New List",
            command=lambda: self.prepare_create_list(),
        )
        self.bottomNewListButton.grid(row=0, column=1, columnspan=2)


# create active list page
class ActiveListPage(tk.Frame):
    """Active List page of the application. Contains functions to manage items like delete and mark as done"""

    # define constructor method
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

        # define styles
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("PT Mono", 14))
        self.style.configure(
            "GreyedOut.TLabel", font=("PT Mono", 14), foreground="grey"
        )
        self.item_labels = {}  # init empty dict used for setting style

        self.done_items = set()  # create set for storing "done" items

    def create_widgets(self):
        # create top frame for nav and quit buttons
        self.topMenuFrame = ttk.Frame(self, height=50, width=300, padding=(10, 5))
        self.topMenuFrame.pack(fill="x")
        self.topMenuFrame.columnconfigure(0, weight=1)
        self.topMenuFrame.columnconfigure(1, weight=1)
        self.topMenuFrame.columnconfigure(2, weight=1)
        self.topMenuFrame.pack_propagate(False)

        # top nav button
        self.topNavButton = ttk.Menubutton(
            self.topMenuFrame, text="Menu", direction="below"
        )
        self.menu = tk.Menu(self.topNavButton, tearoff=0)
        self.menu.add_command(
            label="All Lists", command=lambda: self.controller.show_all_lists_page()
        )
        self.menu.add_command(
            label="Home", command=lambda: self.controller.show_home_page()
        )
        self.topNavButton["menu"] = self.menu
        self.topNavButton.grid(row=0, column=0, sticky="W")

        # top page name label
        self.topPageName = ttk.Label(
            self.topMenuFrame, text="Active List", font=("PT Mono", 16)
        )
        self.topPageName.grid(row=0, column=1)

        # top quit button
        self.topQuitButton = ttk.Button(
            self.topMenuFrame, text="Quit", command=lambda: self.controller.quit_app()
        )
        self.topQuitButton.grid(row=0, column=2, sticky="E")

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create canvas for scrolling functionality
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # function displaying an empty list or triggering the generation of widgets for every item
    def show_active_list_contents(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        active_list = self.controller.lists.get(self.controller.active_list, [])
        if not active_list:  # display label if no active list
            label = ttk.Label(
                self.scrollable_frame, text="No entries", font=("PT Mono", 14)
            )
            label.pack()
        else:
            for item in active_list:
                self.create_item_widget(item)  # populate list

    # creates a separate widget for every item inside list
    def create_item_widget(self, item):
        """Displays an entry for each item (name+amount). Entry also displays two buttons for further action"""
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill="x", pady=5)

        item_label = ttk.Label(item_frame, text=item, font=("PT Mono", 14))
        item_label.pack(side="left", padx=5)

        # store reference to the item label
        self.item_labels[item] = item_label

        # check if the item is marked as done and apply style
        if item in self.done_items:
            item_label.configure(style="GreyedOut.TLabel")

        done_button = ttk.Button(
            item_frame, text="Done", command=lambda: self.mark_as_done(item)
        )
        done_button.pack(side="right", padx=5)

        remove_button = ttk.Button(
            item_frame, text="Remove", command=lambda: self.remove_item(item)
        )
        remove_button.pack(side="right", padx=5)

    # function that changes the style of the widget
    def mark_as_done(self, item):
        """Marks the item as done by setting a different style"""
        if item in self.item_labels:
            item_label = self.item_labels[item]
            item_label.configure(style="GreyedOut.TLabel")
            self.done_items.add(item)
        print(f"Item marked as done: {item}")

    # function that removes the item from the list
    def remove_item(self, item):
        """Removes the item from the active list and refreshes display"""
        if self.controller.active_list:
            self.controller.lists[self.controller.active_list].remove(item)
            if item in self.done_items:
                self.done_items.remove(item)
            self.show_active_list_contents()
            print(f"Item removed: {item}")


# call main
if __name__ == "__main__":
    app = Application()
    app.resizable(width=False, height=False)
    app.mainloop()
