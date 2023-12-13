#################################################################################
#                                                                               #
#   Nano verion micropyton                                                      #
#   V1.0                                                                        #
#                                                                               #
#   Créer par:          Freyr86                                                 #
#   Github:             https://github.com/Freyr86                              #
#                                                                               #
#   Un grand merci à:   RetiredWizard                                           #
#   Github:             https://github.com/RetiredWizard/                       #
#                                                                               #
#################################################################################
import sys
import board
import keypad
import os
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import time
import module
from module import clavier_gestion
import storage




def init_nano(chemin):
    storage.remount("/",False)

    #déclaration variable d'affichage
    global list_affichage
    list_affichage = []

    global index_page
    index_page = 0

    global index_ligne
    index_ligne = 0

    global index_colone
    index_colone = 0

    global index_lettre
    index_lettre = 0

    global main_loop
    main_loop = True

    global size_select_ligne
    size_select_ligne = 0

    global nbr_ligne_total
    nbr_ligne_total = 0

    global curs_ligne
    curs_ligne = Rect(4,22,2,10,fill=0x00ff00)

    global curs_ligne2
    curs_ligne2 = Rect(4,22,2,10,fill=0x00ff00)
    curs_ligne2.hidden = True

    global cursor_mode
    cursor_mode = False

    global index_bouton
    index_bouton = 0

    global egal_symbole
    egal_symbole = False

    global url
    url = chemin

    global cdr_prompt
    cdr_prompt = Rect(50,50,220,140,fill=0x000000,outline=0x00ff00 )
    cdr_prompt.hidden = True

    global txt_title_prompt
    txt_title_prompt = label.Label(terminalio.FONT, text="Save As")
    txt_title_prompt.x = 135
    txt_title_prompt.y = 60
    txt_title_prompt.background_color = 0x000000
    txt_title_prompt.color = 0x00ff00
    txt_title_prompt.hidden = True

    global txt_chemin_prompt
    txt_chemin_prompt = label.Label(terminalio.FONT, text="Chemin: ")
    txt_chemin_prompt.x = 60
    txt_chemin_prompt.y = 140
    txt_chemin_prompt.background_color = 0x000000
    txt_chemin_prompt.color = 0x00ff00
    txt_chemin_prompt.hidden = True

    global txt_instruc
    txt_instruc = label.Label(terminalio.FONT, text="<Enter> Save         <@> Cancel")
    txt_instruc.x = 60
    txt_instruc.y = 180
    txt_instruc.background_color = 0x000000
    txt_instruc.color = 0x00ff00
    txt_instruc.hidden = True

    global txt_alert
    txt_alert = label.Label(terminalio.FONT, text="")
    txt_alert.x = 10
    txt_alert.y = 115
    txt_alert.background_color = 0x0000ff
    txt_alert.color = 0x000000
    txt_alert.hidden = True


    #initialisation trackball
    global trackball
    trackball = keypad.Keys(
    [
        board.TRACKBALL_CLICK,
        board.TRACKBALL_UP,
        board.TRACKBALL_DOWN,
        board.TRACKBALL_LEFT,
        board.TRACKBALL_RIGHT
    ],
    value_when_pressed=False
    )

    #appel clavier
    global read_clavier
    read_clavier = clavier_gestion.clavier()


    #tableau d'affichage du corps de text
    global txt_area2
    txt_area2 = [label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text=""),
                label.Label(terminalio.FONT, text="")
                ]

#zone d'étition de text bas de page
txt_edit = label.Label(terminalio.FONT, text="")

#bouton
global cmd_sav
cmd_sav = label.Label(terminalio.FONT, text="")

global cmd_sav_as
cmd_sav_as = label.Label(terminalio.FONT, text="")

global cmd_annuler
cmd_annuler = label.Label(terminalio.FONT, text="")


#déclaration variable ecrant
screen = displayio.Group()

#fonction de verification d'existance de fichier
def file_exist(chemin):
    ret = False
    try:
        file = open(chemin,"r")
        ret = True
        file.close()
    except:
        ret = False
    return ret

#compter nombre de ligne du fichier
def len_file(chemin):
    global nbr_ligne_total
    #verificaion nombre de ligne du fichier
    with open(chemin) as myfile:
        tot_ligne = sum(1 for line in myfile)
    
    #fermeture du fichier
    myfile.close()

    #si fichier plus petit que 16 passage a 16
    if tot_ligne < 16:
        tot_ligne = 16
    else:
        tot_ligne = tot_ligne + 1

    #mise a jour ligne total
    nbr_ligne_total = tot_ligne

    #retourne le nombre de lignes
    return tot_ligne

#mise a jour du text selon variables
def affiche_variable(index):
    global list_affichage
    global nbr_ligne_total

    #print ligne du fichier
    for loop in range(0,16):
        #verifier si la ligne est plus petit que le nombre de ligne total
        try:
            txt_area2[loop].text = list_affichage[loop + index]
        except:
            None

#lecture de fichier
def read_file(chemin,index = 0):
    global list_affichage
    
    #verification existance du fichier
    if file_exist(chemin):
        #ouverture du fichier
        file = open(chemin,"r")

        #listing des ligne
        for loop in range(0,len_file(chemin)):
            txt = str(file.readline())
            size_select_ligne = len(txt) - 1
            list_affichage.append(txt[0:size_select_ligne])

        #fermeture fichier
        file.close()

#modification de la selection de ligne
def ligne_select():
    global curs_ligne
    curs_ligne.y = 22 + index_ligne * 12

#selection de caratère
def caracter_select():
    global curs_ligne
    global index_lettre
    curs_ligne.x = 4 + index_lettre * 6

#cmd_up
def cmd_up():
    global index_ligne
    global index_page

    #remonter jusqu'a 0 si page pa a 0 remonter la page
    if index_ligne > 0:
        index_ligne = index_ligne - 1

    #remonte de la page
    elif index_page > 0:
        index_page = index_page - 10
        if index_page < 0:
            index_page = 0
        affiche_variable(index_page)

    #selection de ligne
    ligne_select()

#cmd_down
def cmd_down():
    global index_ligne
    global index_page
    global nbr_ligne_total

    #decandre la page si font de page si plus bas que le font de page stop
    if index_ligne < 15:
        index_ligne = index_ligne + 1
    
    #decante de la page
    elif index_page < nbr_ligne_total - 16:
        index_page = index_page + 10
        if(index_page > nbr_ligne_total - 16):
            index_page = nbr_ligne_total - 16

        affiche_variable(index_page)

    #selection de la ligne
    ligne_select()

#cmd right
def cmd_right():
    global index_ligne
    global index_page
    global index_lettre
    global list_affichage
    global txt_area2
    global index_colone

    #jusqu'au font de la ligne
    if index_lettre < len(list_affichage[index_ligne + index_page]) - index_colone:
        if index_lettre < 52:
            index_lettre = index_lettre + 1
        else:
            index_colone = index_colone + 1

    verif_pos()
    
    for loop in range(0,16):
        txt_area2[loop].x = 5 - 6 * index_colone
    
    caracter_select()

#cmd left
def cmd_left():
    global index_ligne
    global index_page
    global index_lettre
    global list_affichage
    global index_colone

    if index_lettre > 0:
        index_lettre = index_lettre - 1
    elif index_colone > 0:
        index_colone = index_colone - 1

    verif_pos()

    for loop in range(0,16):
        txt_area2[loop].x = 5 - 6 * index_colone

    caracter_select()

#verification après mouvement si curseur trop éloigner
def verif_pos():
    global index_ligne
    global index_page
    global index_lettre
    global list_affichage
    global index_colone

    if len(list_affichage[index_ligne + index_page]) < index_lettre + index_colone:
        if len(list_affichage[index_ligne + index_page]) < 52:
            index_lettre = len(list_affichage[index_ligne + index_page]) - index_colone
            if not "\n" in list_affichage[index_ligne + index_page]:
                index_lettre = index_lettre - 1
            if len(list_affichage[index_ligne + index_page]) < index_colone:
                index_colone = len(list_affichage[index_ligne + index_page]) - 1
                index_lettre = 0
    
    if index_lettre < 0:
        index_lettre = 0
        
#fonction nano
def nano_call(chemin):
    init_nano(chemin)

    #variable de continuiter
    continu = True

    #si le fichier n'existe pas le créer
    if not file_exist(chemin):
        try:
            file = open(chemin,'w')
            file.close()
        except Exception as err:
            print(err)
            continu = False

    if continu:
        #lecture du fichier
        read_file(chemin)

        #rectangue exterieur
        cadre_ext = Rect(0,0,320,240,outline = 0x00fff00)

        #création de ligne de text 
        for loop in range(0,16):
            #txt_area2[loop] = label.Label(terminalio.FONT, text="test")
            txt_area2[loop].x = 5
            txt_area2[loop].y = 15 + 12 * (loop + 1)
            txt_area2[loop].color = 0xffffff
            txt_area2[loop].background_color = 0x000000
            screen.append(txt_area2[loop])

        #affichage du corp text
        affiche_variable(index_page)

        #selection de la ligne
        ligne_select()

        #print du haut de page
        txt_area = label.Label(terminalio.FONT, text=(" Nano Text editor    " + chemin + "                        "))
        txt_area.x = 0
        txt_area.y = 6
        txt_area.color = 0x000000
        txt_area.background_color = 0x00ff00
        screen.append(txt_area)

        #print du bas de page
        cmd_sav.text = "     Save     "
        cmd_sav.x = 0
        cmd_sav.y = 233
        cmd_sav.color = 0x000000
        cmd_sav.background_color = 0x00ff00

        #cmd save_as
        cmd_sav_as.text = "    Save as    "
        cmd_sav_as.x = 115
        cmd_sav_as.y = 233
        cmd_sav_as.color = 0x000000
        cmd_sav_as.background_color = 0x00ff00
        
        #cmd_annuler
        cmd_annuler.text = "     Exit        "
        cmd_annuler.x = 235
        cmd_annuler.y = 233
        cmd_annuler.color = 0x000000
        cmd_annuler.background_color = 0x00ff00

        #edite zone
        txt_edit =  label.Label(terminalio.FONT, text="")
        txt_edit.x = 0
        txt_edit.y = 220
        txt_edit.background_color = 0xffffff
        txt_edit.color = 0x0000ff

        #affichage de l'écran
        screen.append(cadre_ext)
        screen.append(txt_edit)
        screen.append(cmd_sav)
        screen.append(cmd_sav_as)
        screen.append(cmd_annuler)
        screen.append(curs_ligne)

        #ajout du prompt
        global cdr_prompt
        global txt_title_prompt
        global txt_chemin_prompt
        global curs_ligne2
        global txt_instruc
        global txt_alert
        
        screen.append(cdr_prompt)
        screen.append(txt_title_prompt)
        screen.append(txt_chemin_prompt)
        screen.append(curs_ligne2)
        screen.append(txt_instruc)
        screen.append(txt_alert)

        board.DISPLAY.root_group = screen
        main_nano()
    else:
        close_nano()
        
#fonction change bouton de de la couleur
def col_bouton():
    global cursor_mode
    global index_bouton
    global cmd_sav
    global cmd_sav_as
    global cmd_annuler

    if cursor_mode:
        if index_bouton == 2:
            cmd_sav.background_color = 0xffaa00
            cmd_sav_as.background_color = 0x00ff00
            cmd_annuler.background_color = 0x00ff00
        elif index_bouton == 1:
            cmd_sav.background_color = 0x00ff00
            cmd_sav_as.background_color = 0xffaa00
            cmd_annuler.background_color = 0x00ff00
        elif index_bouton == 0:
            cmd_sav.background_color = 0x00ff00
            cmd_sav_as.background_color = 0x00ff00
            cmd_annuler.background_color = 0xffaa00
    else:
        cmd_sav.background_color = 0x00ff00
        cmd_sav_as.background_color = 0x00ff00
        cmd_annuler.background_color = 0x00ff00
        time.sleep(1)

#fonction des boutons
def click_bouton():
    global index_bouton
    global main_loop

    if index_bouton == 0:
        main_loop = False

    elif index_bouton == 1:
        sav_as()

    elif index_bouton == 2:
        sav()

#fonction de modification de ligne
def modif_text(press_key):
    global index_ligne
    global index_page
    global index_lettre
    global list_affichage
    global index_colone
    global egal_symbole
    global nbr_ligne_total
    
    #chargement de la ligne text
    try:
        txt_ligne = list_affichage[index_ligne + index_page]
    except:
        None

    txt_modif_ligne = ""
    size = len(txt_ligne)
    num_line_modif = 0

    #recupération du caratère
    carac = ""
    phase_deux = False

    if press_key != None:
        #gestion pour signe =
        if egal_symbole == "_":
            if "-" == press_key:
                carac = "-1"
                carac = carac + "="
            else:
                carac = press_key
            egal_symbole = ""
        
        #gestion pour signe [ et <
        elif egal_symbole == "(":
            if "+" == press_key:
                carac = "-1"
                carac = carac + "["
            elif "-" == press_key:
                carac = "-1"
                carac = carac + "<"
            else: 
                carac = press_key
            egal_symbole = ""

        #gestion pour signe ]
        elif egal_symbole == "+":
            if ")" == press_key:
                carac = "-1"
                carac = carac + "]"
            else:
                carac = press_key
            egal_symbole = ""

        #gestion pour signe >
        elif egal_symbole == "-":
            if ")" == press_key:
                carac = "-1"
                carac = carac + ">"
            else:
                carac = press_key
            egal_symbole = ""

        else:
            #première phase du =
            if "_" == press_key:
                egal_symbole = "_"
                carac = "_"
                phase_deux = True

            #première phase du [ et <
            elif "(" == press_key:
                egal_symbole = "("
                carac = "("
                phase_deux = True

            #première phase ]
            elif "+" == press_key:
                egal_symbole = "+"
                carac = "+"
                phase_deux = True
            
            #première phase >
            elif "-" == press_key:
                egal_symbole = "-"
                carac = "-"
                phase_deux = True
            
            #sinon
            else:
                egal_symbole = ""
                carac = press_key

        #gestion de la ligne
        #effacement
        if  "-1" in carac:
            if len != 0:
                if (index_colone + index_lettre) > 0:
                    #modification du text si pas en début de ligne
                    txt_modif_ligne = txt_ligne[0:(index_colone + index_lettre - 1)] + txt_ligne[(index_colone + index_lettre):size]
                    index_lettre = index_lettre - 1

                    #variable provisoir de ligne
                    num_line_modif = index_ligne
                    
                    #modification de la ligne
                    list_affichage[index_ligne + index_page] = txt_modif_ligne

                else:
                    #modification de ligne si en début de ligne
                    index_lettre = len(list_affichage[index_ligne + index_page - 1]) - 1
                    txt_modif_ligne = list_affichage[index_ligne + index_page - 1] + txt_ligne
                    
                    #modification de la ligne
                    list_affichage[index_ligne + index_page] = txt_modif_ligne

                    #effacement d'une ligne
                    for loop in range((index_ligne + index_page),nbr_ligne_total):
                        list_affichage[loop - 1] = list_affichage[loop]

                    #variable provisoir de ligne
                    num_line_modif = index_ligne - 1

                    #mise a jour nombre de ligne
                    nbr_ligne_total = nbr_ligne_total - 1

                    #supression de la variables si plus de 16 ligne
                    if nbr_ligne_total < 16:
                        nbr_ligne_total = 16
                    else:
                        del list_affichage[nbr_ligne_total]

            #gestion du signe =
            if "=" in carac:
                txt_modif_ligne = list_affichage[index_ligne + index_page] 
                list_affichage[index_ligne + index_page] = txt_modif_ligne + "="
                index_lettre = index_lettre + 1

            #gestion du signe [
            elif "[" in carac:
                txt_modif_ligne = list_affichage[index_ligne + index_page] 
                list_affichage[index_ligne + index_page] = txt_modif_ligne + "["
                index_lettre = index_lettre + 1

            #gestion du signe ]
            elif "]" in carac:
                txt_modif_ligne = list_affichage[index_ligne + index_page] 
                list_affichage[index_ligne + index_page] = txt_modif_ligne + "]"
                index_lettre = index_lettre + 1

            #gestion du signe >
            elif ">" in carac:
                txt_modif_ligne = list_affichage[index_ligne + index_page] 
                list_affichage[index_ligne + index_page] = txt_modif_ligne + ">"
                index_lettre = index_lettre + 1

            #gestion du signe <
            elif "<" in carac:
                txt_modif_ligne = list_affichage[index_ligne + index_page] 
                list_affichage[index_ligne + index_page] = txt_modif_ligne + "<"
                index_lettre = index_lettre + 1

        #gestion retour a la ligne
        elif "+1" in carac:
            #ajouter une variable ligne
            list_affichage.append(list_affichage[nbr_ligne_total - 1])

            #boucle de deplacement
            for loop in range(nbr_ligne_total,(index_ligne + index_page + 1),-1):
                list_affichage[loop] = list_affichage[loop - 1]

            #mise a jour index ligne
            num_line_modif = index_ligne + 1

            #recupération de ligne
            txt = list_affichage[index_ligne + index_page] 
            list_affichage[index_ligne + index_page] = txt[0:index_lettre + index_colone]
            list_affichage[index_ligne + index_page + 1] = txt[index_lettre + index_colone:len(txt)]

            #changement de l'index curseur
            index_lettre = 0

            #maj du nombre de linge
            nbr_ligne_total = len(list_affichage)

        else:
            txt_modif_ligne = list_affichage[index_ligne + index_page]
            list_affichage[index_ligne + index_page] = txt_modif_ligne[0:(index_lettre + index_colone)] + carac + txt_modif_ligne[(index_lettre + index_colone):len(txt_modif_ligne)]
            num_line_modif = index_ligne
            index_lettre = index_lettre + 1

        #modification postion de ligne
        index_ligne = num_line_modif
        ligne_select()
        caracter_select()
        affiche_variable(index_page)

#fonction de sauvgarde sans nom de fichier
def sav():
    global txt_alert
    global nbr_ligne_total
    global cursor_mode

    #verifier si le fichier existe
    if file_exist(url):
        #suprimer le fichier
        os.remove(url)

        #ouvrir le fichier en ecriture
        file = open(url, "w")
        
        #ecriture du fichier
        for loop in range (0,nbr_ligne_total):
            file.write(list_affichage[loop])
            file.write('\n')
        
        file.close()

        #afficher info
        txt_alert.hidden = False
        txt_alert.text = "                  File save                     "
        txt_alert.background_color = 0x00ff00

        #attente avant fermture de l'information
        time.sleep(3)

        #fermture de fichier et sortie du monde curseur
        txt_alert.hidden = True
        cursor_mode = False
        cmd_sav.background_color = 0x00ff00
        cmd_sav_as.background_color = 0x00ff00
        cmd_annuler.background_color = 0x00ff00

#fonction de sauvgarde sous
def sav_as(txt):
    global nbr_ligne_total
    global cdr_prompt
    global txt_title_prompt
    global txt_chemin_prompt
    global curs_ligne2
    global cursor_mode
    global trackball
    global txt_alert
    global list_affichage
    global url

    #init de txt avec l'url complet
    txt = url

    #demande du nom de fichier
    #ouverture de la page prompte
    cdr_prompt.hidden = False
    txt_title_prompt.hidden = False
    txt_chemin_prompt.hidden = False
    curs_ligne2.hidden = False
    txt_instruc.hidden = False

    #arret du mode curseur
    cursor_mode = False
    col_bouton()

    #modification position curseur
    curs_ligne2.x = 105
    curs_ligne2.y = 135

    #variable boucle
    promp = True

    #variable sav
    sav = True

    while promp:
        #maj du chemin
        txt_chemin_prompt.text = "Chemin: " + txt

        #maj de la position du curseur
        curs_ligne2.x = 108 + len(txt) * 6

        #récupération du caratère
        cara = read_clavier.read_keyboard_limit(1)

        #effacement event trackball
        trackball.events.get()

        #si touche entrée est appuyer
        if cara == "+1":
            promp = False
            sav = True
        #si backspace est appuyer
        elif cara == "-1":
            txt = txt[0:len(txt) - 1]
        #si @ est appuyer
        elif cara == 64:
            promp = False
        #sinon ajout de la lettre
        else:
            if cara != None:
                txt = txt + cara

    #verification si non de fichier contien qqc
    if not len(txt) > 0:
        sav = False

    #si enregistrement
    if sav:
        #si le fichier existe
        if file_exist(txt):
            txt_alert.text = "The file already exists do you want to replace it?\n Y = Yes  N = No"
            txt_alert.background_color = 0x0000ff
            txt_alert.hidden = False
            promp = True
            #attente retour user

            while promp:
                cara = read_clavier.read_keyboard_limit(1)
                if cara == "y":
                    promp = False
                    sav = True
                elif cara == "n":
                    promp = False
                    sav = False
        
        #getsion du message
        if sav:
            #effacement du fichier si il existe déjà
            if file_exist(txt):
                os.remove(txt)

            #ouvrir le fichier en ecriture
            file = open(txt, "w")
        
            #ecriture du fichier
            for loop in range (0,nbr_ligne_total):
                file.write(list_affichage[loop])
                file.write('\n')
            
            #fermeture de fichier
            file.close()

            #information fichier sauver
            txt_alert.text = "                  File save                     "
            txt_alert.background_color = 0x00ff00
            txt_alert.hidden = False
        else:
            #information fichier non sauver
            txt_alert.text = "               File not save                     "
            txt_alert.background_color = 0x0000ff
            txt_alert.hidden = False

    else:
        #information fichier non sauver
        txt_alert.text = "               File not save                     "
        txt_alert.background_color = 0x0000ff
        txt_alert.hidden = False
    #attente pour afficher les messages
    time.sleep(3)

    #fermeture de la page prompte
    cdr_prompt.hidden = True
    txt_title_prompt.hidden = True
    txt_chemin_prompt.hidden = True
    curs_ligne2.hidden = True
    txt_instruc.hidden = True
    txt_alert.hidden = True
    
#fonction de fermeture
def close_nano():
    global cursor_mode
    global index_bouton
    global main_loop
    global trackball
    global cdr_prompt
    global txt_title_prompt
    global txt_chemin_prompt
    global curs_ligne2
    global txt_instruc
    global txt_alert

    #dechargement des donnée
    try:
        screen.remove(cmd_sav)
        screen.remove(cmd_sav_as)
        screen.remove(cmd_annuler)
        screen.remove(curs_ligne)
        for loop in range(0,16):
            screen.remove(txt_area2[loop])
        screen.remove(cdr_prompt)
        screen.remove(txt_title_prompt)
        screen.remove(txt_chemin_prompt)
        screen.remove(curs_ligne2)
        screen.remove(txt_instruc)
        screen.remove(txt_alert)
        trackball.deinit()
    except:
        None
    
    storage.remount("/", True)

    board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL  

#boucle principale
def main_nano():
    global cursor_mode
    global index_bouton
    global main_loop
    global trackball
    global cdr_prompt
    global txt_title_prompt
    global txt_chemin_prompt
    global curs_ligne2
    global txt_instruc
    global txt_alert
        

    while main_loop:
        event = trackball.events.get()

        #event click
        if "key_number 0 pressed" in str(event):
            if not cursor_mode:
                cursor_mode = True
                col_bouton()
            else:
                event = trackball.events.get()
                time.sleep(1)
                event = trackball.events.get()
                if "key_number 0 released" in str(event):
                    click_bouton()
                else:
                    cursor_mode = False
                    col_bouton()
        #event up
        elif "key_number 1 pressed" in str(event):
            if not cursor_mode:
                    cmd_up()

        #event down
        elif "key_number 2 pressed" in str(event):
            if not cursor_mode:
                cmd_down()

        #event left
        elif "key_number 3 pressed" in str(event):
            if cursor_mode:
                if index_bouton < 2:
                    index_bouton = index_bouton + 1
                col_bouton()
            else:
                cmd_left()

        #event right
        elif "key_number 4 pressed" in str(event):
            if cursor_mode:
                if index_bouton > 0:
                    index_bouton = index_bouton - 1
                col_bouton()
            else:
                cmd_right()

        #verification clavier
        modif_text(read_clavier.read_keyboard_limit(1))
    
    close_nano()
