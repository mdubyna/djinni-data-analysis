import string

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


STOP_WORDS = stopwords.words("english")
ENG_ALPHABET = set(string.ascii_lowercase)

stop_list = [
    "experience", "english", "knowledge", "requirements", "technical",
    "responsibilities", "strong", "developer", "familiarity", "'s",
    "skills", "develop", "collaborate", "work", "key",
    "team", "excellent", "understanding", "flexible", "usd",
    "’", "paid", "competitive", "engineer", "lead",
    "working", "software", "data", "proficiency", "computer",
    "senior", "development", "engineering", "proven", "good",
    "description", "science", "project", "ability", "friendly",
    "stay", "write", "intermediate", "great", "regular",
    "ukraine", "optimize", "building", "backend", "design"
]

STOP_WORDS_EXTENDED = nltk.corpus.stopwords.words("english") + stop_list


def clear_text(text: str) -> str:
    text = (text.replace("<", " ")
            .replace(">", " ")
            .replace(" br ", " ")
            .replace("/", " ")
            .replace(" b ", " "))

    return text.strip(".,;':/)(")


def check_word(word: str) -> bool:
    if word[0].islower():
        return False
    elif not word[0].isalpha():
        return False
    elif word[0].lower() not in ENG_ALPHABET:
        return False
    return True


def read_data(path_to_data: str) -> pd.DataFrame:
    return pd.read_csv(path_to_data, delimiter=",")


def filter_description(df: pd.DataFrame) -> pd.DataFrame:
    for index, description in enumerate(df["description"]):
        description = clear_text(description)
        words_to_filtering = ""
        for word in description.split():
            word = clear_text(word)
            if word and check_word(word):
                words_to_filtering += f" {word} "

        words = word_tokenize(words_to_filtering)
        df.loc[index, "description"] = " ".join(
            set([w for w in words if w.lower() not in STOP_WORDS_EXTENDED])
        )

    return df


def get_filtered_data(
        path_to_unfiltered_data: str,
        path_to_filtered_data: str
) -> None:
    data = read_data(path_to_unfiltered_data)
    data = filter_description(data)
    data.to_csv(path_to_filtered_data)


if __name__ == "__main__":
    get_filtered_data(
        "../vacancies.csv",
        "../filtered_vacancies.csv"
    )
