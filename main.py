import re
import time
import datetime
def file(link):
    original_list_key=[]
    with open(link) as file_for_record:
        for line_for_original_list in file_for_record:
            line_for_original_list=line_for_original_list.rstrip()
            original_list_key.append(line_for_original_list)
    return original_list_key
def repreg(base_line):
    counter_num_orig_line = 0
    new_list_for_line = []
    global substring
    counter_num_orig_line += 1
    # программа меняет регулярки на спецсимволы. на входе строка с регуляркой. на выходе список строк без регулярок, на входе a - '(под|пере)жар* картошку' - на выходе a - ['поджар* картошку', 'пережар* картошку']
    base_line = base_line.replace('[а-я]', '.').replace('[a-z]', '.').replace('[а-яa-z]', '.').replace('[a-zа-я]', '.').replace('[^а-я]', '£').replace('[1-9]', '£').replace('[0-9]', '£').replace('+', '*').replace('&#091', '©091').replace('&#093', '©093').replace('&#092', '©092').replace('&#047', '©047').replace('&#094', '©094').replace('&#036', '©036').replace('&#046', '©046').replace(
        '&#124', '©124').replace('&#063', '©063').replace('&#042', '©042').replace('&#043', '©043').replace('&#040', '©040').replace('&#041', '©041').replace('&#123', '©123').replace('&#125', '©125').replace('&#821', '©821').replace('&#061', '©061').replace('&#182', '©182')  # замена регулярок на звёздочки и точки
    # программа раскрывает квадратные скобки по выбранному диапозону. (0|1|2|3) вместо [0-3]
    p1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    p2 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    if re.fullmatch('.*\[\w\-\w\].*', base_line):
        num = len(re.findall('\[\w\-\w\]', base_line))  # количество квадратных скобок с '-'
        for i in range(num):  # замена квадратных скобко и букв на варианты круглых скобок
            dl = len(base_line)  # количество букв в элементе
            for k in range(dl):  # в диапозоне количества букв
                if base_line[k] == '[' and base_line[k + 2] == '-':
                    if base_line[k + 1] in p1:
                        s_o = p1.index(base_line[k + 1])
                    if base_line[k + 1] in p2:
                        s_o = p2.index(base_line[k + 1])
                    start = k  # начальная позиция квадратной скобки
                if base_line[k] == ']' and base_line[k - 2] == '-':
                    if base_line[k - 1] in p1:
                        s_f = p1.index(base_line[k - 1])
                    if base_line[k - 1] in p2:
                        s_f = p2.index(base_line[k - 1])
                    end = k  # финальная позиция квадратной скобки
                    break
            if base_line[k - 1] in p1:  # если это цифра
                p = '|'.join(p1[s_o:s_f + 1])  # добавляем в указанное перечисление цифр этой скобки слэши
            if base_line[k - 1] in p2:  # если это буква
                p = '|'.join(p2[s_o:s_f + 1])  # добавляем в указанное перечисление букв  этой скобки слэши
            base_line = base_line[:start] + '(' + p + ')' + base_line[end + 1:]  # преобразовываем квадратные скобки в круглые. становится основным выражением.
            # дальше по кругу

    # программа рабоатет с выражением [^x], раскрывает и выдаёт полную скобку за исключением символа x
    if re.findall('.*\[\^.*', base_line):
        p0 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы',
              'ь', 'э', 'ю', 'я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # символы, которые используются в [^x]
        y = 0
        num = len(re.findall('\^', base_line))  # количество квадратных скобок с '^'
        base_line = base_line.split(' ', 0)  # сделай из изначальной строки список с одним элементом
        schetchik = 0
        for s in base_line:
            dl = len(s)  # количество букв в элементе
            for k in range(dl):  # в диапозоне количества букв
                if s[k] == '^' and y == 0:  # высчитывает, откуда начинается скобка и где заканчивается
                    start = k + 1
                    y = y + 1
                if s[k] == ']' and y == 1:
                    end = k
                    y = y - 1
                    break
            x = s[int(start):int(end)]  # все буквы-цифры , которые не должны учитываться
            vrem = []
            for i in x:  # перебирает все символы в скобке
                isk = p0.index(i)  # находит индекс в списке, чтобы потом исключить его
                p = p0[:isk] + p0[isk + 1:]  # собирает скобку без учёта указанных символов
                vrem.append(p)  # добавляет во временный список
            vrem = '(' + '|'.join(list(set.intersection(*map(set, vrem)))) + ')'  # собирает готовую скобку
            s = s[:start - 2] + vrem + s[end + 1:]  # собирает готовое выражение, строку
            base_line.append(s)  # добавляет в текущий список
            schetchik = schetchik + 1
            if schetchik != num:  # прекращает работать, если проверил все значения
                continue
            else:
                break
        base_line = [i for i in base_line if '^' not in i]  # выбирает значения только без ^
        base_line = ''.join(base_line)

    # программа заменяет квадратные скобки и буквы в них на варианты круглых скобок
    #base_line = re.sub(' \d,\d+ ', ' ', base_line)  # убираем расстояния, делаем так, будто их не было
    base_line = base_line.replace(',', '®')
    num = len(re.findall('\[', base_line))  # количество квадратных скобок
    num2 = len(re.findall('\[\^', base_line))  # количество квадратных скобок исключений
    num = num - num2  # вычитаем разницу, чтобы считать нужное число вариантов
    r = 0
    for i in range(num):  # замена квадратных скобко и букв на варианты круглых скобок
        dl = len(base_line)  # количество букв в элементе
        for k in range(dl):  # в диапозоне количества букв
            if base_line[k] == '[' and base_line[k + 2] != '-' and base_line[k + 1] != '^':
                start = k  # начальная позиция квадратной скобки
                r = r + 1
            if base_line[k] == '[' and base_line[k + 1] == '^':
                continue
            if base_line[k] == '[' and base_line[k + 2] == '-':
                continue
            if base_line[k] == ']' and base_line[k - 2] != '-' and r == 1:
                end = k  # финальная позиция квадратной скобки
                r = r - 1
                break
        p = base_line[start + 1:end]  # участок квадратной скобки
        p = '|'.join(p)  # добавляем между буквами в этой скобки слэши
        base_line = base_line[:start] + '(' + p + ')' + base_line[end + 1:]  # преобразовываем квадратные скобки в круглые. становится основным выражением.  дальше по кругу


    # программа раскрывает фигурные скобки и даёт все значения согласно {x}
    base_line = base_line.split(' ', 0)  # сделай из изначальной строки список с одним элементом
    for str_ss in base_line:  # итерация по списку строк
        if '{' in str_ss:  # если в строке есть круглая скобка
            for kes in range(len(str_ss)):  # пройдись по каждому элементу строки. по каждой букве
                if str_ss[kes] == '{':  # если есть открыв.скобка
                    t1 = kes  # назначь индекс этой скобке
                if str_ss[kes] == '}':  # если есть открыв.скобка
                    t2 = kes  # назначь индекс этой скобке
                    if re.search('®', str_ss[t1 + 1:t2]):  # в этих круглых скобках есть диапозон?
                        start_finish = str_ss[t1 + 1:t2].split('®')
                        start_f1 = round(float(start_finish[0]))
                        finish_f1 = round(float(start_finish[1]))
                        len_sumok = finish_f1 - start_f1  # знай сколько вариантов в диапазоне
                    else:
                        start_finish = [(str_ss[t1 + 1:t2]), (str_ss[t1 + 1:t2])]
                        start_f1 = round(float(start_finish[0]))
                        finish_f1 = round(float(start_finish[1]))
                    break
            nvs = []  # временный список для добавления новых значений
            for dnkz in range(start_f1, (finish_f1) + 1):  # в диапозоне начального и конечного значения
                if str_ss[t1 - 1] != ')' and str_ss[t1 - 1] != ']':
                    nvs.append(str_ss[:t1 - 1] + str_ss[t1 - 1] * dnkz + str_ss[t2 + 1:])  # добавь в новый список строки с учётом количества {
                if str_ss[t1 - 1] == ')':
                    for index, bukva in reversed(list(enumerate(str_ss[:t1]))):
                        if bukva == '(':
                            nvs.append(str_ss[:index] + str_ss[index:t1] * dnkz + str_ss[t2 + 1:])
                            break
                if str_ss[t1 - 1] == ']':
                    for index, bukva in reversed(list(enumerate(str_ss[:t1]))):
                        if bukva == '[':
                            nvs.append(str_ss[:index] + str_ss[index:t1] * dnkz + str_ss[t2 + 1:])
                            break
            [base_line.append(nvs_i) for nvs_i in nvs]  # добавь новые значения из временного в основной список
    base_line = [ai for ai in base_line if '{' not in ai]

    # программа убирает лишние скобки, которые не имели нагрузки
    for substring in base_line:
        substring = list(substring)  # строка меняется на элемент списка
        kn = len(substring)  # количество строк в списке
        predel = 0
        # определяет, где начинается старт и финиш - маскируя внутренние скобки со слешами, убирая пустые скобки , где нет слеша или знака вопрсоа
        while '(' in substring or ')' in substring or '|' in substring:  # пока есть слэши и скобки в списке
            predel += 1
            for k in range(0, kn):  # итерация по количеству букв в списке
                if re.fullmatch('\(', substring[k]) and re.fullmatch('\)', substring[k + 1]):  # если в строке есть скобка откр и закр ()
                    start = k  # фиксация начала
                    finish = k + 1  # фиксация конца
                    break
                if re.fullmatch('\(', substring[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\=|\?|@|<|\-|\*|\[|\]|\+|\.|#)', substring[k + 1]):  # если в строке скобка откр и дальше буква
                    start = k  # фиксация начала
                    continue
                if re.fullmatch('\)', substring[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\=|\?|@|>|\-|\*|\[|\]|\?|\+|\.|#)', substring[k - 1]):  # если в строке скобка закр  и перед этим буква
                    finish = k  # фиксация конца
                    break  # останавливай цикл, переходи к след
            dlskob = len(''.join(substring[start + 1:finish]))
            try:
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and finish != dlskob + 1:  # если нет слэша внутри скобок , тогда
                    if '?' not in substring[finish + 1]:
                        substring[start] = '@'  # меняй скобки начала и конца на знак
                        substring[finish] = '@'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' not in substring[finish] and finish == dlskob + 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' in substring[finish + 1] and dlskob >= 2:  # если нет слэша внутри скобок , тогда
                    substring[start] = '<'  # меняй скобки начала и конца на знак
                    substring[finish] = '>'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' in substring[finish + 1] and dlskob == 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' in substring[start + 1:finish]:  # если слэш между скобок
                    substring[start] = '<'  # меняй скобки начала и конца на знак
                    substring[finish] = '>'
                    spisok = []  # создай пустой список
                    for k, i in enumerate(substring[start + 1:finish]):  # итерация по внутренности скобки
                        if i == '|':  # есть если слэш
                            spisok.append(k)  # добавь в список индекс этого слэша
                    for i in range(len(spisok)):  # итерация по индексам слэшей
                        substring[start + 1 + spisok[i]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
            except IndexError:
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and finish != dlskob + 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' not in substring[finish] and finish == dlskob + 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' in substring[start + 1:finish]:  # если слэш между скобок
                    substring[start] = '<'  # меняй скобки начала и конца на знак
                    substring[finish] = '>'
                    spisok = []  # создай пустой список
                    for k, i in enumerate(substring[start + 1:finish]):  # итерация по внутренности скобки
                        if i == '|':  # есть если слэш
                            spisok.append(k)  # добавь в список индекс этого слэша
                    for i in range(len(spisok)):  # итерация по индексам слэшей
                        substring[start + 1 + spisok[i]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
            if predel > 100:
                substring = (''.join([k for k in substring]))  # подготавливаем из списка строку
                substring = list(substring.replace('@|@', '|').replace(' @', ' (').replace('@ ', ') '))
                if substring[0] == '@':
                    substring[0] = '('
                if substring[len(substring) - 1] == '@':
                    substring[len(substring) - 1] = ')'

    base_line = (''.join([k for k in substring if k != '@']))  # верни строку, не замечая знак @ - пустые скобки
    f = base_line.replace('<', '(').replace('>', ')').replace('&', '|')
    f = f.split(maxsplit=0)

    # программа раскрывает скобки со знаком '?' и делает все возможные варианты
    for x, i in enumerate(f):  # иетарция по элементам списка, где есть знак вопроса, так мы находим скобки , после которых стоит знак вопроса. означает - или да или нет.
        if ')?' in i:
            i = list(i)  # преобразуем строку в список. чтобы была итерация по буквам этой строки
            for k in range(len(i)):  # итерация по количеству букв в списке
                if re.fullmatch('\(', i[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|\-|\*|\[|\]|\.|\+|\|)', i[k + 1]):  # если в строке скобка
                    start = k  # фиксация начала скобки со знаком вопроса
                    continue
                if re.fullmatch('\(', i[k]) and re.fullmatch('\)', i[k + 1]) and re.fullmatch('\?', i[k + 2]):  # если есть выражение вида ()?, то сразу преобраует в спец символы, чтобы потом убирать эту строку
                    f[x] = '#$'
                    break
                try:
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\|)', i[k + 1]):  # если есть выражение вида -   текст)|
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('\)', i[k + 1]) and re.fullmatch('\?', i[k + 2]):  # если есть выражение вида -  ( абв))?
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\|)', i[start - 1]) and re.fullmatch('\)', i[k]) and i[k + 1] != '?':  # если есть выражение вида -   текст)|
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k + 1]):  # !!! тут был прецедент. стоял знак вопроса. я его убрал.   если есть выражение вида -   текст))
                        i[k] = '>'
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break

                    if i[0] == '(' and start == 1 and re.fullmatch('\)', i[k]) and i[k + 1] != '?':  # если есть выражение вида -   текст)|
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\?)', i[k + 1]):  # если  выражение -   текст)? - дальше перечисляются все ситуации, чтобы раскрывать эти скобки
                        finish = k  # фиксация конца скобки со знаком вопроса
                        if ')' not in i[start + 1:finish] and '(' not in i[start + 1:finish]:
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] != '(' and finish + 1 == len(i) - 1:  # 1.2.2.0
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] != '(' and i[finish + 2] != ' ':  # 1.1.1.0
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] != '(' and i[finish + 2] == ' ':  # 1.2.2.0
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] == '(' and i[finish + 2] != '|':  # 1.1.1
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] == '(' and i[finish + 2] == '|':  # 1.1.2
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 3:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and i[start - 2] == '(':  # 1.2.1
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start - 1] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 2]) and i[finish + 2] == ')':  # 1.2.2.1
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start - 1] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 2]) and i[finish + 2] == '|':  # 1.2.2.2
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 3:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 2]) and re.fullmatch(
                                    '(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[finish + 2]):  # 1.2.2.3
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                                # дальше была одна скобка, но её  из-за длины и несовпадения (индекс выходил за пределы диапозона) пришлось размножить
                            if len(i) - 1 < finish + 2:  # если длина итеририруемого выражения меньше индекса элемента, то тогда проверяем ближайший элемент после )

                                if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 1] != '|':  # 1.3.1
                                    f.append(''.join(i[:start] + i[start + 1:finish]))  # добавь в общий список скобку, где есть знак вопроса
                                    f.append(''.join(i[:start]))  # добавь в общий список скобку, где нет знака вопроса
                                    f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                    break
                            if len(i) - 1 >= finish + 2:  # если длина итеририруемого выражения больше или равна индексу элемента, то тогда всё ок, проверяем дальний элемент после ) (финиша)

                                if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 2] != '|':  # 1.3.2
                                    f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                    f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                    f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                    break

                            if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 2] == '|' and i[start - 1] == '(':  # 1.4.1
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 3:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 2] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 1]):  # 1.4.2
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                            if '|' in i[start + 1:finish] and i[start - 1] == '|':  # 1.5
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                except IndexError:
                    pass
            if re.search('\)\)\?', ''.join(i)) and re.search('\(\(', ''.join(i)):  # chebur
                for k in range(len(i)):  # итерация по количеству букв в списке
                    if re.fullmatch('\(', i[k - 1]) and re.fullmatch('\(', i[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|\-|\*|\[|\]|\.|\+|\|)', i[k + 2]):  # если в строке скобка ((а
                        start2 = k  # фиксация начала скобки со знаком вопроса
                        continue
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 2]) and re.fullmatch('\)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\?)', i[k + 1]):  # б))?
                        f.append(''.join(i[:start2] + i[start2 + 1:k] + i[k + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                        f.append(''.join(i[:start2 - 1] + i[k + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
        base_line = (list(set([k for k in f if k != '#$'])))  # генерируем список, в котором нет обрабатываемых строк. через множество избавляемся от повторяющихся значений. создаём обратно список
        for x in range(len(base_line)):
            base_line[x] = base_line[x].replace('<', '(').replace('>', ')').replace('&', '|')  # возвращаем обратно скобки и слэши

    sl_zap = []
    for i in base_line:
        sl_zap.append(i.replace(',', '®'))
    base_line = sl_zap

    # программа раскрывает скобки и делает все возможны варианты
    stroka = ', '.join(base_line)

    while '|' in stroka:
        spis_strok = stroka.split(',')

        spis_strok = list(set(spis_strok))
        for indexstr, stroka in enumerate(spis_strok):
            if '|' in stroka:
                if re.search('\(\S+ ', stroka):
                    while re.search('\(\S+ ', stroka) or re.search(' \S+\)', stroka) or re.search(' \S+\|', stroka) or re.search('\|\S+ ', stroka):
                        for bukva in range(len(stroka)):
                            if (re.fullmatch('\(', stroka[bukva])) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', stroka[bukva + 1]):  # если в строке скобка
                                start = bukva  # фиксация начала скобки со знаком вопроса
                                continue
                            if (re.fullmatch('\)', stroka[bukva])) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', stroka[bukva - 1]):  # если в строке скобка
                                end = bukva  # фиксация начала скобки со знаком вопроса
                                break
                        skobka = stroka[start:end + 1]
                        if re.search('\(\S+ ', skobka) or re.search(' \S+\)', skobka) or re.search(' \S+\|', skobka) or re.search('\|\S+ ', skobka):
                            skobka = skobka.replace(' ', '_').replace('(', '<').replace(')', '>').replace('|', '&')
                            stroka = stroka[:start] + skobka + stroka[end + 1:]
                        else:
                            skobka = skobka.replace('(', '<').replace(')', '>').replace('|', '&')
                            stroka = stroka[:start] + skobka + stroka[end + 1:]
                    stroka = stroka.replace('<', '(').replace('>', ')').replace('&', '|')
                spis_slov = stroka.split()
                for slovo in spis_slov:  # определяем кусок со скобкой
                    if re.match('\)\S*', slovo) or re.match('\S*\(', slovo):
                        slovo = list(slovo)
                        for bukva in range(len(slovo)):
                            if re.fullmatch('\(', slovo[bukva]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', slovo[bukva + 1]):  # если в строке скобка
                                start = bukva  # фиксация начала скобки со знаком вопроса
                                continue
                            if re.fullmatch('\)', slovo[bukva]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', slovo[bukva - 1]):  # если в строке скобка
                                end = bukva  # фиксация начала скобки со знаком вопроса
                                break
                        slovo = ''.join(slovo)
                        skobka = slovo[start:end + 1]
                        skobka = skobka.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", '')
                        slova_v_skobke = skobka.split('|')  # сделали варианты внутри скобки. добавили в новый список
                        slova_v_skobke.insert(0, spis_slov.index(slovo))  # добавили индекс
                        kolvo_slov_v_skob = len(slova_v_skobke) - 1  # минусуем на один, потому что один из элементов - это индекс. а нам надо знать точно количество слов
                        break
                new_stroki_vmeste = []
                for nomer_slova_v_skob in range(0, kolvo_slov_v_skob):
                    new_stroka = []
                    for indexslova, slovo in enumerate(spis_slov):
                        if '|' not in slovo:
                            new_stroka.append(slovo)
                        if '|' in slovo:
                            if indexslova == slova_v_skobke[0]:
                                vrem1 = []
                                vrem1.append(slovo[:start])
                                vrem1.append(slova_v_skobke[nomer_slova_v_skob + 1])
                                vrem1.append(slovo[end + 1:])
                                new_stroka.append(''.join(vrem1))
                            else:
                                new_stroka.append(slovo)
                    new_stroki_vmeste.append(' '.join(new_stroka))
                for new_stroka_vmeste in new_stroki_vmeste:
                    new_stroka_vmeste = new_stroka_vmeste.replace('_', ' ')
                    spis_strok.append(new_stroka_vmeste)
                spis_strok[indexstr] = '$'
                stroka = ', '.join([k for k in spis_strok if k != '$'])

        base_line = list(set([k for k in spis_strok if k != '$']))


    # программа перебирает все возможные варианты с одиночным знаком вопроса
    sp_bez_zn_vopr = []
    for nom_strok in range(len(base_line)):
        if '?' in base_line[nom_strok]:
            #print(a[nom_strok], 'a[nom_strok]')
            slovo = base_line[nom_strok]
            count = 0
            slovo = slovo.replace('((', '(').replace('))', ')').replace(')|(', '|')
            slovo = re.sub('^\(', '', slovo)
            slovo = re.sub('\)$', '', slovo)
            from itertools import permutations
            chet = []
            num_var = 2 ** len(re.findall("\?", slovo))  # количество вариатов перебора со знаком вопроса
            for k, e in enumerate(slovo):
                if e == '(':
                    chet.append(k)
                if e == ')':
                    chet.append(k)
            lend = len(chet)
            for i in range(0, lend - 1):
                if i % 2 == 0:
                    k = slovo[chet[i]:chet[i + 1] + 1].replace('(', '<').replace(')', '>').replace('|', '$')
                    slovo = slovo[:chet[i]] + k + slovo[chet[i + 1] + 1:]  # код ради того, чтобы правильно делить внутренние скобки
            if re.match('.*\?*', slovo):
                slovo = slovo.split('|')  # разбили строку на подстроки-слова по слэшу
                for i, j in enumerate(slovo):  # индекс слова. итерируем внутри каждого элемента между слэшами
                    if '?' in j:  # если в элементе есть знак вопроса, то
                        for k, p in enumerate(j):  # итерируем этот элемент между слэшами по буквам
                            if '?' in p:  # если '?' в букве, то
                                slovo.append(slovo[i][:k] + slovo[i][k + 1:])  # добавляем обработанные новые элементы в тек.список
                                slovo.append(slovo[i][:k - 1] + slovo[i][k + 1:])
                                slovo[i] = []  # делаем пустыми элементы, которые уже обработали
            name_var = list(filter(lambda x: x, slovo))  # итоговый варианты (список) со знаком "?" и без него.
            for i in name_var:
                sp_bez_zn_vopr.append(''.join(i))
        else:
            sp_bez_zn_vopr.append(base_line[nom_strok])
    new_list_from_original_line_key = list(set(sp_bez_zn_vopr))
    return new_list_from_original_line_key
def compare_words(word_from_line_key, word_from_line_exc):
    fix_match_word_key_and_exc = 0
    # ключ - *абв* - ключ
    if word_from_line_key[0] == '*' and word_from_line_key[len(word_from_line_key) - 1] == '*':

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *а*бв* или *абв*
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0

                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da1')
                        break

            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da2')
                        break  # искл - *а*бв* или *абв*   #искл - *а*бв* или *абв*

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(word_from_line_key[1:len(word_from_line_key) - 1]) and word_from_line_key[len(word_from_line_key) - 2] == word_from_line_exc[
                len(word_from_line_exc) - 1]:  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da3')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da4')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв*
            if len(word_from_line_exc[:len(word_from_line_key) - 1]) == len(word_from_line_key[1:len(word_from_line_key) - 1]) and word_from_line_key[1] == word_from_line_exc[0]:  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_key) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1

                    if counter_match == len(word_from_line_exc[:len(word_from_line_key) - 1]) - 1:
                        fix_match_word_key_and_exc = 1
                        #print('da5')
                        break
            if len(word_from_line_exc[:len(word_from_line_key) - 1]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0

                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc)]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                #print(num, '+++num')

                    if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da6')
                        break



        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None:  # искл - слово без звёзд. обычное слово
            #print(line_exc, 'искл - слово без звёзд. обычное слово2')
            sind = 0

            while fix_match_word_key_and_exc != 1:

                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                # time.sleep(0.2)
                #print('while prov != 1')
                for index_letter_key, letter_key in (list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in (list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc + 1 and index_letter_key == fix_index_letter_key + 1):

                            if (letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key))):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1

                        if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                            fix_match_word_key_and_exc = 1
                            #print('da7')
                            break

                if fix_match_word_key_and_exc != 1:
                    #print('точно нет совпадений между *ключом* и простым исклом')
                    break

                #     sind += 1
                #
                # if sind == len(line_exc) :
                #     #print(sind,  len(line_exc) - 1, 'sind == len(line_exc) - 1    -     точно нет совпадений между ключом и исклом (искл простое слово без звёзд)', line_key, line_exc)
                #     break

    # ключ - абв* - ключ
    if word_from_line_key[0] != '*' and word_from_line_key[len(word_from_line_key) - 1] == '*':
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *а*бв* или *абв*
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(
                    word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da8')
                        break
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(
                    word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da9')
                        break
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(word_from_line_key[:len(word_from_line_key) - 1]) and (
                    word_from_line_key[len(word_from_line_key) - 2] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 2] == '.' or word_from_line_exc[
                len(word_from_line_exc) - 1] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da10')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key[:len(word_from_line_key) - 1]) and (word_from_line_key[0] == word_from_line_exc[1] or word_from_line_key[0] == '.' or word_from_line_exc[
                1] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da11')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв* или а*бв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key[:len(word_from_line_key) - 1]) and (word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_key) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1

                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]) - 1:
                        fix_match_word_key_and_exc = 1
                        #print('da12')
                        break
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) > len(word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_key) - 1]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da13')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc):  # искл аб*в
            if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) == len(word_from_line_key[:len(word_from_line_key) - 1]) and (
                    word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[
                0] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                #print(line_key, line_exc)
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]):
                        fix_match_word_key_and_exc = 1
                        #print('da14')
                        break
            if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(
                    word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da15')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):  # искл - слово без звёзд. обычное слово
            counter_match = 0
            fix_index_letter_key = 0
            fix_index_letter_exc = 0
            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение

                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                            fix_index_letter_key = index_letter_key
                            fix_index_letter_exc = index_letter_exc
                            counter_match += 1

                if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                    fix_match_word_key_and_exc = 1
                    #print('da16')
                    break

    # ключ - *абв - ключ
    if word_from_line_key[0] == '*' and word_from_line_key[len(word_from_line_key) - 1] != '*':
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *а*бв* или *абв*
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(
                    word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da17')
                        break
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(
                    word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key)]):
                        fix_match_word_key_and_exc = 1
                        #print('da18')
                        break
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da19')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key)]):
                        fix_match_word_key_and_exc = 1
                        #print('da20')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв* или а*бв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key[1:]) and (word_from_line_key[1] == word_from_line_exc[0] or word_from_line_key[1] == '.' or word_from_line_exc[0] == '.'):

                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                #print(num, '   ', len(line_exc[:len(line_exc) - 1]))
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da21_000')
                        break

            if len(word_from_line_exc[1:]) > len(word_from_line_key[:len(word_from_line_key) - 1]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 2] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[len(word_from_line_exc) - 2] == '.'):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1

                    if counter_match == len(word_from_line_exc[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da21_111')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc):  # искл аб*в
            if len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]) == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[
                len(word_from_line_exc) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):

                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da23')
                        break
            if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(word_from_line_key[1:len(word_from_line_key) - 1]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[
                len(word_from_line_exc) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                #print(num)

                    if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_exc)).start():]):
                        fix_match_word_key_and_exc = 1
                        #print('da24')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and (
                word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[len(word_from_line_exc) - 1] == '.'):  # искл - слово без звёзд. обычное слово
            counter_match = 0
            fix_index_letter_key = 0
            fix_index_letter_exc = 0
            #print('1258', word_from_line_key[1:], word_from_line_exc)
            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение

                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                            fix_index_letter_key = index_letter_key
                            fix_index_letter_exc = index_letter_exc
                            counter_match += 1
                if counter_match == len(word_from_line_key[1:len(word_from_line_key)]):
                    fix_match_word_key_and_exc = 1
                    #print('da25')
                    break

    # ключ - а*бв - ключ
    if word_from_line_key[0] != '*' and word_from_line_key[len(word_from_line_key) - 1] != '*' and re.search('\w+\*\w+', word_from_line_key):
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*': fix_match_word_key_and_exc = 1  # искл - *а*бв* или *абв*

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da19')
                        break
            if len(word_from_line_exc[1:]) > len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da20')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв* или а*бв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]) and (
                    word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):
                counter_match = 0

                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                #print(num, '   ', len(line_exc[:len(line_exc) - 1]))
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da31')
                        break

            if len(word_from_line_exc[1:]) > len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 2] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[len(word_from_line_exc) - 2] == '.'):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                #print(len(line_key[:(re.search('\*', line_key)).start()]))
                    if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                        fix_match_word_key_and_exc = 1
                        #print('da32')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.') and (
                word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[
            len(word_from_line_exc) - 1] == '.'):  # искл аб*в
            if len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]) == len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):

                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]):
                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start() + 1]) == len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start() + 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд

                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                #print(line_key, line_exc, num, len(line_exc[:(re.search('\*', line_exc)).start()]))
                                if counter_match == len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da331')
                                    break

                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                for index_letter_exc, letter_exc in reversed(
                                        list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da332')
                                    break

            if len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]) > len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):

                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) == len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                if counter_match == len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da341')
                                    break

                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                for index_letter_exc, letter_exc in reversed(
                                        list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1

                                if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da342')
                                    break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.') and (
                word_from_line_exc[len(word_from_line_exc) - 1] == word_from_line_key[len(word_from_line_key) - 1] or word_from_line_exc[len(word_from_line_exc) - 1] == '.' or word_from_line_key[
            len(word_from_line_key) - 1] == '.'):  # искл - слово без звёзд. обычное слово
            line_key_izm = word_from_line_key[:(re.search('\*', word_from_line_key)).start()] + word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]
            if len(line_key_izm) == len(word_from_line_exc):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(line_key_izm))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc):
                        fix_match_word_key_and_exc = 1
                        #print('da35')
                        break
            if len(line_key_izm) < len(word_from_line_exc):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()])):  # проверка межзвёзднной части на совпадение
                    for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc)):
                        if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc - 1 == fix_index_letter_exc and index_letter_key - 1 == fix_index_letter_key)) and index_letter_key == index_letter_exc:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                #print('shodka')
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                break

                    if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                        counter_match = 0
                        fix_index_letter_key = 0
                        fix_index_letter_exc = 0
                        for index_letter_key, letter_key in reversed(
                                list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                            for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):
                                if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                    if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                        fix_index_letter_key = index_letter_key
                                        fix_index_letter_exc = index_letter_exc
                                        counter_match += 1
                            if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):
                                fix_match_word_key_and_exc = 1
                                #print('da36')
                                break

    # ключ - абв - ключ
    if word_from_line_key[0] != '*' and word_from_line_key[len(word_from_line_key) - 1] != '*' and re.search('\w+\*\w+', word_from_line_key) == None:
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *абв*
            #print('бобонька')
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0

                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da411')
                        break
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da412')
                        break

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and (
                word_from_line_exc[len(word_from_line_exc) - 1] == word_from_line_key[len(word_from_line_key) - 1] or word_from_line_exc[len(word_from_line_exc) - 1] == '.' or word_from_line_key[
            len(word_from_line_key) - 1] == '.'):  # искл - *абв
            if len(word_from_line_exc[1:]) == len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da421')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da422')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*' and (word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):  # искл - абв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da431')
                        break
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) > len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        #print(letter_key, letter_exc)
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                #print(counter_match, counter_match)
                    #print(counter_match , len(word_from_line_key), 'проверить da432')
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da432')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.') and (
                word_from_line_exc[len(word_from_line_exc) - 1] == word_from_line_key[len(word_from_line_key) - 1] or word_from_line_exc[len(word_from_line_exc) - 1] == '.' or word_from_line_key[
            len(word_from_line_key) - 1] == '.'):  # искл - слово без звёзд. обычное слово
            line_exc_izm = word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()] + word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]
            if len(line_exc_izm) == len(word_from_line_key):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):  # проверка межзвёзднной части на совпадение
                    for index_letter_exc, letter_exc in reversed(list(enumerate(line_exc_izm))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da46')
                        break
            if len(line_exc_izm) < len(word_from_line_key):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()])):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in list(enumerate(word_from_line_key)):
                        if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc - 1 == fix_index_letter_exc and index_letter_key - 1 == fix_index_letter_key)) and index_letter_key == index_letter_exc:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                #print('shodka22')
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                break

                    if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_exc)).start()]):
                        counter_match = 0
                        fix_index_letter_key = 0
                        fix_index_letter_exc = 0
                        for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                                if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                    if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                        fix_index_letter_key = index_letter_key
                                        fix_index_letter_exc = index_letter_exc
                                        counter_match += 1
                            if counter_match == len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]):
                                fix_match_word_key_and_exc = 1
                                #print('da47')
                                break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None:  # искл - слово без звёзд. обычное слово
            if len(word_from_line_key) == len(word_from_line_exc):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in list(enumerate(word_from_line_key)):  # проверка межзвёзднной части на совпадение
                    for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc)):
                        if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc - 1 == fix_index_letter_exc and index_letter_key - 1 == fix_index_letter_key)) and index_letter_key == index_letter_exc:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                break
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da50')
                        break

    # ключ-искл - .* - ключ-искл
    if word_from_line_exc == '.*' or word_from_line_key == '.*':
        fix_match_word_key_and_exc = 1
        #print('da51')


    return fix_match_word_key_and_exc
def compare_lines_new(stroka1, stroka2):
    count = 0
    maxdist = 0
    sum = 0
    factor = 0
    maxdist1 = 0
    num_word = 0
    fix_index_letter_key = 0
    fix_index_letter_exc = 0
    match = 0

    for index1, slovo1 in enumerate(stroka1.split()) :
        if re.fullmatch('\d+\®\d+', slovo1) == None :
            num_word += 1
        for index2, slovo2 in enumerate(stroka2.split()):
            #print('                              ', slovo1,  '-',slovo2,  '    ', count, '---ключ-', index1, fix_index_letter_key, '---искл-', index2, fix_index_letter_exc, '------sum, num_word-', sum, num_word)
            if compare_words(slovo1, slovo2) == 1 and re.fullmatch('\d+\®\d+', slovo1) == None and re.fullmatch('\d+\®\d+', slovo2) == None:  # совпадение слов
                if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index2 == fix_index_letter_exc + 1 and index1 == fix_index_letter_key + 1)) and count == 0 and factor == 0:
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -*1*-  ', slovo2)
                    sum += 1
                    factor = 1
                    break
            if re.fullmatch('\d+\®\d+', slovo1) and re.fullmatch('\d+\®\d+', slovo2) == None and count == 0:  # если ключ - расстояние 0,1
                if index2 == fix_index_letter_exc + 1 and index1 == fix_index_letter_key + 1:
                    maxdist1 = slovo1.split('®')[1]
                    ##print(slovo1, 'maxdist1')
                    count = 1
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -2-  ', slovo2)
                    break

            if re.fullmatch('\d+\®\d+', slovo1) and re.fullmatch('\d+\®\d+', slovo2) == None and count != 0:  # если ключ - расстояние 0,1
                if index2 == fix_index_letter_exc + 1 and index1 == fix_index_letter_key + 1:
                    maxdist1 = slovo1.split('®')[1]
                    count += int(maxdist1)
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -3-  ', slovo2)
                    break

            #print(compare_words(slovo1, slovo2), count, maxdist1, 'случай')
            if re.fullmatch('\d+\®\d+', slovo1) == None and re.fullmatch('\d+\®\d+', slovo2) == None and compare_words(slovo1, slovo2) == 0 and 0 <= int(count) <= int(maxdist1):  # переходим к следующему слову-ключу, итерируясь по словам-исключениям, используя запас
                if index2 == fix_index_letter_exc + 1:
                    count += 1
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -4-  ', slovo2)

            if compare_words(slovo1, slovo2) == 1 and re.fullmatch('\d+\®\d+', slovo1) == None and re.fullmatch('\d+\®\d+', slovo2) == None:  # совпадение слов
                # print(count, maxdist1, 'внутри слово слово')
                if index2 == fix_index_letter_exc + 1 and 0 <= int(count) <= int(maxdist1):
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -*5*-  ', slovo2)
                    count = 0
                    sum += 1
                    break

            if compare_words(slovo1, slovo2) == 1:  # совпадение слов, в строке исключении - последнее слово
                if index2 == fix_index_letter_exc and index2 == len(stroka2.split()) - 1:
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -*6*-  ', slovo2)
                    sum += 1
                    break

            if re.fullmatch('\d+\®\d+', slovo1) and re.fullmatch('\d+\®\d+', slovo2) and count == 0:
                if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index2 == fix_index_letter_exc + 1 and index1 == fix_index_letter_key + 1):
                    ##print(slovo1, 'slova', slovo2, )
                    mindist1 = int(slovo1.split('®')[0])
                    maxdist1 = int(slovo1.split('®')[1])
                    mindist2 = int(slovo2.split('®')[0])
                    maxdist2 = int(slovo2.split('®')[1])
                    count = maxdist2
                    fix_index_letter_key = index1
                    fix_index_letter_exc = index2
                    #print('предшественник 5го -', slovo1, slovo2)
                    #if mindist1 == mindist2 and maxdist2 <= maxdist1:
                        #print(slovo1, '  -7-  ', slovo2)

            if re.fullmatch('\d+\®\d+', slovo1) == None and re.fullmatch('\d+\®\d+', slovo2) and count != 0:
                if index2 == fix_index_letter_exc + 1:
                    maxdist2 = slovo2.split('®')[1]
                    count = int(count) + int(maxdist2)
                    fix_index_letter_exc = index2
                    #print(slovo1, '  -8-  ', slovo2)

    #print('в конце', sum, num_word)

    if sum == num_word:
        match = 1

    return match
def add_dist(a):
    while re.search(' \d*\®\d* ', a):
        z_start = int(re.search(' \d*\®\d* ', a).start() )
        z_end = int(re.search(' \d*\®\d* ', a).end())-1
        a=a[:z_start]+'¢'+a[z_start+1:z_end]+'¢'+a[z_end+1:]
    a=a.replace(' ',' 0®0 ').replace('¢',' ')
    return a
def timeit(func):
    def wrapper():
        global total_time
        t_start = time.monotonic()
        func()
        t_stop = time.monotonic()
        t_run = t_stop - t_start
        one_time = round(t_run, 1)
        total_time = total_time + one_time
        left_time = time.strftime("%H:%M:%S", time.gmtime((len(original_list) - counter_line_from_orig_list_key) * round(total_time / counter_line_from_orig_list_key, 1)))
        print(f'{round(counter_line_from_orig_list_key+1, 1)} пройдено из {len(original_list)}   |   ',    time.strftime("%H:%M:%S", time.gmtime(round(total_time, 1))), 'прошло со старта   |   ', round(one_time, 1), 'сек. время этой операции   |   ', round(total_time / counter_line_from_orig_list_key, 1) , 'cреднее время одной строки сек   |   ',  left_time, "осталось до конца программы   |   ",  len(dict1[orig_index_line1+1]), "строк в след строке   |   ",  original_list[orig_index_line1+1][:30], f" --- след строка {round(counter_line_from_orig_list_key+2, 1)}   |   ", datetime.datetime.now().strftime('%H:%M:%S'))
        #print(orig_line1)

    return wrapper
@timeit
def main_compare():
    if orig_index_line1 != len(dict1) - 1:
        count_orig_line2 = 0
        if len(dict1[orig_index_line1]) <= 5:
            for orig_index_line2, orig_line2 in enumerate(dict1):
                if len(dict1[orig_index_line2]) <= 5:
                    count_orig_line2 += 1
                    #print(count_orig_line1, 'из', len(original_list), '---',count_orig_line2, 'из', len(original_list),'      ', dict1[orig_index_line1],'-', dict1[orig_index_line2])
                    if orig_index_line2 > orig_index_line1:
                        # print(orig_index_line1, orig_index_line2)
                        count_match = 0
                        for new_line1 in dict1[orig_index_line1]:
                            for new_line2 in dict1[orig_index_line2]:
                                #print(add_dist(new_line1), '-', add_dist(new_line2), '----строки')
                                if compare_lines_new(add_dist(new_line1), add_dist(new_line2)) == 1:
                                    count_match += 1
                                    if count_match == len(dict1[orig_index_line2]) and re.search('.*\[а-я\]\+.*', original_list[orig_index_line2]) == None:
                                        print('!!!ДУБЛЬ!!! ---> ', original_list[orig_index_line1][:50], '---', original_list[orig_index_line2][:50])
                                        original_list[orig_index_line2] = '¶'
def get_all_elements_in_list_of_lists(list):
    count_elem = 0
    for element in list:
        count_elem += len(element)
    return count_elem
def show_big_lines(list):
    dict_big_line = []
    for indexel, element in enumerate(list):
        if len(element)>10:
            dict_big_line.append(original_list[indexel])
    return dict_big_line

original_list=file('C:\\Users/piolv/Desktop/file_for_program/iskl000.txt')
dict1=[]
dict2=[]
dict3={}

for original_line in original_list:
    dict3[original_line]=len(repreg(original_line))
sorted_tuples = sorted(dict3.items(), key=lambda item: item[1], reverse=True)
sorted_dict = {k: v for k, v in sorted_tuples}
original_list= [key for key in sorted_dict]

for original_line in original_list:
    original_line = original_line.replace(u'\xa0', u' ')
    dict2.append(original_line)
original_list=dict2
for original_line in original_list:
    dict1.append(repreg(original_line))

print(dict1)
print(f'\n\n{len(dict1)} - число строк в изначальном словаре \n{get_all_elements_in_list_of_lists(dict1)} - число внутренних строк \n{len(show_big_lines(dict1))} число строк, с которыми не работаем')

total_time = 0
counter_line_from_orig_list_key=0
count_orig_line1 = 0
for orig_index_line1, orig_line1 in enumerate(dict1):
    count_orig_line1+=1
    counter_line_from_orig_list_key += 1
    #print(count_orig_line1, 'из 1 части', len(original_list))
    main_compare()
original_list=[k for k in original_list if k != '¶']
print(len(original_list), '- столько строк осталось1', original_list)

file_for_record = open('C:\\Users/piolv/Desktop/file_for_program/rezult_compare_keys_exc.txt', 'w')
for newlinerec in original_list:
	file_for_record.write(str(newlinerec + '\n'))
file_for_record.close()