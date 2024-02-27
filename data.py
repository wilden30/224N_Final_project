"""
x: some exercpts from the day's speaches
y: whether GPR increases, decreases, same

"""
import pandas as pd

filename1 = "./hein-daily/speeches_097.txt"
filename2 = "./hein-daily/descr_097.txt"
df_txt = pd.read_csv(filename1, sep="|", encoding='utf-8', on_bad_lines="skip")
df_txt.set_index(keys="speech_id", inplace=True)
df_info = pd.read_csv(filename2, sep="|", encoding='utf-8', on_bad_lines="skip")
df_info.set_index(keys="speech_id", inplace=True)

both = df_txt.join(df_info)

print(both.head())
