# import modules
import os
import tkinter as tk
from tkinter import ttk

# from idlelib.tooltip import Hovertip


# create main application window
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Shopping Manager")
        self.container = ttk.Frame(self, height=300, width=300, padding=2)
        self.container.pack()
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        # setup navigation controller
        self.frames = {}
        for F in (MainPage, ActiveListPage, AllListsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        # Data structures for lists and items
        self.lists = {}
        self.active_list = None

        # show Main Page on start
        self.show_frame("MainPage")
        # check for existing list files
        # self.check_for_files()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "ActiveListPage":
            self.frames[page_name].show_active_list_contents()
        if page_name == "AllListsPage":
            self.frames[page_name].show_all_lists_contents()

    def show_home_page(self):
        self.show_frame("MainPage")

    def show_active_list_page(self):
        self.show_frame("ActiveListPage")

    def show_all_lists_page(self):
        self.show_frame("AllListsPage")

    def quit_app(self):
        self.quit()

    # manipulate files
    # def check_for_files(self):
    #     cwd = os.getcwd()+"/lists/"
    #     print(cwd)
    #     if not cwd:
    #         file = open("test.txt", "a")
    # dir_list = os.listdir(os.getcwd())

    def add_item(self, item):
        if self.active_list:
            self.lists[self.active_list].append(item)
            print(self.lists)
            print(self.active_list)
        else:
            self.lists["Default"] = [item]
            self.active_list = "Default"
            print(self.lists)
            print(self.active_list)


# create main page
class MainPage(tk.Frame):
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
        self.menu = tk.Menu(self.topNavButton, tearoff=0)
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
        # image tooltip
        # self.confirmItemButtonTooltip = Hovertip(self.confirmItemButton, 'Add to list')

        # separator
        self.menuSeparator = ttk.Separator(self)
        self.menuSeparator.pack(fill="x")

        # create bottom frame for displaying available lists
        self.bottomListFrame = ttk.Frame(self, height=300, width=300, padding=(10, 5))
        self.bottomListFrame.pack(fill="x")
        self.bottomListFrame.columnconfigure(0, weight=1)
        self.bottomListFrame.columnconfigure(1, weight=1)
        self.bottomListFrame.columnconfigure(2, weight=1)

        # Lists Title
        self.bottomListTitle = ttk.Label(
            self.bottomListFrame,
            text="All Lists",
            padding=(10, 10),
            font=("PT Mono", 16),
        )
        self.bottomListTitle.grid(row=0, column=1)

        # Icon button to navigate to All Lists window
        self.allListsIcon = tk.PhotoImage(file="icons8-documents-100.png")
        self.allListsLabel = tk.Label(self.bottomListFrame, image=self.allListsIcon)
        self.allListsLabel.grid(row=1, column=1, pady=10)
        self.allListsLabel.bind(
            "<Button-1>", lambda event: self.controller.show_all_lists_page()
        )

        # image tooltip
        # self.allListsLabelTooltip = Hovertip(self.allListsLabel, 'Access all lists')

    # function for adding a new item
    def prepare_item(self):
        item_name = self.inputItemBox.get()
        if item_name.isalpha():
            for widget in self.middleMenuFrame.winfo_children():
                widget.destroy()

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
        item_quantity = self.inputQuantityBox.get()
        if item_quantity.isnumeric():
            item = (item_name, item_quantity)
            print(item)
            self.controller.add_item(item)
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

    def show_all_lists_contents(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        all_lists = self.controller.lists
        active_list = self.controller.active_list
        print(all_lists)
        if len(all_lists) == 0:
            label = ttk.Label(
                self.scrollable_frame, text="No entries", font=("PT Mono", 14)
            )
            label.pack()

        else:
            for list_name in all_lists:
                self.create_list_widget(list_name, list_name == active_list)

    def create_list_widget(self, list_name, is_active):
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill="x", pady=5)
        
        print(f"Creating widget for: {list_name}")

        item_label = ttk.Label(item_frame, text=list_name, font=("PT Mono", 14))
        item_label.pack(side="left", padx=5)

        if is_active:
            action_text = "Open"
            action_command = lambda: self.controller.show_active_list_page()
        else:
            action_text = "Set Active"
            action_command = lambda: self.mark_as_active(list_name)
            
        action_button = ttk.Button(
            item_frame, text=action_text, command=action_command
        )
        action_button.pack(side="right", padx=5)

        remove_button = ttk.Button(
            item_frame, text="Remove", command=lambda: self.remove_list(list_name)
        )
        remove_button.pack(side="right", padx=5)

    # Mark list as active
    def mark_as_active(self, list_name):
        self.controller.active_list = list_name
        print(f"Item marked as active: {list_name}")
        self.show_all_lists_contents()

    def remove_list(self, list_name):
        # Check if the list exists in the controller
        if list_name in self.controller.lists:
        # If the list is the active list, reset the active list to None
            if list_name == self.controller.active_list:
                self.controller.active_list = None
            # Remove the list from the controller
            self.controller.lists.pop(list_name)
            # Refresh the list contents display
            self.show_all_lists_contents()
            print(f"List removed: {list_name}")

    def prepare_create_list(self):
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

    def show_active_list_contents(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        active_list = self.controller.lists.get(self.controller.active_list, [])
        if not active_list:
            label = ttk.Label(
                self.scrollable_frame, text="No entries", font=("PT Mono", 14)
            )
            label.pack()
        else:
            for item in active_list:
                self.create_item_widget(item)

    def create_item_widget(self, item):
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill="x", pady=5)

        item_label = ttk.Label(item_frame, text=item, font=("PT Mono", 14))
        item_label.pack(side="left", padx=5)

        done_button = ttk.Button(
            item_frame, text="Done", command=lambda: self.mark_as_done(item)
        )
        done_button.pack(side="right", padx=5)

        remove_button = ttk.Button(
            item_frame, text="Remove", command=lambda: self.remove_item(item)
        )
        remove_button.pack(side="right", padx=5)

    def mark_as_done(self, item):
        # Implement the logic for marking the item as done TO DO
        print(f"Item marked as done: {item}")

    def remove_item(self, item):
        if self.controller.active_list:
            self.controller.lists[self.controller.active_list].remove(item)
            self.show_active_list_contents()
            print(f"Item removed: {item}")


# call main
if __name__ == "__main__":
    app = Application()
    app.resizable(width=False, height=False)
    app.mainloop()
