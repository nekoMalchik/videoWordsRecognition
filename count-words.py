if __name__ == '__main__':
    word = 'сиськ'
    with open('./multiplevideotestexport/result.txt', 'r', encoding='utf-8') as file:
        contect = file.read()
        res = contect.lower().count(word.lower())
    print(res)