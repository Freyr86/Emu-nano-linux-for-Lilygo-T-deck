# Emu-nano-linux-for-Lilygo-T-deck
Français:  
Emulateur de l'éditeur Nano Linux pour le Lilygo T-Deck, permettant la modification des fichiers directement sur le T-Deck.

Cela peut être utile pour du développement mobile rapide sans avoir à connecter votre T-Deck à un PC. Idéal pour les développeurs voyageurs comme moi :-)

Le module est basé sur deux bibliothèques graphiques d'Adafruit que vous trouverez sur ces pages.

https://github.com/ladyada/Adafruit_CircuitPython_Display_Shapes
https://github.com/adafruit/Adafruit_CircuitPython_Display_Text

Ainsi que sur le module `clavier_gestion.py`, qui est une modification du module de gestion du clavier créé par RetiredWizard. Merci à lui pour son aide et ses conseils.

Son GitHub
https://github.com/RetiredWizard

Vous trouverez tous les fichiers nécessaires directement dans le dépôt.

Pour lancer l'éditeur, importez la bibliothèque et le module.

taper:
nano(_nom du fichier_)

Si le nom de fichier n'existe pas, Nano le crée directement.

Une fois l'interface ouverte, le trackball sert à naviguer entre les lignes et les caractères. Si vous appuyez sur le trackball, vous passez en mode curseur et pouvez choisir les options dans le menu. Un autre appui court permet de sélectionner la commande voulue. Pour sortir sans valider d'option, effectuez un appui long jusqu'à ce que les trois boutons redeviennent verts.

J'espère sincèrement que ce module apportera un outil utile aux autres développeurs.

Vos commentaires et suggestions sont les bienvenus.

Bien que je sois francophone, les zones de texte sont en anglais, mais les commentaires sont en français.





English:
Emulator of the Nano Linux text editor for the Lilygo T-Deck, enabling direct file modification on the T-Deck.

This can be useful for rapid mobile development without needing to connect your T-Deck to a PC. Ideal for traveling developers like me :-)

The module is based on two Adafruit graphic libraries that you can find on these pages:

https://github.com/ladyada/Adafruit_CircuitPython_Display_Shapes
https://github.com/adafruit/Adafruit_CircuitPython_Display_Text

It also relies on the `clavier_gestion.py` module, which is a modification of the keyboard management module created by RetiredWizard. Thanks to him for his assistance and advice.

His GitHub:
https://github.com/RetiredWizard

You will find all the necessary files directly in the repository.

To launch the editor, import the library and the module.

Type:
```
nano(_file name_)
```

If the file name does not exist, Nano creates it directly.

Once the interface is open, the trackball is used to navigate between lines and characters. If you press the trackball, you enter cursor mode and can choose options in the menu. Another short press allows you to select the desired command. To exit without validating an option, perform a long press until the three buttons turn green.

I sincerely hope that this module will provide a useful tool for other developers.

Your comments and suggestions are welcome.

