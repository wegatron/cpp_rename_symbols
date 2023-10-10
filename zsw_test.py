import re

class_test = [
    '{XXX',
    '::XXX::',
    '~XXX()',
    'XXX>',
    'XXX)',
    'a.XXX()',
    '.XXX',
    'kiwi::utils::XXX<IxTibefs>',
    'XXX*',
    '*XXX',
    '}XXX;',
    'XXX,',
    'new XXX();'
]
inv_class_test = [
    'AAAaaXXX',
    'XXXAAA',
    '::XXXaa('
]
#
#re_class = r'(?:(?<=[\s:\{~\.\*\<\(\},])|(?<=^))XXX(?:(?=$)|(?=[\s]*[\>|\<|\*|\)|;|\(|,|:|\s]+))'
re_class = r'(?:(?<=[^\w])|(?<=^))XXX(?:(?=$)|(?=[^\w]))'
for tc in class_test:
    result = re.sub(re_class, 'YYY', tc)
    print(result)

print('--------------')

for tc in inv_class_test:
    result = re.sub(re_class, 'YYY', tc)
    print(result)

func_test = [
    'XXX(',
    'a.XXX',
    'XXX<',
    '::XXX (',
    '!XXX',
    '!XXX()',
    '<=XXX(',
    '=XXX',
    '->XXX',
    '&XXX',
    'aaa(XXX())',
    '*XXX(',
    '[XXX a]',
    '/XXX()',
    ' - XXX()',
    '+XXX()',
    '/XXX()',
    'pVec)/XXX(pProjectionVec',
]
inv_func_test = [
    'AAAaaXXX',
    'XXXAAA',
    '::XXXaa('
]


print('=====================')
#re_func = r'(?:(?<=[\*\.\s\:!&\(\>\=\[/\+\-])|(?<=^)|(?<=-\>))XXX(?:($)|(?=[\s\n\(\)\<]))'
re_func = r'(?:(?<=[^\w])|(?<=^))XXX(?:($)|(?=[^\w]))'
for tc in func_test:
    result = re.sub(re_func, 'YYY', tc)
    print(result)

print('--------------')

for tc in inv_func_test:
    result = re.sub(re_class, 'YYY', tc)
    print(result)