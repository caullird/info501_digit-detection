# import des bibliotheques
from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class image:
    # Initialisation d'une image composee d'un tableau 2D vide
    # (pixels) et de 2 dimensions (H = height et W = width) mises a 0
    def __init__(self):
        self.pixels = None 
        self.H = 0
        self.W = 0
        
    # Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
    # et affectation des dimensions de l'image self avec les dimensions 
    # du tableau 2D (tab_pixels) 
    def set_pixels(self, tab_pixels):
        self.pixels = tab_pixels
        self.H,self.W = self.pixels.shape 

    # Lecture d'un image a partir d'un fichier de nom "file_name"
    def load_image(self, file_name):
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")

    # Affichage a l'ecran d'une image
    def display(self, window_name):
        fig=plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide")
            

    #==============================================================================
    # Methode de binarisation
    #   2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================

    def binaris(self,seuil):
    
        # creation d'une image vide 
        im_binarise = image()
        # affectation de l'image avec la même taille que l'image de base
        im_binarise.set_pixels(np.zeros((self.H,self.W), dtype=np.uint8))
                                                
        # parcours de l'ensemble des pixels en hauteur et en largeur
        for l in range(self.H):
            for c in range(self.W):
                # Verification du seuil passé en paramètre
                if self.pixels[l][c] >= seuil:
                    im_binarise.pixels[l][c] = 255
                else :
                    im_binarise.pixels[l][c] = 0
        return im_binarise
    
        
    
    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================

    def localisation(self):
        
        im_bin = self.binaris(150)
        
        #Instantiation des variable 
        l_min = l_max = c_min = c_max = None
        
        #Création des tableaux de resultat pour la hauteur et la largeur
        result_l = []
        result_c = []
        
        #Parcours de l'ensemble des pixels
        for l in range(im_bin.H):  
            # Pour chaque colonnes de pixels sur la hauteur, 
            # si il y a un pixel noir on l'ajoute au tableau
            if 0 in im_bin.pixels[l]:
                result_l.append(l)                     
            for c in range(im_bin.W):
                # Pour chaque ligne de pixels sur la largeur, 
                # si il y a un pixel noir on l'ajoute au tableau
                if 0 == im_bin.pixels[l][c]:
                    result_c.append(c)
           
         # Nous avons maintenant des tableau contenant toutes les lignes et colonnes qui comportent des
         # pixels noirs, pour avoir les lignes extremes nous pouvons utiliser la fonction min() et max()
         
        l_min = min(result_l)
        l_max = max(result_l)
        c_min = min(result_c) 
        c_max = max(result_c) 
        
        
        
        #On crée une nouvelle image vide, on set les pixels avec les valeurs récupère précédement
        im_modif = image()
        im_modif.set_pixels(im_bin.pixels[l_min:l_max+1,c_min:c_max+1])
    
        return im_modif
    
    
      
    #==============================================================================
    # Methode de redimensionnement d'image
    #
    # Permet de redimmentionner l'image en fonction de deux parametre, un nouveau
    # H et un nouveau W.
    #
    #==============================================================================

    def resize_im(self,new_H,new_W):
        
        # Création d'une nouvelle image vide
        im_resized = image()
        
        # Création d'un tableau de valeur en fonction des nouvelles mesures de H et de W
        tableau_de_pixels = resize(self.pixels, (new_H, new_W),0)
        tableau_de_pixels = np.uint8(tableau_de_pixels*255)
        
        #Ajout du tableau de pixels dans l'image
        im_resized.set_pixels(tableau_de_pixels)
        

        return im_resized

    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================

    def simil_im(self,im):
      
        #Modification de la taille de  l'image de base en fonction de l'image de test
        self = self.resize_im(im.H,im.W)

        #Creation de compteur 
        count_pixels_total = 0
        count_pixels_egale = 0

        #Parcours de l'ensemble des pixels en hauteur est en largeur
        for l in range(im.H):
            for c in range(im.W):
                #Compteur pour ajouter à chaque fois le pixels
                count_pixels_total += 1

                #Si la valeur des pixels est la meme sur les deux images
                if self.pixels[l][c] == im.pixels[l][c]:
                    count_pixels_egale += 1 
          
        #Retour d'un % de ressemblance              
        return (count_pixels_egale / count_pixels_total) *100
    
   
# fin class image


#==============================================================================
#  Fonction de lecture des fichiers contenant les images modeles et des tests
#  Les differentes images sont mises dans des listes
#==============================================================================

def lect_modeles():

    fichiers= ['_0.png','_1.png','_2.png','_3.png','_4.png','_5.png','_6.png','_7.png','_8.png','_9.png']
    list_model = []
    for fichier in fichiers:
        model = image()
        model.load_image(fichier);
        list_model.append(model)
    return list_model

def lect_tests():

    fichiers= ['test1.JPG','test2.JPG','test3.JPG','test4.JPG','test5.JPG','test6.JPG','test7.JPG']
    list_test = []
    for fichier in fichiers:
        model = image()
        model.load_image(fichier);
        list_test.append(model)
    return list_test
   
#==============================================================================
#
# FONCTIONS DE TEST
#
#==============================================================================

if __name__ == '__main__': 

    img = image()

    img.load_image('test10.JPG')
    img.display("image initiale")

    #==============================================================================
    # Binarisation
    #
    # Fonction de binarisation de l'image, passage d'un seuil en paramètre 
    #
    #==============================================================================
    
    img_binariser = img.binaris(150)
    img_binariser.display("Binarisation : Fonction binaris()")
        


    #==============================================================================
    # Localisation chiffre
    #
    # Localisation de l'image, pour cela nous prenons une image qui est binarisé
    #
    #==============================================================================

    img_recadrer = img_binariser.localisation()
    img_recadrer.display("Image recadré : Fonction localisation()")


    #==============================================================================
    # Test de la fonction resize
    # 
    # Modification de la taille de l'image avec pour dimension H: 60 et W:100
    #
    #==============================================================================

    img_resize = img_recadrer.resize_im(60,100)
    img_resize.display("Image resize : Fonction resiz()")


    #==============================================================================
    # Test de la fonction similitude
    #
    # Pour tester cette méthode plusieurs tests : 
    #   -> Similitude entre l'image et elle même (objectif 100%)
    #   -> Similitude entre l'image est son inverse
    #
    #==============================================================================

    img_similitude_meme_image = img.simil_im(img)
    print('ressemblance de ' + str(img_similitude_meme_image) + '%')

    img_inverser = image()

    #Inversion de l'image (tout les pixels 255 deviennent 0 et inversement)
    img_inverser.set_pixels(255-img.pixels)
    img_similitude_inverser = img.simil_im(img_inverser)

    print('ressemblance de ' + str(img_similitude_inverser) + '%')


    #==============================================================================
    # Lecture des chiffres modeles
    # Mesure de similitude entre l'image et les modeles 
    # et recherche de la meilleure similitude
    #==============================================================================


    def Comparaisons_all():
        #Récupération de tableau avec l'ensemble des images
        list_model = lect_modeles()
        list_test = lect_tests()


        #Parcours de l'ensembler des images à tester
        for img_test in list_test:

            #Creation d'un tableau vide de résultats
            tableau_resultat = []

            #Mise en place d'une binarisation et d'une localisation
            img_test = img_test.localisation()
            
            #Parcours de l'ensemble des images à tester
            for img_model in list_model:

                #Ajout du calcul de pourcentage dans le tableau global
                tableau_resultat.append(img_test.simil_im(img_model))
                
            #Affichage pour chaque modèle a tester de la meilleure correspondance   
            print(str(tableau_resultat.index(max(tableau_resultat))) + ' pour une ressemblance de ' + str(max(tableau_resultat)) + '%')
        
      
    Comparaisons_all()