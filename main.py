import sys
from itertools import count

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from mi import *

#initialization class : 

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("GUI.ui", self)
        self.goal_input.setVisible(False)
        self.goal_label.setVisible(False)
        self.type_chainage.currentIndexChanged.connect(self.chainage_change)
        self.run.clicked.connect(self.run_app)
        self.clear_btn.clicked.connect(self.clear_text)
        self.checkBox.stateChanged.connect(self.goal_show_input)

    def chainage_avant(self):
        rules = self.rules.toPlainText().strip().split("\n")
        facts = self.facts.toPlainText().strip().split(",")
        goals = self.goal_input.toPlainText()
        c = count(0)
        while True:
            filtered_rules = filter_avant(rules, facts)
            selected_rule = select_first_rule(filtered_rules)
            if not selected_rule:
                break
            else:
                rules_applied = execution_avant(selected_rule, facts, rules)
                self.output.append(
                    f"Cycle {next(c)}:\n\tRegles appliquer:{', '.join(rules_applied[0])}={rules_applied[1]}\n\tFaits: {', '.join(facts)}\n\tRegles non-appliquer: {' - '.join(rules)}\n")
            if not goals:
                if goals in facts:
                    self.output.append("\nLe but est realiser.")
                    break
        self.output.append(f"Faits: {str(facts)[1:-1]}\nRegles non-appliquer: {str(rules)[1:-1]}")

    def chainage_arriere(self):
        

        self.output.setText("")
        rules = self.rules.toPlainText().strip().split("\n")
        facts = self.facts.toPlainText().strip().split(",")
        goals = self.goal_input.toPlainText().strip().split(",")
        goal_past = []
        c2 = count(0)
        while goals:
            if goals[0] in goal_past:
                goals.pop(0)
                if not goals:
                    break
            if goals[0] in facts:
                goals.pop(0)
                if not goals:
                    break
            self.output.append(f"Cycle: {next(c2)}\nBut: {', '.join(goals)}")
            filtered_rules_arriere = filter_arriere(rules, goals[0])
            print(len(filtered_rules_arriere))
            if goals[0] in goal_past:
                goals.pop(0)
            self.output.append("Regle applicable:")
            for rule_applicable in filtered_rules_arriere:
                self.output.append(
                    f"Regle {rule_applicable[2] + 1}: {', '.join(rule_applicable[0])}={rule_applicable[1]}\n")
            goal_past.append(goals[0])

            if not filtered_rules_arriere:
                break
            else:
                goals = execution_arriere(select_rule_most(filtered_rules_arriere), facts, rules, goals)
        if not goals:
            self.output.append("Le but est realiser.\n")
        else:
            self.output.append("TODO: Backtrack")
        self.output.append(f"Faits: {str(facts)[1:-1]}\nRegles non-appliquer: {str(rules)[1:-1]}")

    def clear_text(self):
        self.output.setText("")
        self.rules.setText("")
        self.facts.setText("")
        self.goal_input.setText("")

    def run_app(self):
        if self.type_chainage.currentText() == "Avant":
            self.chainage_avant()
        else:
            self.chainage_arriere()

    def goal_show_input(self):
        if self.checkBox.isChecked():
            self.goal_label.setVisible(True)
            self.goal_input.setVisible(True)
        else:
            self.goal_label.setVisible(False)
            self.goal_input.setVisible(False)

    def chainage_change(self):
        if self.type_chainage.currentText() == "Arriere":
            self.goal_label.setVisible(True)
            self.goal_input.setVisible(True)
        else:
            if self.type_chainage.currentText() == "Avant":
                self.goal_label.setVisible(False)
                self.goal_input.setVisible(False)


app = QApplication(sys.argv)
root = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(root)
widget.setWindowTitle("TP IA")
widget.show()

try:
    sys.exit(app.exec_())
except:
    exit(0)
