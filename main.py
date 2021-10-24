from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6 import QtCore, QtGui

from backend import Database
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load('main-window.ui')
        self.ui.show()
        self.database=Database()
        self.data=self.database.data
        self.show_task()
        self.ui.btn_add.clicked.connect(self.add_task)
        self.done_tab()
    def done_tab(self):
        done_details_list=[]
        for i in range(len(self.data)):

            if int(self.data[i][3])==1:
                # create details buttom
                new_pushbuttom_details = QPushButton()
                new_pushbuttom_details.setText('Details')
                new_pushbuttom_details.setObjectName(f'detail_{i}')
                new_pushbuttom_details.setStyleSheet('border:1px solid #000')
                new_pushbuttom_details.setMaximumSize(100,16777215)
                done_details_list.append(new_pushbuttom_details)
                # create label to title tasks
                new_label = QLabel()
                new_label.setMaximumSize(16777215,20)
                new_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                new_label.setText(self.data[i][1])
                self.ui.gridLayout_done.addWidget(new_label,i,0)
                self.ui.gridLayout_done.addWidget(new_pushbuttom_details, i, 1)
        for i in range(len(done_details_list)):
            done_details_list[i].clicked.connect(self.details)


    def show_task(self):
        self.checkBox_list = []
        self.pushButtom_detail = []
        self.pushButtom_remove = []
        self.star_list = []

        for i in range(len(self.data)):
            #Create a check box to specify that task (done or not done)
            new_checkbox=QCheckBox()
            if self.data[i][3]==1:
                new_checkbox.setChecked(True)
            new_checkbox.setMaximumSize(20,16777215)
            new_checkbox.setObjectName(f'checkbox_{i}')
            self.checkBox_list.append(new_checkbox)
            #create label to title tasks
            new_label=QLabel()
            new_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            new_label.setText(self.data[i][1])
            # Create stars to prioritize tasks
            new_star=QPushButton()
            if self.data[i][6]==1:
                new_star.setIcon(QtGui.QPixmap('images/star-gold.png'))
            else:
                new_star.setIcon(QtGui.QPixmap('images/star.png'))
            new_star.setMaximumSize(30,30)
            new_star.setObjectName(f'star_{i}')
            new_star.setStyleSheet('border:0')
            self.star_list.append(new_star)
            new_pushbuttom_details=QPushButton()
            new_pushbuttom_details.setText('Details')
            new_pushbuttom_details.setObjectName(f'detail_{i}')
            self.pushButtom_detail.append(new_pushbuttom_details)
            new_pushbuttom_details.setStyleSheet('border:1px solid #000')
            new_pushbuttom_details.setMaximumSize(150, 400)
            # create remove buttom
            new_pushbuttom_remove=QPushButton()
            new_pushbuttom_remove.setText('remove')
            new_pushbuttom_remove.setObjectName(f'remove_{i}')
            new_pushbuttom_remove.setStyleSheet('border:1px solid #000')
            new_pushbuttom_remove.setMaximumSize(150,400)
            self.pushButtom_remove.append(new_pushbuttom_remove)
            # add to gridLayout
            self.ui.gridLayout.addWidget(new_checkbox,i,0)
            self.ui.gridLayout.addWidget(new_label,i,1)
            self.ui.gridLayout.addWidget(new_star,i,2)
            self.ui.gridLayout.addWidget(new_pushbuttom_details,i,3)
            self.ui.gridLayout.addWidget(new_pushbuttom_remove, i, 4)


        for i in range(len(self.data)):
            self.checkBox_list[i].clicked.connect(self.checked_checkeBox)
            self.pushButtom_detail[i].clicked.connect(self.details)
            self.pushButtom_remove[i].clicked.connect(self.remove)
            self.star_list[i].clicked.connect(self.star)
    def checked_checkeBox(self):
        objectName_checkeBox=self.sender().objectName()
        objectName_checkeBox=objectName_checkeBox.split('_')
        id=self.data[int(objectName_checkeBox[1])][0]
        # cleat done tab
        for i in range(len(self.data)):
            for j in range(2):
                if self.data[i][3]==1:
                    self.ui.gridLayout_done.itemAtPosition(i, j).widget().deleteLater()
        if self.checkBox_list[int(objectName_checkeBox[1])].isChecked()==True:
            done=1
        else:
            done=0
        self.database.update_data(id,done)
        for i in range(len(self.data)):
            if self.data[i][0]==int(id):
                data_list=list(self.data[i])
                data_list[3]=done

                da=tuple(data_list)
                self.data[i]=da


        self.done_tab()
    def remove(self):
        object_name=self.sender().objectName()
        object_id=object_name.split('_')
        id=int(self.data[int(object_id[1])][0])
        # clear gridlayout
        for i in range(len(self.data)):
            for j in range(5):
                self.ui.gridLayout.itemAtPosition(i,j).widget().deleteLater()
        self.data.pop(int(object_id[1]))
        self.database.remove_data(id)
        self.show_task()
    def details(self):
        object_name=self.sender().objectName()
        object_name=object_name.split('_')
        id=self.data[int(object_name[1])][0]
        data=self.data[int(object_name[1])]
        self.ui=WindowDetails(data,id)
    def add_task(self):
        title=self.ui.add_title.text()
        if title=='':
            self.ui.add_title.setStyleSheet('background-color:#d32f2f')
        else:
            self.ui.add_title.setStyleSheet('background-color:#fff')
            description=self.ui.add_description.text()
            time=self.ui.add_time.text()
            date=self.ui.add_date.text()
            self.database.add_data(title,description,time,date)
            self.data.append((len(self.data)+1,title,description,0))
            self.show_task()
    def star(self):
        objectName_star=self.sender().objectName()
        objectName_star=objectName_star.split('_')
        id=self.data[int(objectName_star[1])][0]
        if self.data[int(objectName_star[1])][6]==1:
            star=0
            self.star_list[int(objectName_star[1])].setIcon(QtGui.QPixmap('images/star.png'))
        else:
            star=1
            self.star_list[int(objectName_star[1])].setIcon(QtGui.QPixmap('images/star-gold.png'))

        self.database.update_data_star(id,star)
        for i in range(len(self.data)):
            if self.data[i][0]==int(id):
                data_list=list(self.data[i])
                data_list[6]=star

                da=tuple(data_list)
                self.data[i]=da

class WindowDetails(QWidget):
    def __init__(self,data,id):
        super().__init__()
        self.data=data
        self.id=id
        loader=QUiLoader()
        self.ui=loader.load('window_details.ui')
        self.ui.show()
        self.show_data()
        self.ui.btn_back.clicked.connect(self.back)
    def show_data(self):
        for i in range(6):
            new_label=QLabel()
            if i==3 and self.data[i]==1:
                new_label.setText('Yes')
            elif i==3 and self.data[i]==0 :
                new_label.setText('No')
            else:
                new_label.setText(f'{self.data[i]}')
            new_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.ui.gridLayout.addWidget(new_label,i,1)
    def back(self):
        self.ui=MainWindow()

app=QApplication([])
window=MainWindow()
app.exec()
