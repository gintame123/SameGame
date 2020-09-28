from random import randint
import string

class Case :
    
    def __init__(self,couleur):
        '''Case, int -> None
        '''
        assert couleur >=0
        self.__couleur = couleur
        self.__compo = -1
    
    def couleur(self):
        '''Case --> int
        Retourne la valeur de la couleur de la Case
        '''
        return self.__couleur
    
    def change_couleur(self,couleurs):
        '''Case, int --> Case(modifier)
        Change la couleur de la Case par celle donner en paramètre
        '''
        self.__couleur = couleurs
        self.__compo = -1
        
    def supprime(self):
        '''Case --> Case(modifier)
        Modifie la valeur de la couleur de la case en -1 pour la mettre vide
        '''
        
        self.__couleur = -1
        self.__compo = 0
    
    def est_vide(self):
        '''Case --> Boolean
        Verifie si la Case est vide
        '''
        return self.__couleur == -1
    
    def composante(self):
        '''Case -> int
        '''
        return self.__compo

    def pose_composante(self,nouv):
        '''Case, int -> None
        '''
        self.__compo = nouv

    def supprime_composante(self):
        if self.est_vide():
            self.__compo = 0
        else:
            self.__compo = -1

    def parcourue(self):
        '''Case -> booleen
        '''
        return self.__compo > 0

 
class ModeleSame :
    
    def __init__(self,nblig=10,nbcol=10,nbcouleur=3):
        
        self.__nblig=nblig
        self.__nbcol=nbcol
        self.__nbcouleur=nbcouleur
        self.__couleur=randint(0,nbcouleur-1)
        self.__mat=[]
        for i in range(nblig):
            ligne=[]
            for j in range(nbcol):
                num=randint(0,nbcouleur-1)
                ligne.append(Case(num))
            self.__mat.append(ligne)
        self.__nb_elts_compo = [0]
        self.calcule_composantes()
        self.__score=0

    def score(self):
        '''ModeleSame -> int
        '''
        return self.__score

    def nblig(self):
        '''ModeleSame -> int
        '''        
        return self.__nblig

    def nbcol(self):
        '''ModeleSame -> int
        '''        
        return self.__nbcol

    def nbcouleurs(self):
        '''ModeleSame -> int
        '''        
        return self.__couleur

    def coords_valides(self,i,j):
        '''ModeleSame, int, int -> booleen
        '''
        return (0<=i<self.nblig() and 0<=j<self.nbcol())

    def couleur(self,i,j):
        '''ModeleSame, int, int -> int
        '''
        return self.__mat[i][j].couleur()

    def supprime_bille(self,i,j):
        '''ModeleSame, int, int -> None
        '''
        self.__mat[i][j].supprime()

    def nouvelle_partie(self):
        '''ModeleSame -> None
        '''
        self.__mat=[]
        for i in range(self.nblig()):
            ligne=[]
            for j in range(self.nbcol()):
                nbcol=randint(0,self.nbcouleurs()-1)
                ligne.append(Case(nbcol))
            self.__mat.append(ligne)

    def composante(self,i,j):
        '''ModeleSame, int, int -> int
        '''
        return self.__mat[i][j].composante()

    def calcule_composantes(self):
        '''ModeleSame -> None
        '''
        self.__nb_elts_compo = [0]
        num_compo = 1
        for i in range(len(self.__mat)):
            for j in range(len(self.__mat[i])):
                if self.composante(i,j) == -1:
                    coul = self.couleur(i,j)
                    self.__nb_elts_compo.append(self.calcule_composante_numero(i, j,num_compo,coul))
                    num_compo+=1

    def calcule_composante_numero(self,i,j,num_compo, couleur):
        '''ModeleSame, int, int, int, int -> int
        '''
        if self.__mat[i][j].parcourue() or self.__mat[i][j].couleur() != couleur:
            return 0
        else :
            self.__mat[i][j].pose_composante(num_compo)
            var = 1
            if self.coords_valides(i-1,j):
                var += self.calcule_composante_numero(i-1,j,num_compo,couleur)
            if self.coords_valides(i+1,j):
                var += self.calcule_composante_numero(i+1,j,num_compo,couleur)
            if self.coords_valides(i,j+1):
                var += self.calcule_composante_numero(i,j+1,num_compo,couleur)
            if self.coords_valides(i,j-1):
                var += self.calcule_composante_numero(i,j-1,num_compo,couleur)
            return var

    def recalc_composantes(self):
        '''ModeleSame -> None
        '''
        for ligne in range(len(self.__mat)):
            for colonne in range(len(self.__mat[ligne])):
                self.__mat[ligne][colonne].supprime_composante()
        self.calcule_composantes()
        
    def supprime_composante_colonne(self, j, num):
        '''Modelesame, int, int -> None
        '''
        for ligne in range(len(self.__mat)):
            if self.__mat[ligne][j].composante() == num:
                self.supprime_bille(ligne, j)
                if ligne !=0:
                    var = self.__mat[ligne][j]
                    for i in range(ligne,0,-1):
                        self.__mat[i][j] = self.__mat[i-1][j]
                    self.__mat[0][j] = var
                    

    def supprime_composante(self ,num):
        '''ModeleSame, int -> int
        '''
        if self.__nb_elts_compo[num]>=2:
            for colonne in range(len(self.__mat[0])):
                self.supprime_composante_colonne(colonne,num)
            self.supprime_colonnes_vides()
            self.__score += (self.__nb_elts_compo[num]-2)**2
            self.recalc_composantes()
            return True
        return False

    def est_vide(self,i,j):
        '''ModeleSame, int, int -> booleen
        '''
        return self.__mat[i][j].est_vide()

    def est_colonne_vide(self,j):
        '''ModeleSame, int -> None
        '''
        for i in range(len(self.__mat)):
            if (not(self.est_vide(i,j))):
                return False
        return True

    def supprime_colonnes_vides(self):
        '''Modelesame -> None
        '''
        for i in range(len(self.__mat[0])):
            if self.est_colonne_vide(i):
                col_vide = self.trouve_colonne_vide()
                for i in range(len(col_vide)):
                    self.decale_colonne(col_vide[i]-i)

    def trouve_colonne_vide(self):
        '''Modelesame -> list
        '''
        l_var =[]
        l_cmpt= []
        for i in range(len(self.__mat[0])):
            if self.est_colonne_vide(i):
                l_cmpt += [i]
            else:
                l_var += l_cmpt
                l_cmpt = []
        return l_var

    def decale_colonne(self,j):
        '''ModeleSame, int -> None
        '''
        for ligne in range(len(self.__mat)):
            var = self.__mat[ligne][j]
            for i in range(j,len(self.__mat[0])-1):
                self.__mat[ligne][i] = self.__mat[ligne][i+1]
            self.__mat[ligne][len(self.__mat[0])-1] = var
