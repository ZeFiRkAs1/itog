import tkinter as tk
import sqlite3
from tkinter import ttk


#self.add_img = tk.PhotoImage(file = './img/add.png')
# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_record()

    # Панель инструментов
    def init_main(self):
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)

        toolbar.pack(side = tk.TOP, fill = tk.X)

        # Создание кнопки добавления контакта
        self.add_img = tk.PhotoImage(file = 'add.png')
        btn_add = tk.Button(toolbar, bg = '#d7d7d7', bd = 0,image = self.add_img,  command = self.open_dialog) #image = self.add_img,

        btn_add.pack(side = tk.LEFT)
        self.edit_img = tk.PhotoImage(file = 'update.png')
        btn_edit = tk.Button(toolbar, bg = '#d7d7d7', bd = 0,image = self.edit_img,  command = self.open_edit)
        btn_edit.pack(side = tk.LEFT)

        # создание кнопки удаления контакта
        self.delete_img = tk.PhotoImage(file = 'delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                            image=self.delete_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # создание кнопки поиска контакта
        self.search_img = tk.PhotoImage(file = 'search.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                            image=self.search_img,
                            command=self.open_search)
        btn_del.pack(side=tk.LEFT)

        # Создание кнопки таблицы
        self.refresh_img = tk.PhotoImage(file = 'refresh.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                            image=self.refresh_img,
                            command=self.view_record)
        btn_del.pack(side=tk.LEFT)

        # Создание таблицы
        self.tree = ttk.Treeview(root, 
                                 columns=('id', 'name', 'tel', 'email','salary'),
                                 height=45,
                                 show='headings')
        # добавляем параметры столбцам
        self.tree.column('id', width=45, anchor=tk.CENTER)#айди
        self.tree.column('name', width=150, anchor=tk.CENTER)#имя
        self.tree.column('tel', width=150, anchor=tk.CENTER)#номер телефона
        self.tree.column('email', width=150, anchor=tk.CENTER)# электронная почта
        self.tree.column('salary',width=150,anchor=tk.CENTER)#зарплата - salare

        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary',text='зарплата сотрудника')
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(root, command = self.tree.yview)
        scroll.pack(side = tk.LEFT, fill = tk.Y)
        self.tree.configure(yscrollcommand = scroll.set)

    def records(self, name, tel, email,salary):
        self.db.insert_data(name, tel, email,salary)
        self.view_record()
    
    # метод редактирования
    def edit_record(self, name, tel, email,salary):
        ind = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, tel, email, salary,ind))

        self.db.conn.commit()

        self.view_record()

    # метод удаления записей
    def delete_records(self):
        # проходим циклом по всем выделенным строкам в таблице
        for i in self.tree.selection():
            # берем id каждой строки
            id = self.tree.set(i, '#1')
            # удаляем по id
            self.db.cur.execute('''
                DELETE FROM users
                WHERE id = ?
            ''', (id, ))
        self.db.conn.commit()
        self.view_record()

    # метод поиска записей
    def search_records(self, name):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?',
                            ('%' + name + '%', ))
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # Вызов дочернего окна
    def open_dialog(self):
        Child()

    # Вызов окна редактирования
    def open_edit(self):
        Update()

    def open_search(self):
        Search()

    def view_record(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM users')
        [self.tree.insert('', 'end', values = i) for i in self.db.cur.fetchall()]


# класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')

        # Запрет на изменения
        self.resizable(False, False)

        # Перехват изменений
        self.grab_set()

        # Захватываем фокус
        self.focus_set()

        # создание формы
        label_name = tk.Label(self, text = 'ФИО') 
        label_name.place(x = 50, y = 50)

        label_tel = tk.Label(self, text = 'Телефон')
        label_tel.place(x = 50, y = 80)

        label_email = tk.Label(self, text = 'E-Mail')
        label_email.place(x = 50, y = 110)

        label_email = tk.Label(self, text = 'зарплата сотрудника')
        label_email.place(x = 50, y = 140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x = 200, y = 50)

        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x = 200, y = 80)

        self.entry_email = tk.Entry(self)
        self.entry_email.place(x = 200, y = 110)

        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x = 200, y = 140)


        self.btn_ok = tk.Button(self, text = 'Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                    self.entry_tel.get(),
                                                                    self.entry_email.get(),
                                                                    self.entry_salary.get()))
        self.btn_ok.place(x = 220, y = 160)

        btn_exit = tk.Button(self, text = 'Закрыть', command = self.destroy)
        btn_exit.place(x = 300, y = 160)

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db

    def init_edit(self):
        self.title('Редактирование контакта')

        self.btn_ok.destroy() # Убираем кнопку добавить

        btn_ok = tk.Button(self, text = 'Редактировать')
        btn_ok.bind('<Button-1>', lambda ev: self.view.edit_record(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get(),
            self.entry_salary.get()
        ))
        btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        btn_ok.place(x = 200, y = 160)

    # метод автозаполнения формы старыми данными
    def load_data(self):
        self.db.cur('''SELECT * FROM users WHERE id = &''',
                    self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('400x200')

        # Запрет на изменения
        self.resizable(False, False)

        # Перехват изменений
        self.grab_set()

        # Захватываем фокус
        self.focus_set()

        # создание формы
        label_name = tk.Label(self, text = 'ФИО')
        label_name.place(x = 50, y = 50)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x = 200, y = 50)


        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>', 
                         lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', 
                         lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=230, y=70)

        btn_exit = tk.Button(self, text = 'Закрыть', command = self.destroy)
        btn_exit.place(x = 300, y = 160)

# класс бд
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary TEXT
                )
            '''
        )



    # Метод добавления в бд
    def insert_data(self, name, tel, email,salary):
        self.cur.execute(
            '''
                INSERT INTO users (name, phone, email,salary)
                VALUES(?, ?, ?,?)
            ''', (name, tel, email,salary)
        )

        self.conn.commit()


# действия при запуске
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)

    root.title('Список сотрудников компании')
    root.geometry('665x400')

    # Запрет на изменения
    root.resizable(False, False)
    root.mainloop()