# English test data for yasbd
# Format: (input_text, expected_sentences)

ISO_CODE = "en"
TEST_DATA = [
    # Basic punctuation
    "Hello world.| How are you?| I'm fine.",
    "What is your name?| My name is Jonas.",
    "There it is!| I found it.",
    "Did you remove num 2.| Put it back.",
    "Her email is Jane.Doe@example.com.| I sent her an email.",
    "The site is: https://www.example.50.com/new-site/awesome_content.html.| Please check it out.",

    # Abbreviations
    "My name is Jonas E. Smith.",
    "Please turn to p. 55.",
    "Were Jane and co. at the party?",
    "They closed the deal with Pitt, Briggs & Co. at noon.",
    "Let's ask Jane and co.| They should know.",
    "I can see Mt. Fuji from here.",
    "St. Michael's Church is on 5th st. near the light.",
    "That is JFK Jr.'s book.",
    "I visited the U.S.A. last year.",
    "I live in the E.U.| How about you?",
    "I work for the U.S. Government in Virginia.",
    "I have lived in the U.S. for 20 years.",
    "She has $100.00 in her bag.",
    "She has $100.00.| It is in her bag.",
    "The meeting is at 2 p.m.| Please be on time.",
    "Q. What is his name?| A. His name is Alfred E. Sloan.",
    "I need you to find 3 items, e.g. a hat, a coat, and a bag.",
    "The report was published in Dec.| It was approved by Prof. Smith and Dr. Jones.",
    "The agreement was signed by A.B. Holdings Ltd. in 2024",
    "The temperature reached 37.5°C at 6 a.m. on Tue., Feb. 4.",
    "See fig. 2 in vol. 3, ch. 4, pp. 18-22.",
    "The proof is shown in eq. (7) and ex. IV",
    "Mr. Smith lives on Hwy. 7 near Ave. Central.",
    "The delivery van broke down right in front of Sunset Blvd.| The driver called a tow truck.",
    "I'll see you on Fri., Feb. 14th. ",
    "A. B. said hello.| Then C. D. replied.",
    "You can find it at N°. 1026.253.553.| That is where the treasure is.",
    "We make a good team, you and I.| Did you see Albert I. Jones yesterday?",

    # Parentheses and quotes
    "He teaches science (He previously worked for 5 years as an engineer.) at the local University.",
    "(See Fig. 4. This outlines the memory layout.)| The engine executes next.",
    'She turned to him, "This is great." she said.',
    'She turned to him, "This is great."| She held the book out to show him.',
    "Can you believe how much money he has made from his Where's Wally? series of books (published in the US as Where's Waldo?)?",
    "According to his publisher, Smith bought the company in 1985 [or 1984?], but he wasn't active in its management until 1990.",
    'Then he stop.| "wait" he said',
    "The letter concluded with a simple warning: 'Do not follow me.'| Then she left.",
    'He said: "First sentence. Second sentence."| Then done.',

    # Contiguous terminators
    "Hello ! ! ! !",
    "Hello!!| Long time no see.",
    "Hello!?| Is that you?",
    "Hello!? !! ?!| Is that you?",

    # Lists
    "1.) The first item.| 2.) The second item.",
    "a) The first item.| b) The second item.",
    "1. The first item.| 2. The second item.",
    "• 9. The first item.| • 10. The second item.",

    # Elipsis/TOC leaders
    "The project (Sinta) was nearing completion... or so we thought.",
    '"How could we miss this!..."| Mark shouted, slamming his hand on the desk.',
    "We found a memory leak in the C# wrapper....| It was subtle.",
    f"Why Complex Carbohydrates{'.' * 15} 19",

    # Exclamation words
    "We spent the afternoon playing Adopt Me! on the computer while eating Chips Ahoy! cookies.",
    "My dad logged into Yahoo! finance to check on Yum! Brands stock performance before dinner.",
    "Yahoo!| The server is down.",

    # Mixed language
    "我喜欢AI。|It is useful",
    "The meeting is at 2 p.m.| 请别迟到。",
    "那个会议在下午两点。|Please don't be late!",
]
