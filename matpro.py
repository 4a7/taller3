import os#cambiare princippal por root y principal sera un frame que tiene a las
import socket
from tkinter import *
import random
import PyPDF2
from time import strftime
root=Tk()
root.geometry("600x600+0+0")
root.title("MatPro")
root.config(bg="white")
#frame=Frame(principal,bg="red")
#frame.pack()
Titulo=Label(root, bg="light grey", bd=0,    
             text=" MatPro                                                                                                              F1 = Ayuda",
             anchor="w",
             font=("Calibri",14))
Titulo.pack(fill=X)
root.title("MatPro")
statprint=[0]
nombre_print=[""]
cont=[0]
principal=Frame(root,width=600,height=500)
principal.place(x=0,y=25)
entrada=Entry(principal,bd=0,width=600)
entrada.insert(0,"cmd>>")
entrada.focus()
entrada.pack(fill=X)
scrollhor = Scrollbar(root,orient="horizontal")
scrollver = Scrollbar(root,orient="vertical")
#scrollhor.config(command=principal.xview)
#scrollver.config(command=principal.yview)
scrollhor.pack(fill="x",side="bottom")
scrollver.pack(fill="y",side="right")


matrices={}
def nueva_linea(Event):
    global entrada
    texto=entrada.get()
    entrada.config(state="disabled")
    identifica(texto)
def agrega():
    global entrada
    entrada.config(state="disabled")
    entrada=Entry(principal,bd=0)
    
        
    entrada.insert(0,"cmd>>")
    
    entrada.focus()
    
    entrada.pack(fill=X)
    
    entrada.bind('<Return>', nueva_linea)
def error(causa):
    if statprint[0]==1:
        f=open(nombre_print[0],"a")
        f.write("Error en comando\n")
        f.write(causa+"\n")
        f.close()
    entrada=Entry(principal,bd=0)
    entrada.insert(0,"Error en comando")
    entrada.pack(fill=X)
    entrada.config(state="disabled")
    entrada=Entry(principal,bd=0)
    entrada.insert(0,causa)
    entrada.pack(fill=X)
    entrada.config(state="disabled")
    agrega()
    
    

entrada.bind('<Return>', nueva_linea)


class Matriz:
    def __init__(self,val):
        self.valor=val
    def __add__(self,x):
        retorno=[]
        for i in range(len(self.valor)):
            temp=[]
            for j in range(len(self.valor[0])):
                temp.append(self.valor[i][j]+x.valor[i][j])
            retorno.append(temp)
        return retorno
    def __mul__(self,x):
        retorno=[]
        for i in range(len(self.valor)):
            temp=[]
            for j in range(len(self.valor[0])):
                temp.append(self.valor[i][j]*x.valor[i][j])
            retorno.append(temp)
        return retorno
    def __pow__(self,x):
        retorno=[]
        for i in range(len(self.valor)):
            temp=[]
            for j in range(len(self.valor[0])):
                temp.append(self.valor[i][j]**x)
            retorno.append(temp)
        return retorno
    def __sub__(self,x):
        retorno=[]
        for i in range(len(self.valor)):
            temp=[]
            for j in range(len(self.valor[0])):
                temp.append(self.valor[i][j]-x.valor[i][j])
            retorno.append(temp)
        return retorno
    def get(self):
        return self.valor

###########analisis de operaciones1#####
def crear(tira):
    tira=tira.replace(" ","")
    tira=tira.replace("**","^")
    tiranueva=[]
    ops=["(",")","^","*","+","-","="]
    a=""
    for i in range(len(tira)):
        if tira[i]=="=":
            if not valida(tira[:i]):
                error("Nombre no valido")
                return None
            datos["nombreextra"]=tira[:i]
            datos["activado"]=1
            tira=tira[i+1:]
            break
    else:
        datos["activado"]=0
    listatemp=[]
    for i in tira:
        if i in list(matrices.keys()):
            listatemp.append(i)
            
    
    for i in tira:
        if i not in ops:
            a=a+i
        else:
            if a!="":
                tiranueva.append(a)
                tiranueva.append(i)
            else:
                tiranueva.append(i)
            a=''
    if a!="":
        tiranueva.append(a)

        
        
            
    arbol(tiranueva)

def arbol(tira):
    for i in range(len(tira)):
        if tira[i]==")":
            for j in range(0,i):
                if tira[j]=="(":
                    ult=j
            sub=analiza(tira[ult+1:i],0)
            for w in range(i,ult-1,-1):
                tira.pop(w)
            
            tira.insert(ult,sub[0])
            return arbol(tira)
            
    else:
        
        tira=analiza(tira,0)
        if tira==None:
            return None
        if datos["activado"]==1:
            datos["activado"]=0
            datos["nombre"]=datos["nombreextra"]
            matrices[datos["nombreextra"]]=Matriz(matrices[tira[0]].get())
            imprime_cualquier(datos["nombre"])
        else:
        
            datos["nombre"]=tira[0]
        resultado_leer()
        agrega()
        
                
matrices_aux={}                   
                
def analiza(tira,counter):
    
    
    if len(tira)!=1:
        ops=["^","*","+-"]
        for i in range(len(ops)):
            for j in range(len(tira)-1):
                if tira[j] in ops[i]:
                    operador1=tira[j-1]
                    if ops[i]=="^":
                        operador2=int(tira[j+1])
                    else:
                        operador2=tira[j+1]
                    
                    if ops[i]=="^":
                        
                        nuevo=matrices[operador1]**operador2
                    elif tira[j]=="+":
                        if valida_tamano(matrices[operador1].get(),matrices[operador2].get()):
                            
                            nuevo=matrices[operador1]+matrices[operador2]
                        else:
                            
                            error("Matrices de diferente tamaño")
                            
                            return None
                    elif tira[j]=="-":
                        if valida_tamano(matrices[operador1].get(),matrices[operador2].get()):
                            
                            nuevo=matrices[operador1]-matrices[operador2]
                        else:
                            error("Matrices de diferente tamaño")
                            return None
                    elif ops[i]=="*":
                        if valida_tamano(matrices[operador1].get(),matrices[operador2].get()):
                            
                            nuevo=matrices[operador1]*matrices[operador2]
                        else:
                            error("Matrices de diferente tamaño")
                            return None
                    tira.pop(j+1)
                    tira.pop(j)
                    tira.pop(j-1)
                    tira.insert(j-1,str(counter))

                    nuevo=Matriz(nuevo)
                    matrices[str(counter)]=nuevo
                    counter+=1
                    return analiza(tira,counter)
    else:
        
        return tira
def valida_tamano(m1,m2):#arreglar esto
    if len(m1)==len(m2):
        if len(m1[0])==len(m2[0]):
            return True
    return False
##############analisis de operaciones 2################
    
def identifica(texto):
    try:
        
        if statprint[0]==1:
            
            f=open(nombre_print[0],"a")
            f.write(texto+"\n")
            f.close()
        a=texto.replace(" ","")
        reservadas=["finalizar", "fin","leer", "lee", "leerarchivo"
                       ,"leearc ", "guardararchivo","guaarc", "imprimir", "imp",
                       "noimprimir", "noi", "matrizaleatoriaenteros", "mae",
                       "matrizaleatoriaflotantes","maf", "ayuda", "ayu","binario","bin",
                    "acercade","ace" ]
        if a=="cmd>>":
            
            agrega()
            return None
        texto=texto[5:]
        
        
            
        
        abc=texto.split()
        palabra=abc[0]
        
        
        
        
        
        for j in reservadas:
            if j==palabra:
                
                
                if j=="fin" or j=="finalizar":
                    fin()
                    return None
                elif j=="lee" or j=="leer":
                    try:
                        abc.pop(0)
                        
            
                        if len(abc)==1:
                            if valida(abc[0]):
                                datos["nombre"]=abc[0]
                                datos["leyendo"]=[]
                                leer()
                                return None
                            else:
                                error("Nombre de la matriz debe y solo debe tener letras y numeros")
                                return None
                        else:
                            error("Nombre no valido")
                            return None
                    except:
                        error("Comando no valido")
                        return None
                elif j=="leerarchivo" or j=="leearc":
                    abc.pop(0)
                    if len(abc)<2:
                        
                        if abc==[]:
                            datos["nombre"]="datos_matpro.txt"
                        else:
                            datos["nombre"]=abc[0]
                        
                            
                        leerarchivo()
                    else:
                        error("Nombre no valido")
                    return None
                elif j=="guardararchivo" or j=="guaarc":
                    abc.pop(0)
                    
                    if len(abc)<2:
                        if abc==[]:
                            datos["nombre"]="datos_matpro.txt"
                        else:
                            datos["nombre"]=abc[0]
                        
                        guardar_archivo()
                    else:
                        error("Nombre no valido")
                    return None
                elif j=="ayuda" or j=="ayu":
                    abc.pop(0)
                    if len(abc)<2:
                        if abc==[]:
                            ayuda("nada")
                        else:
                            ayuda(abc[0])
                    else:
                        error("Comando no reconocido")
                    return None
                elif j=="mae" or j=="matrizaleatoriaenteros" or j=="maf" or j=="matrizaleatoriaflotantes":
                    abc.pop(0)
                    try:
                        if len(abc)==1:
                            error("Configuraciones no validas")
                            return None
                        if not valida(abc[0]):
                            error("Nombre no valido")
                            return None
                        datos["nombre"]=abc[0]
                        abc.pop(0)
                        tamano=""
                        for i in abc:
                            tamano=tamano+str(i)
                        if j=="mae" or j=="matrizaleatoriaenteros":
                            letra="e"
                        else:
                            letra="f"
                        ma(tamano,letra)
                        return None
                    except:
                        error("Especificaciones no validas")
                        return None
                elif j=="binario" or j=="bin":
                    
                    abc.pop(0)
                    try:
                        
                        for i in abc:
                            
                            mat_bin(i)
                    except:
                        error("Especificaciones no validas")
                elif j=="acercade" or j=="ace":
                    
                    imprime_cualquier("MatPro V1.0")
                    
                    imprime_cualquier("Junio 2016")
                    
                    imprime_cualquier("Creada por Juan F. Villacis")
                    agrega()
                    return None
                elif j=="imprimir" or j=="imp":
                    if len(abc)<2:
                        if statprint[0]==1:
                            imprime_cualquier("Impresion ya esta activada")
                            agrega()
                            return None
                        else:
                            
                            imprime_cualquier("Impresion Activada")
                            agrega()
                            nombre="matpro_"
                            nombre+=str(socket.gethostname())
                            nombre+="_"
                            nombre+=strftime("%Y-%m-%d %H:%M:%S")
                            nombre=nombre.replace(":","-")
                            nombre=nombre+".txt"
                            nombre_print[0]=nombre
                            statprint[0]=1
                            f=open(nombre,"w")
                            f.close()
                            
                            return None
                    else:
                        error("Comando no reconocido")
                elif j=="noi" or j=="noimprimir":
                    if len(abc)<2:
                        try:
                            imprime_cualquier("Impresion Desactivada")
                            os.startfile(nombre_print[0],"print")
                            nombre_print[0]=""
                            statprint[0]=0
                            return None
                        except:
                            error("Comando no reconocido")
                            return None
                        
                    else:
                        error("Comando no reconocido")
                        return None
                        
                        
                        
                    
                        
           
        else:
            try:
                
                lee_directo(abc)
                agrega()
                return None
            except:
                pass
            try:
                crear(texto)
                
                return None
            except:
                pass
            imprime_cualquier("Error en comando")
            imprime_cualquier("Comando no reconocido")
            agrega()
    except:
        error("Entrada no valida")
#########lee las amtrices que se dan directamente
def lee_directo(lista):
    
    for j in lista:
        if j not in list(matrices.keys()):
            a=10/0
    else:
        for j in lista:
            datos["nombre"]=j
            imprime_cualquier(j)
            resultado_leer()
        
        
def fin():
    global entrada
    imprime_cualquier("Confirmar la salida (si/no)")
    agrega()
    entrada.bind('<Return>',fin2)
    
def fin2(x):
    e=entrada.get()
    
    e=e.lower()
    e=e[5:]
    e.replace(" ","")
    
    if e=="si":
        root.quit()
        root.destroy()
    else:
        entrada.config(state="disabled")
        agrega()

#operacion de lectura
def valida(nombre):
    lista=list(matrices.keys())
    
    
    if nombre  not in lista:
        
        for i in nombre:
            
            if not i.isalnum():
                return False
        return True
    else:
        return False
def confirma_tamano(a):
    if len(a)==1:
        return True
    else:
        q=len(a[0])
        for z in a:
            if not len(z)==q:
                return False
        else:
            return True
datos={"leyendo":[],"nombre":"","nombreextra":"","activado0":0}
def leer():
    global entrada
    entrada.config(state="disabled")
    entrada=Entry(principal,bd=0)
    entrada.insert(0,"Fila"+str(cont[0])+" ")
    entrada.focus()
    entrada.pack(fill=X)
    entrada.bind('<Return>', analiza_leer)


def analiza_leer(x):
    try:
        global entrada
        texto=entrada.get()
        
        texto=texto.replace(","," ")
        texto=texto.split()
        texto.pop(0)
        
        
        if texto[0]==".":
            matrices[datos["nombre"]]=Matriz(datos["leyendo"])
            imprime_cualquier(datos["nombre"])
            resultado_leer()
            cont[0]=0
            agrega()
        else:
            for i in range(len(texto)):
                if "." in texto[i]:
                    texto[i]=float(texto[i])
                else:
                    
                    texto[i]=int(texto[i])
            
            
            datos["leyendo"].append(texto)
            if confirma_tamano(datos["leyendo"]):
                cont[0]+=1
                leer()
            else:
                entrada.config(state="disabled")
                error("Filas deben tener misma cantidad de elementos")
                cont[0]=0
    except:
        error("Entrada invalida")
        cont[0]=0
    
def resultado_leer():
    global entrada
    entrada.config(state="disabled")
    mat=(matrices[datos["nombre"]].get())
    for i in mat:
        a=0
        for j in i:
            w=len(str(j))
            if w>a:
                a=w
    
    a+=1
    for i in mat:
        string=""
        lista_tup=[]
        for j in i:
            string=string+(" "*(a-len(str(j)))+str(j))+" "#("%"+str(a)+"d"+" ")
            lista_tup.append(j)
        res=string#string%tuple(lista_tup)
        
        imprime_cualquier(res)
            
        
######imprime cualquier cosa que se le mande
def imprime_cualquier(cosa):
    global entrada
    if statprint[0]==1:
        f=open(nombre_print[0],"a")
        f.write(cosa+"\n")
        f.close()
    entrada.config(state="disabled")
    entrada=Entry(principal,bd=0)
    entrada.insert(0,cosa)
    entrada.pack(fill=X)
    entrada.config(state="disabled")
########################


##########leer archivos
def leerarchivo():
    f=open(datos["nombre"],"r")
    
        
    listita=[123]#lista donde se tiene lo que se va a imprimir
    estado="nombre"
    nombre=""
    
    while listita!=[]:
        if estado=="nombre":
            
            linea=f.readline()
            
            linea=linea.replace("\n","")
            
            nombre=linea
            print(nombre,valida(nombre))
            if not valida(nombre):
                error("Nombre invalido")
                return None
            imprime_cualquier(nombre)
            datos["leyendo"]=[]
            estado="lee"
            check=1
        elif estado=="lee":
            linea=f.readline()
            linea=linea.replace("\n","")
            linea=linea.replace(","," ")
            check=linea.split()
            
            for j in check:
                for w in j:
                    
                    if not w.isdigit() and not w==".":
                
                        a=3/0
                   
                
            
            if linea!=".":
                imprime_cualquier(linea)
                linea=linea.split()
                
                datos["leyendo"].append(linea)
            else:
                if check!=0:
                    mat=[]
                    
                    for i in datos["leyendo"]:
                        lis=[]
                        for w in i:
                            if "." in w:
                                lis.append(float(w))
                            else:
                                lis.append(int(w))
                        
                        mat.append(lis)
                    
                matrices[nombre]=Matriz(mat)
                estado="nombre"
        
        listita=list(linea)
    #f.close()
    agrega()
   
###########guardararchivo
def guardar_archivo():
    retorno=[]
    f=open(datos["nombre"],"w")
    for i in matrices:
        f.write(i+"\n")
        retorno.append(i+"\n")
        mat=matrices[i].get()
        for j in mat:
            a=0
            for j in i:
                y=len(str(j))
                if y>a:
                    a=y
        for k in mat:
            string=""
            lista_tup=[]
            for z in k:
                
                string=string+("%"+str(a)+"d"+" ")
                lista_tup.append(z)
               
            res=string%tuple(lista_tup)
            
            f.write(res+"\n")
            retorno.append(res+"\n")
        f.write("."+"\n")
        
    
    imprime_cualquier(datos["nombre"])
    for ele in retorno:
        imprime_cualquier(ele)
    f.close()
    agrega()
    #leerarchivo()
def ayuda2(x):#muestra el manual
    os.startfile("manual_de_usuario_matpro.pdf")
################ayuda
def ayuda(cosa):
    
    if cosa=="nada":
        ayuda2(1)
        agrega()
    elif cosa=="fin" or cosa=="finalizar":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Termina el programa")
        agrega()
    elif cosa=="leer" or cosa=="lee":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Se lee una matriz")
        imprime_cualquier("Las entradas se separan por comas o espacios")
        imprime_cualquier("Para termina la lectura se presiona enter y en la fila nueva se introduce un punto")
        agrega()
    elif cosa=="leerarchivo" or cosa=="leearc":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Se guardan en la memoria las matrices de un archivo")
        imprime_cualquier("Si no se introduce un nombre de archivo seguido del comando se leeran las matrices del archivo datos_matpro.txt")
        imprime_cualquier("De lo contrario se leeran las matrices del archivo cuyo nombre se introdujo")
        agrega()
    elif cosa=="guardararchivo" or cosa=="guaarc":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Se importan desde un archivo las matrices")
        #imprime_cualquier("")
        agrega()
    elif cosa=="imp" or cosa=="imprimir":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Todo lo que se muestre en la consola desde que se activa el comando en adelante se imprimira")
        imprime_cualquier("Para detener la impresion se introduce el comando noimprimir")
        agrega()
    elif cosa=="+" :
        imprime_cualquier("Comando +")
        imprime_cualquier("Suma las matrices que se eligen")
        agrega()
    elif cosa=="noi" or cosa=="noimprimir":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Detiene la impresion")
        agrega()
    elif cosa=="-" :
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Resta las matrices que se eligen")
        agrega()
    elif cosa=="**" :
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Eleva a la potencia que se elija todos los elementos de la matriz")
        agrega()
    elif cosa=="*" :
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Multiplic las matrices que se eligen")
        agrega()
    elif cosa=="=" :
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Iguala una matriz a una operacion de matrices")
        agrega()
    elif cosa=="matrizaleatoriaenteros" or cosa=="mae":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Crea una matriz aleatoria de tamaño mxn de enteros")
        agrega()
    elif cosa=="matrizaleatoriaflotantes" or cosa=="maf":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Genera una matriz aleatoria de flotantes de tamaño mxd")
        agrega()
    elif cosa=="ayuda" or cosa=="ayu":
        imprime_cualquier("Comando "+str(cosa))
        imprime_cualquier("Muestra la ayuda")
        imprime_cualquier("Si no se incluye un comando entonces se abre la guia de usuario, de lo contrario se mostrara la ayuda del comando introducido")
        agrega()
    else:
        imprime_cualquier("Comando no reconocido")
        agrega()
        
root.bind('<F1>', ayuda2)        
###########mae
def ma(tamano,tipo):
    try:
        for j in range(len(tamano)):
            if tamano[j]=="x" or tamano[j]=="X":
                op1=tamano[:j]
                op2=tamano[j+1:]
        if op1=="" or op2=="":
            error("Configuraciones no validas")
        nueva=[]
        for r in range(int(op2)):
            nueva1=[]
            for t in range(int(op1)):
                if tipo=="f":
                    nueva1.append(random.uniform(-10000,10000))
                else:
                    nueva1.append(random.randint(-10000,10000))
                    
            nueva.append(nueva1)
        
        matrices[datos["nombre"]]=Matriz(nueva)
        imprime_cualquier(datos["nombre"])
        resultado_leer()
                
                        
                    
                
        agrega()
    except:
        
        error("Configuraciones no validas")
        
        
        
def mat_bin(nom):
    if nom in list(matrices.keys()):
        
        try:
            
            mat=matrices[nom].get()
            
            nuevamat=[]
            for j in mat:
                
                nueva2=[]
                for w in j:
                    
                    if int(w)<0:
                        nueva2.append(0)
                    else:
                        nueva2.append(1)
                nuevamat.append(nueva2)
            matrices[nom]=Matriz(nuevamat)
        except:
            error("Especificaciones no validas")
            return None
    else:
        error("Matriz no existe")
        return None
        
    

#principal.mainloop()
