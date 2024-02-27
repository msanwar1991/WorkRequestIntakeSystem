# pattern_analyzer_test.py

from text_pattern_analyzer import TextPatternAnalyzer
import unittest

class TestPatternAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Pre-tokenized training dataset
        cls.training_dataset = [
            ["need", "replace", "<PART>"],
            ["check", "<CAT_ID>", "available"],
            ["detected", "malfunction", "requires", "<PART>"],
            ["stuck", "suspect", "<CAT_ID>", "replacement"],
            ["leak", "potentially", "needs", "<PART>"],
            ["not responding", "consider", "ordering", "<CAT_ID>"],
            ["wearing out", "might need", "<PART>"],
            ["degrading", "suggest checking", "<CAT_ID>"],
            ["issue detected", "likely needs", "<PART>"],
            ["glitching", "might require", "<CAT_ID>"]
        ]

        cls.positive_examples = [
            "Cooling fan efficiency has dropped, may need to order Part F123 for optimal performance.",
            "Noticed a discrepancy in the voltage regulator, should verify if Cat ID N456 is in stock.",
            "The gearbox is making unusual noises, probable need for Part G789 to address the issue.",
            "Water pump pressure is below standard, consider replacing with Cat ID O012 for proper function.",
            "Elevator response time is lagging, likely requires Part H345 for maintenance.",
            "Heating system not reaching set temperatures, possible need for Cat ID P678 adjustment.",
            "Pressure valves are corroding, might have to procure Part I901 for safety.",
            "The backup generator is not starting, suggest inspecting Cat ID Q234 for faults.",
            "Detected wear in the conveyor rollers, likely to replace with Part J567 soon.",
            "Security system sensors are malfunctioning, could require Cat ID R890 for system integrity."
        ]

        cls.negative_examples =[
            "Regular maintenance required for the pump, please schedule a check-up.",
            "The software on the control system needs an update, please initiate.",
            "Routine inspection needed for the HVAC system, no immediate issues reported.",
            "The lighting in the warehouse area is suboptimal, suggest evaluating.",
            "Noise coming from the rooftop unit, likely needs a routine inspection.",
            "The vehicle fleet is due for their annual service, please arrange.",
            "Security cameras need realignment, please schedule a technician visit.",
            "The landscaping around the building needs attention, please plan the work.",
            "The meeting rooms require AV setup verification, please conduct a review.",
            "Water pressure in the main building is fluctuating, needs investigation."
        ]

        cls.analyzer = TextPatternAnalyzer(cls.training_dataset, min_frequency=3)

    def test_positive_examples(self):
        matched_count = 0
        for example in self.positive_examples:
            patterns = self.analyzer.analyze_text([example])
            if any(patterns):  # If any pattern is matched for the current example
                matched_count += 1
        
        # Check if the number of matched examples equals the number of positive examples
        self.assertEqual(matched_count, len(self.positive_examples), f"Not all positive examples were matched. Matched {matched_count}/{len(self.positive_examples)} examples.")
        print(f"Positive Examples: Matched {matched_count}/{len(self.positive_examples)}")

    def test_negative_examples(self):
        matched_count = 0
        for example in self.negative_examples:
            patterns = self.analyzer.analyze_text([example])
            if any(patterns):  # If any pattern is matched for the current example
                matched_count += 1
        
        # Assuming no matches for negative examples, the matched count should be 0
        self.assertEqual(matched_count, 0, f"Patterns incorrectly matched for {matched_count} negative examples.")
        print(f"Negative Examples: Matched {matched_count}/{len(self.negative_examples)}")


if __name__ == '__main__':
    unittest.main()
