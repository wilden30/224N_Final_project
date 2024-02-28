"""
x: some exercpts from the day's speaches
y: whether GPR increases, decreases, same

"""
import pandas as pd
import random

def classify_GPR_daily(filename):
    def classification(row):
        ratio = row['GPRD']/row['avg']
        if ratio > 1.2:
            return "high"
        if ratio < 0.8:
            return "low"
        return "average"
    
    daily_gpr_df = pd.read_csv(filename, sep = '\t', on_bad_lines="skip", index_col="DAY", thousands=',')
    gpr_frame = daily_gpr_df["GPRD"].to_frame()
    # Calculate Exponential Moving Average (EWMA) with a span of 30, adjust these parameters
    gpr_frame['avg'] = gpr_frame['GPRD'].ewm(span=30).mean()
    gpr_frame["classification"] = gpr_frame.apply(classification, axis=1)

    print(gpr_frame['classification'].value_counts()['high'])
    print(gpr_frame['classification'].value_counts()['low'])
    print(gpr_frame['classification'].value_counts()['average'])

    gpr_frame.drop(columns=["GPRD", "avg"], inplace=True)

    return gpr_frame



def process_congress(speeches_text, descr_text):
    df_txt = pd.read_csv(speeches_text, sep="|", encoding="latin1", on_bad_lines="skip", engine="python")
    df_txt.set_index(keys="speech_id", inplace=True)
    df_info = pd.read_csv(descr_text, sep="|", encoding="latin1", on_bad_lines="skip", engine="python")
    df_info.set_index(keys="speech_id", inplace=True)
    both = df_txt.join(df_info)
    both['txt'] = both.groupby(['date'])['speech'].transform(lambda x : '\n'.join(x))
    both = both.groupby(['date']).head(1) #j take a single text entry for each
    both.drop(columns=["chamber", "number_within_file", "speaker", "first_name", "last_name", "state", "gender", 
                      "line_start", "line_end", "file", "char_count", "word_count"], inplace=True)

    total_tokens = 2000
    num_samples = 10
    sample_len = total_tokens // num_samples
    def random_text(row):
        txt = row["txt"].split(" ")
        output = ""
        if len(txt) < total_tokens:
            return "\"" + " ".join(txt) + "\""
        for i in range(num_samples):
            start_index = random.randrange(0, len(txt) - sample_len)
            sample = txt[start_index: start_index + sample_len]
            output += "\"" + " ".join(sample) + "\"\n"
        return output
    
    both["sample"] = both.apply(random_text, axis=1)
    both.set_index(keys="date", inplace=True)
    both.drop(columns=["speech", "txt"], inplace=True)

    return both

def match_classification_text(congress_df, sentiment_df):
    matched = congress_df.join(sentiment_df)
    matched.dropna(inplace = True)
    return matched


def process_all_files(first_inclusive, num_files):
    total_df = None
    for i in range(num_files):
        print(i)
        if (i == 0):
            total_df = process_congress(f"./hein-daily/speeches_{first_inclusive + i:03}.txt",
                                        f"./hein-daily/descr_{first_inclusive + i:03}.txt")
        else:
            next = process_congress(f"./hein-daily/speeches_{first_inclusive + i:03}.txt",
                                        f"./hein-daily/descr_{first_inclusive + i:03}.txt")
            total_df = pd.concat([total_df, next], axis=0)
    return total_df


# all_congress = process_all_files(97, 18)
# all_congress = process_all_files(100, 2)
filename3 = "./GPR_daily.tsv"
# classification = classify_GPR_daily(filename3)
# matched_sentiment = match_classification_text(all_congress, classification)
# matched_sentiment.to_csv("dataset.csv", index=False)

df = pd.read_csv("dataset.csv")
print(df.shape)
