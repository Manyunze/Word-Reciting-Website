#!/usr/bin/env python3
# coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


import django
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from wordrecite.models import Vocabulary
from wordrecite.models import Word


wordlist = []
TEST = Vocabulary.objects.create(name='测试')
CET4 = Vocabulary.objects.create(name='四级')
CET6 = Vocabulary.objects.create(name='六级')
POST = Vocabulary.objects.create(name='考研')
IELTS = Vocabulary.objects.create(name='雅思')
TOEFL = Vocabulary.objects.create(name='托福')


def main():

    with open('dictionaries/POST.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            name, explanation =\
                line.split('|')[0], line.split('|')[1].strip('\n')
            example = 'This an example for {}'.format(name)
            wordlist.append(Word(name=name,
                                 explanation=explanation,
                                 example=example))
    Word.objects.bulk_create(wordlist)
    postwords = Word.objects.order_by('?')[:5000]
    POST.words.add(*postwords)
    print('考研导入完成')
    cet4words = Word.objects.order_by('?')[:3000]
    CET4.words.add(*cet4words)
    print('四级导入完成')

    cet6words = Word.objects.order_by('?')[:4000]
    CET6.words.add(*cet6words)
    print('六级导入完成')

    testwords = Word.objects.order_by('?')[:100]
    TEST.words.add(*testwords)
    print('测试导入完成')

    tfwords = Word.objects.order_by('?')[:4000]
    TOEFL.words.add(*tfwords)
    print('托福导入完成')

    iewords = Word.objects.order_by('?')[:4000]
    IELTS.words.add(*iewords)
    print('雅思导入完成')


if __name__ == "__main__":
    main()
    print('Done!')
