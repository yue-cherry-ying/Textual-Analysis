# <title type="main">Pride and Prejudice</title>

title = ""
with open("pride_and_prejudice.xml") as input_file:
    for line in input_file:
        if "<title type='main'>" in line:
            pattern = r">([^<]+)"
            if re.search(pattern, line):
                print(re.search(pattern, line).groups())