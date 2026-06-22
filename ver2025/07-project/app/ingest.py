import os
import minsearch

import pandas as pd


data_directory = os.path.join(os.path.dirname(__file__), "..", "data")


def ingest_data(filename: str):
    df = pd.read_csv(data_directory + f"/{filename}")
    documents = df.to_dict(orient="records")

    index = minsearch.AppendableIndex(
        text_fields=[
            "exercise_name",
            "type_of_activity",
            "type_of_equipment",
            "body_part",
            "type",
            "muscle_groups_activated",
            "instructions",
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index
