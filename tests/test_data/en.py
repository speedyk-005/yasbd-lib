# English test data for yasbd
# Format: (input_text, expected_sentences)

TEST_DATA = [
    # Basic punctuation
    ("Hello world. How are you? I'm fine.", ["Hello world.", "How are you?", "I'm fine."]),
    ("What is your name? My name is Jonas.", ["What is your name?", "My name is Jonas."]),
    ("There it is! I found it.", ["There it is!", "I found it."]),
    ("Did you remove num 2. Put it back.", ["Did you remove num 2.", "Put it back."]),
    ("Her email is Jane.Doe@example.com. I sent her an email.", ["Her email is Jane.Doe@example.com.", "I sent her an email."]),
    ("The site is: https://www.example.50.com/new-site/awesome_content.html. Please check it out.", ["The site is: https://www.example.50.com/new-site/awesome_content.html.", "Please check it out."]),

    # Abbreviations
    ("My name is Jonas E. Smith.", ["My name is Jonas E. Smith."]),
    ("Please turn to p. 55.", ["Please turn to p. 55."]),
    ("Were Jane and co. at the party?", ["Were Jane and co. at the party?"]),
    ("They closed the deal with Pitt, Briggs & Co. at noon.", ["They closed the deal with Pitt, Briggs & Co. at noon."]),
    ("Let's ask Jane and co. They should know.", ["Let's ask Jane and co.", "They should know."]),
    ("I can see Mt. Fuji from here.", ["I can see Mt. Fuji from here."]),
    ("St. Michael's Church is on 5th st. near the light.", ["St. Michael's Church is on 5th st. near the light."]),
    ("That is JFK Jr.'s book.", ["That is JFK Jr.'s book."]),
    ("I visited the U.S.A. last year.", ["I visited the U.S.A. last year."]),
    ("I live in the E.U. How about you?", ["I live in the E.U.", "How about you?"]),
    ("I work for the U.S. Government in Virginia.", ["I work for the U.S. Government in Virginia."]),
    ("I have lived in the U.S. for 20 years.", ["I have lived in the U.S. for 20 years."]),
    ("She has $100.00 in her bag.", ["She has $100.00 in her bag."]),
    ("She has $100.00. It is in her bag.", ["She has $100.00.", "It is in her bag."]),
    ("The meeting is at 2 p.m. Please be on time.", ["The meeting is at 2 p.m.", "Please be on time."]),

    # Parentheses and quotes
    ("He teaches science (He previously worked for 5 years as an engineer.) at the local University.", ["He teaches science (He previously worked for 5 years as an engineer.) at the local University."]),
    ('She turned to him, "This is great." she said.', ["She turned to him, \"This is great.\" she said."]),
    ('She turned to him, "This is great." She held the book out to show him.', ["She turned to him, \"This is great.\"", "She held the book out to show him."]),

    # Double punctuation
    ("Hello!! Long time no see.", ["Hello!!", "Long time no see."]),
    ("Hello?? Who is there?", ["Hello??", "Who is there?"]),
    ("Hello!? Is that you?", ["Hello!?", "Is that you?"]),
    ("Hello?! Is that you?", ["Hello?!", "Is that you?"]),

    # Lists
    ("1.) The first item. 2.) The second item.", ["1.) The first item.", "2.) The second item."]),
    ("a) The first item. b) The second item.", ["a) The first item.", "b) The second item."]),
    ("1. The first item. 2. The second item.", ["1. The first item.", "2. The second item."]),
    ("• 9. The first item. • 10. The second item.", ["• 9. The first item.", "• 10. The second item."]), 

    # Elipsis
    ("The project (Sinta) was nearing completion... or so we thought.", ["The project (Sinta) was nearing completion... or so we thought."]),
    ("\"How could we miss this!...\" Mark shouted, slamming his hand on the desk.", ["\"How could we miss this!...\"", "Mark shouted, slamming his hand on the desk."]),
    ("We found a memory leak in the C# wrapper.... It was subtle.", ["We found a memory leak in the C# wrapper....", "It was subtle."]),
]
