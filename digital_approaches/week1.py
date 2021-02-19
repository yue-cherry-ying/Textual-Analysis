# Yue "Cherry" Ying
# Python Exercise 1 for Tuesday January 19th

s = "This is a random testing of how to process a string or strings in Python. Making these changes can be quite difficult depending on a number of varying factors."
s = s.replace(".", "")
words = s.split()

result = []
for word in words:
    if len(word) >= 3:
        if word.endswith("ing"):
            result.append(word + "ly")
        else:
            result.append(word + "ing")
    else:
        result.append(word)
print(" ".join(result))
