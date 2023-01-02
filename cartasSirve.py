from ast import Global
from pickle import FALSE
from sys import builtin_module_names
from PIL import Image, ImageTk
from  itertools import combinations
import random
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno
import tkinter as tk
import logging
import os
import time
import clases as cl

class Juegos:
    def __init__(self):
    
        self.current_player = 'jug'
        self.ronda = 1

    def flip_player(self):
        if self.current_player == 'bot':
            self.current_player = 'jug'
        elif self.current_player == 'jug':
            self.current_player = 'bot'

    def sigue_juego(self):
        if len(objCartasJug.cartasJug) >0 and len(objCartasCasa.cartasCasa) >0:        
            return True
        else:
            return False    

class Baraja(cl.Cartas): 

    def __init__(self): 
        cl.Cartas.__init__(self) 
        self.baraja = [] 
        self.orden = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k' , 'A')   
        for p in cl.palos:
            for v in cl.valores:
                #       0  1   2                3                                                             
                carta = (v,p,"img/rojo.png", "img/"+v+" "+p+".png")
                self.baraja.append(carta)
                carta = (v,p,"img/azul.png", "img/"+v+" "+p+".png")
                self.baraja.append(carta)
        for i in range(2):        
            carta = ("Joker","","img/rojo.png", "img/joker.png")
            self.baraja.append(carta)
            carta = ("Joker","","img/azul.png", "img/joker.png")
            self.baraja.append(carta)
        
    def barajar(self): 
        random.shuffle(self.baraja) 
        return self.baraja 

    def tomarCarta(self): 
        if len(self.baraja) == 0: 
            return "No quedan cartas para repartir"
        else: 
            carta_tomada = self.baraja.pop(0)
            return (carta_tomada) 
            
    def repartir(self,cp):
        global cartasCasa, cartasJug, objMesa
        objCartasCasa.cartasCasa = []
        objCartasJug.cartasJug = []
        for num in range(9):
            carta_casa = self.tomarCarta() 
            objCartasCasa.cartasCasa.append(carta_casa)
            #se muestra el reverso de la carta para el juego de cartas de la casa
            bot_casa[num].change_image(carta_casa[2])
            carta_jug = self.tomarCarta()
            objCartasJug.cartasJug.append(carta_jug)
            #se muestra el anverso de la carta para el juego de cartas de la casa
            bot_jug[num].change_image(carta_jug[3])
        #indico que sera la primera jugada, para q la casa organice su juego
        objCartasCasa.jugada = 1    
        carta_mesa = self.tomarCarta()
        objMesa.cartasMesa.append(carta_mesa)
        agregar("En repartir Cartas Casa")
        agregar(str(objCartasCasa.cartasCasa))
        agregar("En repartir Cartas Jugador")
        agregar(str(objCartasJug.cartasJug))
        agregar("Carta mesa")
        agregar(str(carta_mesa))
        #se muestra el anverso de la carta para la carta de la mesa
        btnmesa.change_image(carta_mesa[3])
        resto.change_image(self.baraja[0][2])
        agregar("Carta a robar, primera del mazo")
        agregar(str(self.baraja[0]))

        if cp == 'jug':
            actualizar_mensaje("Es tu turno!\n Ordena tus cartas, haciendo click en una carta y moviendola con los botones \nAtras y Adelante y cuando estes listo toma una carta del mazo o de la mesa")
        else:
            actualizar_mensaje("Juega el bot")
            time.sleep(1)            
            objCartasCasa.jugar()

class Mesa(): 
    def __init__(self): 
        self.cartasMesa = [] 
        self.tricas=[]
        self.escaleras =[]
        self.sopar_escaleras = []
        self.ultTrica = 0
        self.ultEsca = 1
    
    def esCorrida(self,order_list):
        agregar("en es corrida lista es")
        agregar(str(order_list))
        for i in range(len(order_list)-1) :
            if ((order_list[i][1]+1) != (order_list[i+1][1])) :
                return i+1
        return -1  

    def ordenar(self,lista):
        agregar("lista en ordenar")
        agregar(str(lista))
        hay_jok = False
        hay_jok_rojo = False
        hay_jok_azul = False
        if ('Joker', '', 'img/rojo.png', 'img/joker.png') in lista:
            agregar("en ordenar elimino joker rojo")
            hay_jok_rojo = True
            lista.remove(('Joker', '', 'img/rojo.png', 'img/joker.png'))
            jok = ('Joker', '', 'img/rojo.png', 'img/joker.png')
        elif ('Joker', '', 'img/azul.png', 'img/joker.png') in lista:
            agregar("en ordenar elimino joker azul")
            hay_jok_azul = True
            lista.remove(('Joker', '', 'img/azul.png', 'img/joker.png'))
            jok = ('Joker', '', 'img/azul.png', 'img/joker.png')
        elif [('Joker', '', 'img/joker.png')] in lista:
            agregar("en ordenar elimino joker sin color")
            hay_jok = True    
            lista.remove([('Joker', '', 'img/joker.png')])
            jok = ('Joker', '', 'img/joker.png')
        elif ('Joker', '', 'img/joker.png') in lista:
            agregar("en ordenar elimino joker sin color solo tupla")
            hay_jok = True    
            lista.remove(('Joker', '', 'img/joker.png'))
            jok = ('Joker', '', 'img/joker.png')  
        if hay_jok_rojo or hay_jok_azul:
            hay_jok = True 
        lis = sorted(lista, key=lambda carta: carta[-1])                
        lugar = self.esCorrida(lis)
        if hay_jok:
            if lugar == -1: #esta ordenada 
                max = lis[-1][1]
                lis.append([jok,max+1])
            else:
                ind = lis[lugar][1]
                lis.insert(lugar,[jok,ind-1])    
        return lis

    def revisar_faltantes(self, de_donde, a_donde):
        #reviso en posibles escaleras
        i = 0
        falta1 =[]
        falta2 =[]
        
        detalle("En revisar faltantes de_donde es")
        detalle(str(de_donde))
        for e in de_donde:
            detalle("e es " + str(e))
            min = objBaraja.orden.index(e[0][0][0])
            detalle("min es "+ str(min))
            try:
                max = objBaraja.orden.index(e[-1][0][0]) 
            except ValueError:
                max = objBaraja.orden.index(e[-2][0][0])     
            detalle("max es "+ str(max)) 
            if e[0][0][1] == '':
                #es joker
                palo = e[1][0][1]
            else:    
                palo = e[0][0][1]
            if max == 0:
                max = 13
            detalle("a es corrida va con  " + str(e))    
            if len(e) == 2 and max-min == 1:
                corri = -1
            else:    
                corri = self.esCorrida(e) 
            if corri == -1:
                detalle("es corrida")
                if min == 0: #Es A al inicio    
                    falta1 = [objBaraja.orden[max+1],palo,i, max+1]
                elif max ==13: #es A al final
                    falta1 = [objBaraja.orden[min-1],palo,i, min-1]
                else:
                    falta1 = [objBaraja.orden[max+1],palo,i, max+1]       
                    falta2 = [objBaraja.orden[min-1],palo,i, min-1]
            else: #falta la carta del medio
                detalle("falta la carta del medio")
                falta1 = [objBaraja.orden[min+corri],palo,i,min+corri]       
            i+=1
            detalle("falta 1 es " + str(falta1))
            a_donde.append(falta1)
            detalle("falta_esca es lego del append 1" + str(a_donde))
            if falta2 != []:
                detalle("falta 2 es " + str(falta2))
                a_donde.append(falta2)
                detalle("falta_esca es luego del appensd 2" + str(a_donde))
                falta2 = []
            detalle("falta_esca es " + str(a_donde))

    def puntaje(self, quien):
        if quien == 'BOT':
            actualizar_mensaje("El bot gano la partida. Para continuar jugando presiona el boton Reiniciar")
            valor = int(pts_bot.cget("text"))
            valor =+1 
            pts_bot.config(text=valor)        
        else:    
            actualizar_mensaje("Ganaste la partida. Para continuar jugando presiona el boton Reiniciar")
            valor = int(pts_jug.cget("text"))
            valor =+1 
            pts_jug.config(text=valor)
        time.sleep(1)    

    def tomarCarta(self): 
        if len(self.cartasMesa) == 0: 
            return "No quedan cartas para tomar"
        else: 
            carta_robada = self.cartasMesa.pop()
            return (carta_robada) 

    def pintar_trica(self,lista):
        i = objMesa.ultTrica
        objMesa.tricas.append(lista)
        for t in lista:
            if len(t)==3:
                bot_trica[i].change_image(t[2])
            else:    
                bot_trica[i].change_image(t[3])
            i+=1
        objMesa.ultTrica = i
            
    def pintar_esca(self,lista, cual):
        """Funcion que solo pinta la escalera dponde corresponde
        ordena la lista antes de pintar, inclusive la ordena si tiene joker"""
        agregar("en pintar esca llrga esta lista" + str(lista))
        ordered = self.ordenar(lista)
        agregar("en pintar esca con escalera ordenada" + str(ordered))
        objMesa.escaleras.append(ordered)
        i=0
        for esc in ordered:
            #for t in esc:
            if cual == 1:
                if len(esc[0])==3:
                    bot_esca1[i].change_image(esc[0][2])
                else:
                    bot_esca1[i].change_image(esc[0][3])    
            elif cual == 2:
                if len(esc[0])==3:
                    bot_esca2[i].change_image(esc[0][2])
                else:
                    bot_esca2[i].change_image(esc[0][3])    
            elif cual == 3:
                if len(esc[0])==3:
                    bot_esca3[i].change_image(esc[0][2])
                else:
                    bot_esca3[i].change_image(esc[0][3])    
            else:
                if len(esc[0])==3:
                    bot_esca4[i].change_image(esc[0][2])
                else:
                    bot_esca4[i].change_image(esc[0][3])    
            i+=1
        self.ultEsca += 1        
        agregar("al salir de pintar la escalera ordenada es" + str(ordered))

    def grisar_todo(self):
        btnmesa.change_image("img/gris.png")
        for i in range(10):
            bot_casa[i].change_image("img/gris.png")
            bot_jug[i].change_image("img/gris.png")
        for i in range(18):
            bot_trica[i].change_image("img/fondo.png")
        for i in range(5):
            bot_esca1[i].change_image("img/fondo.png")
            bot_esca2[i].change_image("img/fondo.png")
            bot_esca3[i].change_image("img/fondo.png")
            bot_esca4[i].change_image("img/fondo.png")
    
    def no_tiene_joker(self):
        for esc in objMesa.escaleras:
            jok = False
            agregar("en no tiene joker escalera es " + str(esc))
            for e in esc:
                if e[0][0] == 'Joker':
                    jok = True
            if jok == False:
                agregar("devuelco esta escalera " + str(esc))
                return esc  
        return []          

    def puedo_aumentar(self,esca,carta,lis_jok, escaleras):
        agregar("en puedo aumentar esca es" + str(esca))
        agregar("carta es" + str(carta))
        puedo = False
        posible = False
        esc_modif = []
        mas_valores = []
        if carta[0]== 'Joker':
            if self.no_tiene_joker()==[]: 
                return []
        else:    
            for e in esca:
                if e[0] == carta[0] and e[1] == carta[1]:
                    ind = e[2]
                    lugar = e[3]
                    agregar("e if es " + str(e))
                    esc_modif = escaleras[e[2]]
                    #print("esc modif es" + str(esc_modif))
                    #agregar("puedo sopar en")
                    #agregar(str(esc_modif))
                    puedo = True
                else:
                    if e[1] == carta[1]:       
                        esc_modif = escaleras[e[2]]                 
                        try:      
                            mas_valores.append([objBaraja.orden[e[3]+1],e[1],e[2],e[3]+1])
                        except:
                            None
                        try:    
                            mas_valores.append([objBaraja.orden[e[3]-1],e[1],e[2],e[3]-1])
                        except:
                            None    
                        posible = True    

            if puedo:    
                agregar("en puedo carta es " + str(carta))   
                #si e[2] que me indica en que escalera esta en la lista de jokers
                if ind in lis_jok:
                    agregar("en if de ind " + str(ind))
                    #agregar("la escalera original tenia joker")
                    #la escalera original tenia un joker
                    esc_modif.append([carta,lugar])
                    esc_modif.append(('Joker', '', 'img/joker.png'))
                    return esc_modif 
                else:    
                    agregar("en else de ind " + str(ind))
                    agregar("lis_jok es " + str(lis_jok))
                    agregar("esc modif antes es " + str(esc_modif))
                    #agregar("la escalera original no tenia joker")
                    esc_modif.append([carta,lugar])
                #agregar("esta es la escalera q devuelvo ")
                #agregar(str(esc_modif))   
                    return esc_modif
            elif posible:
                agregar("+++++mas valores es" + str(mas_valores))
                agregar("carta es" + str(carta))
                for v in mas_valores:
                    if v[0]==carta[0] and v[1]== carta[1]:                
                        #agregar("la escalera original tenia joker")
                        #la escalera original tenia un joker
                        esc_modif.append([(carta[0],carta[1],carta[3]),v[3]])
                        esc_modif.append(('Joker', '', 'img/joker.png'))
                        return esc_modif 
                else:    
                    return []
            else:    
                return []    

    def re_pintar_esca(self,lista):
        agregar("Lista en repintar es " + str(lista))
        agregar("en re pintar")
        agregar(str(lista[0]))
        agregar("cual esca es " + str(lista[1]))
        self.pintar_esca(lista[0],lista[1]+1)

    def evaluar_sope(self,carta):
        lis_joker = []
        i = 0
        nueva = []
        agregar("entre a evaluar sope")    
        agregar("tricas en mesa")
        agregar(str(objMesa.tricas))
        agregar("escaleras en mesa")
        agregar(str(objMesa.escaleras))    
        for esc in objMesa.escaleras:
            #print("esc es " + str(esc))
            tiene = False
            nu = []
            if esc[0][0][0]== 'Joker' or esc [-1][0][0] == 'Joker':
                tiene = True
            if tiene:
                for e in esc:
                    if e[0][0]== 'Joker':
                        lis_joker.append(i)
                    else:
                        nu.append(e)
            else:
                nu = esc            
            #print("#######nu es " + str(nu))        
            i+=1    
            nueva.append(nu)        
        agregar("nueva escalera en evaluar sope")
        agregar(str(objMesa.escaleras)) 
        agregar("lista joker es")
        agregar(str(lis_joker))       
        agregar("la carta es" +str(objCartasJug.cartasJug[carta]))
        self.revisar_faltantes(nueva,objMesa.sopar_escaleras)
        agregar("los faltanes en sope son " )
        agregar(str(objMesa.sopar_escaleras))
        if objCartasJug.cartasJug[carta][0]!= 'Joker':
            agregar("en if de no es joker")
            for t in objMesa.tricas:
                agregar("en for tricas la carta es" + str(objCartasJug.cartasJug[carta]))
                agregar("en for tricas t es" + str(t))
                if t[0]==objCartasJug.cartasJug[carta][0] and t[1]==objCartasJug.cartasJug[carta][1]:
                    return ["trica",[]]
        esca = objMesa.puedo_aumentar(objMesa.sopar_escaleras,objCartasJug.cartasJug[carta],lis_joker, nueva)
        if len(esca)>0:
            return ["escalera",esca]
        else:
            agregar("no hay escaleras para sopar")    
            return ["nada", []]                
        

class JuegoCasa(cl.Basicos):
    def __init__(self): 
        self.posibles_tri = []
        self.posibles_esca = []
        self.falta_tri = []
        self.falta_esca = []
        #self.falta_esca_jok = []
        self.descarte = []
        self.descarte_pri = []
        self.cartasCasa = []
        self.simplificada = []
        self.tricas =[]
        self.escaleras = []
        self.joker =[]
        #self.boto = False
        #self.jugada = 0

    def simplificar(self):
        l=[]
        for c in self.cartasCasa:
            l.append((c[0],c[1],c[3]))
        return l

    def inicio(self,lista):
        for l in lista:
            if l[0][0] == 'A':
                return True
            else:#hay k o q
                return False        
            
    def jugar(self):
        # debe organizar sus cartas al inicio y luego de bajar un juego
        if objJuego.ronda ==1:
            self.simplificada = self.simplificar()
            agregar("Cartas Casa en Jugar en 1ra ronda")
            agregar(str(self.cartasCasa))
            agregar("Cartas simplificada en 1ra ronda")
            agregar(str(self.simplificada))
            self.descarte_pri = self.carta_duplicada()
            agregar("Desacrte cartas duplicadas en jugar en 1ra ronda")
            agregar(str(self.descarte_pri))
            for d in self.descarte_pri:
                #el = (d[0],d[1],d[2])
                self.simplificada.remove(d)
                #for c in self.cartasCasa:
                    #if d[0]==c[0] and d[1]==c[1]:
                        #self.cartasCasa.remove(c)
            #agregar("luego de descarte de duplicados cartas casa es")
            #agregar(str(self.cartasCasa)) 
        #agregar("simplificada antes de armar juego")           
        #agregar(str(self.simplificar))
        self.armar_juego()
        agregar("Juega la casa, tomara una carta")
        #debe validar si toma la carta de la mesa o la carta del mazo segun su juego
        self.tomar_carta()
        
    def bajar_armadas(self):
        baje = False
        #si hay tricas hechas las bajo
        #agregar("entre a bajar_armadas")
        if len(self.tricas) > 0:
            self.bajar_trica(-1,None)
            #agregar("Bajo tricas armadas")
            #agregar("Luego de bajar cartas casa es")
            #agregar(str(self.cartasCasa))
            baje = True
        if len(self.escaleras) > 0:
            #agregar("bajare estas escaleras armada")
            #agregar(str(self.escaleras))
            #agregar("LLamo a bajar_esca 4")
            self.bajar_esca(-1,-1 )
            baje = True
        if len(self.posibles_esca) > 0 and len(self.joker)>0:
            #agregar("bajare esta escalera con un joker q tengo")
            #agregar(str(self.posibles_esca))
            #agregar("LLamo a bajar_esca 5")
            self.bajar_esca(0,self.joker[0])
            baje = True      
        if baje: 
            agregar("Baje un juego armado")       
            self.grisar()    
            self.limpiar_listas()
            #vuelvo a rearmar con las cartas que quedan
            self.armar_juego()  
        #agregar("sali de bajar armadas")
        #agregar("cartas casa es luego de salir "+ str(self.cartasCasa))            

    def solo_esc(self):
        res = []
        for e in self.posibles_esca:
            for x in e:
                res.append(x[0])
        return(res)   

    def armar_descarte(self):
        #agregar("en armar descarte cartas_casa es")
        #agregar(str(self.cartasCasa))
        lista = []
        #si ya habian cartas en descarte
        if len(self.posibles_esca) > 0: lista += self.posibles_esca
        if len(self.posibles_tri) > 0: lista += self.posibles_tri
        if len(self.joker) > 0: lista += self.joker
        if len(self.escaleras) > 0: lista += self.escaleras
        if len(self.tricas) > 0: lista += self.tricas
        #si ya habian cartas en descarte las pongp al fonal para que se descarte de ahi
        if len(self.descarte) >0: lista += self.descarte
        #agregar("Lista que va a aplanar es")
        #agregar(str(lista))
        sirven = self.aplanar(lista)
        self.descarte = list(set(self.simplificada) - sirven)
        agregar("Arme descarte con estas cartas")
        agregar(str(self.descarte)) 
        
    def armar_par_esca(self):
        if ('Joker', '', 'img/joker.png') in self.simplificada:
            agregar("hay un joker entre las ultimas tres")
            for s in self.simplificada:
                if s[0] != 'Joker':
                    ind_carta = objBaraja.orden.index(s[0])
                    agregar("ind es " + str(ind_carta))
                    if ind_carta == 0:#es la A 
                        posi = [[[s,ind_carta],[('Joker', '', 'img/joker.png'),1]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),2]], [[s,13],[('Joker', '', 'img/joker.png'),12]],  [[s,13],[('Joker', '', 'img/joker.png'),11]] ]
                    elif ind_carta == 1: #es el 2
                        posi = [[[s,ind_carta],[('Joker', '', 'img/joker.png'),0]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),2]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),4]]]
                    elif ind_carta ==12: #es la k
                        posi = [[[s,ind_carta],[('Joker', '', 'img/joker.png'),13]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),10]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),11]]]
                    else:
                        posi = [[[s,ind_carta],[('Joker', '', 'img/joker.png'),ind_carta + 1]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),ind_carta + 2]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),ind_carta - 1]], [[s,ind_carta],[('Joker', '', 'img/joker.png'),ind_carta - 2]]]
                    return {'Posibles':posi, 'Escaleras':[]}

    def carta_duplicada(self):
        #revisa si hay una carta duplicada, si la hay la prepara para el descarte
        res = list(set([ele for ele in self.simplificada if self.simplificada.count(ele) > 1]))
        lista = []
        for r in res:
            #solo elimino las duplicadas q no sean joker
            if r[0] != "Joker":
                lista.append(r)
        return lista

    def elim_cartas_de_trica(self):
        for tri in self.tricas:
            for t in tri: 
                self.simplificada.remove(t)

    def sopar(self):
        agregar("en sopar casa")    
        juego = objMesa.evaluar_sope(carta_jug)                
        if juego[0]=="trica":
            self.grisar()                                  
            agregar("Cartas de la mes luego de sopar la trica")
            agregar(str(self.cartasCasa))
            agregar("despues de sopar tricas objMesa.tricas es")
            agregar(str(objMesa.tricas))
            self.botar("descarte",0)
        elif juego[0]=="escalera": #es escalera
            lista = juego[1]            
            agregar("cartasJug en sopar escalera es")
            agregar(str(self.cartasCasa))
            objMesa.re_pintar_esca(lista)                                                                                    
            self.grisar()      
            agregar("despues de sopar escalera las escarelas de la mesa")
            agregar(str(objMesa.escaleras))                                            
            self.botar("descarte",0)

    def armar_juego(self):
        """revisa carta por carta tratando de armar tricas o escaleras las cuales ira colocando en
        self.posibles_tricas y self.posibles_esca = []
        y si encuentra juegos armados ira colocando los juegos en self.tricas y self.escaleras
        tambien arma las cartas de descarte"""
        agregar("En armar juego simplificada es ")
        agregar(str(self.simplificada))
        if len(self.simplificada)==0:
            self.simplificada = self.simplificar()
        if len(self.simplificada) == 3 and ('Joker', '', 'img/joker.png') in self.simplificada:
            result = self.armar_par_esca()    
        else:    
            result = self.posibles_escaleras()        
        #agregar("result es " + str(result) + " " + str(len(result)))
        self.posibles_esca = result['Posibles']
        #agregar("posibles esca es " + str(self.posibles_esca))
        self.escaleras = result["Escaleras"]
        #agregar("escaleras es " + str(self.escaleras))
        agregar("En armar juego escaleras  es")
        agregar(str(self.escaleras))   
        agregar("En armar juego posibles_esca  es")
        agregar(str(self.posibles_esca))                        
        objMesa.revisar_faltantes(self.posibles_esca,self.falta_esca)
        agregar("en Armar Juego Cartas Faltantes para escaleras es")
        agregar(str(self.falta_esca))
        self.posibles_tri = self.posibles_tricas()
        
        for t in self.posibles_tri:
            if len(t) == 3:
                if t[0][1] == t[1][1]:
                    t.pop(1)
                    agregar("t luego de eliminar duplicada " + str(t))
                elif t[0][1] == t[2][1] or t[1][1] == t[2][1]: 
                    agregar("Hay tres cartas, dos con el mismo palo")   
                    t.pop(2)    
                    agregar("t luego de eliminar duplicada " + str(t))
                else:    
                    self.tricas.append(t)
                    self.posibles_tri.remove(t)
                #bajar trica
            elif len(t) == 4:
                #si hay 4 cartas para formar la trica, desecho una y me quedo con 3
                agregar("tengo una trica de 4")
                agregar("FALTA VER SI ALGUNA CARTA FORMA PARTE DE UNA ESCALERA")
                t.pop(-1)
                self.tricas.append(t)
                #self.posibles_tri.remove(t)
        for t in self.tricas:
            if t in self.posibles_tri:
                self.posibles_tri.remove(t)                    
        agregar("En armar juego Posibles Tricas es")
        agregar(str(self.posibles_tri))        
        agregar("En armar juego Tricas es")
        agregar(str(self.tricas))
        #hasta aca arme posibles tricas y tricas
        #self.elim_cartas_de_trica() ver si hay q eliminar 
        #vuelvo a armar la lista de simplificadas
        #agregar("Cartas casa despues de armar juego")
        #agregar(str(self.cartasCasa))
        agregar("simplificada despues de armar juego")
        agregar(str(self.simplificada))
        # de la simplificada elimino las cartas de tricas armadas
        self.armar_descarte()  
        
    def tomar_basura(self):   
        carta = objMesa.tomarCarta()
        self.cartasCasa.append(carta)
        #messagebox.showinfo(title="Loba 1.0", message="la carta que tome de la mesa es " + str(carta))
        agregar("Carta que tome de la mesa")
        agregar(str(self.cartasCasa[-1]))
        agregar("luego de tomar cartas casa es")
        agregar(str(self.cartasCasa))
        #####OJOA NO SIEMORE VA SER EL 9######
        bot_casa[-1].change_image(carta[3])
        if len(objMesa.cartasMesa) == 0:
            #tomo la unica carta de la mesa
            btnmesa.change_image("img/gris.png")
        else:
            #agregar("la anterior carta de la mesa es")
            #agregar(str(objMesa.cartasMesa[-1]))
            btnmesa.change_image(objMesa.cartasMesa[-1][3])

    def elim_joker(self, lista):
        for l in lista:
            if l[0][0]== "Joker":
                lista.remove(l)
                    
    def analizar_juego(self):
        ult_carta = self.cartasCasa[-1]
        valor = ult_carta[0]
        palo = ult_carta[1]
        agregar("Entre a analizar juego con " + str(ult_carta))
        agregar("cartas casa en analizar juego " +str(self.cartasCasa))
        #evaluo en tricas
        i=0
        for p in self.posibles_tri:
            #si es del mismo valor
            if p[0][0]== valor: 
                if palo != p[0][1] and palo != p[1][1]:
                    agregar("Bajo trica con la carta que tome")
                    agregar(str(ult_carta))
                    self.bajar_trica(i,ult_carta)
                    break
            i+=1        
        #evaluo escaleras
        for f in self.falta_esca:
            if f[0]==valor and f[1]==palo:
                agregar("LLamo a bajar_esca 1")
                self.bajar_esca(f[2],ult_carta)
                break
                #ya_baje = True
        if valor == 'Joker' and len(self.posibles_esca) > 1:
            #si hay al menos una posible escalera y tehgo un joker
            agregar("LLamo a bajar_esca 2")
            self.bajar_esca(0,ult_carta)
            #ya_baje = True
        #agregar("Sali de analizar juego ")
        #agregar("cartas casa en analizar juego " +str(self.cartasCasa))           

    def par_trica(self,carta):
        agregar("Entre a par trica con " + str(carta))
        agregar("descarte en par trica es ")
        agregar(str(self.descarte))
        if len(self.descarte) == 0 and len(self.posibles_esca) == 0:
            return False
        for p in self.descarte:
            #si es del mismo valor
            if p[0]== carta[0]: 
                if carta[1] != p[1]:
                    posi = [(p[0],p[1],p[2]),(carta[0],carta[1],carta[3])]
                    self.posibles_tri.append(posi)
                    self.descarte.remove(p)
                    agregar("en par trica devuelvo true") 
                    agregar(str(posi))               
                    return True
        for esc in self.posibles_esca:
            for e in esc:
                if e[0][0]== carta[0]: 
                    if carta[1] != e[1]:
                        posi = [(e[0][0],e[0][1],e[0][2]),(carta[0],carta[1],carta[3])]
                        self.posibles_tri.append(posi)
                        agregar("en par esca devuelvo true")
                        agregar(str(posi))                
                        return True
        agregar("en par trica devuelvo false")                
        return False

    def par_esca(self,donde,carta):
        agregar("par esca con "+ str(donde))
        agregar("Entre a par esca con " + str(carta))
        agregar("descarte en par esca es ")
        agregar(str(self.descarte))
        arme = False
        posi = []
        for d in donde:
            #si es del mismo palo
            if d[1]== carta[1]:
                ind_carta = objBaraja.orden.index(carta[0])
                ind_p = objBaraja.orden.index(d[0])
                if ind_carta == 1:#es el 2 
                    if ind_p == ind_carta+1 or ind_p == ind_carta+2 or ind_p == ind_carta-1:
                        posi = [[(d[0],d[1],d[2]),ind_p],[(carta[0],carta[1],carta[3]),ind_carta]]
                        arme = True
                elif ind_carta == 12: #es la K  
                    if ind_p == 0: #si la otra carta es A y tiene valor 0
                        ind_p = 13       
                        if ind_carta == ind_p+1 or ind_carta == ind_p-2 or ind_carta == ind_p-1:
                            posi = [[(d[0],d[1],d[2]),ind_p],[(carta[0],carta[1],carta[3]),ind_carta]]
                            arme = True
                    else:  
                        if ind_p == ind_carta-1 or ind_p == ind_carta-2 or ind_p == ind_carta+1 or ind_p== ind_carta+2:
                            posi = [[(d[0],d[1],d[2]),ind_p],[(carta[0],carta[1],carta[3]),ind_carta]]
                            arme = True   
                elif ind_carta ==0: #es la A
                    if ind_p == 12 or ind_p == 11:# es la k o q
                        ind_carta = 13
                        if ind_carta == ind_p+1 or ind_carta == ind_p+2:
                            posi = [[(d[0],d[1],d[2]),ind_p],[(carta[0],carta[1],carta[3]),ind_carta]]
                            arme = True
                    elif ind_p == 1 or ind_p == 2:# es el 2 o 3
                        if ind_carta == ind_p-1 or ind_carta == ind_p-2:
                            posi = [[(d[0],d[1],d[2]),ind_p],[(carta[0],carta[1],carta[3]),ind_carta]]
                            arme = True        
                else:
                    if ind_p == ind_carta-1 or ind_p == ind_carta-2 or ind_p == ind_carta+1 or ind_p== ind_carta+2:        
                        posi = [[(d[0],d[1],d[2]),ind_p],[(carta[0],carta[1],carta[3]),ind_carta]]
                        arme = True
            if arme == True: 
                self.posibles_esca.append(posi)
            if donde == self.descarte and arme:    
                self.descarte.remove(d)
            agregar("en par esca decuelvo "+str(arme))    
        return arme

    def me_sirve(self, carta):
        agregar("************Veo si me sirve esta carta*******")
        agregar(str(carta))
        #if len(self.descarte) in (0,1):
        if carta[0] == 'Joker':
            agregar("La carta es joker")
            agregar("posibles esca es " + str(self.posibles_esca))
            if len(self.posibles_esca)>0:
                agregar("tengo escalera y la bajo con el joker q me toco")
                self.bajar_esca(0,carta)   
            return True
        else:
            li = self.sirve_para_bajar(carta)
            juego = li[0]
            indice = li[1]
            if juego in ("trica","escalera"):
                agregar("la carta que robe me sirve para bajar")
                self.bajar_juego(juego,indice,carta)
            else:
                agregar("la carta que robe no me sirve para bajar")
                agregar("antes de revisar tengo esto")
                agregar("posibles escaleras " + str(self.posibles_esca))
                agregar("posibles tricas " + str(self.posibles_tri))
                agregar("descarte " + str(self.descarte))
                return self.par_esca(self.descarte,carta) or  self.par_trica(carta) or self.par_esca(self.aplanar(self.posibles_tri),carta)
                #si es una carta igual a las que tengo la elimino
                
    def botar_casa(self, carta):
        ultima = self.cartasCasa[carta]
        #boto la ultima carta que acabo te tomar    
        btnmesa.change_image(ultima[3])
        objMesa.cartasMesa.append(self.cartasCasa[carta])
        self.cartasCasa.remove(ultima)
        agregar("Descarto la carta que acabo de tomar")
        agregar(str(ultima))
        agregar("Cartas casa es")
        agregar(str(self.cartasCasa))
        #bot_casa[carta].change_image("img/gris.png")
        #Ya boto en esta ronda

    def eliminar_de_casa(self,ultima):
        agregar("descarto esta carta de cartas_casa")
        agregar(str(ultima))
        t_rojo = (ultima[0],ultima[1],'img/rojo.png',ultima[2])
        t_azul = (ultima[0],ultima[1],'img/azul.png',ultima[2] )
        try:
            ind = self.cartasCasa.index(t_rojo)
            objMesa.cartasMesa.append(t_rojo)
        except ValueError:
            ind = self.cartasCasa.index(t_azul)
            objMesa.cartasMesa.append(t_azul)
        self.cartasCasa.pop(ind)
        agregar("Cartas casa es luego de descartar")
        agregar(str(self.descarte))
            #agregar("cambiara esta imagne")
            #agregar(str(ultima[2]))
        btnmesa.change_image(ultima[2])

    def botar(self, donde, carta):
        global carta_jug, robo, bajo
        if donde == "descarte":
            agregar("len descarte pri es " + str(self.descarte_pri))
            if len(self.descarte_pri) > 0:
                ultima = self.descarte_pri[-1]
                self.descarte_pri.pop(-1)
                agregar("descarto esta carta de descarte_pri")
                agregar(str(ultima))
                self.eliminar_de_casa(ultima)
            else:    
                if len(self.descarte) == 0:
                    self.armar_descarte()
                if len(self.descarte) > 0: 
                    #agregar("elimino de descarte")
                    if self.descarte[-1][0] == 'Joker':
                        agregar("trato de eliminar un joker")
                        ultima = self.descarte[-2]
                        self.descarte.pop(-2)
                    else:
                        ultima = self.descarte[-1]
                        self.descarte.pop(-1)                        
                    self.eliminar_de_casa(ultima)    
                else:
                    self.botar_casa(carta)        
        else:
            self.botar_casa(carta)
        self.grisar()
        agregar("Al salir de botar simplificada es ")
        agregar(str(self.simplificada))
            #self.boto = True
        if objJuego.sigue_juego():
            carta_jug = -1
            robo = False
            bajo = False  
            self.boto = False  
            objJuego.current_player = 'jug'
            objCartasJug.cambiar_estado("active")
            #la siguiente ya no sera la primera jugada
            #self.jugada =1
            time.sleep(0.5)
            actualizar_mensaje("Es tu turno, toma una casa de la mesa o del mazo ")
            objJuego.ronda +=1
            
        else:
            objMesa.puntaje('BOT')

    def grisar(self):
        for i in range(10):
            bot_casa[i].change_image("img/gris.png")
        for i in range(len(self.cartasCasa)):
            bot_casa[i].change_image(self.cartasCasa[i][2])
            
    def bajar_trica(self,que_trica,con_que_carta):
        i = objMesa.ultTrica
        if que_trica == -1:
            for tri in self.tricas:
                objMesa.pintar_trica(tri)
                for t in tri:
                    #ubico la carta en cartasCasa
                    t_rojo = (t[0],t[1],'img/rojo.png',t[2])
                    t_azul = (t[0],t[1],'img/azul.png',t[2] )
                    try:
                        ind = self.cartasCasa.index(t_rojo)
                    except ValueError:
                        ind = self.cartasCasa.index(t_azul)
                    bot_casa[ind].change_image("img/gris.png")
                    self.cartasCasa.pop(ind)
                    #la trica armada ya fue eliminada
                    i+=1
        else:
            trc = []
            for p in self.posibles_tri[que_trica]:
                trc.append(p)
                #ubico la carta en cartasCasa
                p_rojo = (p[0],p[1],'img/rojo.png',p[2])
                p_azul = (p[0],p[1],'img/azul.png',p[2])
                try:
                    ind = self.cartasCasa.index(p_rojo)
                except ValueError:
                    ind = self.cartasCasa.index(p_azul)
                bot_casa[ind].change_image("img/gris.png")
                self.cartasCasa.pop(ind)
                i+=1
            #falta elimiar na carta del parametro con_que_carta  
            trc.append(con_que_carta)
            agregar("La trica que bajo es (en else bajar_trica)")
            agregar(str(trc))
            agregar("con esta carta")
            objMesa.pintar_trica(trc)
            ind_carta = self.cartasCasa.index(con_que_carta)
            agregar(str(con_que_carta))
            bot_casa[ind_carta].change_image("img/gris.png")
            self.cartasCasa.pop(ind_carta)
        #como me sirvio la de la mesa boto la de descarte
        #agregar("Luego de bajar la trica y antes de descartar la lista de descarte es")
        #agregar(str(self.descarte))    
        #self.botar("descarte",0)            
        self.grisar()    
        agregar("cartas luego de bajar la trica")
        agregar(str(self.cartasCasa))
        self.limpiar_listas()
        #vuelvo a rearmar con las cartas que quedan
        self.armar_juego()
            
    def limpiar_listas(self):   
        self.posibles_tri = []
        self.posibles_esca = []
        self.falta_tri = []
        self.falta_esca = []
        #self.falta_esca_jok = []
        self.descarte = []
        self.descarte_pri = []
        self.simplificada = []
        self.tricas =[]
        self.escaleras = []
        self.joker =[]
        #self.jugada = 0     

    def bajar_esca(self,que_esca,con_que_carta):
        """Funcion que:
        1. Si viene la escalera armada 
            Pinta la escalera
            Elimina las cartas de la escalera de cartas_casa
        2. Si no viene la escalera armanda
            agrega con_que_carta a que_esca
            Pinta la escalera
        grisa    
        limpia listas
        rearma el juego (armar_juego())
        """
        i = objMesa.ultEsca
        if que_esca == -1:
            #se bajan todas las escaleras que ya esten armadas 
            agregar("escaleras armadas en bajar_esca")
            agregar(str(self.escaleras))
            for esc in self.escaleras:
                agregar("bajo esta escalera en bajar_esca")
                agregar(str(esc))
                objMesa.pintar_esca(esc, objMesa.ultEsca)
                for e in esc:
                    agregar("cartas casa en for de eliminar en")
                    agregar(str(self.cartasCasa))
                    #ubico la carta en cartasCasa
                    t_rojo = (e[0][0],e[0][1],'img/rojo.png',e[0][2])
                    t_azul = (e[0][0],e[0][1],'img/azul.png',e[0][2])
                    try:
                        ind = self.cartasCasa.index(t_rojo)
                    except ValueError:
                        ind = self.cartasCasa.index(t_azul)
                    #elimino la carta de las cartas casa
                    self.cartasCasa.pop(ind)
            agregar("**************cartas casa luego de bajar_escalera armada*******")
            agregar(str(self.cartasCasa))
        else:
            agregar("en else, bajare esta escalera")
            agregar(str(que_esca))
            #agregar("posibles_esca cartas casa es")
            #agregar(str(self.cartasCasa))
            agregar("con que carta es")
            agregar(str(con_que_carta))
            escale = list(self.posibles_esca[que_esca])
            min = escale[0][1]
            agregar("min es "  + str(min))
            if min in (12,13):
                agregar("min es 12 0 13" )
                if con_que_carta[0] == 'Joker':
                    agregar("bajare con joker, lo pongo al inicio")
                    carta = [con_que_carta,min-1]
                else:        
                    carta = [con_que_carta,13]
                    agregar("en else la carta es " + str(carta))
                escale.append(carta)
                    #es una escalera con k o q
            else:
                if con_que_carta[0] != 'Joker':
                    carta = [con_que_carta,objBaraja.orden.index(con_que_carta[0])]    
                    escale.append(carta)
                else: 
                    agregar("agrego a escale un joker")
                    agregar(str(con_que_carta))   
                    escale.append(con_que_carta)
            #agregar("antes de pintar escale es")
            #agregar(str(escale))        
            agregar("escale es")
            agregar(str(escale))
            for p in escale:
                if len(p) == 2:
                    if len(p[0]) == 3:
                        agregar("la carta es simplificada " + str(p))
                        #ubico la carta en cartasCasa
                        p_rojo = (p[0][0],p[0][1],'img/rojo.png',p[0][2])
                        p_azul = (p[0][0],p[0][1],'img/azul.png',p[0][2])
                        try:
                            ind = self.cartasCasa.index(p_rojo)
                        except ValueError:
                            ind = self.cartasCasa.index(p_azul)
                        #bot_casa[ind].change_image("img/gris.png")
                    else:
                        agregar("La carta es completa " + str(p[0][0]) )
                        ind = self.cartasCasa.index(p[0])
                else:
                    if len(p) == 3:
                        agregar("la carta es simplificada " + str(p))
                        #ubico la carta en cartasCasa
                        p_rojo = (p[0],p[1],'img/rojo.png',p[2])
                        p_azul = (p[0],p[1],'img/azul.png',p[2])
                        try:
                            ind = self.cartasCasa.index(p_rojo)
                        except ValueError:
                            ind = self.cartasCasa.index(p_azul)
                        #bot_casa[ind].change_image("img/gris.png")
                    else:
                        agregar("La carta es completa " + str(p) )
                        ind = self.cartasCasa.index(p)
                self.cartasCasa.pop(ind)
            objMesa.pintar_esca(escale, objMesa.ultEsca)    
            agregar("**********cartas luego de bajar la escalera con ;a carta que tome*********")
            agregar(str(self.cartasCasa))
        self.grisar()    
        #self.botar("descarte",0)
        self.limpiar_listas()
        #vuelvo a rearmar con las cartas que quedan
        self.armar_juego()
        #eliminar las cartas de posibles FALTA
        
    def tomar_mazo(self):
        carta = objBaraja.tomarCarta()
        self.cartasCasa.append(carta)
        #messagebox.showinfo(title="Loba 1.0", message="tomo esta caerta del mazo" + str(carta))
        agregar("&&&&&&&&&Tomo esta carta del mazo&&&&&&")
        agregar(str(carta))
        #agregar("cartas casa es " + str(self.cartasCasa))
        bot_casa[-1].change_image(carta[2])
        self.analizar_juego()

    def bajar_juego(self,que_juego,ind, carta):
        """si ind es 0 and escalera bajo una escalera, que ya las tengo ordenadas
        sino, bajo una trica, la del indice"""
        if que_juego == "trica":
            self.bajar_trica(ind,carta)
        else:
            agregar("LLamo a bajar_esca 3") 
            agregar("ind es" + str(ind))
            self.bajar_esca(ind,carta)   
            
    def tomar_carta(self):   
        carta = objMesa.cartasMesa[-1]
        if len(self.cartasCasa) <=2:            
            sopar(carta)
        else:    
            #agregar("entre en tomar carta")             
            li = self.sirve_para_bajar(carta)
            juego = li[0]
            indice = li[1]
            if juego in ("trica","escalera"):
                #tomo la carta 
                agregar("Toma de la basura")
                self.tomar_basura()
                self.bajar_juego(juego,indice,carta)
                self.bajar_armadas()
                self.botar("descarte",0)
            else:
                agregar("Tomo una carta del mazo, no me sirvio la de la mesa")
                self.tomar_mazo()
                self.bajar_armadas()
                agregar("en analizar juego, no baje con la carta, veo si me sirve")
                if self.me_sirve(self.cartasCasa[-1]):
                    self.bajar_armadas()
                    #la carta me sirve, la conservo y tiro ina del descarte
                    self.botar("descarte",0)
                else:
                    #la carta no me sirve la tiro(es la ultioma de cartas casa)
                    #veo si es duplicada
                    carta = (carta[0],carta[1],carta[3])
                    if (carta) in self.simplificada:
                        self.simplificada.remove(carta)
                        self.descarte_pri.append(carta)
                        self.botar("descarte",0)
                    else:

                        self.botar("casa",-1)  
                    #no importa de donde tome la carta bajo lo que ya tengo armado
        agregar("sali de tomar carta y tire") 
        

    def sirve_para_bajar(self, carta):
        """Reviso si la carta me sirve en posibles tricas o posibles escaleras"""
        valor = carta[0]
        palo = carta[1]
        #imag = carta[3]
        agregar("en sirve mesa reviso si esta carta me sirve")
        agregar(str(carta))
        #evaluo en tricas para posible trica
        i = 0
        for p in self.posibles_tri:
            #si es del mismo valor
            if p[0][0]== valor: 
                agregar("palo es " + str(palo))
                agregar(str(p[0][1]))
                agregar(str(p[1][1]))
                if palo != p[0][1]:
                    if palo != p[1][1]:
                        return(["trica",i])
            i+=1
        #evalio escaleras
        #si la carta es joker y hay algua posible escalera
        if valor == 'Joker':
            agregar("La carta es joker")
            if len(self.posibles_esca)>0:
                agregar("La puedo usar en posibles esca")
                return(["escalera",0])  
            else:
                return(["nada",-1])
        else:
            agregar("reviso si esta en falta_esca")
            agregar(str(self.falta_esca))
            agregar("y mis posibles escaleras son")
            agregar(str(self.posibles_esca))
            agregar("y simplificada es")
            i == 0
            for e in self.falta_esca:
                if e[0] == valor and e[1] == palo:
                    #agregar("la escalera es i " + str(i))
                    #agregar("la escalera es e[2] " + str(e[2]))
                    return(["escalera", e[2]])  
                i+=1               
            return(["nada",-1]) 

    def posibles_tricas(self):    
        posibles = []
        ordenada = sorted(self.simplificada, key=lambda carta: carta[0])
        diferentes = set([x[0] for x in ordenada])
        for d in diferentes:
            result = list(filter(lambda x: (x[0] == d), ordenada))
            if len(result) >1:
                posibles.append(result)
        return(posibles)        

    def escaleritas(self,lista):
        elem = []
        esca = []
        final = []
        for i in range(len(lista)-1):
            elem.append(int(lista[i+1][1])-int((lista[i][1])))
        i = 0
        for e in elem:
            if e in (1,2):
                if lista[i] not in esca:
                    esca.append(lista[i])
                esca.append(lista[i+1])    
            else:
                if (len(esca))>0:
                    final.append(esca)
                    esca = []    
            i+=1    
        if len(esca)> 1:    
            final.append(esca)  
        if len(final)== 0:
            return([])
        else:        
            return(final[0])

    def posibles_escaleras(self):
        #escaleras
        posibles = []
        escaleras = []
        cora = []
        bastos = []
        tre_o = []
        rom_o = []
        cora_o = []
        bastos_o = []
        tre = []
        rom = []
        ases = []
        #joker =[]
        #en la lista Joker quedan todos los jokers y los elimino de somplificada
        agregar("******en posibles_escalesas simplificada es")
        agregar(str(self.simplificada))
        for s in self.simplificada:
            if s[0] == "Joker":
                self.joker.append(s)
            else:
                if s[0] == 'A':
                    ases.append(s)
                else:
                    ind = objBaraja.orden.index(s[0])
                    if s[1] == 'bas':
                        bastos.append([s,ind])
                    elif s[1] == 'cor':
                        cora.append([s,ind])
                    elif s[1] == 'tre':
                        tre.append([s,ind])
                    else: #rombo
                        rom.append([s,ind])
        if len(cora)> 0:
            cora_o = sorted(cora, key=lambda carta: carta[-1])                
        if len(bastos)> 0:
            bastos_o = sorted(bastos, key=lambda carta: carta[-1])                    
        if len(tre)> 0:
            tre_o = sorted(tre, key=lambda carta: carta[-1])                                
        if len(rom)> 0:
            rom_o = sorted(rom, key=lambda carta: carta[-1])  
        for a in ases:
            if a[1] == 'bas':
                if len(bastos_o)>0:
                    if bastos_o[0][1] in (1,2):#hay un dos o un tres
                        bastos_o.insert(0,[a,0])
                    elif bastos_o[-1][1] in (11,12):#hay una q o una k
                        bastos_o.append([a,13])
            elif a[1] == 'cor':
                if len(cora_o)>0:
                    if cora_o[0][1] in (1,2):#hay un dos o un tres
                        cora_o.insert(0,[a,0])
                    elif cora_o[-1][1] in (11,12):#hay una q o una k
                        cora_o.append([a,13])
            elif a[1] == 'tre':
                if len(tre_o)> 0:
                    if tre_o[0][1] in (1,2):#hay un dos o un tres
                        tre_o.insert(0,[a,0])
                    elif tre_o[-1][1] in (11,12):#hay una q o una k
                        tre_o.append([a,13])
            else: #rombo
                if len(rom_o)> 0:
                    if rom_o[0][1] in (1,2):#hay un dos o un tres
                        rom_o.insert(0,[a,0])
                    elif rom_o[-1][1] in (11,12):#hay una q o una k
                        rom_o.append([a,13])
        ases = []
        if len(cora_o)>1:
            cora = self.escaleritas(cora_o)
        if len(bastos_o)>1:
            bastos = self.escaleritas(bastos_o)
        if len(tre_o)> 1:
            tre = self.escaleritas(tre_o)
        if len(rom_o)> 1:
            rom = self.escaleritas(rom_o)
        #armo posibles    
        if len(cora)==2:
            posibles.append(cora)
        elif len(cora) > 2:
            com = self.combinatoria(cora)
            if self.faltan_esca(com) == 0:
                escaleras.append(com)
            else:
                posibles.append(com)
        if len(bastos)==2:
            posibles.append(bastos)
        elif len(bastos) > 2:
            com = self.combinatoria(bastos)
            if self.faltan_esca(com) == 0:
                escaleras.append(com)
            else:
                posibles.append(com)
        if len(tre)==2:
            posibles.append(tre)
        elif len(tre) > 2:
            com = self.combinatoria(tre)
            if self.faltan_esca(com) == 0:
                escaleras.append(com)
            else:
                posibles.append(com)
        if len(rom)==2:
            posibles.append(rom)
        elif len(rom) > 2:
            com = self.combinatoria(rom)
            if self.faltan_esca(com) == 0:
                escaleras.append(com)
            else:
                posibles.append(com)
        #agregar("*******Posibles escaleras en funcion posibles_escaleras es")
        #agregar(str(posibles))     
        return {'Posibles':posibles, 'Escaleras':escaleras}

    
     
"""-------------------------------------hasta aca clase juego casa--------------------------------"""

class JuegoJug(cl.Basicos):
    def __init__(self):
        global cartasJug        
        self.cartasJug = []
        self.cantCtricas = 0
        self.cantCescaleras = 0
        self.debe_bajar = False
        self.robo = False
        self.bajo = False
        self.ya_tomo = False
        self.tiro = True

    def esTrica(self,lista):
        agregar("entre a es trica con")
        agregar(str(lista))
        palos = [lista[0][1],lista[1][1],lista[2][1]]
        agregar("palos es " + str(palos))
        if lista[0][0] == lista[1][0] == lista[2][0]:
            if len(palos)==len(set(palos)):
                return True
        return False
    
    def agregar_ind(self, lista):
        agregar("lista en agregar_ind es ")
        agregar(str(lista))
        altos = False
        nueva = []
        hay_A = False
        for l in lista:
            agregar("l en agregar_ind es " + str(l))
            ind = objBaraja.orden.index(l[0])            
            if ind == 0:
                hay_A = True
            if ind in (11,12):
                altos = True
            nueva.append([l, ind])
        #si hay una A y una Q o una K, temgo q cambiar el indice 0 a 13
        if hay_A and altos:
           nueva = list(map(lambda x: 13 if x[1]==0  else x[1], lista))
        return sorted(nueva, key=lambda carta: carta[-1])   

    def esEscalera(self,lista):
        agregar("entre a esEscalera con " )
        agregar(str(lista))
        if lista[0][1] == '': # es joker
            palo = lista[1][1]
        else:    
            palo = lista[0][1]
        joker = []
        for l in lista:
            agregar("l es "+ str(l))
            if l[0]=='Joker':
                agregar("En es escalera hay joker")
                joker.append(l)
                agregar("joker es " + str(joker))
            else:    
                if l[1] != palo:
                    agregar("diferente palo " + str(l))
                    return [False,[]]                    
        if len(joker)> 0:           
            agregar("antes de eliminar el joker "+ str(joker[0])) 
            lista.remove(joker[0])
            agregar("elimine el joker")
        nueva_lista = self.agregar_ind(lista)
        agregar("nueva lista es")
        agregar(str(nueva_lista))
        if joker == []:
            agregar("no hay hoker")
            if objMesa.esCorrida(nueva_lista):
                agregar("es corrida " + str(nueva_lista))
                return [True,nueva_lista]
            else:
                return [False,[]]
        else:
            agregar("es corrida " + str(nueva_lista))
            if len(joker) > 1:
                agregar("es corrida mas joker" + str(nueva_lista))
                messagebox.showinfo(title="Loba 1.0", message="Una escalera solo puede tener un joker")
                return [False,[]]
            else:
                agregar("hay solo un joker")
                nueva_lista.append(joker[0])
                agregar("nueva lista es" )
                agregar(str(nueva_lista))
                return [True,nueva_lista]

    def robar(self):
        """
        esta permitido que el jugador tome la carta de la mesa si la va usar para bajar un juego
        """
        #global turnos, carta_jug, robo, bajo
        agregar("Ronda"+str(objJuego.ronda))
        if objJuego.sigue_juego():
            if objJuego.current_player == 'jug':
                if len(self.cartasJug)==10:
                    messagebox.showinfo(title="Loba 1.0", message="No puede tomar la carta de la mesa, ya tiene 10 cartas") 
                    actualizar_mensaje("No puede tomar la carta de la mesa, ya tiene 10 cartas") 
                else:
                    if (not self.ya_tomo or not self.robo):
                        self.robo = True
                        carta = objMesa.tomarCarta()
                        agregar("Jugador roba carta de la mesa")
                        agregar(str(carta))
                        ult=len(self.cartasJug)
                        self.cartasJug.append(carta)
                        bot_jug[ult].change_image(carta[3])
                        #si toma la carta el jugador debe bajar un juego
                        self.bajo = False
                        #inicializa la variable para senalar la carta marcada
                        carta_jug = -1
                        #habilito el check del jugador en su carta numero 10
                        juegos[9].config(state="normal") 
                        #habilito todos los checks
                        for i in range (10):
                            #juegos[i].state(['!selected'])
                            juegos[i].config(state="normal")
                        if len(objMesa.cartasMesa) == 0:
                            #tomo la unica carta de la mesa
                            btnmesa.change_image("img/gris.png")
                        else:
                            agregar("luego de que el jugador robo la anterior carta de la mesa es")
                            agregar(str(objMesa.cartasMesa[-1]))
                            btnmesa.change_image(objMesa.cartasMesa[-1][3])                                                
                    self.debe_bajar = True
                    self.tiro = False
                    actualizar_mensaje("Debes bajar un juego y luego descartar una carta")       
        

    def tomar(self):
        global carta_jug
        #global turnos, carta_jug, ya_tomo
        agregar("Ronda"+str(objJuego.ronda))
        if objJuego.sigue_juego():
            if objJuego.current_player == 'jug':
                agregar("ya tomo es " + str(self.ya_tomo))
                agregar("robo es " + str(self.robo))
                if self.tiro:
                    if not self.ya_tomo and not self.robo:
                        #se setea la variable que ya tomo una carta en True
                        self.ya_tomo = True
                        self.tiro = False
                        carta = objBaraja.tomarCarta()
                        agregar("Jugador toma carta del mazo")
                        agregar(str(carta))
                        self.cartasJug.append(carta)
                        agregar("Cartas jug es")
                        agregar(str(self.cartasJug))
                        agregar("la carta que tome es " + str(carta))
                        agregar("len es" + str(len(self.cartasJug)))


                        bot_jug[len(self.cartasJug)-1].change_image(carta[3])
                        #inicializa la variable para senalar la carta marcada
                        carta_jug = -1
                        if objJuego.ronda == 1:
                            #habilito el check del jugador en su carta numero 10
                            juegos[9].config(state="normal") 
                            #habilito todos los checks
                            for i in range (10):
                                #juegos[i].state(['!selected'])
                                juegos[i].config(state="normal")
                        actualizar_mensaje("Baja un juego si lo deseas o presiona el mouse sobre la carta que descartaras\n y presiona el boton Basura")
                else:
                    actualizar_mensaje("ya tomaste la carta que te corresponde en este turno, debes desechar una carta ")
        else:
            messagebox.showinfo(title="Loba 1.0", message="No puede tomar la carta, la partida ya finalizo") 

    def devolver(self):
        global carta_jug,check
        """ Si el jugador tomo una carta de la mesa y no pudo bajar un juego,
        la carta debe ser devuelta a la mesa"""
        carta_mesa = self.cartasJug[-1]
        objMesa.cartasMesa.append(carta_mesa)
        agregar("Jugador devuelve carta de la mesa, la levanto pero no le sirve")
        agregar(str(carta_mesa))
        #se muestra el anverso de la carta para la carta de la mesa
        btnmesa.change_image(carta_mesa[3])            
        self.cartasJug.pop(-1)
        bot_jug[len(self.cartasJug)].change_image("img/gris.png")
        carta_jug = -1
        self.robo = False
        #desmarco los checks
        #for i in range(10):
            #check[i] = 0 
        for i in range(10):
            check[i].set(False)
        

    def botar(self):
        global carta_jug
        if "img/gris.png" in bot_jug[0].image_path:
            messagebox.showinfo(title="Loba 1.0", message="Aun no puede desechar, no ha iniciado el juego")
            actualizar_mensaje("Aun no puede desechar, no ha iniciado el juego")
        else:
            if not self.ya_tomo and not self.robo:
                messagebox.showinfo(title="Loba 1.0", message="No puede desechar una carta sin tomar una previamente")
                actualizar_mensaje("No puede desechar una carta sin tomar una previamente")   
            elif self.tiro:
                messagebox.showinfo(title="Loba 1.0", message="Ya tiro una carta en esta ronda")                                
            else:
                if carta_jug == -1:
                    messagebox.showinfo(title="Loba 1.0", message="Seleccione una carta para desecharla")
                    actualizar_mensaje("Seleccione una carta para desecharla")   
                else:
                    agregar("robo es " + str(self.robo))
                    agregar("bajo es " + str(self.bajo))
                    agregar("ya_tomo es " + str(self.ya_tomo))
                    if (self.robo == False and self.ya_tomo == True) or (self.robo and self.bajo):
                        btnmesa.change_image(bot_jug[carta_jug].image_path)
                        #eliminar la carta del juego del jugador
                        agregar("abtes de tirar cartas jug es")
                        agregar(str(self.cartasJug))
                        agregar("Jugador tira la carta")
                        agregar("carta_jug es " + str(carta_jug))
                        #agregar(str(objCartasJug.cartasJug[carta_jug]))
                        objMesa.cartasMesa.append(objCartasJug.cartasJug[carta_jug])
                        self.cartasJug.pop(carta_jug)
                        agregar("Cartas jugador luego de tirar es")
                        agregar(str(self.cartasJug))    
                        agregar("len cartas jug es " + str(len(self.cartasJug)))
                        for i in range (carta_jug,len(self.cartasJug)):    
                            bot_jug[i].change_image(bot_jug[i+1].image_path) 
                        bot_jug[len(self.cartasJug)].change_image("img/gris.png")
                        if objJuego.sigue_juego():
                            carta_jug = -1  
                            objJuego.current_player = 'bot'  
                            #deshabilito lo correspondiente al jugador
                            self.cambiar_estado("disabled")
                            self.ya_tomo = False
                            self.robo=False
                            objCartasCasa.limpiar_listas()
                            objCartasCasa.jugar()
                            self.tiro = True
                        else:
                            messagebox.showinfo(title="Loba 1.0", message="Ganaste la partida!")
                            objMesa.puntaje('jug')
                            #aumentar el puntaje del jugador
                    else: #robo y no bajo
                        #debe devolver    
                        messagebox.showinfo(title="Loba 1.0", message="Toma una carta de la mesa y no bajo un juego, la carta tomada de la mesa sera devuelta")
                        self.devolver()
    
    def cambiar_estado(self,estado):
        agregar("en cambiar estado")
        for i in range (10):
            juegos[i].config(state=estado)
            bot_jug[i].config(state=estado)
        atras.config(state=estado)
        adel.config(state=estado)
        btnmesa.config(state=estado)
        resto.config(state=estado)
        descarte.config(state=estado)
        botar.config(state=estado)
        self.robo = False
        self.ya_tomo = False
        if estado == "disabled":
            actualizar_mensaje("Es el turno del bot")
        else:
            actualizar_mensaje("Es tu turno")    


    def puedeBajar(self, mensaje):
        """Funcion que devuelve true si la suma de cartas del jugador 
        entre las que tiene en mesa y las que bajo son 10
        """
        cant = len(self.cartasJug)
        agregar("self.cantCtricas  es " + str(self.cantCtricas))
        agregar("self.cantescaleras  es " + str(self.cantCescaleras))
        agregar("cant  es " + str(cant))
        if cant + self.cantCtricas + self.cantCescaleras == 10:    
            agregar("en if puede bajar, retorno true")
            return True
        else:
            messagebox.showinfo(title="Loba 1.0", message="Para " + mensaje + " debes tomar una carta antes")

    def juegoValido(self):
        """
        Funcion que determina si con las cartas marcadas se puede hacer una trica o una escalera"""
        selected = []
        agregar("check en juegoValido")
        for c in check:
            selected.append(c.get())
        ind = [indice for indice, dato in enumerate(selected) if dato == 1]
        posible_juego =[]
        for i in ind:
            #en posible juego quedan las cartas marcadas por el jugador
            posible_juego.append(self.cartasJug[i])
        if len(posible_juego) >= 3:
            #puede ser trica o escalera
            res = self.esEscalera(posible_juego)
            if res[0]:
                return(res[1],"escalera",ind)
            elif self.esTrica(posible_juego):
                return(posible_juego,"trica",ind)
            else:
                return([],"nada",[])    

    def marcadas(self):
        #global selected
        selected = []
        agregar("check en marcadas")
        agregar(str(check))
        for c in check:
            selected.append(c.get())
        ind = [indice for indice, dato in enumerate(selected) if dato == 1]
        agregar("ind en marcadas es " + str(ind))
        #for x, n in enumerate( check ):
            #selected.append( n.get() )
        #if selected.count(1)>= 3:
        if len(ind) >= 3:
            return True
        else:
            messagebox.showinfo(title="Loba 1.0", message="Deben haber al menos tres cartas para bajar")
        return False    

    def grisar_cartas(self):
        global check
        for i in range(10):
            bot_jug[i].change_image("img/gris.png")
            #juegos.check[i].set(True)  
            check[i].set(False) 
        for i in range(len(self.cartasJug)):
            bot_jug[i].change_image(self.cartasJug[i][3])
        
    def bajar(self):
        global check
        """Funcion que es llamada desde el boton bajar presionado por el jugador"""
        if objJuego.current_player == 'jug':
            if self.puedeBajar("bajar"):
                if self.marcadas():
                    juego = self.juegoValido()
                    if self.debe_bajar and juego[0]==[]:
                            messagebox.showinfo(title="Loba 1.0", message="No es un juego valido, la carta tomada de la mesa sera devuelta")
                            self.devolver()
                            self.debe_bajar = False
                    else:
                        agregar("El juego que bajara el jugadpr es")
                        agregar(str(juego))
                        if juego[1]=="trica":
                            objMesa.pintar_trica(juego[0])
                            #elimino las cartas del juego del 
                            for i in juego[0]:
                                self.cartasJug.remove(i)
                            #las cartas q componen la trica debeb quedar en gris
                            self.cantCtricas +=3  
                            self.bajo = True
                            self.grisar_cartas()                                  
                            agregar("Cartas del jugador luego de bajar la trica")
                            agregar(str(self.cartasJug))
                        elif juego[1]=="escalera": #es escalera
                            lista = juego[0]
                            self.cantCescaleras += len(lista)
                            agregar("juego[0] antes del for es")
                            agregar(str(juego[0]))
                            for i in juego[0]:
                                agregar("en for i es " + str(i))                            
                                if i[0]=='Joker':                                
                                    self.cartasJug.remove(i)                                
                                else:
                                    self.cartasJug.remove(i[0])    
                                agregar("cartasJug es")
                                agregar(str(self.cartasJug))
                            objMesa.pintar_esca(lista, objMesa.ultEsca)                                                                                    
                            #las cartas q componen la trica debeb quedar en gris                            
                            self.bajo = True
                            self.grisar_cartas()      
                            #falta agregar ca cantidad de cartas q componen la escalera a self.escaleras
                        #falta eliminar las cartas de las cartas del jugador
                        #falta desmarcar o deshabilitar los check del jugador
                        
                        else:    
                            for i in range(10):
                                #desmarco los check
                                check[i].set(False)
                            messagebox.showinfo(title="Loba 1.0", message="No es un juego valido")
                        if self.debe_bajar:
                            self.debe_bajar = False
        
        
    def sopar(self):
        agregar("en sopar")
        if objJuego.current_player == 'jug':
            if self.puedeBajar("sopar"):
                if carta_jug == -1:
                    messagebox.showinfo(title="Loba 1.0", message="Seleccione una carta para sopar")
                    actualizar_mensaje("Seleccione una carta para sopar")   
                else:
                    agregar("carta_jug es " + str(carta_jug))
                    juego = objMesa.evaluar_sope(carta_jug)        
                    agregar("Juego es " + str(juego))
                    if juego[0]=="trica":
                        self.cartasJug.pop(carta_jug)
                        self.cantCtricas +=1  
                        self.bajo = True
                        self.grisar_cartas()                                  
                        agregar("Cartas del jugador luego de sopar la trica")
                        agregar(str(self.cartasJug))
                        agregar("despues de sopar tricas objMesa.tricas es")
                        agregar(str(objMesa.tricas))
                    elif juego[0]=="escalera": #es escalera
                        lista = juego[1]
                        self.cantCescaleras += 1
                        self.cartasJug.pop(carta_jug)
                        agregar("cartasJug en sopar escalera es")
                        agregar(str(self.cartasJug))
                        objMesa.re_pintar_esca(lista)                                                                                    
                        self.bajo = True
                        self.grisar_cartas()      
                        agregar("despues de sopar escalera las escarelas de la mesa")
                        agregar(str(objMesa.escaleras))
                        
                    else:    
                        messagebox.showinfo(title="Loba 1.0", message="No puede sopar esa carta")
                        

#inicio del juego
def iniciar():  
    global  objBaraja, objMesa, objCartas,objBasicos, objCartasCasa, objCartasJug, objJuego
    objCartas = cl.Cartas() 
    objBaraja = Baraja() 
    objBaraja.barajar()
    objBasicos = cl.Basicos()
    objMesa = Mesa()
    objJuego = Juegos()
    objMesa.grisar_todo()
    
    #inicializo el juegop de la casa, el juego del jugador y la mesa
    #las 9 cartas quedan en las listas de cartas de la casa y del jugador
    objJuego.current_player = 'jug'
    objBaraja.repartir(objJuego.current_player)
    

def reiniciar():  

    global  objBaraja, objMesa, objCartas,objBasicos, objCartasCasa, objCartasJug, objJuego
    if len(objCartasCasa.cartasCasa) >0 and len(objCartasJug.cartasJug) > 0:
        
        answer = askyesno(title='Confirmación',message='Hay un juego en curso, deseas empezar de nuevo?')
        if answer:
           iniciar()        
    else:    
        objCartas = cl.Cartas() 
        objBaraja = Baraja() 
        objBaraja.barajar()
        objBasicos = cl.Basicos()
        objMesa = Mesa()
        objJuego = Juegos()
        objCartasCasa = JuegoCasa() 
        objCartasJug = JuegoJug()
        objJuego.flip_player()
        objMesa.grisar_todo()
        objBaraja.repartir(objJuego.current_player)
        
    
def mover_atras():
    global carta_jug
    if carta_jug == -1:
        messagebox.showerror(title="Error", message="Debe seleccionar la carta que desa mover y luego presionar el boton para mover hacia la izquierda")
    else:
        if carta_jug-1 == -1:
            messagebox.showerror(title="Error", message="La carta no se puede mover a la izquierda ")
        else:
            imagen = bot_jug[carta_jug-1].image_path
            bot_jug[carta_jug-1].change_image(bot_jug[carta_jug].image_path)    
            bot_jug[carta_jug].change_image(imagen)  
            #juegos[carta_jug].toggle()  
            carta_jug = carta_jug-1
            #juegos[carta_jug].toggle()  

def mover_adelante():
    global carta_jug
    if carta_jug == -1:
        messagebox.showerror(title="Error", message="Debe seleccionar la carta que desa mover y luego presionar el boton para mover hacia la derecha")
    else:
        if carta_jug+1 == 9:
            messagebox.showerror(title="Error", message="La carta no se puede mover a la derecha")
        else:
            imagen = bot_jug[carta_jug+1].image_path
            bot_jug[carta_jug+1].change_image(bot_jug[carta_jug].image_path)    
            bot_jug[carta_jug].change_image(imagen)
            #juegos[carta_jug].toggle()  
            carta_jug = carta_jug+1
            #juegos[carta_jug].toggle()  

def guardar_ultima(num):
        global bot_jug
        """Guarda el indice de la carta del jugador en la cual hace click"""
        global carta_jug
        carta_jug = num
        
def terminar():
    messagebox.showerror(title="Error", message="Se cerrara la ventana de juego")
    f.close()
    d.close()
    ventana.destroy()      

def ayuda():
    mensaje = """1- Se reparten 9 cartas a cada jugador dejando una dada vuelta al final.
    2- Se pueder realizar tricas y escaleras 
    3- Para iniciar un turno se levanta una carta del mazo.
    4- Si el jugador tiene un juego puede dejarlo sobre la mesa a la vista de todos (si el jugador lo desea).
    5- Si hay otros juegos sobre la mesa se puede "sopar" o sea agregar más cartas a un juego.
    6- Se cierra el turno tirando una carta.
    7- Para poder levantar una carta de las cartas desechadas se debe bajar el juego en la mesa.
    8- Gana la partida el jugador que se quede sin cartas en la mano."""
    messagebox.showinfo(title="Loba 1.0", message=mensaje)

def actualizar_mensaje(mnsj):
   mensaje["text"] = mnsj    
   
class ImageButton(tk.Button):
    def __init__(self, parent, image_path=None, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.logger = logging.getLogger('main.ImageButton')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] <%(name)s>: %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self._image_path = None
        self._image = None
        self.image_path = image_path

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, path):
        path = os.path.abspath(path)
        try:
            self._image = tk.PhotoImage(file=path)
            self.config(image=self._image)
            self._image_path = path
        except tk.TclError:
            self.logger.warn("No se pudo cargar la imagen desde '{}'".format(path))
    
    def change_image(self,imagen):    
        self.image_path = imagen

    

ventana = tk.Tk()

ventana.title('Loba 1.0')
ventana.geometry('1425x900')
ventana['bg'] = '#eaeded'

objCartasCasa = JuegoCasa()
objCartasJug = JuegoJug()
objMesa = Mesa()

f = open("jugadas.txt", "a", encoding="utf-8" )
f.truncate()

d = open("detalle.txt", "a", encoding="utf-8" )
d.truncate()

def agregar(linea):
    f.write(linea)
    f.write("\n")

def detalle(linea):
    d.write(linea)
    d.write("\n")

tk.Frame(ventana)

#scrollbar = tk.Scrollbar(ventana)
#scrollbar.grid(row=0,column=1,sticky="nwes")

#checks para los juegos
juegos = [None] * 10
check = [] 
for k in range(10):
    check.append( tk.IntVar(ventana, value = 0) )
    juegos[k] = tk.Checkbutton(ventana, text="",state="disabled", variable=check[k], onvalue=1, offvalue=0)
    juegos[k].grid(padx=0, pady=0, row=0, column=k) 

#botones para las cartas del jugador
bot_jug = [None] * 10 
for j in range(10):
    bot_jug[j] = ImageButton(ventana,image_path="img/gris.png",text=j,state="active")#lambda e, n=i: self.button_click(n))
    bot_jug[j].grid(padx=0.1, pady=0.1, row=1, column=j) 
    bot_jug[j].bind('<Button-1>', lambda e: guardar_ultima(e.widget.cget('text')))
    #bot_jug[j] = tk.Frame(ventana, highlightbackground = "red", highlightthickness = 5, bd=0)

#botones para la mesa y el resto de la baraja
btnmesa = ImageButton(ventana,image_path="img/gris.png",text="",command=objCartasJug.robar) 
btnmesa.grid(row=2, column=2, columnspan = 3) 
resto = ImageButton(ventana,image_path="img/gris.png",text="",command=objCartasJug.tomar) 
resto.grid(row=2, column=6)    

#botones para las cartas de la casa
bot_casa = [None] * 10 
for i in range(10):
    bot_casa[i] = ImageButton(ventana,image_path="img/gris.png",text="",state="disabled")#lambda e, n=i: self.button_click(n))
    bot_casa[i].grid(padx=0.1, pady=0.1, row=3, column=i)  

#botones para las tricas
bot_trica = [None] * 18 

for i in range(9):
    bot_trica[i] = ImageButton(ventana,image_path="img/fondo.png",text="",state="disabled",borderwidth=0)#lambda e, n=i: self.button_click(n))
    #bot_trica[i] = tk.Frame(ventana, highlightbackground = "#eaeded", highlightthickness = 2, bd=0)
    bot_trica[i].grid(padx=0.1, pady=0.1, row=4, column=i)  
for i in range(9):
    bot_trica[i+9] = ImageButton(ventana,image_path="img/fondo.png",text="",state="disabled",borderwidth=0)#lambda e, n=i: self.button_click(n))
    #bot_trica[i+9] = tk.Frame(ventana, highlightbackground = "#eaeded", highlightthickness = 2, bd=0)
    bot_trica[i+9].grid(padx=0.1, pady=0.1, row=5, column=i)      

#botones para las escaleras

bot_esca1 = [None] * 5
for i in range (5):
    bot_esca1[i] = ImageButton(ventana,image_path="img/fondo.png",text="",state="disabled",borderwidth=0)#lambda e, n=i: self.button_click(n))
    #bot_esca1[i] = tk.Frame(ventana, highlightbackground = "#eaeded", highlightthickness = 2, bd=0)
    bot_esca1[i].grid(padx=0.1, pady=0.1, row=i+1, column=10)  
bot_esca2 = [None] * 5
for i in range (5):
    bot_esca2[i] = ImageButton(ventana,image_path="img/fondo.png",text="",state="disabled",borderwidth=0)#lambda e, n=i: self.button_click(n))
    #bot_esca2[i] = tk.Frame(ventana, highlightbackground = "#eaeded", highlightthickness = 2, bd=0)
    bot_esca2[i].grid(padx=0.1, pady=0.1, row=i+1, column=11)  
bot_esca3 = [None] * 5
for i in range (5):
    bot_esca3[i] = ImageButton(ventana,image_path="img/fondo.png",text="",state="disabled",borderwidth=0)#lambda e, n=i: self.button_click(n))
    #bot_esca3[i] = tk.Frame(ventana, highlightbackground = "#eaeded", highlightthickness = 2, bd=0)
    bot_esca3[i].grid(padx=0.1, pady=0.1, row=i+1, column=12)
bot_esca4 = [None] * 5
for i in range (5):
    bot_esca4[i] = ImageButton(ventana,image_path="img/fondo.png",text="",state="disabled",borderwidth=0)#lambda e, n=i: self.button_click(n))
    #bot_esca4[i] = tk.Frame(ventana, highlightbackground = "#eaeded", highlightthickness = 2, bd=0)
    bot_esca4[i].grid(padx=0.1, pady=0.1, row=i+1, column=13)  

#boton para descartar
img0 = ImageTk.PhotoImage(Image.open('img/basura.png'))
descarte = tk.Button(ventana,image=img0, command=objCartasJug.botar) 
descarte.grid(row=2, column=7) 
#boton para sopar
imgSo = ImageTk.PhotoImage(Image.open('img/sopar.png'))
sopar = tk.Button(ventana,image=imgSo, command=objCartasJug.sopar) 
sopar.grid(row=2, column=8)
#boton para bajar jugadas
img1 = ImageTk.PhotoImage(Image.open('img/bajar.png'))
botar = tk.Button(ventana,image=img1, command=objCartasJug.bajar) 
botar.grid(row=2, column=9) 

#boton para mover hacia atras
img4 = ImageTk.PhotoImage(Image.open('img/atras.png'))
atras = tk.Button(ventana,image=img4, command=mover_atras) 
atras.grid(row=2, column=1)
#boton para mover hacia adelante
img5 = ImageTk.PhotoImage(Image.open('img/adelante.png'))
adel = tk.Button(ventana,image=img5, command=mover_adelante) 
adel.grid(row=2, column=2)

img = ImageTk.PhotoImage(Image.open('img/play.png'))
jugar = tk.Button(ventana,image=img, command=iniciar) 
jugar.grid(row=6, column=0) 
img2 = ImageTk.PhotoImage(Image.open('img/replay.png'))
repetir = tk.Button(ventana,image=img2, command=reiniciar) 

repetir.grid(row=6, column=1) 
img3 = ImageTk.PhotoImage(Image.open('img/exit.png'))
salir = tk.Button(ventana,image=img3, command=terminar) 
salir.grid(row=6, column=2) 

img6 = ImageTk.PhotoImage(Image.open('img/ayuda.png'))
ayuda = tk.Button(ventana,image=img6, command=ayuda) 
ayuda.grid(row=6, column=3)

mensaje = tk.Label(ventana,text="Presiona Play para iniciar el juego")
mensaje.grid(row=6,column=4, columnspan = 7, sticky="w")
mensaje.config(font=('Arial', 14),fg="red")

bot = tk.Label(ventana,text="BOT:")
bot.grid(row=6,column=10)
bot.config(font=('Arial', 24),fg="red") #Cambiar tipo y tamaño de fuente
jug = tk.Label(ventana,text="Jugador:")
jug.grid(row=6,column=12)
jug.config(font=('Arial', 24),fg="red") #Cambiar tipo y tamaño de fuente

pts_bot = tk.Label(ventana,text="0")
pts_bot.grid(row=6,column=11)
pts_bot.config(font=('Arial', 24),fg="red")
pts_jug = tk.Label(ventana,text="0")
pts_jug.grid(row=6,column=13)
pts_jug.config(font=('Arial', 24),fg="red")

ventana.mainloop()   
        

    










