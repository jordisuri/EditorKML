from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from EditorKML_v2_1 import *

#-----------------------------------------------------------------
class ElementList(QWidget):
    
    ColorLiniaCanviat=pyqtSignal(int,QColor)
    ColorPuntsCanviat=pyqtSignal(int,QColor)
    
    VisibilitatCanviada=pyqtSignal(int,bool)
    SeleccioCanviada=pyqtSignal(int,bool)

    #-------------------------------------------------------------
    def __init__(self,nom_ruta,idruta,mare):
        super().__init__(mare)
        self.mare=mare
        self.idruta=idruta
        
        self.vis=QCheckBox('V',self)
        self.sel=QCheckBox('S',self)
        self.nr=QLineEdit(nom_ruta,self)
        self.cl=QPushButton('CL',self)
        self.cp=QPushButton('CP',self)

        self.vis.setMaximumSize(35,30)
        self.sel.setMaximumSize(35,30)
        self.nr.setMinimumSize(125,20)
        self.cl.setMaximumSize(30,30)
        self.cp.setMaximumSize(30,30)
        
        layout=QHBoxLayout(self)
        layout.addWidget(self.vis)
        layout.addWidget(self.sel)
        layout.addWidget(self.nr)
        layout.addWidget(self.cl)
        layout.addWidget(self.cp)
        self.setLayout(layout)

        self.vis.setCheckState(Qt.Checked)
        self.sel.setCheckState(Qt.Checked)

        self.cl.clicked.connect(self.CanviColorLinia)
        self.cp.clicked.connect(self.CanviColorPunts)
        self.vis.stateChanged.connect(self.CanviVisibilitat)
        self.sel.stateChanged.connect(self.CanviSeleccio)

    #-------------------------------------------------------------
    # SLOTS
    #-------------------------------------------------------------
    def CanviColorLinia(self):
        color=QColorDialog.getColor(QColor(0,255,0,0),self,"Color de la línia")
        if color.isValid():     # hem sortit del diàleg sense cancel·lar
            self.ColorLiniaCanviat.emit(self.idruta,color)
    #-------------------------------------------------------------
    def CanviColorPunts(self):
        color=QColorDialog.getColor(QColor(255,0,0,0),self,"Color dels punts")
        if color.isValid():     # hem sortit del diàleg sense cancel·lar
            self.ColorPuntsCanviat.emit(self.idruta,color)
    #-------------------------------------------------------------
    def CanviVisibilitat(self,estat):
        visible=estat==Qt.Checked
        self.VisibilitatCanviada.emit(self.idruta,visible)
        self.mare.disp.update()
    #-------------------------------------------------------------
    def CanviSeleccio(self,estat):
        seleccionada=estat==Qt.Checked
        self.SeleccioCanviada.emit(self.idruta,seleccionada)
        
    #-------------------------------------------------------------
    # GETTERS
    #-------------------------------------------------------------
    def GetNom(self):
        return self.nr.text()
    #-------------------------------------------------------------
    def GetSel(self):
        return self.sel.checkState()==Qt.Checked
    
    #-------------------------------------------------------------
    # SETTERS
    #-------------------------------------------------------------
    def SetNom(self,nom):
        self.nr.setText(nom)
    #-------------------------------------------------------------
    def SetSel(self,estat):
        if estat:
            self.sel.setCheckState(Qt.Checked)
        else:
            self.sel.setCheckState(Qt.Unchecked)

#-----------------------------------------------------------------
#-----------------------------------------------------------------
class FinestraRutes(QListWidget):
    
    def __init__(self,mare,rutes,disp):
        super().__init__(mare)
        self.mare=mare
        self.rutes=rutes
        self.disp=disp      # cal per fer l'update de la visibilitat
    #-------------------------------------------------------------
    def AfegirRuta(self,nom,idr):
        item=QListWidgetItem('',self)
        el=ElementList(nom,idr,self)
        item.setSizeHint(QSize(80,40))
        self.setItemWidget(item,el)
        self.addItem(item)

        el.ColorLiniaCanviat.connect(self.rutes.SetColorLinia)
        el.ColorPuntsCanviat.connect(self.rutes.SetColorPunts)
        el.VisibilitatCanviada.connect(self.rutes.SetVisibilitat)
        el.SeleccioCanviada.connect(self.rutes.SetSeleccio)
    #-------------------------------------------------------------
    def DividirRuta(self,idr1,idr2):
        nom=self.GetNomRuta(idr1)   # recupero el nom d'idr1
        nom1=nom+"_1"
        self.SetNomRuta(nom1,idr1)  # li actualitzo el  nom
        nom2=nom+"_2"
        self.AfegirRuta(nom2,idr2)  # creo idr2
    #-------------------------------------------------------------
    def SuprimirRuta(self,idr):
        # busquem la posició de la ruta idr
        pos=-1
        for i in range(0,self.count()):
            if self.itemWidget(self.item(i)).idruta==idr:
                pos=i
        # si l'hem trobat, eliminem la posició
        if pos!=-1:
            self.takeItem(pos)
    #-------------------------------------------------------------
    def DuplicarRuta(self,idr1,idr2):
        nom=self.GetNomRuta(idr1)   # recupero el nom d'idr1
        nom1=nom+"_A"
        self.SetNomRuta(nom1,idr1)  # li actualitzo el  nom
        nom2=nom+"_B"
        self.AfegirRuta(nom2,idr2)  # creo idr2
    #-------------------------------------------------------------
    def TreureRutesSel(self):
        # recorrem totes les rutes a l'inrevés
        # així quan suprimim, els índexs anteriors no canvien
        for i in range(self.count()-1,-1,-1):
            if self.itemWidget(self.item(i)).GetSel():
                self.takeItem(i)
        
    #-------------------------------------------------------------
    # GETTERS
    #-------------------------------------------------------------
    def GetNomRuta(self,idr):
        nom='-'
        for i in range(0,self.count()):
            if self.itemWidget(self.item(i)).idruta==idr:
                nom=self.itemWidget(self.item(i)).GetNom()
        return nom
        
    #-------------------------------------------------------------
    # SETTERS
    #-------------------------------------------------------------
    def SetNomRuta(self,nom,idr):
        pos=-1
        for i in range(0,self.count()):
            if self.itemWidget(self.item(i)).idruta==idr:
                pos=i
        if pos!=-1:
            self.itemWidget(self.item(pos)).SetNom(nom)

    #-------------------------------------------------------------
    # SLOTS    
    #-------------------------------------------------------------
    def ToggleSeleccio(self):
        if self.count()>0:      # només si hi ha rutes
            # posarem la selecció de tots al contrari del primer
            primer_sel=self.itemWidget(self.item(0)).GetSel()
            nou_estat=not primer_sel
            for i in range(0,self.count()):
                self.itemWidget(self.item(i)).SetSel(nou_estat)
            return nou_estat
        else:
            return None

#-----------------------------------------------------------------
if __name__=="__main__":
    main()
#-----------------------------------------------------------------
    
