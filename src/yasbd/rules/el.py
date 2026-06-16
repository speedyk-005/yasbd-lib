from yasbd.rules.base import Rules


# fmt: off
class ElRules(Rules):


    # Greek uses the Greek question mark (；) [U+037E] instead of the standard (?) [U+003F].
    TERMINATORS = Rules.TERMINATORS | {";"}

    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "κ", "κκ", "κα", "κος", "δις", "δισ",
        "δρ", "δρα", "καθ", "υποψ", "αναπλ", "επίκ",
        "υπ", "πρόεδρ", "περιφ", "συμβ", "πρωτ", "εισαγγ",
        "αθ", "αλεξ", "δημ", "ιωαν", "νικ", "χαρ", "χρ", "βασ",
        "γρ", "γ.γ", "διόν", "θεμ", "θεοδ", "μιλτ", "μιχ", "φιλ",

        # Military ranks
        "στρ", "αντ/γος", "ταξ", "ταξ/ρχος", "συντ", "τάγμ", "λοχ",
        "ανθπγ", "υπαστ",

        # Noble / Royal / Religious
        "αγ", "αρχιμ", "μητρ", "επίσκ", "πρ", "πρεσβ",
        "πρωτοπρ", "διάκ", "σεβ", "μακαρ",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        # Core & Historical
        "Η.Π.Α", "Ε.Ε", "Ο.Η.Ε", "Η.Β", "Ε.Σ.Σ.Δ", "Κ.Δ", "Π.Δ",

        # Asia / Middle East
        "Υ.Α.Ε", "Π.Ρ.Κ", "Ρ.Ο.Κ",

        # Major International Organizations
        "Ν.Α.Τ.Ο", "Υ.Ν.Ε.Σ.Κ.Ο", "Π.Ο.Υ", "Δ.Ν.Τ", "Π.Ο.Ε",
        "Ο.Π.Ε.Κ", "Ο.Τ.Σ", "Δ.Ε.Α", "Δ.Τ",

        # Regional Organizations
        "Α.Ε", "Ο.Α.Κ", "Α.Σ.Ε.Α.Ν",

        # Other sovereign states
        "Λ.Δ.Κ", "Ν.Α", "Λ.Δ.Κ.Γ",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographic & Layout structure
        "τομ", "τόμ", "σελ", "αρ", "παρ", "εδ", "τχ", "περ", "εκδ", "έκδ",
        "κεφ", "άρθρ", "αριθ", "αριθμ", "γραμμ", "σ", "γεν",

        # Citations & Comparisons
        "βλ", "βλ.σχ", "πρβλ", "εικ", "πίν",

        # Academic Shorthands & Structural Markers
        "χ.χ", "χ.τ", "χ.μ", "χγρ", "σ.σ",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Κεφ", "Κεφάλαιο", "Άρθρ", "Άρθρο", "Τομ", "Τόμος", "Τεύχος", "Τχ",
        "Παρ", "Παράγραφος", "Τμήμα", "Ενότητα", "Εδάφιο", "Εδ",
        "Παράρτημα", "Βιβλίο", "Μέρος", "Εισαγωγή",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Document
        "π.χ", "λ.χ", "δηλ", "σημ", "υποσημ", "εξ",
        "κ.ε", "κ.εξ", "τηλ",

        # Street
        "οδ", "λεωφ", "λεωφ_εθν_αντ", "πλ",
        "παρ", "περ", "οικ", "τμ"
    }

    NAMES_WITH_EXCLAMATION = {
        # Domestic and highly active digital platforms / retail
        "efood!", "jumbo!", "skroutz!", "box!", "wolt!", "viva!", "public!",

        # Media, entertainment, and youth lifestyle brands
        "ciao!", "down town!", "mad!", "yolo!",

        # Commercial promotional markers (frequently injected inline)
        "προσφορά!", "στοπ!", "super!", "extra!", "bazaar!", "sales!"
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "ιαν", "φεβ", "φεβρ", "μαρ", "μάρτ", "απρ", "μαϊ", "μάι",
        "ιουν", "ιούν", "ιουλ", "ιούλ", "αυγ", "αύγ", "σεπ", "σεπτ",
        "οκτ", "νοε", "νοέμ", "δεκ",

        # Days
        "δευ", "τρι", "τετ", "πεμ", "παρ", "σαβ", "κυρ",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "Ο", "Η", "Το", "Οι", "Τα", "Ένας", "Μια", "Ένα",

        # Pronouns
        "Εγώ", "Εμείς", "Εσύ", "Εσείς", "Αυτός", "Αυτή", "Αυτό", "Αυτοί", "Αυτές", "Αυτά",
        "Εκείνος", "Εκείνη", "Εκείνο", "Εκείνοι", "Εκείνες", "Εκείνα", "Εδώ", "Εκεί",

        # Question words
        "Ποιος", "Ποια", "Ποιο", "Ποιοι", "Ποιες", "Τι", "Πού", "Πότε", "Γιατί", "Πώς",
        "Ποιανού", "Ποιανής", "Ποιον", "Ποιαν",

        # Adverbs
        "Ωστόσο", "Επιπλέον", "Εντούτοις", "Επομένως", "Συνεπώς", "Εντωμεταξύ", "Εξάλλου",
        "Επίσης", "Διαφορετικά", "Τότε", "Μετά", "Αργότερα", "Επί του παρόντος", "Τέλος",
        "Αρχικά", "Στη συνέχεια", "Έπειτα", "Τελευταία", "Πρώτα", "Δεύτερον", "Τρίτον",
        "Τελικά", "Προηγουμένως",

        # Other common starters
        "Κάνεις", "Έκανε", "Έκαναν", "Κάνουν", "Εκατομμύρια",
    }

# fmt: on
