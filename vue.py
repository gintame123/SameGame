import tkinter
import modele
from random import *



class VueSame:
    
    def __init__(self, modelesame):

        self.__same = modelesame

        #créer la fenetre principale
        fenetre = tkinter.Tk()
        #titre
        fenetre.title("Same Game")

        # puis on créé chaque composant graphique
        self.__score = tkinter.Label(fenetre, 
                           text="Score : "+str(self.__same.score()),
                           fg="red")
        # on pose le composant sur la fenetre
        self.__score.grid()

        self.__images = [tkinter.PhotoImage(file="img/medium_sphere1.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere2.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere3.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere4.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere5.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere6.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere7.gif"),
                         tkinter.PhotoImage(file="img/medium_sphere8.gif"),
                         tkinter.PhotoImage(file="img/spherevide.gif")]
        self.__les_btns = []
        for i in range(self.__same.nblig()):
            ligne=[]
            for j in range(self.__same.nbcol()):
                n_couleur = self.__same.couleur(i, j)
                grille = tkinter.Button(fenetre,
                                        width = 40,
                                        height = 40,
                                        image = self.__images[n_couleur],
                                        command = self.creer_controleur_btn(i, j))
        

                grille.grid(row=i, column=j)
                ligne.append(grille)
            self.__les_btns.append(ligne)
        
        
        self.__score.grid(row = 4, column = self.__same.nbcol())
        
        # le deuxième composant est un Button
        # un clic sur le bouton fait quitter l'appli
        btn_quitter = tkinter.Button(fenetre, 
                            text="Au revoir",
                            command = fenetre.destroy)
        
        btn_nouveau = tkinter.Button(fenetre, 
                            text="Nouvelle partie",
                            command = self.nouvelle_partie) 

        btn_nouveau.grid(row = 5, column = same.nbcol())
        btn_quitter.grid(row = 6, column = same.nbcol())
        
        # on lance la boucle d'écoute des événements
        fenetre.mainloop()

    def redessine(self):
        '''VueSame -> None
        '''
        for i in range(len(self.__les_btns)):
            for j in range(len(self.__les_btns[i])):
                self.__les_btns[i][j]["image"] = self.__images[self.__same.couleur(i,j)]
        self.__score["text"]="Score : "+str(self.__same.score())
        
    def nouvelle_partie(self):
        '''VueSame -> None
        '''
        same = modele.ModeleSame(self.__same.nblig(),self.__same.nbcol())
        self.__same = same
        self.redessine()

    def creer_controleur_btn(self,i,j):
        '''VueSame, int, int -> controleur_btn()
        '''
        def controleur_btn():
            self.__same.supprime_composante(self.__same.composante(i,j))
            self.redessine()
            
        return controleur_btn
                
if __name__ == "__main__" :
    # création du modèle
    same = modele.ModeleSame()
    # création de la vue qui créé les contrôleurs
    # et lance la boucle d’écoute des évts
    vue = VueSame(same)
