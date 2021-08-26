
from PyQt5.QtGui import *   # QColor
from copy import deepcopy

from EditorKML_v2_2 import *

#-----------------------------------------------------------------
#-----------------------------------------------------------------
class Ruta:
    def __init__(self,lp):
        self.lp=lp          # llista de punts
        
        # colors per defecte
        self.colorPunts=QColor(255,0,0)
        self.colorLinia=QColor(0,255,0)
        
        self.visible=True
        self.seleccionada=True

        self.BoundingBoxRuta()  # la guarda a self.win
    #-----------------------------------------------------------------
    def BoundingBoxRuta(self):
        # x:longitud
        wx0=self.lp[0][0]   # 1r punt, 1a coord (x)
        wx1=self.lp[0][0]
        # y:latitud
        wy0=self.lp[0][1]
        wy1=self.lp[0][1]
        for p in self.lp:   # tots els punts de la ruta
            if p[0]<wx0:
                 wx0=p[0]
            if p[0]>wx1:
                wx1=p[0]
            if p[1]<wy0:
                wy0=p[1]
            if p[1]>wy1:
                wy1=p[1]
        return [wx0,wx1,wy0,wy1]    # retornem la BB
        
#-----------------------------------------------------------------
#-----------------------------------------------------------------
class Rutes:
    idruta=0                # identificador de cada ruta
                            # és la clau del diccionari dr
    #-------------------------------------------------------------
    def __init__(self):
        self.dr={}          # diccionari: {idruta:Ruta}
        self.marcats={}     # diccionari de punts marcats: {idruta:[ip]}
        self.win=[]         # caixa contenidora del conjunt de rutes

    #-----------------------------------------------------------------
    # RUTES
    #-------------------------------------------------------------
    def AfegirRuta(self,lp):
        idr=self.idruta     # generació de l'identificador de la ruta
        self.idruta+=1
        
        r=Ruta(lp)          # creació de l'objecte ruta
        self.dr[idr]=r      # inserció en el diccionari

        self.BoundingBoxRutes()     # calculem la BB amb la nova ruta
        self.AjustarAR()            # ajusta el viewport
        
        return idr          # retornem l'identificador
    #-------------------------------------------------------------
    def InvertirRutes(self):
        for idr in self.g_id_seleccionades():   # només rutes seleccionades
            self.dr[idr].lp.reverse()
    #-------------------------------------------------------------
    def DividirRuta(self,idr1):
        # idr1 està seleccionada i té 1 marca
        ip=self.marcats[idr1][0]        # índex del primer punt: serà el punt de tall
        ruta1=self.dr[idr1].lp[:ip+1]   # primera part (inclou el punt de tall)
        ruta2=self.dr[idr1].lp[ip:]     # segona part

        self.dr[idr1].lp=ruta1          # reassignem la primera part a la ruta original
        idr2=self.AfegirRuta(ruta2)     # creem la segona part com a nova ruta

        self.Desmarcar()        # no té sentit mantenir la marca de la ruta

        return idr2             # retornem l'id de la segona part
    #-----------------------------------------------------------------
    def FusionarRutes(self,idr1,idr2):
        self.dr[idr1].lp+=self.dr[idr2].lp  # unim idr2 al final de idr1
        del self.dr[idr2] 
    #-----------------------------------------------------------------
    def DuplicarRuta(self,idr1):
        ruta2=deepcopy(self.dr[idr1].lp)    # dupliquem la ruta idr1
        for i in range(0,len(ruta2)):
            ruta2[i][0]+=1.5e-5
        idr2=self.AfegirRuta(ruta2)     # afegim la ruta duplicada
        return idr2                     # retornem l'id del duplicat
    #-----------------------------------------------------------------
    def TreureRutesSel(self):
        # enlloc de suprimir d'un diccionari (no es pot fer en una iteració),
        # genero un nou diccionari amb les que no s'han d'eliminar (les no sel)
        # i finalment assigno el nou diccionari a self.dr
        d={}
        for kr in self.dr:
            if not self.EsSeleccionada(kr):
                d[kr]=self.dr[kr]
        self.dr=d
        
        self.Desmarcar()            # traiem totes les marques
        self.BoundingBoxRutes()     # recalculem la nova BB
        self.AjustarAR()            # ajustem l'ar del viewport
    #-----------------------------------------------------------------
    def SubstituirSegments(self,idr1,idr2):
        # primera i última marca d'idr1
        pm1=self.marcats[idr1][0]
        um1=self.marcats[idr1][-1]
        
        # primera i última marca d'idr2
        pm2=self.marcats[idr2][0]
        um2=self.marcats[idr2][-1]

        # elimino el segment d'idr1
        for ip in range(um1,pm1-1,-1):
            del self.dr[idr1].lp[ip]

        # copio els punts d'idr2 a idr1
        for ip in range(um2,pm2-1,-1):  # recorrent-los a l'inrevés els puc inserir
                                        # tots en la mateixa posició: pm1
            self.dr[idr1].lp.insert(pm1,self.dr[idr2].lp[ip])

        self.Desmarcar()
    #-------------------------------------------------------------
    # GENERADORS
    #-------------------------------------------------------------
    # generador d'idr de les rutes seleccionades
    def g_id_seleccionades(self):
        for kr in self.dr:
            if self.dr[kr].seleccionada:
                yield kr
    #-------------------------------------------------------------
    # generador d'idr de les rutes visibles
    def g_id_visibles(self):
        for kr in self.dr:
            if self.dr[kr].visible:
                yield kr
    #-------------------------------------------------------------
    # generador d'idr de les rutes visibles i seleccionades
    def g_id_vis_sel(self):
        for kr in self.dr:
            if self.dr[kr].visible and self.dr[kr].seleccionada:
                yield kr
    #-------------------------------------------------------------
    # generador dels punts una ruta específica
    def g_punts_ruta(self,idr):
        punts_ruta=self.dr[idr].lp
        for px,py in punts_ruta:
            yield px,py
    #-------------------------------------------------------------
    # generador dels punts una ruta específica, excepte el primer
    def g_punts_ruta2(self,idr):
        punts_ruta=self.dr[idr].lp
        for ip in range(1,len(punts_ruta)):
            yield punts_ruta[ip]

    #-------------------------------------------------------------
    # GETTERS I CONSULTORES
    #-------------------------------------------------------------
    def EsVisible(self,idr):
        return self.dr[idr].visible
    #-------------------------------------------------------------
    def Caixa(self):
        return self.win[:]          # en fa un duplicat!
    #-------------------------------------------------------------
    def HiHaRutes(self):
        return len(self.dr)>0
    
    #-------------------------------------------------------------
    def ColorLiniaRuta(self,idr):
        return self.dr[idr].colorLinia
    #-------------------------------------------------------------
    def ColorPuntsRuta(self,idr):
        return self.dr[idr].colorPunts
    
    #-------------------------------------------------------------
    # PUNTS
    #-------------------------------------------------------------
    def PrimerPunt(self,idr):       # primer punt de la ruta idr
        return self.dr[idr].lp[0]
    #-------------------------------------------------------------
    def PuntIndexat(self,idr,ip):   # punt ip de la ruta idr
        return self.dr[idr].lp[ip]
    #-------------------------------------------------------------
    def LlistaPunts(self,idr):      # llista dels punts de la ruta idr
        return self.dr[idr].lp
    #-------------------------------------------------------------
    def NumPuntsRuta(self,idr):     # nombre de punts de la ruta idr
        return len(self.dr[idr].lp)

    #-------------------------------------------------------------
    # SELECCIÓ
    #-------------------------------------------------------------
    def EsSeleccionada(self,idr):
        return self.dr[idr].seleccionada
    #-------------------------------------------------------------
    def HiHaSeleccionades(self):    # indica si hi ha com a mínim una ruta seleccionada
        c=0
        for k in self.dr:
            if self.dr[k].seleccionada:
                c+=1
        return c>0        
    #-------------------------------------------------------------
    def UnaSeleccionada(self):      # retorna la ruta seleccionada
        rs=[]       # llista de rutes seleccionades
        for kr in self.dr:
            if self.dr[kr].seleccionada:
                rs.append(kr)
        if len(rs)!=1:
            return -1       # no hi ha 1 ruta seleccionada
        return rs[0]
    #-------------------------------------------------------------
    def DuesSeleccionades(self):    # retorna les dues rutes seleccionades
        rs=[]       # llista de rutes seleccionades
        for kr in self.dr:
            if self.dr[kr].seleccionada:
                rs.append(kr)
        if len(rs)!=2:
            return -1,-1    # no hi ha 2 rutes seleccionades
        return rs[0],rs[1]
        
    #-----------------------------------------------------------------
    # SETTERS
    #-----------------------------------------------------------------
    def SetColorLinia(self,idr,color):
        self.dr[idr].colorLinia=color
    #-----------------------------------------------------------------
    def SetColorPunts(self,idr,color):
        self.dr[idr].colorPunts=color
    #-----------------------------------------------------------------
    def SetVisibilitat(self,idr,visible):
        self.dr[idr].visible=visible
    #-----------------------------------------------------------------
    def SetSeleccio(self,idr,seleccio):
        self.dr[idr].seleccionada=seleccio
    #-------------------------------------------------------------
    def ToggleSeleccio(self,estat):
        for kr in self.dr:
            self.dr[kr].seleccionada=estat

    #-----------------------------------------------------------------
    # MARCATS
    #-------------------------------------------------------------
    def HiHaMarcats(self):
        return len(self.marcats)>0
    #-------------------------------------------------------------
    def NumMarcatsRuta(self,idr):
        if idr in self.marcats:
            return len(self.marcats[idr])
        else:
            return 0
    #-----------------------------------------------------------------
    def MarcarAlternat(self,idr,ip):    # marca o desmarca, segons si el punt hi era o no
        if idr in self.marcats: # hi ha ruta
            if ip in self.marcats[idr]:
                self.marcats[idr].remove(ip)    # ja hi ha el punt: el treiem
            else:
                self.marcats[idr].append(ip)    # no hi ha el punt: l'afegim
                self.marcats[idr].sort()        # els posem en ordre!
        else:   # no hi ha la ruta: afegim ruta i punt
            self.marcats[idr]=[ip]
    #-----------------------------------------------------------------
    def MarcarSegment(self,idr):
        # marquem tots els punts entre el primer i l'últim
        # ja hem controlat que n'hi hagi un mínim de dos

        dm=self.marcats[idr]
        ip1=dm[0]    # primer marcat
        ip2=dm[-1]   # últim marcat

        for ip in range(ip1,ip2+1): # afegeixo els punts entre el primer i l'últim...
            if ip not in dm:        # ...si és que ja no hi eren...
                dm.append(ip)
        dm.sort()                   # ...i al final ordenem
    #-----------------------------------------------------------------
    def Desmarcar(self):
        for kr in self.dr:                  # iterem per totes les rutes
            if self.dr[kr].seleccionada:    # però ens fixem només en les seleccionades
                if kr in self.marcats:      # si tenen algun marcat...
                    del self.marcats[kr]    # ...eliminem l'entrada de la ruta de marcats
                    
    #-------------------------------------------------------------
    def EliminarPunts(self):
        for kr in self.dr:                  # iterem per totes les rutes
            if self.dr[kr].seleccionada:    # però ens fixem només en les seleccionades
                if kr in self.marcats:      # si tenen algun marcat
                    lp=self.marcats[kr][:]
                    lp.reverse()            # llista inversa d'índexs de punts
                    for ip in lp:           # esborrant a l'inrevés, els índexs no canvien
                        del self.dr[kr].lp[ip]
        self.Desmarcar()                    # reset dels marcats


    #-----------------------------------------------------------------
    # ALTRES
    #-----------------------------------------------------------------
    def BoundingBoxRutes(self):
        self.win=[1e12,0,1e12,0]
        for kr in self.dr:
            w=self.dr[kr].BoundingBoxRuta()
            self.Superconjunt(w)
    #-----------------------------------------------------------------
    # guarda a self.win la BB contenidora de self.win i w
    def Superconjunt(self,w):
        if w[0]<self.win[0]:
            self.win[0]=w[0]
        if w[1]>self.win[1]:
            self.win[1]=w[1]
        if w[2]<self.win[2]:
            self.win[2]=w[2]
        if w[3]>self.win[3]:
            self.win[3]=w[3]
    #-----------------------------------------------------------------
    def AjustarAR(self):
        # ajustem els aspect ratios de la window i el viewport
        dx=self.win[1]-self.win[0]
        dy=self.win[3]-self.win[2]
        if dx>dy:   # disposició apaisada de les rutes
            dif2=(dx-dy)/2
            self.win[2]-=dif2
            self.win[3]+=dif2
        else:       # disposició retrat de les rutes
            dif2=(dy-dx)/2
            self.win[0]-=dif2
            self.win[1]+=dif2
            
#-----------------------------------------------------------------
if __name__=="__main__":
    main()
#-----------------------------------------------------------------
    
