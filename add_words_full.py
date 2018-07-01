#!/usr/bin/env python3
# coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()

from wordrecite.models import Vocabulary
from wordrecite.models import Word

TEST = Vocabulary.objects.create(name='测试')
CET4 = Vocabulary.objects.create(name='四级')
CET6 = Vocabulary.objects.create(name='六级')
POST = Vocabulary.objects.create(name='考研')
IELTS = Vocabulary.objects.create(name='雅思')
TOEFL = Vocabulary.objects.create(name='托福')
data = {
    'dictionaries/wordlist.txt': TEST,
    'dictionaries/IELTS.txt': IELTS,
    'dictionaries/TOEFL.txt': TOEFL,
    'dictionaries/CET4.txt': CET4,
    'dictionaries/CET6.txt': CET6,
    'dictionaries/POST.txt': POST

}


def create(filename, vocabulary):
    with open(filename, 'r', encoding='UTF-8') as f:
        for line in f:
            name, explanation =\
                line.split('|')[0], line.split('|')[1].strip('\n')
            example = 'This an example for {}'.format(name)
            word = Word.objects.create(name=name, explanation=explanation,
                                       example=example)
            vocabulary.words.add(word)
    print('{} 导入成功'.format(filename))


def main():
    for x, y in data.items():
        create(x, y)


if __name__ == "__main__":
    main()
    print('Done!')
