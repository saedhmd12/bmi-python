from database_connector import DatabaseConnector
from commands import Commands
import tkinter as tk
from tkinter.ttk import Style

class Application():
	"""A class that represents the BMI app."""

	def __init__(self):
		"""Initialize database connector and window."""
		self.db_connector = DatabaseConnector()
		self.data_table = self.db_connector.retrieve_table()

		self.window = tk.Tk()  # initialize the gui window
		self.style = Style()  # initialize the styler

	def run_app(self):
		self.init_window()
		self.load_images()
		self.init_menus_buttons()

	def init_window(self):
		self.window.title('Body Mass Index')
		self.window.grid('620x420')
		self.window.bind('<Control-x>', quit)
		self.window.bind('<Control-s>', Save)
		self.window.bind('<Control-d>', Delete)
		self.window.bind('<Control-B>', VAll)
		self.window.bind('<Control-b>', VOne)
		self.window.bind('<Control-u>', Update)
		self.window.bind('<Control-r>', Calcul)
		self.window.bind('<Control-q>', Clear)

	def load_images(self):
		"""Load the images."""
		self.exit_img = tk.PhotoImage(file='../assets/exit.png')
		self.about_img = tk.PhotoImage(file='../assets/about.png')
		self.theme_img = tk.PhotoImage(file='../assets/theme.png')
		self.save_img = tk.PhotoImage(file='../assets/save.png')
		self.delete_img = tk.PhotoImage(file='../assets/delete.png')
		self.improve_img = tk.PhotoImage(file='../assets/improve.png')
		self.viewall_img = tk.PhotoImage(file='../assets/viewall.png')
		self.viewone_img = tk.PhotoImage(file='../assets/viewone.png')
		self.update_img = tk.PhotoImage(file='../assets/update.png')
		self.calculate_img = tk.PhotoImage(file='../assets/calculate.png')
		self.color_img = tk.PhotoImage(file='../assets/color.png')
		self.clear_img = tk.PhotoImage(file='../assets/clear.png')

	def init_menus_buttons(self):
		"""Initialize all menus and all buttons."""
		# Initialize the menu bar and the file menu.
		self.menu_bar = tk.Menu(self.window)

		self.file_menu = tk.Menu(self.menu_bar, tearoff=0)

		# Initialize the edit menu and the help menu.
		self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
		self.help_menu = tk.Menu(self.menu_bar, tearoff=0)

		self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)  # add edit menu cascade

		# Initialize the sub menus.
		self.theme_sub_menu = tk.Menu(self.edit_menu, tearoff=0)
		self.sub_menu = tk.Menu(self.edit_menu, tearoff=0)  # TODO dont understand what this is for!

		# Add cascades to the file menu.
		self.file_menu.add_cascade(label='  Save                  Ctrl+S', image=self.save_img, compound=tk.LEFT, command=Save)
		self.file_menu.add_cascade(label='  Delete               Ctrl+D', image=self.delete_img, compound=tk.LEFT, command=Delete)
		self.file_menu.add_cascade(label='  View one          Ctrl+b', image=self.viewone_img, compound=tk.LEFT, command=VOne)
		self.file_menu.add_cascade(label='  View all             Ctrl+shift+b', image=self.viewall_img, compound=tk.LEFT, command=VAll)
		self.file_menu.add_separator()

		# Add cascades to the edit menu.
		self.edit_menu.add_cascade(label='  Update             Ctrl+u', image=self.update_img, compound=tk.LEFT, command=Update)
		self.edit_menu.add_cascade(label='Calculate           Ctrl+R', image=self.calculate_img, compound=tk.LEFT, command=Calcul)
		self.edit_menu.add_cascade(label='Clear                  Ctrl+Q', image=self.clear_img, compound=tk.LEFT, command=Clear)
		self.edit_menu.add_separator()
		self.edit_menu.add_cascade(label='  Colors', image=self.color_img, compound=tk.LEFT, menu=submenu, underline=0)

		# Add theme changing buttons.
		self.theme_sub_menu.add_radiobutton(label='Light-theme', command=test)
		self.theme_sub_menu.add_radiobutton(label='White-red theme', command=white_red)
		self.theme_sub_menu.add_radiobutton(label='white-gray theme', command=white_gray)
		self.theme_sub_menu.add_radiobutton(label='Dark-red theme', command=dark_red)
		self.theme_sub_menu.add_radiobutton(label='Brown-yellow theme', command=brown_yello)

		self.edit_menu.add_cascade(label='  Themes', image=self.theme_img, compound=tk.LEFT, menu=self.sub_menu)

		# TODO add comment here, what do these functions do?
		self.sub_menu.add_radiobutton(label='default', command=default)
		self.sub_menu.add_radiobutton(label='clam', command=clam)
		self.sub_menu.add_radiobutton(label='alt', command=alt)
		self.sub_menu.add_radiobutton(label='classic', command=classic)

		# Add help menu cascades.
		self.menu_bar.add_cascade(label='help', menu=self.help_menu)
		self.help_menu.add_cascade(label='improve your health?', image=self.improve_img, compound=tk.LEFT, command=help_me)
		self.help_menu.add_cascade(label='About bmi calculator', image=self.about_img, compound=tk.LEFT, command=about)

		# Add exit cascade and window configuration.
		self.file_menu.add_cascade(label='  Exit                    Ctrl+X', image=self.exit_img, compound=tk.LEFT, command=Exit)
		self.window.config(menu=self.menu_bar)

	def init_labels(self):
		"""Initialize labels."""
		self.bmi_calculator_label = tk.Label(self.window, text='BMI CALCULATOR', font=('Arial', 20))
		self.full_name_label = tk.Label(self.window, text='Full Name')
		self.weight_label = tk.Label(self.window, text='Weight in kg')
		self.height_label = tk.Label(self.window, text='Height in m')
		self.birthdate_label = tk.Label(self.window, text='Date of Birth')

	def init_entries(self):
		"""Initialize entries."""
		self.name_entry = tk.Entry(self.window, textvariable=tk.StringVar())  # name entry
		self.weight_entry = tk.Entry(self.window, textvariable=tk.StringVar(), justify='right')  # weight entry
		self.height_entry = tk.Entry(self.window, textvariable=tk.StringVar(), justify='right')  # height entry

		# TODO might need to refactor some of the following code:
		date_var = date.today()
		self.date_today = datetime(date_var.year, date_var.month, date_var.day)
		self.date_entry = DateEntry(win, width=12, borderwidth=2, day=date_var.day, month=date_var.month,
									year=date_var.year, date_pattern='dd/mm/yyyy', maxdate=date_var)
