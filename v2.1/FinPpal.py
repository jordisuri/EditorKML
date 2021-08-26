from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from EditorKML_v2_1 import *
from Rutes import *
from Display import *
from FinestraRutes import *
from Ajuda import *


#-----------------------------------------------------------------
#-----------------------------------------------------------------
class FinPpal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EditorKML  v2.1")
        self.c=700
        self.resize(self.c+350,self.c)

        self.cami="."       # subdirectori dels fitxers
        
        self.rutes=Rutes()                          # llista de rutes
        self.disp=Display(self,self.c,self.rutes)   # Display de les rutes
        self.fr=FinestraRutes(self,self.rutes,self.disp)    # finestra de les rutes

        self.CrearUI()      # posem els elements visuals de la finestra
        self.CrearMenu()    # afegim el menú
        
        # connexions dels signals
        self.midaLinia.valueChanged.connect(self.disp.CanviMidaLinia)
        self.midaPunts.valueChanged.connect(self.disp.CanviMidaPunts)
        
    #-------------------------------------------------------------
    def CrearUI(self):
        # MIDES
        
        # slider
        self.midaLinia=QSlider(Qt.Horizontal,self)
        self.midaLinia.setMinimum(0)
        self.midaLinia.setMaximum(8)
        self.midaLinia.setTickInterval(1)
        self.midaLinia.setPageStep(1)
        self.midaLinia.setTickPosition(QSlider.TicksBelow)
        self.midaLinia.setValue(2)

        # slider mida dels punts
        self.midaPunts=QSlider(Qt.Horizontal,self)
        self.midaPunts.setMinimum(0)
        self.midaPunts.setMaximum(8)
        self.midaPunts.setTickInterval(1)
        self.midaPunts.setPageStep(1)
        self.midaPunts.setTickPosition(QSlider.TicksBelow)
        self.midaPunts.setValue(2)

        # layout
        layoutH1=QHBoxLayout()
        layoutH1.addWidget(QLabel("Línies"))
        layoutH1.addWidget(self.midaLinia)
        layoutH1.setStretch(0,1)
        layoutH1.setStretch(1,10)

        layoutH2=QHBoxLayout()
        layoutH2.addWidget(QLabel("Punts"))
        layoutH2.addWidget(self.midaPunts)
        layoutH2.setStretch(0,1)
        layoutH2.setStretch(1,10)

        layoutV1=QVBoxLayout()
        layoutV1.addLayout(layoutH1)
        layoutV1.addLayout(layoutH2)
        
        # groupbox
        self.gbmides=QGroupBox("Mides",self)
        self.gbmides.setLayout(layoutV1)
        
        #---------------------------------------------------------
        # BICOLOR
        
        # checkbox
        self.cbbicolor=QCheckBox('')
        
        # slider
        self.slbicolor=QSlider(Qt.Horizontal)
        self.slbicolor.setMinimum(1)
        self.slbicolor.setMaximum(10)
        self.slbicolor.setTickInterval(1)
        self.slbicolor.setPageStep(1)
        self.slbicolor.setValue(5)
        self.slbicolor.setEnabled(False)

        # layout
        layoutH3=QHBoxLayout()
        layoutH3.addWidget(self.cbbicolor)
        layoutH3.addWidget(self.slbicolor)
        layoutH3.setStretch(0,1)
        layoutH3.setStretch(1,10)
        
        # groupbox
        self.gbbicolor=QGroupBox("Bicolor",self)
        self.gbbicolor.setLayout(layoutH3)

        # connexions
        self.cbbicolor.stateChanged.connect(self.CanviCBBicolor)
        self.slbicolor.valueChanged.connect(self.disp.PuntBicolorCanviat)
        
        #---------------------------------------------------------
        # TOGGLE SELECCIÓ
        self.btoggleSeleccio=QPushButton("Toggle selecció",self)
        self.btoggleSeleccio.clicked.connect(self.ToggleSeleccio)
        
        #---------------------------------------------------------
        # CONTROLS LATERALS
        
        layoutV=QVBoxLayout()
        layoutV.addWidget(self.gbmides)
        layoutV.addWidget(self.gbbicolor)
        layoutV.addWidget(self.btoggleSeleccio)
        layoutV.addWidget(self.fr)
        #layoutV.addStretch()

        self.fr.setMaximumWidth(350)
        self.fr.setMinimumWidth(350)
        self.gbmides.setMaximumWidth(350)
        self.gbbicolor.setMaximumWidth(350)

        layoutH=QHBoxLayout()
        layoutH.addWidget(self.disp)
        self.disp.setMinimumSize(400,400)
        layoutH.addLayout(layoutV)
        
        cw=QWidget(self)
        cw.setLayout(layoutH)
        self.setCentralWidget(cw)

    #---------------------------------------------------------
    def CrearMenu(self):
        bar=self.menuBar()
        
        fitxers=bar.addMenu("Fitxers")
        fitxers.addAction("Obrir")
        fitxers.addAction("Guardar")
        fitxers.addAction("Nou")
        
        rutes=bar.addMenu("Rutes")
        rutes.addAction("Invertir")
        rutes.addAction("Dividir")
        rutes.addAction("Fusionar")
        rutes.addAction("Duplicar")
        rutes.addAction("Suprimir")
        
        punts=bar.addMenu("Punts")
        punts.addAction("Segment")
        punts.addAction("Desmarcar")
        punts.addAction("Eliminar")
        punts.addAction("Substituir")

        ajuda=bar.addAction("Ajuda")

        # connexions dels menús
        bar.triggered.connect(self.ProcessarMenu)
    #-------------------------------------------------------------
    def ProcessarMenu(self,op):
        if op.text()=="Obrir":
            self.Obrir()
            
        elif op.text()=="Guardar":
            if self.rutes.HiHaRutes() and self.rutes.HiHaSeleccionades():
                self.Guardar()
            else:
                QMessageBox().question( self,
                                        "Error guardant",
                                        "Hi ha d'haver alguna ruta seleccionada",
                                        QMessageBox.Ok) 
                
        elif op.text()=="Nou":
            if self.rutes.HiHaRutes():
                self.Nou()


                
        elif op.text()=="Invertir":
            if self.rutes.HiHaRutes():
                self.rutes.InvertirRutes()   # inverteix les rutes seleccionades
                self.disp.update()

        elif op.text()=="Dividir":
            if self.rutes.HiHaRutes():
                self.Dividir()

        elif op.text()=="Fusionar":
            if self.rutes.HiHaRutes():
                self.Fusionar()

        elif op.text()=="Duplicar":
            if self.rutes.HiHaRutes():
                self.Duplicar()

        elif op.text()=="Suprimir":
           if self.rutes.HiHaRutes():
                self.Suprimir()


        
        elif op.text()=="Segment":
            if self.rutes.HiHaRutes():
                self.Segment()

        elif op.text()=="Desmarcar":
            if self.rutes.HiHaRutes():
                self.rutes.Desmarcar()
                self.disp.update()

        elif op.text()=="Eliminar":
            if self.rutes.HiHaRutes():
                self.Eliminar()
                
        elif op.text()=="Substituir":
            if self.rutes.HiHaRutes():
                self.Substituir()
        

        elif op.text()=="Ajuda":
            self.fin_ajuda=FinAjuda()
            self.fin_ajuda.setWindowModality(Qt.ApplicationModal)
            self.fin_ajuda.show()
    
    #-------------------------------------------------------------
    # OBRIR
    #-------------------------------------------------------------
    def Obrir(self):
        # obtenim el nom del fitxer
        nom_fitxer=QFileDialog.getOpenFileName(
                        self,"Obrir fitxer kml",self.cami,
                        "Fitxers kml (*.kml);;Tots (*.*)")
        self.cami=os.path.dirname(nom_fitxer[0])    # actualitzo el camí, per si hagués canviat

        if nom_fitxer[0]!='':                   # si no hem tancat el diàleg
            lr,ln=self.ObtenirRutesFitxer(nom_fitxer[0])    # llegim les rutes (llista de punts) i noms de les rutes del fitxer
            for i in range(len(lr)):                        # les guardem
                idr=self.rutes.AfegirRuta(lr[i])
                self.fr.AfegirRuta(ln[i],idr)
            
            # actualitzem les dades del Display
            self.disp.ActualitzarCaixa()
            self.disp.ActualitzarFactors()
    #-----------------------------------------------------------------
    def ObtenirRutesFitxer(self,fitxer):
        # llegim les rutes
        # ha de tenir en compte els diferents formats kml que hi ha
        # Pot ser que tot el fitxer sigui una sola línia (wikiloc)
        
        # separo els tags en línies (i potser afegeixo línies en blanc)
        # genero el fitxer temporal zzz1.kml
        f=open(fitxer,'r')
        g=open("zzz1.kml","w")
        linia=f.readline()
        while linia!='':
            linia=linia.strip()
            r=self.PartirLinia(linia)   # talla (afegeix \n) a cada '<' i '>'
            g.write(r+'\n')
            linia=f.readline()
        f.close()
        g.close()

        # elimino les línies en blanc
        # usa zzz1.kml i genera el segon fitxer temporal zzz2.kml
        f=open("zzz1.kml","r")
        g=open("zzz2.kml","w")
        linia=f.readline()
        while linia!='':
            linia=linia.strip()
            if linia!='':           # línia no en blanc (l'strip ha suprimit el \n final)
                g.write(linia+'\n')
            # si la línia és en blanc, no fa el write
            linia=f.readline()
        f.close()
        g.close()

        # analitzo el fitxer i en recupero el nom i les coordenades de les seves rutes
        # usa el fitxer temporal zzz2.kml

        # hi ha noms (<name>) de moltes coses. El nom d'un segment és l'últim declarat abans de la ruta
        # vaig llegint noms (esborrant l'anterior) i guardo l'últim llegit abans de la ruta
        # hi ha coordenades (<coordinates>) de segments i de waypoints:
        # les coordenades de rutes van precedides per <LineString> (no necessàriament estan de manera consecutiva)
        # les coordenades estan en la línia següent a <coordinates>
        LineString=False    # hem llegit <LineString> i encara no </LineString>?
        coordinates=False   # hem llegit <coordinates> i encara no </coordinates>?
        nom='-'             # nom de l'últim <name> llegit
        lr=[]               # llista de les rutes del fitxer
        ln=[]               # llista dels noms del fitxer

        f=open("zzz2.kml","r")
        linia=f.readline()
        while linia!='':
            linia=linia.strip()
            if linia=="<name>":
                nom=f.readline().strip()    # recupero el nom (línia següent a <name>)
            if linia=="<LineString>":
                LineString=True
            if linia=="</LineString>":
                LineString=False
            if linia=="<coordinates>":
                coordinates=True
                ruta=[]                     # pot (o no) començar una ruta
                linia=f.readline().strip()
            if linia=="</coordinates>":
                coordinates=False
                # ja tenim la ruta i el seu nom
                if len(ruta)>0:     #
                    lr.append(ruta)
                    nom=self.TreureCDATA(nom)   # suprimeix el CDATA, si és el cas
                    ln.append(nom)

            if LineString and coordinates:  # estem llegint punts
                # la línia conté un o més punts
                w=linia.split()     # separo per punts
                if len(w)>1:
                    # tots els punts en una sola línia
                    for punt in w:  # recorrem els punts
                        lcoord=punt.split(',')
                        ruta.append([float(lcoord[0]),float(lcoord[1])])
                else:
                    # un punt per línia
                    lcoord=w[0].split(',')
                    ruta.append([float(lcoord[0]),float(lcoord[1])])
                    
            linia=f.readline()

        f.close()

        # netegem fitxers temporals
        if os.path.exists("zzz1.kml"):
            os.remove("zzz1.kml")
            
        if os.path.exists("zzz2.kml"):
            os.remove("zzz2.kml")
            
        return lr,ln
    #-----------------------------------------------------------------
    def PartirLinia(self,linia):
        r=""
        for c in linia:
            if c=='<':
                r+='\n<'
            elif c=='>':
                r+='>\n'
            else:
                r+=c
        return r
    #-----------------------------------------------------------------
    def TreureCDATA(self,nom):
        if "CDATA" in nom:
            nom=nom.replace("<![CDATA[","")
            nom=nom.replace("]]>","")
        return nom

    #-------------------------------------------------------------
    # GUARDAR
    #-------------------------------------------------------------
    def Guardar(self):
        # demanem el nom del fitxer
        nom_fitxer=QFileDialog.getSaveFileName(
                    self,"Guardar fitxer kml",self.cami,
                    "Fitxers kml (*.kml);;Tots (*.*)")

        self.cami=os.path.dirname(nom_fitxer[0])   # actualitzo el camí, per si hagués canviat
        if nom_fitxer[0]!='':                   # si no hem tancat el diàleg
            nom=nom_fitxer[0].split('/')[-1]
            # recorrem la plantilla del document
            f1=open("PlantillaDoc.kml",'r')
            resultat=''
            s=f1.readline()
            while s!='':
                if '%f%' in s:
                    s=s.replace('%f%',nom)
                if '<!--r-->' in s:
                    s=self.PosarRutes() # posem les rutes visibles
                resultat+=s
                s=f1.readline()  
            f1.close()
            
        # guardem el text
        f2=open(nom_fitxer[0],'w')
        f2.write(resultat)
        f2.close()
    #-------------------------------------------------------------
    def PosarRutes(self):
        resultat=''
        for idr in self.rutes.g_id_seleccionades():
            nom_ruta=self.fr.GetNomRuta(idr)            # obtenim el nom de la ruta
             # generem el color de la ruta en format aabbggrr (hexa)
            color_linia=self.rutes.ColorLiniaRuta(idr)   # només em cal el color de la línia, no dels punts
            alfa="%0.2X"%color_linia.alpha()
            vermell="%0.2X"%color_linia.red()
            verd="%0.2X"%color_linia.green()
            blau="%0.2X"%color_linia.blue()
            color=alfa+blau+verd+vermell
            
            f=open("PlantillaRuta.kml",'r')
            s=f.readline()
            while s!='':
                if '%r%' in s:
                    s=s.replace('%r%',nom_ruta)
                if '%c%' in s:
                    s=s.replace('%c%',color)
                if '%a%' in s:
                    s=s.replace('%a%',str(self.midaLinia.value()))
                if '%p%' in s:
                    s=self.LC2String(idr) # posem els punts de la ruta r
                resultat+=s
                s=f.readline()
            f.close()
        resultat+="\n"
        return resultat
    #-------------------------------------------------------------
    def LC2String(self,idr):
        resultat=''
        for x,y in self.rutes.g_punts_ruta(idr):
            resultat+='\t\t\t\t'+str(x)+','+str(y)+'\n'
        return resultat

    #-------------------------------------------------------------
    # NOU
    #-------------------------------------------------------------
    def Nou(self):
        confirmacio=QMessageBox().question( self,
                                            "Nou",
                                            "Vols eliminar totes les rutes?",
                                            QMessageBox.Yes|QMessageBox.No)
        if confirmacio==QMessageBox.Yes:
            self.rutes=Rutes()                          # llista de rutes
            self.disp=Display(self,self.c,self.rutes)   # Display de les rutes
            self.fr=FinestraRutes(self,self.rutes,self.disp)    # finestra de les rutes

            self.CrearUI()  # posem els elements visuals de la finestra
                            # no creem el menú: el duplicaríem!
            
    #-------------------------------------------------------------
    # SEGMENT
    #-------------------------------------------------------------
    def Segment(self):
        idr=self.rutes.UnaSeleccionada()
        if idr!=-1:
            if self.rutes.NumMarcatsRuta(idr)<2:
                QMessageBox().question( self,
                                        "Error segment",
                                        "Hi ha d'haver un mínim de dos punts marcats",
                                        QMessageBox.Ok)
            else:
                self.rutes.MarcarSegment(idr)   # marca de la primera a última marca de cada ruta
                self.disp.update()
        else:
            QMessageBox().question( self,
                                    "Error segment",
                                    "Només hi ha d'haver una ruta seleccionada",
                                    QMessageBox.Ok)

    #-------------------------------------------------------------
    # ELIMINAR
    #-------------------------------------------------------------
    def Eliminar(self):
        if self.rutes.HiHaMarcats():
            confirmacio=QMessageBox().question( self,
                                                "Eliminar punts",
                                                "Vols eliminar els punts marcats de les rutes seleccionades?",
                                                QMessageBox.Yes|QMessageBox.No)
            if confirmacio==QMessageBox.Yes:
                self.rutes.EliminarPunts()            
                self.disp.update()

    #-------------------------------------------------------------
    # DIVIDIR
    #-------------------------------------------------------------
    def Dividir(self):
        idr1=self.rutes.UnaSeleccionada()
        if idr1!=-1:    # només una ruta seleccionada
            if self.rutes.NumMarcatsRuta(idr1)==1:  # només un punt marcat en la ruta
                confirmacio=QMessageBox().question( self,
                                                    "Dividir rutes",
                                                    "Vols dividir les rutes?",
                                                    QMessageBox.Yes|QMessageBox.No)
                if confirmacio==QMessageBox.Yes:
                    idr2=self.rutes.DividirRuta(idr1)   # dividim la ruta
                        # idr1 s'ha reaprofitat per a contenir la primera part
                        # idr2 és un nou id i conté la segona part
                    self.fr.DividirRuta(idr1,idr2)      # dividim l'entrada a la fr
                    self.disp.update()
            else:
                QMessageBox().question( self,
                                        "Error dividint",
                                        "Només hi ha d'haver una sola marca",
                                        QMessageBox.Ok)
        else:
            QMessageBox().question( self,
                                    "Error dividnt",
                                    "Només hi ha d'haver una ruta seleccionada",
                                    QMessageBox.Ok)
    
    #-------------------------------------------------------------
    # FUSIONAR
    #-------------------------------------------------------------
    def Fusionar(self):
        # trobar dues rutes per fusionar-les
        idr1,idr2=self.rutes.DuesSeleccionades()
        if idr1==-1:
            QMessageBox().question( self,
                                    "Error fusionant",
                                    "No hi dues rutes marcades",
                                    QMessageBox.Ok)
            return

        nom_ruta_1=self.fr.GetNomRuta(idr1)
        nom_ruta_2=self.fr.GetNomRuta(idr2)
        ordre=QMessageBox().question(   self,"Ordre de la fusió",
                                        "Fusionem "+nom_ruta_1+" + "+nom_ruta_2+"?",
                                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        if ordre==QMessageBox.Yes:
            self.rutes.FusionarRutes(idr1,idr2)
            self.fr.SuprimirRuta(idr2)
        elif ordre==QMessageBox.No:
            self.rutes.FusionarRutes(idr2,idr1)
            self.fr.SuprimirRuta(idr1)

        self.disp.update()
        
    #-------------------------------------------------------------
    # DUPLICAR
    #-------------------------------------------------------------
    def Duplicar(self):
        idr1=self.rutes.UnaSeleccionada()
        if idr1!=-1:    # només una ruta seleccionada
            confirmacio=QMessageBox().question( self,
                                                "Duplicar ruta",
                                                "Vols duplicar la ruta seleccionada?",
                                                QMessageBox.Yes|QMessageBox.No)
            if confirmacio==QMessageBox.Yes:
                idr2=self.rutes.DuplicarRuta(idr1)  # dupliquem la ruta
                self.fr.DuplicarRuta(idr1,idr2)     # dividim l'entrada a la fr
                    # la ruta original canvia el nom: afegeix el sufix _A i
                    # la segona té el mateix nom amb el sufix _B
                self.disp.update()

        else:
            QMessageBox().question( self,
                                    "Error duplicant",
                                    "Només hi ha d'haver una ruta seleccionada",
                                    QMessageBox.Ok)

    #-------------------------------------------------------------
    # SUPRIMIR
    #-------------------------------------------------------------
    def Suprimir(self):
        confirmacio=QMessageBox().question( self,"Suprimir rutes",
                                            "Vols suprimir les rutes seleccionades?",
                                            QMessageBox.Yes|QMessageBox.Cancel)
        if confirmacio==QMessageBox.Yes:
            self.rutes.TreureRutesSel()
            self.fr.TreureRutesSel()
            
            # actualitzem les dades del Display
            self.disp.ActualitzarCaixa()
            self.disp.ActualitzarFactors()


    #-------------------------------------------------------------
    # SUBSTITUIR
    #-------------------------------------------------------------
    def Substituir(self):
        # trobar dues rutes per fer la substitució
        idr1,idr2=self.rutes.DuesSeleccionades()
        if idr1==-1:
            QMessageBox().question( self,
                                    "Error substituint",
                                    "No hi dues rutes marcades",
                                    QMessageBox.Ok)
            return

        nom_ruta_1=self.fr.GetNomRuta(idr1)
        nom_ruta_2=self.fr.GetNomRuta(idr2)
        ordre=QMessageBox().question(   self,"Ordre de la substitució",
                                        "El segment de "+nom_ruta_1+" qudarà substituit pel de "+nom_ruta_2,
                                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        if ordre==QMessageBox.Yes:
            self.rutes.SubstituirSegments(idr1,idr2)
        elif ordre==QMessageBox.No:
            self.rutes.SubstituirSegments(idr2,idr1)

        self.disp.update()

    #-------------------------------------------------------------
    # AJUDA
    #-----------------------------------------------------------------
    def MostrarAjuda(self):
        fa=open("Ajuda.html","r")
        
        r=""
        linia=fa.readline()
        while linia!="":
            r+=linia+'\n'
            linia=fa.readline()
        fa.close()
        
        self.fin_ajuda=FinAjuda(r)
        self.fin_ajuda.setWindowModality(Qt.ApplicationModal)
        self.fin_ajuda.show()
    
    #-------------------------------------------------------------
    # ALTRES
    #-------------------------------------------------------------
    def ToggleSeleccio(self):
        estat=self.fr.ToggleSeleccio()  # retorna l'estat (True/False) que ha posat
        if estat!=None:
            self.rutes.ToggleSeleccio(estat)
    #-----------------------------------------------------------------
    def CanviCBBicolor(self,estat):
        if estat==Qt.Checked:
            idr=self.rutes.UnaSeleccionada()
            if idr!=-1:
                np=self.rutes.NumPuntsRuta(idr)
                self.slbicolor.setEnabled(True)
                self.slbicolor.setMinimum(0)
                self.slbicolor.setMaximum(np)
                self.slbicolor.setTickInterval(50)
                self.slbicolor.setPageStep(1)
                self.slbicolor.setTickPosition(QSlider.TicksBelow)
                self.slbicolor.setValue(np//2)
                
                self.disp.ActivarBicolor(idr)   # activo el bicolor i de pas indico la ruta
            else:
                self.cbbicolor.setCheckState(Qt.Unchecked)
                QMessageBox().question( self,
                                        "Error activant bicolor",
                                        "No hi ha només una ruta marcada",
                                        QMessageBox.Ok)
        else:
            self.slbicolor.setEnabled(False)
            self.disp.ActivarBicolor(-1)



#-----------------------------------------------------------------
if __name__=="__main__":
    main()
#-----------------------------------------------------------------
