from bs4 import BeautifulSoup as bs
import pandas as pd

lingq_input = ".\data\lingq_inp.html"
kor_srt_file = r"C:\Users\Roanna\Documents\Anki\kor_texts\IiK_e16_ko.srt"
eng_srt_file = r"C:\Users\Roanna\Documents\Anki\kor_texts\IiK_e16_en.srt"
ko_sentences = []
en_sentences = []
start_time = []
end_time = []

with open(lingq_input) as f:
    soup = bs(f, "html.parser")

for tag in soup.find_all('span'):
    if tag.has_attr("data-text") == True:
        ko_sentences.append(tag.text)

for tag in soup.find_all('textarea'):
    if tag.text != "":
        en_sentences.append(tag.text)

for tag in soup.find_all(class_="video-set--start"):
    start_time.append(tag.find("input").attrs['value'])

for tag in soup.find_all(class_="video-set--end"):
    end_time.append(tag.find("input").attrs['value'])

print(len(ko_sentences))
print(len(en_sentences))
print(len(start_time))
print(len(end_time))
df = pd.DataFrame(data={
    "ko": ko_sentences,
    "en": en_sentences[1:],
    "start": start_time[1:],
    "end": end_time[1:]
})

df["start"] = df["start"].replace(regex=r"(\d\d:\d\d)\.(\d)", value=r"00:\1,\2")+"00"
df["end"] = df["end"].replace(regex=r"(\d\d:\d\d)\.(\d)", value=r"00:\1,\2")+"00"

with open(kor_srt_file, "w") as f:
    for i in df.index:
        f.write(str(i) + "\n")
        f.write(str(df.at[i, "start"]) + " --> " + str(df.at[i, "end"]) + "\n")
        f.write(str(df.at[i, "ko"]) + "\n")
        f.write("\n")

with open(eng_srt_file, "w") as f:
    for i in df.index:
        f.write(str(i) + "\n")
        f.write(str(df.at[i, "start"]) + " --> " + str(df.at[i, "end"]) + "\n")
        f.write(str(df.at[i, "en"]) + "\n")
        f.write("\n")
    
