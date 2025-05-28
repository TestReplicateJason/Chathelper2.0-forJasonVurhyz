from rapidfuzz import process, fuzz
import re

class FuzzyMatcher:
    @staticmethod
    def normalize_text(text):
        """Приводит текст к нижнему регистру, заменяет ё на е, удаляет пунктуацию"""
        if not text:
            return ""
        text = text.lower().replace('ё', 'е').replace('Ё', 'е')
        return re.sub(r'[^\w\s]', '', text)

    def find_best_match(self, command_text, choices, threshold=70):
        """Находит лучшее соответствие среди вариантов"""
        if not command_text or not choices:
            return None, None, None
            
        normalized_command = self.normalize_text(command_text)
        normalized_choices = [self.normalize_text(choice) for choice in choices]
        
        # Используем частичное совпадение
        match = process.extractOne(
            normalized_command, 
            normalized_choices,
            scorer=fuzz.partial_ratio,
            score_cutoff=threshold
        )
        
        if not match:
            return None, None, None
            
        normalized_name, score, index = match
        return choices[index], score, index