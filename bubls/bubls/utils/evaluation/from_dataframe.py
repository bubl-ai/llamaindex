import pandas as pd
from typing import Dict, Any


def is_hit(row):
    return row["reference_id"] in row["contexts_ids"]


def reciprocal_ranking(row):
    if row["reference_id"] in row["contexts_ids"]:
        return 1 / (row["contexts_ids"].index(row["reference_id"]) + 1)
    else:
        return 0


def evaluate_with_judge(row, judge):
    f = judge.evaluate(
        query=row["query"],
        response=row["response"],
        contexts=row["contexts"],
        reference=row["reference"],
    ).score
    return f


def evaluators_df(row, judges: Dict[str, Any]):
    e = []
    for judge in judges.values():
        e.append(evaluate_with_judge(row, judge))

    return pd.Series(e, index=list(judges.keys()))
