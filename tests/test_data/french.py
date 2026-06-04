ISO_CODE = "fr"
TEST_DATA = [
    # Basic punctuation
    "Bonjour tout le monde.| Comment allez-vous?| Je vais bien.",
    "Quel est votre nom?| Mon nom est Pierre.",
    "Le voilà!| Je l'ai trouvé.",

    # Abbreviations
    "M. Dupont est un professeur.",
    "Veuillez consulter la p. 55 du livre.",
    "Voir fig. 3 dans le chap. 5.",
    "L'ouvrage est publié dans le t. II du recueil.",
    "Le rapport a été publié en janv. 2024.",
    "Elle est arrivée un lun. matin.",
    "Rendez-vous au 12 av. des Champs-Élysées.",
    "Ils habitent au 5 bd. Saint-Michel.",
    "L'ambassadeur a rencontré LL. AA. le prince et la princesse.",

    # structural headings
    "Chapitre 1. Introduction.| Il faisait sombre. | Rien ne bougeait.",
    "Partie II. Analyse.| Le système commence ici. | L’initialisation suit.",
    "Les données ont été validées.| Chapitre 4. Méthodologie.",

    # Parentheses and quotes
    "Il a dit (Je viendrai demain.) pendant la réunion.",
    "Il a demandé: Êtes-vous prêt?| J'ai répondu oui.",
    "Léa dit : « Bonjour ! Je suis Léa. Et toi ? »",
    'Elle s\'est tournée vers lui, "C\'est magnifique." dit-elle.',

    # Ellipsis
    "Le projet était presque terminé... mais nous avons trouvé un problème.",
    'Il a dit: "Comment avons-nous pu manquer cela!..."| Puis il s\'en va.',
]
