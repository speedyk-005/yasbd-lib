from yasbd.rules.base import Rules


# fmt: off
class TrRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social & Address
        "sn", "han", "hz",

        # Standard Professional / Academic (Shared & Native)
        "av", "bşk", "uzm", "md", "müh", "mim", "ecz",
        "doç", "ord", "yrd", "gör", "arş",

        # Military Ranks & Administration
        "alb", "bnb", "tğm", "ütğm", "atğm", "yzb", "yarb",
        "korg", "tümg", "tuğg", "org", "bçvş", "çvş", "üçvş",
        "onb", "astsb", "asb", "sb", "gnkur", "kur",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "T.C", "A.B.D", "K.K.T.C", "İng", "Alm", "Fr", "Rus",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "s", "ss", "c",  "yay", "yy", "doğ", "vb", "v.b",
        "sf", "mad", "par", "böl", "bzk", "md", "sy",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Bibliographical & reference abbreviations
        "vb", "bnz", "ör", "drl", "dzl", "bk", "bkz",
        "bknz", "çev", "haz",

        # Academic & subject abbreviations
        "huk", "ekon", "jeol", "ped",

        # Address elements
        "mah", "cad", "sok", "sk", "bul", "blv",
        "apt", "il", "ilç", "şti",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Bölüm", "Kısım", "Madde", "Fıkra", "Bent",
        "Paragraf", "Tablo", "Şekil", "Giriş", "Sonuç",
        "Özet", "Önsöz", "Ek", "Kaynakça", "Kaynaklar",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "oca", "şub", "mar", "nis", "may", "haz", "tem", "ağu",
        "eyl", "eki", "kas", "ara",

        # Days
        "pzt", "sal", "çar", "per", "cum", "cmt", "paz",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        # Banking & Telecommunications
        "Akbank", "Garanti", "Vodafone", "Turkcell", "Türk Telekom",

        # E-commerce, Delivery & Retail
        "Yemeksepeti", "Trendyol", "Hepsiburada", "Getir", "n11",
        "Migros", "A101", "BİM", "ŞOK", "CarrefourSA",

        # Shopping, Fashion & Lifestyle
        "ÇiçekSepeti", "LC Waikiki", "Gratis", "Watsons",
        "MediaMarkt", "Teknosa", "Koçtaş", "Mavi", "Penti",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Ben", "Sen", "O", "Biz", "Siz", "Onlar", "Bu",
        "Şu", "Bunlar", "Şunlar",

        # Question Words
        "Hangi", "Kim", "Nasıl", "Ne", "Neden", "Nerede",
        "Niçin",

        # Conjunctions & Transitions
        "Ama", "Ancak", "Ayrıca", "Bundan", "Dolayısıyla",
        "Fakat", "Halbuki", "İlk", "Lakin", "Mesela", "Oysa",
        "Sonra", "Sonuçta", "Yani", "Zaten", "Çünkü",
        "Öncelikle", "Örneğin", "Üstelik",
    }

# fmt: on
