import re
from prefixspan import PrefixSpan

class TextPatternAnalyzer:
    def __init__(self, tokenized_dataset, min_frequency=2):
        self.min_frequency = min_frequency
        self.tokenized_dataset = tokenized_dataset
        self.ps = PrefixSpan(self.tokenized_dataset)

    def preprocess_text(self, text):
        """Replace specific part numbers and catalog IDs with generic identifiers."""
        text = re.sub(r'\bCat ID \w+\b', '<CAT_ID>', text, flags=re.IGNORECASE)
        text = re.sub(r'\bPart \w+\b', '<PART>', text, flags=re.IGNORECASE)
        return text

    def tokenize_text(self, text):
        """Tokenize text into a list of words. Can be enhanced with NLP libraries."""
        return text.split()

    def analyze_text(self, input_text):
        """Analyze new input text against the stored tokenized dataset."""
        # Preprocess and tokenize the new input text
        tokenized_input = [self.tokenize_text(self.preprocess_text(text)) for text in input_text]

        # Find frequent patterns in the tokenized dataset
        frequent_patterns = self.ps.frequent(self.min_frequency)

        # Filter the input based on the frequent patterns
        matched_patterns = []
        for _, pattern in frequent_patterns:
            for text in tokenized_input:
                if all(elem in text for elem in pattern):
                    matched_patterns.append((' '.join(pattern), text))

        # Return matched patterns and their contexts in the new data
        return matched_patterns
