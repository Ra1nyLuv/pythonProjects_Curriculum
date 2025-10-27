with open('sample.txt', 'r', encoding='utf-8') as fr:
    with open('sample_copy.txt', 'w', encoding='utf-8') as fw:
        fw.write('202212904506_陈俊霖')
        fw.write(fr.read())
