import csv
import re
import string

from tabulate import tabulate


def generate_report(filename):
    words = {"na": 0, "ni": 0, "sa": 0}
    word_count = 0
    i = 0
    with open(filename, "r") as f:
        for line in f:
            word_list = re.split(r"[\s\-\u2013\u2014]+", line)
            if i < 70000:
                for curr_word in word_list:
                    if i < 70000:
                        if curr_word:
                            word_count += 1
                            i += 1
                            word = curr_word.lower().strip(string.punctuation)
                            if word in words:
                                words[word] += 1
                            else:
                                words[word] = 1
                    else:
                        break
            else:
                break

    return [words, word_count]


def generate_csv(language, word_list, word_count):
    headers = ["Word", "Frequency Count", "Probability (%)"]
    filename = f"{language}_model.csv"
    with open(filename, "w") as f:
        fw = csv.writer(f)
        fw.writerow(headers)
        for word in word_list:
            freq = word_list[word]
            prob = (freq / word_count) * 100
            fw.writerow([word, freq, f"{prob:.6f}%"])


def format_value(val):
    if isinstance(val, float) and val != 0 and abs(val) < 0.001:
        return f"{val:.2e}"  # scientific notation
    elif isinstance(val, float):
        return f"{val:.6f}"
    return str(val)


def main():
    file_list = ["tagalog.txt", "english.txt", "spanish.txt"]
    total_words = 0
    lang_probs = {}
    stats = {}
    alpha = 0.01
    data = []
    tot_nb = 0
    csv_data = []
    for file in file_list:
        curr_lang = file.split(".")[0]
        words, lang_count = generate_report(file)
        generate_csv(curr_lang, words, lang_count)
        lang_probs[curr_lang] = {"word_count": lang_count, "word_list": words}
        total_words += lang_count

    for lang in list(lang_probs.keys()):
        stats[lang] = {}
        stats[lang][f"P({lang})"] = lang_probs[lang]["word_count"] / total_words

        stats[lang]["P(na)"] = (lang_probs[lang]["word_list"]["na"] + alpha) / (
            lang_probs[lang]["word_count"] + alpha * lang_probs[lang]["word_count"]
        )
        stats[lang]["P(ni)"] = (lang_probs[lang]["word_list"]["ni"] + alpha) / (
            lang_probs[lang]["word_count"] + alpha * lang_probs[lang]["word_count"]
        )
        stats[lang]["P(sa)"] = (lang_probs[lang]["word_list"]["sa"] + alpha) / (
            lang_probs[lang]["word_count"] + alpha * lang_probs[lang]["word_count"]
        )
        stats[lang]["naive_bayes"] = (
            stats[lang][f"P({lang})"]
            * stats[lang]["P(na)"]
            * stats[lang]["P(ni)"]
            * stats[lang]["P(sa)"]
        )

        data.append(
            [
                lang,
                stats[lang][f"P({lang})"],
                format_value(stats[lang]["P(na)"]),
                format_value(stats[lang]["P(ni)"]),
                format_value(stats[lang]["P(sa)"]),
                format_value(stats[lang]["naive_bayes"]),
            ]
        )
        tot_nb += stats[lang]["naive_bayes"]

    best_lang = max(stats.items(), key=lambda item: item[1]["naive_bayes"])

    headers = [
        "Language",
        "P(Language)",
        "P(na|Language)",
        "P(ni|Language)",
        "P(sa|Language)",
        "Naive Bayes Result",
    ]
    print(tabulate(data, headers=headers, tablefmt="grid"))
    print("\nNormalized Results:")
    for lang in list(stats.keys()):
        print(
            f"{lang.capitalize()}: {((stats[lang]['naive_bayes'] / tot_nb) * 100):.2f}% {'\t\033[1;3;92m<---- Answer\033[0m' if lang == best_lang[0] else ''}"
        )


if __name__ == "__main__":
    main()
