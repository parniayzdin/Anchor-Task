# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 13:30:21 2025

@author: Parnia
"""
import os
from radon.complexity import cc_visit

def compute_repo_complexity(repo_path: str) -> float:
    """
    Walk all .py files under repo_path, compute cyclomatic complexity
    for each code block, and return the average complexity score.
    """
    scores = []
    for root, _, files in os.walk(repo_path):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(root, fname)
            try:
                src = open(path, encoding="utf-8").read()
                blocks = cc_visit(src)
                scores.extend(block.complexity for block in blocks)
            except Exception:
                continue  

    return sum(scores) / len(scores) if scores else 0.0
