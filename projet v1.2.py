#-*-Coding:utf-8-*-
import sys
##"""
#Tkinter
from tkinter import *
win = Tk()
win.title("Dérivateur v1.2")

#Definition des couleurs
color_bg_light ='#102327'
color_bg_dark = '#071719'
color_font_light = '#A5A5A5'
color_font_red = '#A82030'
color_cursor='#A9A9A9'
color_select_bg='#B8B8B8'
color_select_fg='#101719'

win.configure(bg=color_bg_light)
frame_main = Frame(win,bg=color_bg_light)
frame_main.pack(pady=20,padx=20)

frame1 = Frame(frame_main,bg=color_bg_light)
frame1.pack()

frame2 = Frame(frame_main,bg=color_bg_light)
frame2.pack(pady=10)

frame3 = Frame(frame_main,bg=color_bg_light)
frame3.pack()
#Zones de texte avec labels
label_in = Label(frame1,
                text="Fonction à dériver:",
                bg=color_bg_light,
                fg=color_font_light)
label_in.pack(side=LEFT,padx=10)

text_in = Text(frame1,
                height=2,
                width=30,
                bg=color_bg_dark,
                fg=color_font_light,
                insertbackground=color_cursor,
                selectbackground=color_select_bg,
                selectforeground=color_select_fg,
                relief=SUNKEN)
text_in.pack(side=LEFT)

label_out = Label(frame2,
                    text="Dérivée:",
                    bg=color_bg_light,
                    fg=color_font_light)
label_out.pack(pady=5)

text_out = Text(frame2,
                height=2,
                width=90,
                bg=color_bg_dark,
                fg=color_font_light,
                insertbackground=color_cursor,
                selectbackground=color_select_bg,
                selectforeground=color_select_fg,
                relief=SUNKEN)
text_out.pack()

#bouton(s)

def UI_derive():
    text_out.delete("1.0",END)
    func = text_in.get("1.0","end-1c")
    if func != "":
        text_out.insert("1.0",deriver_complexe(func))

def UI_clear():
    text_in.delete("1.0",END)
    text_out.delete("1.0",END)

Button(frame3,text="Deriver",
       fg=color_font_light,
       command=UI_derive,
       bg=color_bg_dark).pack(side=LEFT,padx=5)

Button(frame3,text="Tout effacer",
       fg=color_font_red,
       command=UI_clear,
       bg=color_bg_dark).pack(side=LEFT,padx=5)
##"""

#Fonction qui dérive les polynômes:
# Parametres
#     Entree : Chaine de caractère contenant une fonction a décomposer (parenthèses,ln(),e^(),etc...)
#     Sortie : Liste d'éléments interprètable par deriver_complexe() pour deriver

def decompose(fonc):
    ADev= []
    deb= None
    fin= 0
    o=0
    fonc.strip()
    fonc=fonc.replace(')(',')*(')
    while fonc.find(')')!=-1:
        o=0
        deb=None
        fin=0
        count=0
        if fonc[0]=='-':
            ADev.append('-')
            fonc=fonc[1:]
        else:

            for i in fonc:
                o+=1
                if i=='(':
                    if count==0:
                        if fonc[o-3:o]=='ln(' or fonc[o-3:o]=='e^(':
                            deb=o-3
                        elif fonc[o-5:o]=='sqrt(':
                            deb=o-5
                        elif fonc[o-2:o]=='^(':
                            deb=o-2
                        else:
                            deb= o
                    count+=1

                elif i==')':
                    count-=1
                    if count==0:
                        fin= o-1

                        ADev.append(fonc[deb:fin])
                        if deb==0:
                            fonc=fonc[fin+1:]
                        else:
                            fonc=fonc[:deb-1]+fonc[fin+1:]
                        break
                    elif count <0:
                        sys.exit('ERREUR: pas de début (caractère "(" manquant)')

                elif i=='*' or i=='/':
                    if count==0:
                        ADev.insert(-1,i)
                        fonc=fonc[:o-1]+fonc[o:]
                        break

    ADev.append('stop')
    ADev.append(fonc)

    return ADev



#Fonction qui dérive les polynômes:
# Parametres
#     Entree : Chaine de caractère contenant le polynome a deriver
#     Sortie :  liste de chaines de caractères correspondant aux éléments de la dérivée du polynome
#
#
#
def deriver_simple(fonc):
    while fonc.find("++")!=-1 or fonc.find("--")!=-1:
        fonc=fonc.replace("--","-")
        fonc=fonc.replace("++","+")
    fonc = fonc.replace("-","+-")
    lis = fonc.split("+")
    resultat = []

    for element in lis:
        o=-1
        element.strip()
        for i in element:
            o+=1
            element += " "  #Permet de rajouter un caractere à la fin pour pouvoir effectuer test ligne suivante
            if i =="x" and element[o+1]!= "^":
                if element[:o]!="":
                    resultat.append(element[:o])
                else:
                    resultat.append("1")


            if i == "^":
##                print(element)
                exp = int(element[o+1:])
##                print(exp)
                factor=element[:o-1]
                if factor=='':
                    factor='1'
##                print(int(factor))
                resultat.append(str(int(factor)*exp)+"x^"+str(exp-1))


    return resultat

#Fonction qui dérive les polynômes:
# Parametres
#     Entree : liste de chaines de caractères correspondant aux éléments d'un polynome
#     Sortie :  chaine de caractère contenant un polynome

def fusion(resultat):
    resStr=""
    for element in resultat:
        if element[-3:] == "x^1":
            element = element.replace("x^1", "x")

        resStr = resStr + " + " + element
        resStr = resStr.replace("+ -","- ")


        if resStr[1] == "+":
            resStr = resStr[3:]
        elif resStr[1] == "-":
            resStr = resStr.replace("- ","-") #Enlever espace avant premier nombre et espace tout les "-"
            resStr = "-" + resStr[2:]


    return resStr

#Fonction qui dérive les fonctions(quelles qu'elle soient):
# Parametres
#     Entree : Chaine de caractère contenant la fonction a deriver
#     Sortie :  Chaîne de caractère contenant la dérivée

def deriver_complexe(fonc):
    indice=0
    resultat_temp=''
    resultat=''
    resDecomp= decompose(fonc)
##    print(resDecomp)
    while resDecomp[0]!='stop':
        indice=0
##        print(resDecomp[0])
        for element in resDecomp:
            if element=="*":
                u=resDecomp[indice+1]
                v=resDecomp[indice+2]
                #Recherche de la dérivée udev et vdev
                if u.find(")")==-1:
                    udev = fusion(deriver_simple(u))
                else:
                    udev = deriver_complexe(u)

                if v.find(")")==-1:
                    vdev = fusion(deriver_simple(v))
                else:
                    vdev = deriver_complexe(v)
                #Affichage
                resultat_temp= '(' + udev + ')(' + v + ') + (' + u + ')(' + vdev +')'
##                print(resultat_temp)
                resultat+= '+(' + resultat_temp+')'
                del resDecomp[indice:indice+3]
                break


            elif element=="/":
                u = resDecomp[indice+1]
                v = resDecomp[indice+2]
                #Recherche de la dérivée udev et vdev
                if u.find(")")==-1:
                    udev = fusion(deriver_simple(u))
                else:
                    udev = deriver_complexe(u)

                if v.find(")")==-1:
                    vdev = fusion(deriver_simple(v))
                else:
                    vdev = deriver_complexe(v)
##              resultat_temp'((' + udev + ')(' + v + ') - (' + u + ')(' + vdev +'))/(' + v + ')^2'
                #Affichage
                resultat_temp= '((' + udev + ')(' + v + ') - (' + u + ')(' + vdev +'))'
##                print(resultat_temp)
##                print(len(resultat_temp)*'-')
##                print(int((len(resultat_temp)-len(v)-3)/2)*' ' +'('+ v +')^2')
                resultat+= '+(' + resultat_temp +'/('+v+')^2)'
                del resDecomp[indice:indice+3]
                break


            elif element[:3] =="ln(":

                u= element[3:]
                #Recherche de la dérivée udev
                if u.find(")")==-1:
                    udev = fusion(deriver_simple(u))
                else:
                    udev = deriver_complexe(u)
##                print(fusion(deriver_simple(u))+'/'+u)
                #Affichage
##                print(int((len(u)-len(udev))/2)*' '+udev)
##                print(int(len(u))*'-')
##                print(u)
##                print(fusion(deriver_simple(u))/str(u))
                resultat+='+('+udev+')/('+u+')'
                del resDecomp[indice]
                break


            elif element[:3]=="e^(":
                u = element[3:]
                #Recherche de la dérivée udev
                if u.find(")")==-1:
                    udev = fusion(deriver_simple(u))
                else:
                    udev = deriver_complexe(u)
##                print('('+udev+')e^('+u+')')
                resultat+='+('+udev+')e^('+u+')'
                del resDecomp[indice]
                break


            elif element[:5]=="sqrt(":
                u = element[5:]
                #Recherche de la dérivée udev
                if u.find(")")==-1:
                    udev = fusion(deriver_simple(u))
                else:
                    udev = deriver_complexe(u)
##                print(udev)
##                print((len(u)+7)*'-')
##                print('2*sqrt('+u+')')
                resultat+='+('+udev+')/(2*sqrt('+u+'))'
                del resDecomp[indice]
                break


            elif element[:2]=='^(':
                u=resDecomp[indice-1]
                #Recherche de la dérivée udev
                if u.find(")")==-1:
                    udev = fusion(deriver_simple(u))
                else:
                    udev = deriver_complexe(u)

                n=element[2:]
##                print(u)
##                print(n)
                resultat+='+('+n+')*('+udev+')*('+u+')^('+str(int(n)-1)+')'
                del resDecomp[indice-1:indice+1]
                break


            elif element=='-':
                resultat+='-'
                del resDecomp[indice]
                break

            indice+=1

    if resDecomp[1]!='':
        resultat+='+'+fusion(deriver_simple(resDecomp[1]))

    resultat=resultat.replace('-+','-')
    if resultat[0]=='+':
        resultat=resultat[1:]
    if resultat[-1]=='+':
        resultat=resultat[:-1]
##    resultat=resultat.replace('-','--')
##    resultat=resultat[1:]
##    resultat=resultat.replace('--','-')
    return resultat

win.mainloop()


#||=================================||
#||         Fonctions de test       ||
#||=================================||
#9x^10+7x^6-9x^3-2x^2+x+1
#(3x^2)(5x+2)+(x^3)(9x-3)
#ln(4x^2)-(2x+2)(3x^3)+(x^4)/(6x)+sqrt(9x)+(3x^2+1)^(3)+30x-3x^2+2
#(x)*(ln(x))
#(ln(3x^2)+3)*(150x-5)

#||====================================||
#||         Crédits/random facts       ||
#||====================================||

#174 lignes de code fonctionnel!

#Script par Raphaël Letourneur et Ancelin Bouchet.


#||=============================||
#||     Changelog               ||
#||=============================||
"""
v1.2:
    CHANGEMENT MAJEURS:
        -changement du fonctionnement de la dérivation u*v et u/v:
            ->signe '*' ou '/' placé AVANT les deux éléments u et v
            =>bugfix: plus de loop inf dans le cas où u ou v commence par 'ln(', 'e^(' ou 'sqrt('
    CHANGEMENTS MINEURS:
        -interface, en dark mode
        -changement du cas de 'pas de début' dans decompose():
            -cherche 'None' au lieu de '999'
                -> permet de n'avoir aucune limite de taille concernant la fonction à dériver


v1.1:
    CHANGEMENTS MAJEURS:
        -renommé "principale" en "deriver_complexe"
        -ajout récurrence dans "dériver compexe":
            -> permet de dériver des fonctions avec des parenthèses dans des parenthèses
        -modification de la fct décompose:
            ->ne sépare plus les parenthèses dans les parenthèses (compteur)

    CHANGEMENTS MINEURS:
        -ajout d'un changelog (yay)
        -ajout de com informatifs avant chaque fonction
        -ajout de crédits
        -ajouts de labels
"""



