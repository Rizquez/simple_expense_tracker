from tkinter.ttk import Entry, Button, OptionMenu, Scrollbar, Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, StringVar, Label, ttk, CENTER
import matplotlib.pyplot as plt
from tkcalendar import Calendar
from tkinter import messagebox


from src.utils.db import db_query_params, db_query_simple

class RecordTrackExpense():

    def __init__(self, root):
        self.db = 'src/database/expense_control.db'
        self.window = root
        self.window.title("Control de Gastos")
        self.window.configure(background='PeachPuff3')

        ancho = 940
        alto = 580
        x_window = self.window.winfo_screenwidth() // 2 - ancho // 2
        y_window = self.window.winfo_screenheight() // 2 - alto // 2
        posicion = str(ancho)+'x'+str(alto)+'+'+str(x_window)+'+'+str(y_window)
        self.window.geometry(posicion)
        self.window.resizable(True, True)

        self.window.wm_iconbitmap('src/sources/expense_icon.ico')

        style_button = ttk.Style()
        style_button.configure('boton.TButton', font=('Comic Sans MS', 10), background='NavajoWhite4')

        style_view = ttk.Style()
        style_view.configure('mystyle.Treeview', highlightthickness=0, background='white', font=('Comic Sans MS', 10))
        style_view.configure('mystyle.Treeview.Heading', font=('Comic Sans MS', 13))
        style_view.layout('mystyle.Treeview', [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.var_choice = StringVar()
        self.entries_dct = {}

        frame_info = Frame(self.window, bg='PeachPuff3', padx=10, pady=10)
        frame_info.grid(row=0, column=0, sticky='n', padx=10, pady=10)
        label_categoria = Label(frame_info, text='Categorias', font=('Comic Sans MS', 16), bg='PeachPuff3')
        label_categoria.grid(row=0, column=0)
        lst_categorias = ['Listado - Tipos de Gasto','Comida', 'Compras', 'Facturas', 'Ocio', 'Salud', 'Transporte', 'Viaje', 'Otros']
        self.menu = OptionMenu(frame_info, self.var_choice, *lst_categorias)
        self.menu.grid(row=1, column=0)
        label_amount = Label(frame_info, text='Monto (€)', font=('Comic Sans MS', 16), bg='PeachPuff3')
        label_amount.grid(row=2, column=0)
        self.entry_amount = Entry(frame_info, width=15)
        self.entry_amount.grid(row=3, column=0)
        label_note = Label(frame_info, text='Notas adicionales', font=('Comic Sans MS', 16), bg='PeachPuff3')
        label_note.grid(row=4, column=0)
        self.entry_note = Entry(frame_info, width=35)
        self.entry_note.grid(row=5, column=0)
        boton_save = Button(frame_info, text='Guardar', style='boton.TButton', command=self.save_info)
        boton_save.grid(row=6, column=0)

        frame_calendar = Frame(self.window, bg='PeachPuff3', padx=10, pady=10)
        frame_calendar.grid(row=0, column=1, padx=10, pady=10)
        self.calendar = Calendar(frame_calendar, selectmode='day', day=16, month=9, year=2023)
        self.calendar.config(background='SlateBlue3')
        self.calendar.grid(row=0, column=0)

        
        self.show_by_date = Button(frame_calendar, text='Buscar fecha', style='boton.TButton', command=self.search_by_date)
        self.show_by_date.grid(row=1, column=0)

        self.show_by_month = Button(frame_calendar, text='Mostar Mes', style='boton.TButton', command=self.get_month)
        self.show_by_month.grid(row=2, column=0)

        self.frame_graph = Frame(self.window, bg='PeachPuff3', padx=10, pady=10)
        self.frame_graph.grid(row=0, column=2, padx=10, pady=10)

        frame_tabla = Frame(self.window, borderwidth=6)
        frame_tabla.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
        self.tabla = Treeview(frame_tabla, height=10, columns=[f"#{n}" for n in range(1, 4)], style='mystyle.Treeview')
        self.tabla.heading("#0", text='Fecha', anchor=CENTER)
        self.tabla.heading("#1", text='Monto (€)', anchor=CENTER)
        self.tabla.heading("#2", text='Categoria', anchor=CENTER)
        self.tabla.heading("#3", text='Notas', anchor=CENTER)
        self.tabla.column("#0", anchor=CENTER)
        self.tabla.column("#1", anchor=CENTER)
        self.tabla.column("#2", anchor=CENTER)
        self.tabla.column("#3", anchor=CENTER)
        y_scrollbar = Scrollbar(frame_tabla, orient='vertical', command=self.tabla.yview)
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscroll=y_scrollbar.set)
        self.tabla.grid(row=0, column=0, padx=10, pady=10)

        self.get_record()


    def save_info(self):
        if self.var_choice.get() != 'Listado - Tipos de Gasto':
            try:
                float(self.entry_amount.get())
                self.add_info_db()
            except ValueError:
                messagebox.showinfo("Error", "Introduza un valor numerico")
        else:
            messagebox.showinfo("Error", "Seleccione una categoria")

    def add_info_db(self):
        db_query_params(
            self.db,
            "INSERT INTO record_expense VALUES (NULL, ?, ?, ?, ?)",
            (
                self.calendar.get_date(),
                self.entry_amount.get(),
                self.var_choice.get(),
                self.entry_note.get()
                )
            )
        self.get_record()

    def get_record(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        registros = db_query_simple(
            self.db,
            "SELECT * FROM record_expense ORDER BY period ASC"
            )
        
        for fila in registros:
            self.tabla.insert("", 0, text=(fila[1]), values=(fila[2], fila[3], fila[4]))

        self.create_category_chart("SELECT category FROM record_expense")

    def search_by_date(self):
        for items in self.tabla.get_children():
            self.tabla.delete(items)
        
        exec_query = db_query_params(
            self.db,
            "SELECT * FROM record_expense WHERE period=?",
            (
                self.calendar.get_date(),
                )
            )
        
        result = exec_query.fetchall()
        for fila in result:
            self.tabla.insert("", 0, text=(fila[1]), values=(fila[2], fila[3], fila[4]))

        self.create_category_chart(f"SELECT category FROM record_expense WHERE period='{self.calendar.get_date()}'")
       
    def get_month(self):
        for items in self.tabla.get_children():
            self.tabla.delete(items)

        registros = db_query_simple(
            self.db,
            "SELECT * FROM record_expense ORDER BY period ASC"
            )

        for fila in registros:
            date = fila[1]
            if date.split('/')[1] == str(self.calendar.get_displayed_month()[0]):
                self.tabla.insert("", 0, text=(fila[1]), values=(fila[2], fila[3], fila[4]))
            
        self.create_category_chart(f"SELECT category FROM record_expense WHERE SUBSTR(period, 4, 2) ='{self.calendar.get_displayed_month()[0]}'")


    def create_category_chart(self, query):
        categories = db_query_simple(self.db, query)
        category_counts = {}

        for category in categories:
            category_name = category[0]
            if category_name in category_counts:
                category_counts[category_name] += 1
            else:
                category_counts[category_name] = 1

        plt.figure(figsize=(3.4, 2.5), facecolor='#F5F5DC')
        plt.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', startangle=140)

        chart_container = FigureCanvasTkAgg(plt.gcf(), master=self.frame_graph)
        chart_container_widget = chart_container.get_tk_widget()
        chart_container_widget.grid(row=0, column=0)