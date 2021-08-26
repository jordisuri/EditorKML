
from EditorKML_v2_1 import *

#-----------------------------------------------------------------
class FinAjuda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajuda")
        self.resize(600,600)
        cw=QTextEdit(self)
        cw.setReadOnly(True)
        text=self.CarregarFitxer()
        cw.setHtml(text)
        #cw.setPlainText(text)
        self.setCentralWidget(cw)
    #-------------------------------------------------------------
    def CarregarFitxer(self):
        fa=open("Ajuda.html","r")
        r=""
        linia=fa.readline()
        while linia!="":
            r+=linia+'\n'
            linia=fa.readline()
        fa.close()
        return r
    #-------------------------------------------------------------
    def closeEvent(self,ce):
        self.deleteLater()
        
#-----------------------------------------------------------------
#-----------------------------------------------------------------
if __name__=="__main__":
    main()
#-----------------------------------------------------------------
