from yasbd.rules.base import Rules


# fmt: off
class AmRules(Rules):
    # Ethiopic terminators only, base would split dotted abbreviations
    TERMINATORS = {"።", "፧", "!"}

    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social & Professional
        "አቶ", "ወ/ሮ", "ወ/ሪት", "ዶ/ር", "ፕ/ሮፌሰር", "ኢንጂነር",

        # Traditional Honorifics
        "ራስ", "ልጅ",
    }

    DOTTED_GEOPOL_ABBRVS = {
        # International Countries & Blocs
        "አ.ሜ.ሪ.ካ", "ዩ.ኤስ.ኤ", "ዩ.ኬ", "ዩ.ኤ.ኢ", "ኢ.ፌ.ዴ.ሪ", "ሶ.ቪ.የ.ት",

        # Global / Regional Organizations
        "ተ.መ.ድ", "አ.ህ", "የ.መ.መ.ድር", "የ.ዓ.ባ",

        # Directions / Hemispheres
        "ሰ.ም", "ደ.ቡ", "ም.ራ", "ም.ስ",

        # Regional Subdivisions & Local Government
        "አ.አ", "ድ.ዳ", "ክ.ሀ", "ወ.ረ",
    }

    REFERENCE_ABBRVS = {
        # Publishing / Documents
        "ዕ.ሕ.", "ማ.ታ.", "ም.ዕ.", "ቅ.ጽ.", "ገ.ቁ.", "ገ.", "ም.", "ቅ.", "ማ.", "ማጣ.",

        # Structure / Numbering
        "ክ.ፍ.", "ክፍ.", "አን.", "አንቀ.", "ምዕ.", "ዓ.ም.", "ን.ክ.",
        "ቁ.", "ቁ.ጥር", "ተ.ቁ.", "እ.ኤ.አ.", "ቅ.ክ.", "ተ.ማ.", "ዋ.ማ.", "ዝ.ከ.",

        # General / Measurements
        "ግድ.", "ያህ.", "ደ.ረ.", "ሚ.ሊ.", "ኪ.ግ.", "ሜ.", "ሴ.ሜ.", "ሊ.", "ኪ.ሜ.", "ከ.", "እስ.",
        "ስ.ቁ.", "ቴ.ሌ.", "ዩኒ.", "ኮ.ሌ.", "መ.በ.", "ሳ.ሳ.",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "አልወለድም", "ጉድ", "እንቆቅልሽ",
        "ዋይ", "ዋናው", "የትም ፍጪው", "ባይ ባይ",
        "እሪታ", "አልፋ", "እንቅስቃሴ", "ቶሎ",
        "አዎ", "እልል",
    }

    QUOTATIVE_PARTICLES = {
        # Standalone Converb Quotatives ("Saying...", placed after a quote)
        "ብሎ", "ብላ", "ብለው", "ብዬ", "ብለን", "ብላችሁ",

        # Active/Imperfect Quotative Verbs ("While saying / As says")
        "ሲል", "ስትል", "ሲሉ", "ስል",

        # Subordinating Prefix (Matches "that...", attached to verbs)
        "እንደ-",    # inde- (e.g., እንደተናገረው - "as he said")
    }

# fmt: on
