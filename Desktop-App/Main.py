import os
from PyQt5 import QtWidgets
import sys
sys.path.append('./Backend')
sys.path.append('./Components')
sys.path.append('./Backend/Core')
sys.path.append('./Backend/Core/Models')
sys.path.append('./Backend/Core/PrepareEmbeddings')
sys.path.append('Backend/Core/Dependencies')
from Window import Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec_())