"""Convert CHANGELOG.md to Yaml file"""

md = open("CHANGELOG.md", 'r', encoding="utf-8")
yml = open("docs/changelog.yml", 'w', encoding="utf-8")

year: int = 3000
mode: str = None


def codewrapper(line: str) -> str:
    for _ in range(line.count('`') // 2):
        line = line.replace('`', '<code>', 1)
        line = line.replace('`', '</code>', 1)
    return line


for i, line in enumerate(data := md.readlines()):
    if line.startswith('['):  # version & datatime
        year_ = int(line.split(' ')[2].split('-')[0])
        if year_ < year:
            year = year_
            yml.write(f'- "CL-{year}":\n')
        yml.write(f'    - "{line.strip().replace('[`', '<code>v').replace(
            '`]', '</code>').replace(' - ', ' ').replace('-', '/')}":\n')
    elif line.startswith('###'):  # mode
        mode = line.split(' ')[1]
    elif line.startswith('- [X]'):  # content
        yml.write(codewrapper(f'        - "{mode}": {data[i+1]}'))
    elif line == "Older Log - 之前的日志\n":
        break

md.close()
yml.close()
