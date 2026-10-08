"""
Extracting sentences containing specific keywords.

This example demonstrates how to use YASBD to segment a text into sentences
and then filter out only the sentences that contain specific keywords of interest.
"""

from yasbd import BoundaryDetector

def main():
    text = (
        "The quick brown fox jumps over the lazy dog. "
        "I love reading about foxes and dogs. "
        "However, my favorite animal is the cat! "
        "Cats are very independent creatures. "
        "Have you ever seen a fox in the wild?"
    )

    keywords = ["fox", "foxes"]
    
    # Initialize the detector
    detector = BoundaryDetector(lang="en")
    
    # Segment the text into sentences
    sentences = detector.segment(text)
    
    print(f"Keywords to search for: {keywords}\n")
    print("Found sentences:")
    
    # Filter sentences containing any of the keywords
    for idx, sentence in enumerate(sentences, 1):
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            print(f"[{idx}] {sentence}")

if __name__ == "__main__":
    main()
