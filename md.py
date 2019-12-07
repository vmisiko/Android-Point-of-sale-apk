#! / usr / bin / env python
# - * - coding: utf-8 - * -
from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivymd.textfields import MDTextField
from kivymd.navigationdrawer import MDNavigationDrawer
from kivy.properties import StringProperty, ObjectProperty
from kivymd.navigationdrawer import NavigationLayout
from kivy.uix.screenmanager import ScreenManager,Screen,WipeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import sqlite3
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
#from kivy.graphics.context_instructions import Color
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
#from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
#from kivy.uix.image import AsyncImage
#from KivyCalendar import CalendarWidget
#from KivyCalendar import DatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import sqlite3 as lite
from kivy.uix.image import Image
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager,Screen,WipeTransition
import sys
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.window import Window
import random

Window.size=(320,500)
conn = sqlite3.connect("demo.db")
con = conn.cursor()


class ImageButton(ButtonBehavior, Image):
    pass


class ViewStock(Screen):
    data_items = ListProperty([("?", "?", "?")])
    stock_name = ObjectProperty(None)
    stock_code = ObjectProperty(None)
    stock_price = ObjectProperty(None)
    stock_qty = ObjectProperty(None)
    stock_disc = ObjectProperty(None)
    stock_vat = ObjectProperty(None)
    controller = ObjectProperty(None)

    def go_back(self):
        n = self.manager.current = 'screen2'
        return n

    def __init__(self, **kwargs):
        super(ViewStock, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.viewstock()

    def get_table_column_headings(self):
        connection = sqlite3.connect("demo.db")

        with connection:
            # With the with keyword, the Python interpreter automatically releases the resources.
            # It also provides error handling
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(Stock)")
            col_headings = cursor.fetchall()
            self.total_col_headings = len(col_headings)

    def viewstock(self):
        con.execute("SELECT ITEM, CODE, QUANTITY, INITAL_PRICE FROM Stock ")
        rows = con.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

    def on_press(self, instance):

        self.setup_row_data(self.data_items[instance.index]['Index'])

    def setup_row_data(self, value):
        conn = sqlite3.connect("demo.db")
        con = conn.cursor()

        con.execute("SELECT ITEM, CODE,INITAL_PRICE, QUANTITY, DISCOUNT,VAT FROM Stock WHERE ITEM=?", (value,))
        self.row_data = con.fetchone()

        self.stock_name.text = str(self.row_data[0])
        self.stock_code.text = str(self.row_data[1])
        self.stock_price.text = str(self.row_data[2])
        self.stock_qty.text = str(self.row_data[3])
        self.stock_disc.text = str(self.row_data[4])
        self.stock_vat.text = str(self.row_data[5])

        # print(self.item.text)
        # print(self.qty.text)
        # print(self.price.text)

    def update(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        item = self.ids.stock_name.text
        code = int(self.stock_code.text)
        iprice = int(self.stock_price.text)
        qty = int(self.stock_qty.text)
        disc = int(self.stock_disc.text)
        vat = int(self.stock_vat.text)
        fprice = 0
        try:
            if vat == '0':
                fprice = iprice - disc
            else:
                bprice = (iprice * (vat / 100))
                fprice = bprice + iprice - disc

            save_sql = "UPDATE Stock SET  ITEM=?, CODE=?,QUANTITY =? ,INITAL_PRICE=?,FINAL_PRICE = ?,DISCOUNT =?, VAT=? WHERE ITEM = ?"
            cursor.execute(save_sql, (item, code, qty, iprice, fprice, disc, vat, item))
            connection.commit()
            self.refresh()
            self.successful_popup()
        except sqlite3.IntegrityError as e:
            print("Error: ", e)
            return self.unsuccessful_popup()

    def refresh(self):
        self.controller.refresh_from_data()

    def validate_edit(self, *args):

        if self.stock_name.text and self.stock_code.text and self.stock_price.text and self.stock_qty.text and self.stock_disc.text and self.stock_vat.text:
            return self.update()
        else:
            return self.validnot()

    def validnot(self):

        self.content = Label(text='All fields must be \n   filled Correclty')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()

    def successful_popup(self):

        self.content = Label(text='Eddit Succesful.')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()

    def unsuccessful_popup(self):

        self.content = Label(text=' Unsuccesful, please try Again!')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()


class AddStock(Screen):
    stock_name = ObjectProperty(None)
    stock_code = ObjectProperty(None)
    stock_price = ObjectProperty(None)
    stock_qty = ObjectProperty(None)
    stock_disc = ObjectProperty(None)
    stock_vat = ObjectProperty(None)
    fprice = NumericProperty(None)
    cprice = NumericProperty(None)

    def go_back(self):
        n = self.manager.current = 'screen2'
        return n

    def __init__(self, **kwargs):
        super(AddStock, self).__init__(**kwargs)
        self.create_table()

    def gen_patient_id(self):
        gen = random.randint(500, 50000)

        self.stock_code.text = str(gen)

    def create_table(self):
        con.execute(
            "CREATE TABLE IF NOT EXISTS Stock (ITEM TEXT,CODE VARCHAR, INITAL_PRICE INT, QUANTITY INT,VAT INT,DISCOUNT INT, FINAL_PRICE INT )")
        conn.commit()

    def insert_stock(self, **kwargs):
        item = self.ids.stock_name.text
        code = int(self.stock_code.text)
        iprice = int(self.stock_price.text)
        qty = int(self.stock_qty.text)
        disc = int(self.stock_disc.text)
        vat = int(self.stock_vat.text)
        fprice = 0
        try:
            if vat == '0':
                fprice = iprice - disc
            else:
                bprice = (iprice * (vat / 100))
                fprice = bprice + iprice - disc

            con.execute(
                "INSERT INTO Stock (ITEM,CODE , INITAL_PRICE , QUANTITY ,VAT,DISCOUNT, FINAL_PRICE  ) VALUES(?,?,?,?,?,?,?)",
                (item, code, iprice, qty, vat, disc, fprice,))
            conn.commit()
            self.successful_popup()

            self.ids.stock_name.text = ""
            self.stock_code.text = ""
            self.stock_price.text = ""
            self.stock_qty.text = ""
            self.stock_disc.text = ""
            self.stock_vat.text = ""
        except:
            return self.unsuccessful_popup()

    def validate_signup(self, *args):

        if self.stock_name.text and self.stock_code.text and self.stock_price.text and self.stock_qty.text and self.stock_disc.text and self.stock_vat.text:
            return self.insert_stock()
        else:
            return self.validnot()

    def validnot(self):

        self.content = Label(text='All fields must be \n   filled Correclty')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()

    def successful_popup(self):

        self.content = Label(text='Stock Added Succesfully')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()

    def unsuccessful_popup(self):

        self.content = Label(text=' Unsuccesfully, please try Again!')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()


class ZbarScanner(Screen):
    pass


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class SelectableButton1(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton1, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton1, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class RV(Screen):
    ''' Creates Db conn, table, and saves data, retrives stored data and
    displays in the RecycleView .'''
    data_items = ListProperty([("?", "?", "?")])

    total_id = ObjectProperty(None)
    item = ObjectProperty(None)
    qty = ObjectProperty(None)
    price = ObjectProperty(None)
    total_col_headings = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(RV, self).__init__(*args, **kwargs)
        self.create_table()
        self.get_table_column_headings()
        self.get_users()

    def on_press(self, instance):

        self.setup_row_data(self.data_items[instance.index]['Index'])

    def setup_row_data(self, value):
        conn = sqlite3.connect("demo.db")
        con = conn.cursor()

        con.execute("SELECT itemName, itemQty,itemPrice FROM Users WHERE ItemName=?", (value,))
        self.row_data = con.fetchone()

        self.ids.item.text = str(self.row_data[0])
        self.qty.text = str(self.row_data[1])
        self.price.text = str(self.row_data[2])

        # print(self.item.text)
        # print(self.qty.text)
        # print(self.price.text)

    def get_table_column_headings(self):
        connection = sqlite3.connect("demo.db")

        with connection:
            # With the with keyword, the Python interpreter automatically releases the resources.
            # It also provides error handling
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(Users)")
            col_headings = cursor.fetchall()
            self.total_col_headings = len(col_headings)

    def create_table(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Users(
        itemName text PRIMAY KEY,
        itemQty integer NOT NULL,itemPrice integer NOT NULL,itemTotal integer NOT NULL )"""
        cursor.execute(sql)
        connection.close()

    def get_users(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Users ")
        rows = cursor.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

    def clear(self):
        self.item.text = ""
        self.qty.text = ""
        self.price.text = ""

    def clear_also(self):

        self.ids.cash_id.text = "0.00"
        self.ids.total_id.text = "0.00"

    def clear_list(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        try:
            save_sql = "DELETE FROM Users "
            cursor.execute(save_sql)
            connection.commit()

        except sqlite3.IntegrityError as e:
            print("Error: ", e)

    def save(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        item = self.item.text
        Qty = int(self.qty.text)
        price = int(self.price.text)
        total = Qty * price

        try:
            save_sql = "INSERT INTO Users (itemName, itemQty, itemPrice,itemTotal) VALUES (?,?,?,?)"
            cursor.execute(save_sql, (item, Qty, price, total))
            connection.commit()

        except sqlite3.IntegrityError as e:
            print("Error: ", e)

    def update(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        item = self.item.text
        Qty = int(self.qty.text)
        price = int(self.price.text)
        total = Qty * price

        try:
            save_sql = "UPDATE Users SET  itemQty=?, itemPrice=?, itemTotal=? WHERE itemName = ?"
            cursor.execute(save_sql, (Qty, price, total, item))
            connection.commit()
            self.get_users()
            self.clear()
            self.ids.controller.refresh_from_data()
        except sqlite3.IntegrityError as e:
            print("Error: ", e)

    def refresh(self):
        self.ids.controller.refresh_from_data()
        print('refreshed')

    def delete_item(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        item = self.item.text

        try:
            save_sql = "DELETE FROM Users WHERE itemName = ?"
            cursor.execute(save_sql, (item,))
            connection.commit()
            self.get_users()
            self.ids.controller.refresh_from_data()
            self.clear()
            self.total()
        except sqlite3.IntegrityError as e:
            print("Error: ", e)

    def valid_add(self):
        if int(self.qty.text) and int(self.price.text) > 0:
            self.save()
            self.total()
        else:
            self.pop()

    def pop(self):

        self.content = Label(text='Quantity or Price should be \n  greator than zero ')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.8, .3))
        self.popup.open()

    def valid_update(self):
        if int(self.qty.text) and int(self.price.text) > 0:
            self.update()
            self.total()
        else:
            self.pop()

    def pop(self):

        self.content = Label(text='Quantity or Price should \n  be greator than zero ')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.8, .3))
        self.popup.open()

    def total(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()
        self.total_price = 0
        try:
            save_sql = "SELECT SUM(itemTotal) FROM Users"
            cursor.execute(save_sql)
            self.total_price = cursor.fetchone()[0]
            self.ids.total_id.text = str(self.total_price)

        except sqlite3.IntegrityError as e:
            print("Error: ", e)

    def gen_amount(self):

        total = float(self.total_id.text)
        # print(total)
        self.popup = ChangePopup(total)
        self.popup.open()

    def print_reciept(self):
        connection = sqlite3.connect("demo.db")
        cursor = connection.cursor()

        item = []
        qty = []
        price = []
        total = []
        start = 0
        max_col = 3
        try:
            save_sql = "SELECT ItemName FROM Users"
            cursor.execute(save_sql)
            row = cursor.fetchall()

            try:
                for col in row:
                    item.append(col[0])

            except sqlite3.IntegrityError as e:
                print("Error: ", e)

            save_sql = "SELECT ItemQty FROM Users"
            cursor.execute(save_sql)
            row = cursor.fetchall()

            try:
                for col in row:
                    qty.append(col[0])

            except sqlite3.IntegrityError as e:
                print("Error: ", e)

            save_sql = "SELECT ItemPrice FROM Users"
            cursor.execute(save_sql)
            row = cursor.fetchall()

            try:
                for col in row:
                    price.append(col[0])

            except sqlite3.IntegrityError as e:
                print("Error: ", e)

            save_sql = "SELECT ItemTotal FROM Users"
            cursor.execute(save_sql)
            row = cursor.fetchall()

            try:
                for col in row:
                    total.append(col[0])

            except sqlite3.IntegrityError as e:
                print("Error: ", e)


        except sqlite3.IntegrityError as e:
            print("Error: ", e)

        total_price = self.ids.total_id.text
        change = self.ids.change_id.text

        myFile = open("Receipt.txt", "wt")
        myFile.write("\t\t Joy Enterprise\n")
        myFile.write("----------------------------------------------\n")
        myFile.write("Item\t\tQuantity\t\tPrice\n")
        myFile.write("----------------------------------------------\n")

        for i in range(0, len(item)):
            myFile.write(str(i + 1) + ". " + str(item[i]) + "\t\t")
            myFile.write(str(qty[i]) + "\t\t")
            myFile.write(str(total[i]) + "\t\t\n")
        myFile.write("------------------------------------------------\n")
        myFile.write("\t\t\t\t TOTAL:\t" + str(total_price) + "\n")
        myFile.write("\t\t\t\t CHANGE: " + str(change) + "\n")
        myFile.write("------------------------------------------------\n")
        myFile.write("\t Thanks for shoppingwith us!! \n \t  Welcome Back Again!!")
        myFile.close()

        os.startfile("C:\\Users\\V-TECH\\Desktop\\PYTHON TUTS\\dbrc\\Receipt.txt", "print")

    def validate_entry(self):

        if self.item.text and self.qty.text and self.price.text:
            return self.valid_add()
        else:
            return self.valid_not_add()

    def valid_not_add(self):

        self.content = Label(text='Entry cannot be empty')
        self.popup = Popup(title='warning', content=self.content,
                           size_hint=(.7, .2))
        self.popup.open()

    def validate_update_entry(self):

        if self.item.text and self.qty.text and self.price.text:
            return self.valid_update()
        else:
            return self.valid_not_add()

    def valid_not_update(self):

        self.content = Label(text='Entry cannot be empty')
        self.popup = Popup(title='', content=self.content, seperator_height=0,
                           size_hint=(.7, .2))
        self.popup.open()


class ChangePopup(Popup):
    cash_id: ObjectProperty(None)
    change_id: ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(ChangePopup, self).__init__(**kwargs)
        self.obj = obj

    def cash_amount(self):
        cash = float(self.ids.cash_id.text)
        change = cash - self.obj

        try:
            self.ids.change_id.text = str(change)
            print(self.obj)
        except:
            print('Error')


class ScreenOne(Screen):
    conn = sqlite3.connect("demo.db")
    con = conn.cursor()

    password = ObjectProperty()
    username = ObjectProperty()

    def user_input(self):
        if self.username.text and self.password.text:
            return self.validate_login()

        else:
            return self.input_empty()

    def input_empty(self):

        self.content = Label(text='username or password cannot be empty')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()
        a = self.manager.current = 'Screen_login'

    def validate_login(self, **kwargs):
        con.execute("SELECT * FROM Access WHERE Name = ? AND Password = ?", (self.username.text, self.password.text))
        data = con.fetchall()
        a = self.manager.current = 'screen2'
        if data:
            return a
        else:
            return self.relogin_popup()

    def relogin_popup(self):
        self.content = Label(text='Invalid username or password')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()
        a = self.manager.current = 'Screen_login'


    def show_password(self, field, button):
        """
        Called when you press the right button in the password field
        for the screen TextFields.

        instance_field: kivy.uix.textinput.TextInput;
        instance_button: kivymd.button.MDIconButton;

        """

        # Show or hide text of password, set focus field
        # and set icon of right button.
        field.password = not field.password
        field.focus = True
        button.icon = 'eye' if button.icon == 'eye-off' else 'eye-off'

class Signup(Screen):
    password = ObjectProperty()
    username = ObjectProperty()

    def create_table():
        con.execute("CREATE TABLE IF NOT EXISTS Access (Name TEXT, Password VARCHAR)")
        conn.commit()

    create_table()

    def insert_user(self, **kwargs):

        con.execute("INSERT INTO Access  VALUES(?,?)", (self.username.text, self.password.text))
        conn.commit()

    def validate_signup(self):

        n = self.manager.current = 'Screen_login'
        if self.username.text and self.password.text:
            return n and self.insert_user()
        else:
            return self.validnot()

    def validnot(self):

        self.content = Label(text='username and password \n  cannot be empty')
        self.popup = Popup(title='', content=self.content, separator_height=0,
                           size_hint=(.8, .2))
        self.popup.open()
        n = self.manager.current = 'screen_signup'

    def show_password(self, field, button):
        """
        Called when you press the right button in the password field
        for the screen TextFields.

        instance_field: kivy.uix.textinput.TextInput;
        instance_button: kivymd.button.MDIconButton;

        """

        # Show or hide text of password, set focus field
        # and set icon of right button.
        field.password = not field.password
        field.focus = True
        button.icon = 'eye' if button.icon == 'eye-off' else 'eye-off'


class TestApp(App):
    theme_cls = ThemeManager()
    title = "Point Of Sale"



    def build(self):
        main_widget = Builder.load_file("test1.kv")
        # self.theme_cls.theme_style = 'Dark'


        return main_widget




if __name__ == '__main__':
    TestApp().run()

