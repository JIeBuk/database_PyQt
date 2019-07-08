from PyQt5.QtWidgets import QApplication,QLabel,QLineEdit, QMainWindow,QPushButton, QGridLayout, QWidget, QTableWidget,QDateEdit, QTableWidgetItem,QTimeEdit,QComboBox,QMessageBox
from PyQt5.QtCore import QSize, Qt
from datetime import datetime

import sys 
import pyodbc
        
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        super().__init__()
        self.initUI()
        


    def initUI(self):
        self.driver_window=None
        self.route_window=None
        self.type_transport_window=None
        self.form_window = None
        self.setMinimumSize(QSize(600, 600))             # Устанавливаем размеры
        self.setWindowTitle("Журнал автобазы")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        
        self.createtable()
        self.createedits()
        self.createtitles()

        self.btn_form = QPushButton("form")
        self.btn_form.clicked.connect(self.open_window_form)
        
        self.btn = QPushButton("driver list")
        self.btn.clicked.connect(self.open_window_driver)

        self.btn2 = QPushButton("route_list")
        self.btn2.clicked.connect(self.open_window_route)

        
        self.btn3 = QPushButton("transport_list")
        self.btn3.clicked.connect(self.open_window_type)

        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close_app)

        self.grid_layout.addWidget(self.btn_form,4,3)
        self.grid_layout.addWidget(self.btn_close,4,5)
        self.grid_layout.addWidget(self.btn3,4, 1)
        self.grid_layout.addWidget(self.btn,4, 2)
        self.grid_layout.addWidget(self.btn2,4, 0)
        
        self.btn_insert_jurnal = QPushButton("ввести запись")
        self.btn_insert_jurnal.clicked.connect(self.insert_data)
        
        self.grid_layout.addWidget(self.btn_insert_jurnal,3, 0 ,1 ,  6)
        
        central_widget.setLayout(self.grid_layout)

    def close_app(self):
        self.hide()
        

    def open_window_form(self):
        if self.form_window == None:
            self.form_window = FormWindow()
        self.form_window.show()
        
    def open_window_type(self):
        if self.type_transport_window == None:
            self.type_transport_window = TypeTransportWindow()
        self.type_transport_window.show()
        
        
    def open_window_route(self):
        if self.route_window == None:
            self.route_window = RouteWindow()
        self.route_window.show()
        
    def open_window_driver(self):
        if self.driver_window == None:
            self.driver_window = DriverWindow()
        self.driver_window.show()
        

            
    def getFromEdit(self):
        
        l=[]
        for items in self.edit_list:
            if type(items) == QComboBox:
                l.append(items.currentText())
            else:
                l.append(items.text())
        return l

    
    def insert_data(self):
        
        l = self.getFromEdit()
        
        
        Q = QMessageBox.information(self, 'Ок', 'Запись введена!', QMessageBox.Ok)        
        
        
        
        if  '' in l:
            pass
        else:
            cursor.execute("""
                            EXEC [insert_transport] %(route)s,'%(tr)s';
                            EXEC insert_jurnal %(route)s,'%(tr)s','%(fio)s', '%(t_a)s','%(t_d)s','%(date)s';
                            
                            

                            """ % {"route":l[0], "tr":l[1], "fio":l[2], "t_a":l[3], "t_d":l[4], "date":l[5]})
            con.commit()
        self.createtable()
            
        

        
    def createtitles(self):

        self.title1 =QLabel("маршрут")
        self.title2 =QLabel("транспорт")
        
        self.title4 =QLabel("водитель")
        self.title5 =QLabel("время отправления")
        self.title6 =QLabel("время  прибытия")
        self.title7 =QLabel("дата")
        self.title_list=(self.title1,self.title2,self.title4,self.title5,self.title6,self.title7)
        i=0
        for item in self.title_list:
            self.grid_layout.addWidget(item, 1, i)
            i+=1

    def selects_for_combobox(self,data,string):
        cursor.execute(string)
        rows = cursor.fetchall()
        print(rows)
        data.addItems([str(row[0]) for row in rows])
        
    def createedits(self):
        str_select_fio ="""
                       select FIO
                       from driver;
                       """
        str_select_route ="""
                       select no_route
                       from route;
                       """
        str_select_type ="""
                       select type_t
                       from type_transport;
                       """
        self.driver_edit = QComboBox()
        self.route_edit = QComboBox()
        self.transport_edit = QComboBox()
        
        self.selects_for_combobox(self.driver_edit,str_select_fio)
        self.selects_for_combobox(self.route_edit,str_select_route)
        self.selects_for_combobox(self.transport_edit,str_select_type)
        
        
        self.arivaltime_edit =    QTimeEdit()
        self.departuretime_edit = QTimeEdit()
        self.date_edit =          QDateEdit()
        
        self.edit_list = (self.route_edit,self.transport_edit,self.driver_edit,self.arivaltime_edit,self.departuretime_edit,self.date_edit)
        i = 0
        for item in self.edit_list:
            self.grid_layout.addWidget(self.edit_list[i], 2, i)
            i+=1
        
        

        
    def createtable(self):
        self.table = QTableWidget(self)  
        self.table.setColumnCount(6)     
        self.table.setRowCount(50)        
 
        self.table.setHorizontalHeaderLabels(["маршрут №", "транспорт", "водитель","время отправления", "время прибытия", "дата"])
        cursor.execute("""
                       
                        select * from jurnal_restyle
                       order by date_of_work DESC;
                       """)
        rows = cursor.fetchall()
        print(rows)
        print(type(rows))
        print(type(rows[2]),'qwerty')
        no_row = 0
        for row in rows:
            no_col=0
            for item in row:
                #if no_col >= len(row):
                   # break
                self.table.setItem(no_row,no_col, QTableWidgetItem(str(row[no_col])))
                no_col+=1
            no_row+=1
        self.table.resizeColumnsToContents()
        self.grid_layout.addWidget(self.table, 0, 0,1,6)

    

class DriverWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        

    def initUI(self): 
        self.setMinimumSize(QSize(280, 300))             # Устанавливаем размеры
        self.setWindowTitle("Список водителей")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        
        self.createtable()

        self.title1 =QLabel("Фамилия")
        self.title2 =QLabel("Имя")
        self.title3 =QLabel("Отчество")
        self.title4 =QLabel("возраст")
        
        self.grid_layout.addWidget(self.title1, 1, 0,1,1)
        self.grid_layout.addWidget(self.title2, 2, 0,1,1)
        self.grid_layout.addWidget(self.title3, 3, 0,1,1)
        self.grid_layout.addWidget(self.title4, 4, 0,1,1)
        self.edits=[]
        self.edit1 =QLineEdit()
        self.edit2 =QLineEdit()
        self.edit3 =QLineEdit()
        self.edit4 =QLineEdit()
        self.edits= [self.edit1,self.edit2,self.edit3,self.edit4]
        self.grid_layout.addWidget(self.edit1, 1, 1,1,2)
        self.grid_layout.addWidget(self.edit2, 2, 1,1,2)
        self.grid_layout.addWidget(self.edit3, 3, 1,1,2)
        self.grid_layout.addWidget(self.edit4, 4, 1,1,2)
        
        self.btn_close = QPushButton("close")
        self.btn_close.clicked.connect(self.close_app)
         
        self.btn_insert = QPushButton("ввести запись")
        self.btn_insert.clicked.connect(self.insert)

        self.grid_layout.addWidget(self.btn_insert,5, 0,1,3)
        self.grid_layout.addWidget(self.btn_close,6, 1)
        
        central_widget.setLayout(self.grid_layout)
    
    def getFromEdit(self):
        l=[]
        edstr=[self.edit1.text(),self.edit2.text(),self.edit3.text()]
        if '' in edstr:
            Q = QMessageBox.information(self, 'Ок', 'введите ФИО!', QMessageBox.Ok)
            return
        else:
            l.append(" ".join(edstr))
        try:
            l.append(int(self.edit4.text()))
        except:
            Q = QMessageBox.information(self, 'Ок', 'неверный возвраст', QMessageBox.Ok)
            return
            
        return l

    def insert(self):
        
        
        l = self.getFromEdit()
        
        if l == None :
            pass
        else:
            if l in self.drivers:
                Q = QMessageBox.information(self, 'Ок', 'запись уже существует', QMessageBox.Ok)
                
            else:
                print('qwerty')
                for i in self.edits:
                    i.clear()
                cursor.execute("""
                            
                            
                            insert into driver (FIO,age) values ( 
                            '%(fio)s',%(age)s );

                            """ % { "fio":l[0], "age":l[1]})
                con.commit()
                self.createtable()
                Q = QMessageBox.information(self, 'Ок', 'Запись введена!', QMessageBox.Ok)


    def createtable(self):
        self.driver_table = QTableWidget()  
        self.driver_table.setColumnCount(2)     
        self.driver_table.setRowCount(20)
        
        self.driver_table.setHorizontalHeaderLabels(["driver", "age"])
        cursor.execute("""
                       select d.FIO, d.age
                       from driver as d
                       order by FIO;
                       
                       """)
        self.drivers = cursor.fetchall()
        self.drivers = list((list(i) for i in self.drivers))
        print(self.drivers)
        
        no_row = 0
        for row in self.drivers:
            no_col=0
            for item in row:
                if no_col >= len(row):
                    break
                self.driver_table.setItem(no_row,no_col, QTableWidgetItem(str(row[no_col])))
                no_col+=1
            no_row+=1
        
        self.driver_table.resizeColumnsToContents()
        
        self.grid_layout.addWidget(self.driver_table, 0, 0,1,3)
        

        
    def close_app(self):
        self.hide()
        
        mw.createedits()

        
class RouteWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        

    def initUI(self): 
        self.setMinimumSize(QSize(280, 300))             # Устанавливаем размеры
        #self.setWidth(300)
        #self.setHeight(280)
        self.setWindowTitle("Список маршрутов")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        
        self.createtable()

        self.title1 =QLabel("маршрут:")
        
        
        self.grid_layout.addWidget(self.title1, 0, 1,1,1)
        
        self.edit1 =QLineEdit()
        
        self.grid_layout.addWidget(self.edit1, 1, 1,1,1)
                
        self.btn_close = QPushButton("close")
        self.btn_close.clicked.connect(self.close_app)
         
        self.btn_insert = QPushButton("ввести запись")
        self.btn_insert.clicked.connect(self.insert)

        self.grid_layout.addWidget(self.btn_insert,2, 1,1,1)
        self.grid_layout.addWidget(self.btn_close,5, 1)
        
        central_widget.setLayout(self.grid_layout)
    
    

    def insert(self):
        try:
                data = int(self.edit1.text())
        
                
                if data in ( row[0] for row in self.routes):
                    Q = QMessageBox.information(self, 'Ок', 'запись уже существует', QMessageBox.Ok)
                    
                else:
                    print(data)
                    self.edit1.clear()
                    cursor.execute("""
                                insert into route (No_route) values ( 
                                '%(No)s' );

                                """ % { "No":data})
                    con.commit()
                    self.createtable()
                    Q = QMessageBox.information(self, 'Ок', 'Запись введена!', QMessageBox.Ok)
        except:
            Q = QMessageBox.information(self, 'Ок', 'неправильно введенные данные!', QMessageBox.Ok)

                               


    def createtable(self):
                        
        
        self.route_table = QTableWidget()  
        self.route_table.setColumnCount(1)     
        self.route_table.setRowCount(20)
        
        self.route_table.setHorizontalHeaderLabels(["route"])
        cursor.execute("""
                       select No_route
                       from route
                       order by No_route;
                       
                       """)
        self.routes = cursor.fetchall()
        print(self.routes,'qwe')
        #self.routes = list((list(i) for i in self.routes))
        print(self.routes,'wewe')
        
        no_row = 0
        for row in self.routes:
            
            self.route_table.setItem(no_row,0, QTableWidgetItem(str(row[0])))
            no_row+=1
        
#        self.route_table.resizeColumnsToContents()
        
        self.grid_layout.addWidget(self.route_table, 0, 0,6,1)
        
        
        
    def close_app(self):
        self.hide()
        mw.createedits()


class TypeTransportWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        

    def initUI(self): 
        self.setMinimumSize(QSize(280, 300))             # Устанавливаем размеры
        #self.setWidth(300)
        #self.setHeight(280)
        self.setWindowTitle("Список транспорта")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        
        self.createtable()

        self.title1 =QLabel("тип транспорта:")
        
        
        self.grid_layout.addWidget(self.title1, 0, 1,2,1)
        
        self.edit1 =QLineEdit()
        
        self.grid_layout.addWidget(self.edit1, 1, 1,1,1)
                
        self.btn_close = QPushButton("close")
        self.btn_close.clicked.connect(self.close_app)
         
        self.btn_insert = QPushButton("ввести запись")
        self.btn_insert.clicked.connect(self.insert)

        self.grid_layout.addWidget(self.btn_insert,2, 1,1,1)
        self.grid_layout.addWidget(self.btn_close,5, 1)
        
        central_widget.setLayout(self.grid_layout)
    
    

    def insert(self):
        try:
                data = str(self.edit1.text())
        
                
                if data in ( row[0] for row in self.routes):
                    Q = QMessageBox.information(self, 'Ок', 'запись уже существует', QMessageBox.Ok)
                    
                else:
                    print(data)
                    self.edit1.clear()
                    cursor.execute("""
                                insert into type_transport (type_t) values ( 
                                '%(type)s' );

                                """ % { "type":data})
                    con.commit()
                    self.createtable()
                    Q = QMessageBox.information(self, 'Ок', 'Запись введена!', QMessageBox.Ok)
        except:
            Q = QMessageBox.information(self, 'Ок', 'неправильно введенные данные!', QMessageBox.Ok)

                               


    def createtable(self):
                        
        
        self.route_table = QTableWidget()  
        self.route_table.setColumnCount(1)     
        self.route_table.setRowCount(10)
        
        self.route_table.setHorizontalHeaderLabels(["TYPE_TRANSPORT"])
        cursor.execute("""
                       select type_t
                       from type_transport
                       order by type_t;
                       
                       """)
        self.routes = cursor.fetchall()
#        self.routes = list((list(i) for i in self.routes))
        print(self.routes)
        
        no_row = 0
        for row in self.routes:
            
            self.route_table.setItem(no_row,0, QTableWidgetItem(str(row[0])))
            no_row+=1
        
        self.route_table.resizeColumnsToContents()
        
        self.grid_layout.addWidget(self.route_table, 0, 0,6,1)
        
        
        
    def close_app(self):
        self.hide()
        mw.createedits()        

class FormWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        

    def initUI(self): 
        self.setMinimumSize(QSize(500, 500))             # Устанавливаем размеры
        #self.setWidth(300)
        #self.setHeight(280)
        self.setWindowTitle("информация об итогах")    # Устанавливаем заголовок окна
        central_widget = QWidget()                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        
        self.title0 =QLabel("выберите промежуток")
        self.title1 =QLabel("c:")
        self.title2 =QLabel("по:")
        self.title01 = QLabel(" ")
        self.title02 = QLabel(" ")
        self.title03 = QLabel(" ")
        self.title04 = QLabel(" ")

        
        self.grid_layout.addWidget(self.title01, 2, 0,1,5)
        self.grid_layout.addWidget(self.title02, 3, 0,1,5)
        self.grid_layout.addWidget(self.title03, 4, 0,1,5)
        self.grid_layout.addWidget(self.title04, 5, 0,1,5)
        
        self.grid_layout.addWidget(self.title0, 0, 0,1,5)
        
        self.grid_layout.addWidget(self.title1, 1, 0,1,1)
        self.grid_layout.addWidget(self.title2, 1, 2,1,1)
        
        self.edit1 =QDateEdit()
        self.edit2 =QDateEdit()
        
        self.grid_layout.addWidget(self.edit1, 1, 1,1,1)
        self.grid_layout.addWidget(self.edit2, 1, 3,1,1)
        
        self.btn_insert = QPushButton("вывод")
        self.btn_insert.clicked.connect(self.insert)
        
        self.btn_close = QPushButton("close")
        self.btn_close.clicked.connect(self.close_app)
         
        

        self.grid_layout.addWidget(self.btn_insert,1, 4,1,1)
        self.grid_layout.addWidget(self.btn_close,6, 3)
        
        central_widget.setLayout(self.grid_layout)
    
    

    def insert(self):
        
        
        date1 = self.edit1.text()                       
        date2 = self.edit2.text()
        
        
        cursor.execute("""
                       SELECT count(*)
                        FROM jurnal
                        where date_of_work >= '%s'and date_of_work <='%s';
                       
                       """ %(date1,date2))
        a = list(cursor.fetchone())
        self.title01.setText('количество записей журнала в данном промежутке = '+ str(a[0]))
        print('1')
        cursor.execute("""
                       select dbo.get_drivers ('%s','%s');
                       
                       """ %(date1,date2))
        a = list(cursor.fetchone())
        self.title02.setText('количество водителей работавшие в данный период = '+ str(a[0]))
        print('2')
        cursor.execute("""
                       select dbo.get_no_route ('%s','%s');
                       
                       """ %(date1,date2))
        a = list(cursor.fetchone())
        self.title03.setText('количество маршрутов по которым ездили за данный период = '+ str(a[0]))
        print('3')
        cursor.execute("""
                       select dbo.get_type_transport ('%s','%s');
                       
                       """ %(date1,date2))
        a = list(cursor.fetchone())
        self.title04.setText('использованых видов транспорта за текущий период ='+ str(a[0]) )
        print('4')

        
    def close_app(self):
        self.hide()
        mw.createedits()

        
if __name__ == "__main__":
    con = pyodbc.connect('DRIVER={SQL Server};SERVER=LEO-PC;DATABASE=autobase;UID=JIeBuk;PWD=12199529')
    cursor=con.cursor() 
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
