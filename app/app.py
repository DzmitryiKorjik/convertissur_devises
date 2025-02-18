from PySide6 import QtWidgets
import currency_converter

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.converter = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertir devise")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
        self.setup_css()
        self.resize(600, 10)

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_convertir = QtWidgets.QPushButton("Inverser devises")

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_convertir)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.converter.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.converter.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("USD")

        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1, 1000000)

        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_convertir.clicked.connect(self.inverser_devises)

    def setup_css(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E2E;
                color: #E0E0E0;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QComboBox, QSpinBox {
                background-color: #2A2A3A;
                border: 2px solid #4A90E2;
                padding: 6px;
                color: #E0E0E0;
                border-radius: 8px;
            }
            QSpinBox::up-button {
                width: 10px;
                height: 10px;
                border: none;
                background-color: green;
                border-radius: 2px;
                margin: 2px;
            }
            QSpinBox::down-button {
                width: 10px;
                height: 10px;
                border: none;
                background-color: red;
                border-radius: 2px;
                margin: 2px;   

            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #357ABD;
            }
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
                background-color: #2A5A8A;
            }
            QPushButton {
                background-color: #4A90E2;
                border: none;
                padding: 10px;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 8px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2A5A8A;
            }
        """)
    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try:
            resultat = self.converter.convert(montant, devise_from, devise_to)
            self.spn_montantConverti.setValue(int(resultat))  # Convertir en int, car QSpinBox n'accepte que les int
        except currency_converter.currency_converter.RateNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le taux de change pour {devise_from} → {devise_to} n'est pas disponible.")


    def inverser_devises(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        self.compute()

app = QtWidgets.QApplication([])

# Création de la fenêtre principale et l'affichage
win = App()
win.show()

app.exec()