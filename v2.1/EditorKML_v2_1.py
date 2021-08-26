from PyQt5.QtWidgets import *

from FinPpal import *

#-----------------------------------------------------------------       
def main():
    app=QApplication([])
    finestra=FinPpal()
    finestra.show()
    app.exec_()
#-----------------------------------------------------------------       
if __name__=="__main__":
    main()
