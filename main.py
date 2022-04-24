import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial

import dmg_ccl
from character import CHAR

def init(ui,char):
    """
    initalize the app
    """
    # char = None
    ui.lineEdit_CharName.setText('')
    ui.doubleSpinBox_ATK.setValue(1600.0)
    ui.doubleSpinBox_DEF.setValue(800.0)
    ui.doubleSpinBox_HP.setValue(15000.0)
    ui.doubleSpinBox_CritRate.setValue(50.0)
    ui.doubleSpinBox_CritDmg.setValue(100.0)
    ui.doubleSpinBox_AllBonus.setValue(46.6)
    ui.textEdit_BonusDisp.setText('')
    ui.textEdit_DmgDisp.setText('')
    ui.label_State.setText('Init successfully')


def load_char(ui,char):
    """
    load the character's name
    """
    char_name = ui.lineEdit_CharName.text()
    char.setCharName(char_name)
    char.getSkillList()
    ui.label_State.setText('loading done')


def cpt_damage(ui, char):
    """
    compute and show the damage of the skill
    """
    d_skill = ['A','E','Q']
    skill_index =  ui.comboBox_DmgType.currentIndex()
    skill_level = ui.spinBox_SkillLevel.value()
    s = char.display(char.computeDamage(d_skill[skill_index], skill_level, 'E'))
    ui.textEdit_DmgDisp.setText(s)
    ui.label_State.setText('calculation done')


def load_attr(ui, char):
    """
    load the attributes of character
    """
    char.setAttributes(
        atk = ui.doubleSpinBox_ATK.value(),
        DEF = ui.doubleSpinBox_DEF.value(),
        HP = ui.doubleSpinBox_HP.value(),
        crit_rate = ui.doubleSpinBox_CritRate.value(),
        crit_dmg = ui.doubleSpinBox_CritDmg.value(),
        all_dmg = ui.doubleSpinBox_AllBonus.value()
    )
    ui.label_State.setText('Attributes loading done')


def add_bonus(ui,char):
    """
    add a bonus to the bonus list
    """
    d_skill = ['A','E','Q']
    bonus_type = ui.comboBox_BonusType.currentIndex()
    bonus_value = ui.doubleSpinBox_Bonus.value()
    char.addBonus(d_skill[bonus_type],bonus_value)
    s = char.b_display()
    ui.textEdit_BonusDisp.setText(s)
    ui.label_State.setText('Bonus adding done')

def clear_bonus(ui,char):
    """
    clear the bonus list
    """

    l = ['A', 'E', 'Q']
    for i in l:
        char.bonus_list[i] = 0.0
    ui.textEdit_BonusDisp.setText(char.b_display())
    ui.label_State.setText('clear done')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = dmg_ccl.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    char = CHAR()

    ui.pushButton_Init.clicked.connect(partial(init,ui,char))
    ui.pushButton_Char.clicked.connect(partial(load_char,ui,char))
    ui.pushButton_CptDmg.clicked.connect(partial(cpt_damage,ui, char))
    ui.pushButton_Attr.clicked.connect(partial(load_attr,ui,char))
    ui.pushButton_AddBonus.clicked.connect(partial(add_bonus,ui,char))
    ui.pushButton_ClearBonus.clicked.connect(partial(clear_bonus,ui,char))

    sys.exit(app.exec_())