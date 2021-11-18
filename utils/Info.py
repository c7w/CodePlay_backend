def read(file):
    if file == 'A':
        f = open('./info/A.txt', 'r', encoding='utf-8')
        text = f.read().strip()
        f.close()
        return text
    if file == 'B':
        f = open('./info/B.txt', 'r', encoding='utf-8')
        text = f.read().strip()
        f.close()
        return text
    if file == 'broadcast':
        f = open('./info/broadcast.txt', 'r', encoding='utf-8')
        text = f.read().strip()
        f.close()
        return text