from PyQt5.QtWidgets import QApplication,QLabel,QLineEdit, QMainWindow,QPushButton, QGridLayout, QWidget, QTableWidget,QDateEdit, QTableWidgetItem,QTimeEdit
from PyQt5.QtCore import QSize, Qt
import sys 
import pyodbc 
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self): 
        self.setMinimumSize(QSize(800, 600))             # Устанавливаем размеры
        self.setWindowTitle("Журнал автобазы")    # Устанавливаем заголовок окна
        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.createtable()
        self.createedits()
        self.createtitles()
        
        self.btn_insert_jurnal = QPushButton("ввести запись")
        self.btn_insert_jurnal.clicked.connect(self.insert_data)
        
        self.grid_layout.addWidget(self.btn_insert_jurnal, 3, 0,4,7)
        
        central_widget.setLayout(self.grid_layout)
        
        self.show()

            
    def getFromEdit(self):
        l=[]
        for items in self.edit_list:
            l.append(items.text())
        return l

    
    def insert_data(self):
        
        l = self.getFromEdit()
        for i in range(0,3):
            self.edit_list[i].clear()
        if  '' in l:
            pass
        else:
            cursor.execute("""
                            insert into transport(id_route,id_type) 
                            select id_route,id_type
                            from route, type_transport
                            where route.No_route=%(route)s and type_transport.type_t= '%(tr)s';

                            insert into jurnal (id_transport,id_driver,time_arrival,time_departure,date_of_work) values ( 
                            (select id_transport from transport
                            where
                               id_route =(select id_route from route where No_route = %(route)s)
                            and
                               id_type = (select id_type from type_transport where type_t = '%(tr)s') ),
                            (select id_driver from driver where FIO = '%(fio)s' ),
                            '%(t_a)s','%(t_d)s','%(date)s');

                            """ % {"route":l[0], "tr": l[1],"fio":l[2],"t_a":l[3],"t_d":l[4],"date":l[5]})
            con.commit()
            
        

        
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

            
    def createedits(self):
        
        self.route_edit =         QLineEdit()
        self.transport_edit =     QLineEdit()
        self.driver_edit =        QLineEdit()
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
        self.table.setRowCount(10)        
 
        self.table.setHorizontalHeaderLabels(["маршрут №", "транспорт", "водитель","время отправления", "время прибытия", "дата"])
        cursor.execute("""
                       select r.No_route, tt.type_t,  d.FIO, j.time_arrival, j.time_departure, j.date_of_work
                       from jurnal as j
                       Join transport as t on j.id_transport=t.id_transport
                       join type_transport as tt on t.id_type=tt.id_type
                       join route as r on t.id_route= r.id_route
                       join driver as d on j.id_driver=d.id_driver
                       order by j.date_of_work DESC;
                       """)
        rows = cursor.fetchall()
        
        no_row = 0
        for row in rows:
            no_col=0
            for item in row:
                if no_col >= len(row):
                    break
                self.table.setItem(no_row,no_col, QTableWidgetItem(str(row[no_col])))
                no_col+=1
            no_row+=1
        self.table.resizeColumnsToContents()
        self.grid_layout.addWidget(self.table, 0, 0,1,7)

        
if __name__ == "__main__":
    con = pyodbc.connect('DRIVER={SQL Server};SERVER=LEO-PC;DATABASE=autobase;UID=JIeBuk;PWD=12199529')
    cursor=con.cursor() 
    app = QApplication(sys.argv)
    mw = MainWindow()
    
    sys.exit(app.exec())
