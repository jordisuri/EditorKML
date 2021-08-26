from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from EditorKML_v2_1 import *
from Rutes import *

#-----------------------------------------------------------------
class Display(QWidget):
    def __init__(self,mare,c,rutes):
        super().__init__(mare)
        self.mare=mare
        self.c=c            # dimensions del Display
        self.rutes=rutes    # rutes, per accedir-hi directament
        self.windisp=[]     # window del Display, diferent del window de Rutes
                # el de Rutes és fix, el de Display canvia segons zoom i pan

        # fons blanc
        pal=QPalette(self.palette())
        pal.setColor(QPalette.Background,Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.w=self.c
        self.h=self.c
        self.dvx=self.c
        self.dvy=self.c
        self.dvmin=self.c
        self.lbx=0
        self.lby=0

        self.botoL=False
        self.xant=0
        self.yant=0
        self.shiftPremut=False
        self.controlPremut=False

        self.bicolor=-1

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus(Qt.MouseFocusReason)
    #-------------------------------------------------------------
    def resizeEvent(self,re):
        # recuperem les dimensions del display
        self.w=re.size().width()
        self.h=re.size().height()
        # si hi ha rutes, actualitzem factors i redibuixem
        if self.rutes.HiHaRutes():
            self.ActualitzarFactors()
    #-------------------------------------------------------------
    def ActualitzarCaixa(self):
        self.windisp=self.rutes.Caixa()
    #-------------------------------------------------------------
    def ActualitzarFactors(self):        
        arv=self.h/self.w       # aspect ratio viewport

        dwx=self.windisp[1]-self.windisp[0]
        dwy=self.windisp[3]-self.windisp[2]
        arw=dwy/dwx             # aspect ratio window

        # càlcul virtual viewport (dvy/dvx, add letterboxes) 
        if arw<arv:     # letterboxes a dalt i a baix (window més landscape que viewport)
            self.dvx=self.w
            self.dvy=int(self.w*arw)
            self.lbx=0
            self.lby=(self.h-self.dvy)//2
            self.dvmin=self.dvx
        else:           # letterboxes laterals (window més portrait que viewport)
            self.dvy=self.h
            self.dvx=self.h//arw
            self.lbx=(self.w-self.dvx)//2
            self.lby=0
            self.dvmin=self.dvy

        # transformacio window-viewport
        self.ax=self.dvx/dwx
        self.bx=-self.windisp[0]*self.dvx/dwx
        self.ay=self.dvy/dwy
        self.by=-self.windisp[2]*self.dvy/dwy

        self.zoom=dwx/15
        self.pan=dwx/self.dvmin
        
        self.update()
    #-------------------------------------------------------------
    def Punt2Pixel(self,wx,wy):
        # de coordenades món a coordenades pantalla (window -> viewport)
        vx=int(wx*self.ax+self.bx)+self.lbx
        vy=self.h-self.lby-int(wy*self.ay+self.by)
        return vx,vy
    #-------------------------------------------------------------
    def paintEvent(self,pe):
        qp=QPainter(self)
        qp.drawRect(0,0,self.w-1,self.h-1)   # dibuix del marc

        # dibuix de la creu central
        migx=self.w//2
        migy=self.h//2
        qp.drawLine(migx-20,migy,migx+20,migy)
        qp.drawLine(migx,migy-20,migx,migy+20)

        # per si el paintEvent és cridat abans de tenir rutes
        if not self.rutes.HiHaRutes():
            return
        
        # recuperem les mides de les línies i els punts
        mida_linia=self.mare.midaLinia.value()
        mida_punts=self.mare.midaPunts.value()
        
        # dibuix de les línies
        if mida_linia>0:        # només si la línia és visible
            for idr in self.rutes.g_id_visibles():       # ids de les rutes visibles
                color_linia=self.rutes.ColorLiniaRuta(idr)
                qp.setPen(QPen(color_linia,mida_linia))
                wx0,wy0=self.rutes.PrimerPunt(idr)      # primer punt
                vx0,vy0=self.Punt2Pixel(wx0,wy0)        # window -> viewport
                for wx1,wy1 in self.rutes.g_punts_ruta2(idr):   # resta de punts
                    vx1,vy1=self.Punt2Pixel(wx1,wy1)
                    qp.drawLine(vx0,vy0,vx1,vy1)
                    vx0,vy0=vx1,vy1

        # si el bicolor està actiu, recuperem el punt de l'slider
        if self.bicolor!=-1:
            ipbicolor=self.mare.slbicolor.value()
            bicolor0=QColor(0,0,0,255)
            bicolor1=QColor(100,100,100,128)
        
        # dibuix dels punts
        if mida_punts>0:        # només si els punts són visibles
            for idr in self.rutes.g_id_visibles():        # índexs de les rutes visibles
                if idr!=self.bicolor:   # no bicolor o no en la ruta seleccionada
                    color_punts=self.rutes.ColorPuntsRuta(idr)
                    qp.setPen(QPen(color_punts,mida_punts))
                    for wx,wy in self.rutes.g_punts_ruta(idr):   # obtenim els punts
                        vx,vy=self.Punt2Pixel(wx,wy)
                        qp.drawPoint(vx,vy)
                else:   # bicolor activat i estem en la ruta seleccionada
                    ip=0
                    qp.setPen(QPen(bicolor0,mida_punts))
                    for wx,wy in self.rutes.g_punts_ruta(idr):
                        if ip==ipbicolor:   # si estem al punt, canvi a negre
                            qp.setPen(QPen(bicolor1,mida_punts))
                        vx,vy=self.Punt2Pixel(wx,wy)
                        qp.drawPoint(vx,vy)
                        ip+=1
                
                # remarco l'inici
                qp.setPen(QPen(Qt.black,1))
                wx,wy=self.rutes.PrimerPunt(idr)    # primer punt...
                vx,vy=self.Punt2Pixel(wx,wy)        # ...convertit a pixel
                qp.drawLine(vx-4,vy-4,vx+4,vy+4)
                qp.drawLine(vx-4,vy+4,vx+4,vy-4)
        
        # dibuix dels marcats
        #   la ruta ha de ser visible
        #   no importa si està seleccionada o no
        if self.rutes.HiHaMarcats():
            qp.setPen(QPen(Qt.darkBlue,7))
            for idr in self.rutes.marcats:      # iterem per les rutes amb marques
                if self.rutes.EsVisible(idr):   # només si és visible
                    for ip in self.rutes.marcats[idr]:
                        wx,wy=self.rutes.PuntIndexat(idr,ip)
                        vx,vy=self.Punt2Pixel(wx,wy)
                        qp.drawPoint(vx,vy)
          
    #-------------------------------------------------------------
    # RODA RATOLÍ
    #-------------------------------------------------------------
    def wheelEvent(self,we):
        if not self.rutes.HiHaRutes():
            return
        
        if self.shiftPremut:
            if we.angleDelta().y()>0:   # zoom in
                z=3*self.zoom
            else:                       # zoom out
                z=-3*self.zoom
        else:
            if we.angleDelta().y()>0:   # zoom in
                z=self.zoom
            else:                       # zoom out
                z=-self.zoom
        
        # fem zoom canviant la bounding box de la finestra de Display
        self.windisp[0]+=z
        self.windisp[1]-=z
        self.windisp[2]+=z
        self.windisp[3]-=z
        
        self.ActualitzarFactors()
    #-------------------------------------------------------------
    # RATOLÍ
    #-------------------------------------------------------------
    def mouseMoveEvent(self,mme):
        if not self.rutes.HiHaRutes():
            return
        
        if self.botoL:
            dx=(mme.x()-self.xant)*self.pan
            dy=(mme.y()-self.yant)*self.pan

            # fem pan canviant de lloc la bounding box de la finestra
            self.windisp[0]-=dx
            self.windisp[1]-=dx
            self.windisp[2]+=dy
            self.windisp[3]+=dy

            self.xant=mme.x()
            self.yant=mme.y()
            
            self.ActualitzarFactors()
    #-------------------------------------------------------------
    def mousePressEvent(self,mpe):
        if not self.rutes.HiHaRutes():
            return
        
        esquerre=mpe.button()==Qt.LeftButton
        dret=mpe.button()==Qt.RightButton
        
        if esquerre:
            if self.shiftPremut:
                # marco punt
                idr,ip=self.BuscarPunt(mpe.x(),mpe.y())
                if idr!=-1:     # pot no haver-hi cap ruta seleccionada
                    self.rutes.MarcarAlternat(idr,ip)
                    self.update()
            else:
                # pan
                self.botoL=True
                self.xant=mpe.x()
                self.yant=mpe.y()
        elif dret:
            # marco punt
            idr,ip=self.BuscarPunt(mpe.x(),mpe.y())
            if idr!=-1:         # pot no haver-hi cap ruta seleccionada
                self.rutes.MarcarAlternat(idr,ip)
                self.update()
    #-------------------------------------------------------------
    def mouseReleaseEvent(self,mpe):
        if mpe.button()==Qt.LeftButton:
            self.botoL=False
    #-------------------------------------------------------------
    def mouseDoubleClickEvent(self,mpe):
        self.botoL=False
        self.shiftPremut=False
        self.controlPremut=False
        
        if not self.rutes.HiHaRutes():
            return
        
        self.ActualitzarCaixa()
        self.ActualitzarFactors()
        
    #-------------------------------------------------------------
    # TECLAT
    #-------------------------------------------------------------
    def keyPressEvent(self,kpe):
        super().keyPressEvent(kpe)
        if kpe.key()==16777248:         # shift esq
            self.shiftPremut=True
        if kpe.key()==16777249:         # ctrl esq
            self.controlPremut=True
    #-------------------------------------------------------------
    def keyReleaseEvent(self,kpe):
        super().keyReleaseEvent(kpe)
        if kpe.key()==16777248:         # shift esq
            self.shiftPremut=False
        if kpe.key()==16777249:         # ctrl esq
            self.controlPremut=False

    #-----------------------------------------------------------------
    # BUSCAR PUNT
    #-----------------------------------------------------------------
    def BuscarPunt(self,px,py):
        min_d=10000000000
        pos=-1
        en_ruta=-1
        # busquem només en les rutes visibles i seleccionades
        for idr in self.rutes.g_id_vis_sel():
            lp=self.rutes.LlistaPunts(idr)
            for ip in range(0,len(lp)):
                wx,wy=lp[ip]
                vx,vy=self.Punt2Pixel(wx,wy)
                d=self.Distancia2(px,py,vx,vy)
                if d<min_d:
                    min_d=d
                    pos=ip
                    en_ruta=idr
        return en_ruta,pos
    #-----------------------------------------------------------------
    def Distancia2(self,x1,y1,x2,y2):
        return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
    
    #-----------------------------------------------------------------
    # SLOTS
    #-----------------------------------------------------------------
    def CanviMidaLinia(self,ml):
        # no ens cal ml: paintEvent() el consultarà directament
        self.update()
    #-----------------------------------------------------------------
    def CanviMidaPunts(self,mp):
        # no ens cal mp: paintEvent() el consultarà directament
        self.update()
    #-----------------------------------------------------------------
    def ActivarBicolor(self,idr):
        self.bicolor=idr        # ruta en la que s'activa el bicolor
                                # -1 si es desactiva
        self.update()
    #-----------------------------------------------------------------
    def PuntBicolorCanviat(self,v):
        # no ens cal v: paintEvent() el consultarà directament
        self.update()

        
#-----------------------------------------------------------------
#-----------------------------------------------------------------
if __name__=="__main__":
    main()
#-----------------------------------------------------------------
    
