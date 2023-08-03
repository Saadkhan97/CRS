import re
a = "['سبعانك اللًهممً د بناوبحمدكً اللًهمً اغفرالي']"
# print((a))
pattern = re.compile(r'\[([^]]+)\]')
data = re.search("(?<=\[)[^]]+(?=\])",a)
print(data.group())