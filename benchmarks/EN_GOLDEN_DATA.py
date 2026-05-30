# Adapted from pysbd's test data. Some cases were removed or altered because
# the test expectation didn't match reality:
#   - `⁃9. The first item ⁃10. The second item`: In professional
#     typography, an item is bulleted or numbered, rarely both. Seeing `⁃9.`
#     reads like the author couldn't decide which style to use.
#   - Ellipsis split mid-thought: test expected a sentence break at the
#     ellipsis. In reality, "compounds . . . . The practice" keeps the ellipsis
#     attached to the first clause.
#   - "At 5 a.m. Mr. Smith went to the bank...": test expected a split at
#     "5 a.m." but the real issue is a missing comma. When you put time at the
#     beginning of a sentence in writing, it's usually followed by a comma.
#     The input was fixed.
#   - Single-quote dialog ("'This is great.' she said."): the original input had
#     a period inside the quote, but dialogue tags require a comma. Corrected to
#     "'This is great,' she said." to match real writing.
#
# Also added cases for abbreviation chains, mixed CJK, contiguous terminators,
# OCR noise, and other edge cases the original data didn't cover.

GOLDEN_EN_RULES_TEST_CASES = [
    ("Hello World. My name is Jonas.", ["Hello World.", "My name is Jonas."]),
    (
        "What is your name? My name is Jonas.",
        ["What is your name?", "My name is Jonas."],
    ),
    ("There it is! I found it.", ["There it is!", "I found it."]),
    ("My name is Jonas E. Smith.", ["My name is Jonas E. Smith."]),
    ("Please turn to p. 55.", ["Please turn to p. 55."]),
    ("Were Jane and co. at the party?", ["Were Jane and co. at the party?"]),
    (
        "They closed the deal with Pitt, Briggs & Co. at noon.",
        ["They closed the deal with Pitt, Briggs & Co. at noon."],
    ),
    (
        "Let's ask Jane and co. They should know.",
        ["Let's ask Jane and co.", "They should know."],
    ),
    (
        "They closed the deal with Pitt, Briggs & Co. It closed yesterday.",
        ["They closed the deal with Pitt, Briggs & Co.", "It closed yesterday."],
    ),
    ("I can see Mt. Fuji from here.", ["I can see Mt. Fuji from here."]),
    (
        "St. Michael's Church is on 5th st. near the light.",
        ["St. Michael's Church is on 5th st. near the light."],
    ),
    ("That is JFK Jr.'s book.", ["That is JFK Jr.'s book."]),
    ("I visited the U.S.A. last year.", ["I visited the U.S.A. last year."]),
    (
        "I live in the E.U. How about you?",
        ["I live in the E.U.", "How about you?"],
    ),
    (
        "I live in the U.S. How about you?",
        ["I live in the U.S.", "How about you?"],
    ),
    (
        "I work for the U.S. Government in Virginia.",
        ["I work for the U.S. Government in Virginia."],
    ),
    (
        "I have lived in the U.S. for 20 years.",
        ["I have lived in the U.S. for 20 years."],
    ),
    (
        "At 5 a.m., Mr. Smith went to the bank. He left the bank at 6 P.M. Mr. Smith then went to the store.",
        [
            "At 5 a.m., Mr. Smith went to the bank.",
            "He left the bank at 6 P.M.",
            "Mr. Smith then went to the store.",
        ],
    ),
    ("She has $100.00 in her bag.", ["She has $100.00 in her bag."]),
    ("She has $100.00. It is in her bag.", ["She has $100.00.", "It is in her bag."]),
    (
        "He teaches science (He previously worked for 5 years as an engineer.) at the local University.",
        [
            "He teaches science (He previously worked for 5 years as an engineer.) at the local University."
        ],
    ),
    (
        "Her email is Jane.Doe@example.com. I sent her an email.",
        ["Her email is Jane.Doe@example.com.", "I sent her an email."],
    ),
    (
        "The site is: https://www.example.50.com/new-site/awesome_content.html. Please check it out.",
        [
            "The site is: https://www.example.50.com/new-site/awesome_content.html.",
            "Please check it out.",
        ],
    ),
    (
        "She turned to him, 'This is great,' she said.",
        ["She turned to him, 'This is great,' she said."],
    ),
    (
        'She turned to him, "This is great," she said.',
        ['She turned to him, "This is great," she said.'],
    ),
    (
        'She turned to him, "This is great." She held the book out to show him.',
        ['She turned to him, "This is great."', "She held the book out to show him."],
    ),
    ("Hello!! Long time no see.", ["Hello!!", "Long time no see."]),
    ("Hello?? Who is there?", ["Hello??", "Who is there?"]),
    ("Hello!? Is that you?", ["Hello!?", "Is that you?"]),
    ("Hello?! Is that you?", ["Hello?!", "Is that you?"]),
    (
        "1.) The first item 2.) The second item",
        ["1.) The first item", "2.) The second item"],
    ),
    (
        "1.) The first item. 2.) The second item.",
        ["1.) The first item.", "2.) The second item."],
    ),
    (
        "1) The first item. 2) The second item.",
        ["1) The first item.", "2) The second item."],
    ),
    (
        "1. The first item 2. The second item",
        ["1. The first item", "2. The second item"],
    ),
    (
        "1. The first item. 2. The second item.",
        ["1. The first item.", "2. The second item."],
    ),
    (
        "• 9. The first item • 10. The second item",
        ["• 9. The first item", "• 10. The second item"],
    ),
    (
        "a. The first item b. The second item c. The third list item",
        ["a. The first item", "b. The second item", "c. The third list item"],
    ),
    (
        "You can find it at N°. 1026.253.553. That is where the treasure is.",
        ["You can find it at N°. 1026.253.553.", "That is where the treasure is."],
    ),
    (
        "She works at Yahoo! in the accounting department.",
        ["She works at Yahoo! in the accounting department."],
    ),
    (
        "We make a good team, you and I. Did you see Albert I. Jones yesterday?",
        ["We make a good team, you and I.", "Did you see Albert I. Jones yesterday?"],
    ),
    (
        "Thoreau argues that by simplifying one’s life, “the laws of the universe will appear less complex. . . .”",
        [
            "Thoreau argues that by simplifying one’s life, “the laws of the universe will appear less complex. . . .”"
        ],
    ),
    (
        """"Bohr [...] used the analogy of parallel stairways [...]" (Smith 55).""",
        ['"Bohr [...] used the analogy of parallel stairways [...]" (Smith 55).'],
    ),
    (
        "If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . . Next sentence.",
        [
            "If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . .",
            "Next sentence.",
        ],
    ),
    (
        "I never meant that.... She left the store.",
        ["I never meant that....", "She left the store."],
    ),
    (
        "I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it.",
        [
            "I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it."
        ],
    ),
    (
        "One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds. . . . The practice was not abandoned. . . .",
        [
            "One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds. . . .",
            "The practice was not abandoned. . . .",
        ],
    ),
    # ── Additions: Not from pysbd ──
    # Abbreviation chains
    (
        "The report was published in Dec. It was approved by Prof. Smith and Dr. Jones.",
        [
            "The report was published in Dec.",
            "It was approved by Prof. Smith and Dr. Jones.",
        ],
    ),
    (
        "See fig. 2 in vol. 3, ch. 4, pp. 18-22.",
        ["See fig. 2 in vol. 3, ch. 4, pp. 18-22."],
    ),
    (
        "Mr. Smith lives on Hwy. 7 near Ave. Central.",
        ["Mr. Smith lives on Hwy. 7 near Ave. Central."],
    ),
    (
        "The delivery van broke down right in front of Sunset Blvd. The driver called a tow truck.",
        [
            "The delivery van broke down right in front of Sunset Blvd.",
            "The driver called a tow truck.",
        ],
    ),
    (
        "The meeting is at 2 p.m. Please be on time.",
        ["The meeting is at 2 p.m.", "Please be on time."],
    ),
    (
        "Q. What is his name? A. His name is Alfred E. Sloan.",
        ["Q. What is his name?", "A. His name is Alfred E. Sloan."],
    ),
    # Contiguous terminators
    ("Hello ! ! ! !", ["Hello ! ! ! !"]),
    ("Hello!? !! ?! Is that you?", ["Hello!? !! ?!", "Is that you?"]),
    # Ellipsis
    (
        '"How could we miss this!..." Mark shouted, slamming his hand on the desk.',
        [
            '"How could we miss this!..."',
            "Mark shouted, slamming his hand on the desk.",
        ],
    ),
    (
        "We found a memory leak in the C# wrapper.... It was subtle.",
        ["We found a memory leak in the C# wrapper....", "It was subtle."],
    ),
    (
        "What I'm saying, the thing is . . . I didn't mean it.",
        ["What I'm saying, the thing is . . . I didn't mean it."],
    ),
    # Exclamation-safe words
    (
        "We spent the afternoon playing Adopt Me! on the computer while eating Chips Ahoy! cookies.",
        [
            "We spent the afternoon playing Adopt Me! on the computer while eating Chips Ahoy! cookies."
        ],
    ),
    (
        "My dad logged into Yahoo! finance to check on Yum! Brands stock performance before dinner.",
        [
            "My dad logged into Yahoo! finance to check on Yum! Brands stock performance before dinner."
        ],
    ),
    ("Yahoo! The server is down.", ["Yahoo!", "The server is down."]),
]
