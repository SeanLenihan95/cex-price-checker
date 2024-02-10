import tkinter as tk
import ttkbootstrap as ttk
import PIL
import os

from .settings import *
from utils.helpers import *
from logic.cex_checker import *

class App(ttk.Window):
    def __init__(self):
        def initial_setup():
            self.columnconfigure(0, weight=3)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)

            heading = tk.Label(master=self, text=APP_NAME, font=f'{FONT} {H1_STYLES}')
            heading.grid(column=0, row=0, columnspan=2, sticky='new', ipady=DEFAULT_PADDING / 2)

            self.column_a = tk.Frame(master=self)
            self.column_b = tk.Frame(master=self)

            self.column_a.grid(column=0, row=1, sticky='news')
            self.column_b.grid(column=1, row=1, sticky='news')

        def fill_column_a():
            self.title = Entry(master=self.column_a, label_text='Title:   ')
            
            self.categories = LinkedCascadingComboboxes(master=self.column_a, 
                                                        data=self.checker.get_supported_categories(),
                                                        event_to_bind=self.on_category_input)

            midsection = tk.Frame(master=self.column_a)
            midsection.pack(padx=DEFAULT_PADDING, fill='x', pady=10)
            
            self.condition = RadioButtonMenu(master=midsection, label_text='Preferred Condition:', default_value='Boxed',
                             button_templates=(('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')))

            # self.condition = Dropdown(master=midsection, label_text='Condition:      ', options=['A', 'B', 'C'])

            search_button_container = tk.Frame(master=midsection)
            search_button_container.pack(expand=True, anchor='e')
            self.search_button = tk.Button(master=search_button_container, text='SEARCH', width=15, command=self.search, state=tk.DISABLED)
            self.search_button.pack()
            
            self.results_box = ResultsBox(master=self.column_a, checker=self.checker)
            
        def fill_column_b():
            self.scrolllist_heading = tk.Label(master=self.column_b, text='Total (0 Items)', font=f'{FONT} {H2_STYLES}')
            self.scrolllist_heading.pack(fill='x', pady=0)

            self.scroll_list = ScrollList(master=self.column_b)

            button_section = tk.Frame(master=self.column_b)
            button_section.pack(fill='x', padx=DEFAULT_PADDING, pady=0)
            
            tk.Button(master=button_section, text='Add to Total', width=20, command=self.add_to_scrolllist).pack(side='left')
            tk.Button(master=button_section, text='Clear All', width=20, command=self.scroll_list.clear_all_items).pack(side='right')

            self.total_box = TotalBox(master=self.column_b)
            
        # main setup
        super().__init__(themename='darkly')
        self.title(APP_NAME)
        self.geometry(f'{WIDTH}x{HEIGHT}')
        self.checker = CeXChecker()
        
        # create widgets
        initial_setup()
        fill_column_a()
        fill_column_b()
        
        # resizing variables/bindings
        self.debounce_timer = None
        self.bind('<Configure>', self.on_resize)
        
    def run(self):
        self.mainloop()

    def search(self):
        title = self.title.get()
        category, subcategory = self.categories.get()
        condition = None if self.condition.get() == 'None' else self.condition.get()

        self.results_box.search(args=[title, category, subcategory, condition])
        self.results_box.display_result(0)

    def add_to_scrolllist(self):
        def preprocess_image(image_url):
            image = get_image_from_url(image_url)

            ratio = ITEM_IMAGE_MAX_WIDTH / image.width if image.width >= image.height else \
                    ITEM_IMAGE_MAX_HEIGHT / image.height
                
            image = image.resize((round(image.width * ratio), round(image.height * ratio)))
            
            return convert_PIL_to_tk(image)
        
        if not self.results_box.results:
            return
        
        result = self.results_box.results[self.results_box.current_result_index]
        
        if result:
            self.scroll_list.insert(title=result['title'],
                                    cash = result['sell_price_cash'],
                                    voucher = result['sell_price_voucher'],
                                    buy = result['buy_price'],
                                    image=preprocess_image(image_url=result['image']))
            
            self.update_totals()

    def on_category_input(self, event):
        category, subcategory = self.categories.get()
        
        # invalid category/subcategory, disable search button and condition radio buttons
        if category not in self.checker.get_supported_categories() or subcategory not in self.checker.get_supported_categories()[category]:
            self.condition.disable_buttons()
            self.search_button.config(state=tk.DISABLED)
        
        # categories are valid and condition-specific, change condition buttons accordingly and enable searching 
        elif category in CONDITION_BASED_CATEGORIES and subcategory in CONDITION_BASED_CATEGORIES[category]:
            self.condition.change_buttons(CONDITION_BASED_CATEGORIES[category][subcategory])
            self.search_button.config(state=tk.NORMAL)

        # categories are valid and non-condition-specific, disable condition buttons but enable searching
        else:
            self.condition.disable_buttons()
            self.search_button.config(state=tk.NORMAL)

    def update_totals(self):
        total_cash, total_voucher, total_buy = 0, 0, 0

        for item in self.scroll_list.items:
            total_cash += item.cash
            total_voucher += item.voucher
            total_buy += item.buy
        
        self.total_box.set_cash(total_cash)
        self.total_box.set_voucher(total_voucher)
        self.total_box.set_buy(total_buy)

        heading = f'Total ({len(self.scroll_list.items)} Item)' if len(self.scroll_list.items) == 1 else f'Total ({len(self.scroll_list.items)} Items)'
        self.scrolllist_heading.config(text=heading)

    def on_resize(self, event):
        def adjust_label_wraplengths():        
            current_width = self.winfo_width()
            ratio = current_width / WIDTH

            results_box_labels = self.results_box.results_container.grid_slaves()
            for label in results_box_labels:
                if 'bold' in label.cget("font"):
                    label.config(wraplength=TAG_WRAPLENGTH * ratio)
                else:
                    label.config(wraplength=CONTENT_WRAPLENGTH * ratio)

            for item in self.scroll_list.items:
                item_labels = [widget for widget in item.caption_container.winfo_children() if isinstance(widget, tk.Label)]
                for label in item_labels:
                    label.config(wraplength=ITEM_WRAPLENGTH * ratio)

            self.scroll_list.update_scrollregion()
        
        if self.debounce_timer:
            self.after_cancel(self.debounce_timer)

        self.debounce_timer = self.after(200, adjust_label_wraplengths)

class Entry(tk.Frame):
    def __init__(self, master, label_text):
        super().__init__(master=master)
        self.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING / 2, fill='both')

        tk.Label(master=self, text=label_text, font=f'{FONT} {TAG_STYLES}').pack(side='left')

        self.entry = tk.Entry(master=self)
        self.entry.pack(side='right', expand=True, fill='x')

    def get(self):
        return self.entry.get()
    
class Dropdown(tk.Frame):
    def __init__(self, master, label_text, options):
        super().__init__(master=master)
        self.pack(side='left')

        tk.Label(master=self, text=label_text, font=f'{FONT} {TAG_STYLES}').pack(side='left')

        style = ttk.Style()
        style.configure('TCombobox', 
                        padding=(5, 2, 20, 2))

        self.dropdown_menu = ttk.Combobox(master=self, values=options)
        self.dropdown_menu.pack(side='right', expand=True, fill='x')

    def get(self):
        return self.dropdown_menu.get()

class LinkedCascadingComboboxes(tk.Frame):
    class CascadingCombobox(ttk.Combobox):
        def __init__(self, master, values, side, default_text, event_to_bind):
            self.var = tk.StringVar()
            self.default_text = default_text

            super().__init__(master=master, textvariable=self.var, values=values)
            self.pack(padx=5, side=side, anchor='w' if side == 'left' else 'e', fill='x', expand=True)
            
            self.set(default_text)
            self.bind('<KeyRelease>', event_to_bind)
            self.bind('<<ComboboxSelected>>', event_to_bind)

        def get(self):
            return self.var.get()

    def __init__(self, master, data, event_to_bind):
        super().__init__(master=master)
        self.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING // 1.5, fill='x')

        self.data = data

        style = ttk.Style()
        style.configure('TCombobox', padding=(5, 2, 20, 2))

        self.category_combobox = LinkedCascadingComboboxes.CascadingCombobox(master=self,
                                                                             values=list(self.data.keys()),
                                                                             side='left',
                                                                             default_text='Select a Category',
                                                                             event_to_bind=event_to_bind)
        
        self.subcategory_combobox = LinkedCascadingComboboxes.CascadingCombobox(master=self,
                                                                                values=None,
                                                                                side='right',
                                                                                default_text='Select a Subcategory',
                                                                                event_to_bind=event_to_bind)
    
        self.category_combobox.bind('<<ComboboxSelected>>', self.update_subcategory_options)
    
    def update_subcategory_options(self, event):
        category = self.category_combobox.get()
        self.subcategory_combobox['values'] = []
        self.subcategory_combobox.set(self.subcategory_combobox.default_text)

        if category not in self.data:
            return
        
        self.subcategory_combobox['values'] = self.data[category]

    def get(self):
        return (self.category_combobox.get(), self.subcategory_combobox.get())

class RadioButtonMenu(tk.Frame):
    def __init__(self, master, label_text, default_value, button_templates):
        super().__init__(master=master)
        self.pack(side='left')
        
        self.option = tk.StringVar(value=default_value)
        self.buttons = []

        tk.Label(master=self, text=label_text, font=f'{FONT} {TAG_STYLES}').pack(fill='y', expand=True)

        for button_template in button_templates:
            self.create_button(button_template)

    def get(self):
        if any(button.cget('state') == 'normal' for button in self.buttons):
            return self.option.get()

    def create_button(self, button_template):
        text, value = button_template
        radio_button = tk.Radiobutton(master=self, text=text, value=value, variable=self.option)
        radio_button.pack(side='left', padx=2)
        self.buttons.append(radio_button)

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state='disabled')

    def change_buttons(self, button_templates):
        # destroy all current buttons
        while len(self.buttons) != 0:
            button = self.buttons[0]
            self.buttons.remove(button)
            button.destroy()

        for button_template in button_templates:
            self.create_button(button_template)

        self.pack()

class ResultsBox(tk.Frame):
    def __init__(self, master, checker):
        def initialise_top_half():
            os.chdir('C:/Users/seanl/OneDrive/Desktop/projects/cex-only-checker/v_1')
            RELATIVE_PATH = 'images/'
            
            default_image = PIL.Image.open(RELATIVE_PATH + 'cex_logo.jpg')
            default_image = self.preprocess_image(default_image)
            self.default_image = default_image
            
            no_results_image = PIL.Image.open(RELATIVE_PATH + 'cex_no_results.png')
            no_results_image = self.preprocess_image(no_results_image)
            self.no_results_image = no_results_image

            image_and_buttons_container = tk.Frame(master=self)
            image_and_buttons_container.pack(fill='x')

            self.left_button = tk.Button(master=image_and_buttons_container, 
                                         width=3, 
                                         text='<', 
                                         command=lambda: self.display_result(index=self.current_result_index - 1))
            self.left_button.pack(side='left', expand=True)

            self.image_container = tk.Label(master=image_and_buttons_container, text='RESULT X OF X')
            self.image_container.pack(side='left')

            self.right_button = tk.Button(master=image_and_buttons_container, 
                                          width=3, 
                                          text='>', 
                                          command=lambda: self.display_result(index=self.current_result_index + 1))
            self.right_button.pack(side='left', expand=True)

            self.result_number_label = tk.Label(master=self, text='Result 0 of 0', fg='gray')
            self.result_number_label.pack(fill='x', pady=DEFAULT_PADDING // 4)

            self.display_image(default_image)
        
        def initialise_bottom_half():
            self.number_of_results_rows = len(DEFAULT_CEX_CONTENT)
            self.results_container = tk.Frame(master=self)
            
            # initialise columns
            self.results_container.columnconfigure(0, weight=2, minsize=RESULTS_TAG_MIN_WIDTH)
            self.results_container.columnconfigure(1, weight=5, minsize=RESULTS_CONTENT_MIN_WIDTH)
            
            # initialise rows
            for row in range(self.number_of_results_rows):
                self.results_container.rowconfigure(row, weight=1)

            self.results_container.pack(fill='both', expand=True, pady=DEFAULT_PADDING // 2)

            # populate container with empty labels
            for i in range(self.number_of_results_rows):
                label = tk.Label(master=self.results_container, wraplength=TAG_WRAPLENGTH, justify='center', font=f'{FONT} {TAG_STYLES}')
                label.grid(column=0, row=i, sticky='we')

                label = tk.Label(master=self.results_container, wraplength=CONTENT_WRAPLENGTH)
                label.grid(column=1, row=i)
        
        super().__init__(master=master, bd=1, relief="sunken")

        self.checker = checker
        self.results = []
        self.current_result_index = 0

        self.heading = tk.Label(master=self, text='CeX Results', font=f'{FONT} {H2_STYLES}')
        self.heading.pack(fill='both', pady=DEFAULT_PADDING / 2)

        initialise_top_half()
        initialise_bottom_half()
        self.fill(content=DEFAULT_CEX_CONTENT, column='both')

        self.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, fill='both', expand=True)

    def search(self, args):
        self.results = self.checker.search(*args)

    def display_result(self, index):
        if not self.results:
            if self.current_image == self.default_image: # do nothing if no searches have been made
                return
            else:
                self.fill(content=['-'] * self.number_of_results_rows, column='right')
                self.display_image(self.no_results_image)
                self.result_number_label.config(text='Result 0 of 0')
                return
        
        # get result
        index = index % len(self.results)
        result = self.results[index]

        # update image
        image = get_image_from_url(result['image'])
        
        if image is None:
            self.display_image(self.default_image)
        else:
            image = self.preprocess_image(image)
            self.display_image(image)

        self.current_result_index = index
        self.result_number_label.config(text=f'Result {index + 1} of {len(self.results)}')

        # update results
        content = self.checker.prettify_results(result)
        self.fill(content=content, column='right')

    def preprocess_image(self, image):
        ratio = RESULTS_IMAGE_MAX_HEIGHT / image.height
        new_width = round(image.width * ratio) if round(image.width * ratio) <= RESULTS_IMAGE_MAX_WIDTH else RESULTS_IMAGE_MAX_WIDTH
        resized_image = image.resize((new_width, RESULTS_IMAGE_MAX_HEIGHT))

        return convert_PIL_to_tk(resized_image)
    
    def display_image(self, image):
        self.current_image = image
        self.image_container.config(image=image)

    def fill(self, content, column):
        """Fills the given column of the results box with the given content."""
        labels_to_change = self.results_container.grid_slaves()
        labels_to_change.reverse()

        if column == 'left' and isinstance(content, list):
            labels_to_change = [label for label in labels_to_change if 'bold' in label.cget("font")] # tag labels only
        elif column == 'right' and isinstance(content, list):
            labels_to_change = [label for label in labels_to_change if 'bold' not in label.cget("font")] # content labels only
        elif column == 'both' and isinstance(content, dict):
            content = [element for pair in content.items() for element in pair] # convert dictionary into list in the form (key1, value1, key2, value2, etc.)
        else:
            return
        
        if len(labels_to_change) != len(content):
            return

        for i, value in enumerate(content):
            labels_to_change[i].config(text=value)

class ScrollList(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, bd=1, relief="sunken")
        self.pack(fill='both', expand=True, pady=DEFAULT_PADDING)

        self.items = []
        self.images = []

        self.scrollbar = tk.Scrollbar(self, orient="vertical", width=17)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self, width=105, yscrollcommand=self.scrollbar.set, bd=1, relief="sunken")
        self.canvas.pack(side="left", fill='both', expand=True)

        self.frame = tk.Frame(master=self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=SCROLL_LIST_WIDTH)

        self.scrollbar.config(command=self.canvas.yview)

        # Update width of canvas window when GUI is resized
        master.bind("<Configure>", lambda event: self.canvas.itemconfig(self.canvas_window, width=event.width))
    
    def insert(self, image, title, cash, voucher, buy):
        item = ScrollListItem(master=self.frame, 
                              scrolllist=self, 
                              image=image, 
                              title=title, 
                              cash=cash, 
                              voucher=voucher, 
                              buy=buy)
        
        self.items.append(item)
        self.images.append(image)

        # Update the window when the size of the canvas changes
        self.frame.update_idletasks()

        # Update scroll region to accomodate new item
        self.update_scrollregion()

        # Scroll to bottom of list
        self.canvas.yview_moveto(1.0)

    def clear_all_items(self):
        while len(self.items) != 0:
            self.items[0].delete()

        self.items = []
        self.images = []

        self.winfo_toplevel().update_totals()
        self.update_scrollregion()

    def update_scrollregion(self):
        total_height = sum(widget.winfo_height() for widget in self.frame.winfo_children())
        self.canvas.config(scrollregion=(0, 0, SCROLL_LIST_WIDTH, total_height))

class ScrollListItem(tk.Frame):
    def __init__(self, master, scrolllist, image, title, cash, voucher, buy):
        super().__init__(master=master, bd=1, relief="sunken")
        self.pack(fill='x', ipady=5, expand=True)
        self.scrolllist = scrolllist

        self.cash = cash
        self.voucher = voucher
        self.buy = buy

        # Initialise image
        image_container = tk.Label(master=self, image=image, width=100, height=125)
        image_container.pack(side='left')

        # Initialise caption container
        self.caption_container = tk.Frame(master=self)
        self.caption_container.pack(side='left', padx=20, fill='x', expand=True)

        # Populate caption container
        tags = ['Title:', 'Cash:', 'Voucher:', 'Buy Price:']
        for i, tag in enumerate(tags):
            tk.Label(master=self.caption_container, text=tag, font=f'{FONT} {TAG_STYLES}').grid(column=0, row=i, sticky='w', padx=3)    
            
        content = [title, format_currency(cash), format_currency(voucher), format_currency(buy)]
        for i, element in enumerate(content):
            tk.Label(master=self.caption_container, text=element, wraplength=ITEM_WRAPLENGTH, justify='left').grid(column=1, row=i, sticky='w', padx=15)            

        # Initialise delete button
        self.delete_button = None
        self.bind('<Enter>', self.show_delete_button)
        self.bind('<Leave>', self.hide_delete_button)

    def delete(self):
        # Remove reference to item from ScrollList's list of items
        self.scrolllist.items.remove(self)

        # Update totals
        self.winfo_toplevel().update_totals()
        
        # Destroy the widget itself
        super().destroy()

        # Update the scroll region of the ScrollList
        self.scrolllist.update_scrollregion()

    def show_delete_button(self, event):
        self.delete_button = tk.Button(master=self, text='X', width=4, command=self.delete)
        self.delete_button.place(x=self.winfo_width()-20, rely=0.0, anchor='ne')

    def hide_delete_button(self, event):
        if self.delete_button:
            self.delete_button.destroy()

class TotalBox(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, fill='both')

        self.total_cash = tk.Label(master=self, text='€0.00')
        self.total_voucher = tk.Label(master=self, text='€0.00')
        self.total_buy = tk.Label(master=self, text='€0.00')
        
        for i in range(2):
            self.columnconfigure(i, weight=1)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        for i, tag in enumerate(['Total Sell Price (Cash):', 'Total Sell Price (Voucher):', 'Total Buy Price:']):
            tk.Label(master=self, text=tag, font=f'{FONT} {TAG_STYLES}').grid(column=0, row=i, sticky='w', pady=2)

        for i, attribute in enumerate([self.total_cash, self.total_voucher, self.total_buy]):
            attribute.grid(column=1, row=i, sticky='w', pady=2)

    def set_voucher(self, text):
        self.total_voucher.config(text=format_currency(text))

    def set_cash(self, text):
        self.total_cash.config(text=format_currency(text))

    def set_buy(self, text):
        self.total_buy.config(text=format_currency(text))