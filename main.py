import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial

import dmg_ccl

def init(ui):
    ui.lineEdit_CharName.setText('')
    ui.doubleSpinBox_ATK.setValue(0.0)
    ui.doubleSpinBox_DEF.setValue(0.0)
    ui.doubleSpinBox_HP.setValue(0.0)
    ui.doubleSpinBox_CritRate.setValue(0.0)
    ui.doubleSpinBox_CritDmg.setValue(0.0)
    ui.doubleSpinBox_AllBonus.setValue(0.0)
    print('Init successfully')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = dmg_ccl.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()

    ui.pushButton_Init.clicked.connect(partial(init,ui))
    
    sys.exit(app.exec_())