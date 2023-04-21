from abc import ABCMeta
from typing import Type, List

from psdelivery.core.difficulty import ProblemDifficulty, ProblemDifficultyConverter


class ProblemItem(metaclass=ABCMeta):
    seq: str
    title: str
    problem_site: str
    difficulty: ProblemDifficulty
    algorithm_tags: List[str]
    difficulty_converter: Type[ProblemDifficultyConverter]

    def __init__(self, 
                 seq: str, 
                 title: str, 
                 problem_site: str, 
                 website_difficulty: float, 
                 algorithm_tags: List[str]):
        self.seq = seq
        self.title = title
        self.problem_site = problem_site
        self.difficulty = self.difficulty_converter.convert(website_difficulty)
        self.algorithm_tags = algorithm_tags

    def __dict__(self):
        return {
            'seq': self.seq,
            'title': self.title,
            'problem_site': self.problem_site,
            'difficulty': self.difficulty.value,
            'algorithm_tags': self.algorithm_tags,
        }
    