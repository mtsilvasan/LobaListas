from  itertools import combinations

class Cartas: 
    global palos, valores, color
    palos = ['cor', 'rom', 'tre', 'bas'] 
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k'] 
    color = ["Rojo","Azul"]
    
    def __init__(self): 
        pass

class Basicos:

    def faltan_esca(self,lista):
        min = lista[0][1]
        max = lista[-1][1]
        return (max - min + 1) - len(lista)   

    def aplanar(self,lista):
        plana = []
        for lis in lista:
            for l in lis:
                if len(l) == 2:
                    plana.append(l[0])
                else:
                    if isinstance(l, list):
                        plana.append(l[0])
                    else:    
                        plana.append(l)  
        unicos = set(plana)
        return unicos  

    def valida(self,order_list):
        li = []
        j = 0
        for i in range(len(order_list)-1) :
            if ((order_list[i+1][1]) - (order_list[i][1]+1)) > 1:
                return False
            elif ((order_list[i+1][1]) - (order_list[i][1]+1)) == 1:
                j+=1
        if j > 1:
            return False
        else:
            return True

    def combinatoria(self,lista):
        tam = len(lista)
        result = []
        final = []
        for i in range (2,tam+1):
            for c in combinations(lista,i):
                #print(c)
                if self.valida(sorted(c, key=lambda carta: carta[-1])):
                    #print(c)
                    result.append(c)
        comple = []
        juntas = []
        for res in result:
            if self.faltan_esca(res) == 0:
                juntas.append(res)        
            i=1
            encontro = False
            if len(res) >= 3 and self.faltan_esca(res) == 0:
                comple = res
                #print("comple es " + str(comple))
            for j in range(i,len(result)):
                if result[j] != res:
                    if(all(x in result[j] for x in res)): 
                        encontro = True
            if not encontro:
                if len(comple)>0:
                    if len(res) >= 3 and self.faltan_esca(res) == 0:
                        final = res
                    else:
                        final = comple    
                else:
                    final=res        
            i+=1
        fin = list(final)    
        for j in juntas:
            fin.append(j[0])    
        return fin

           
