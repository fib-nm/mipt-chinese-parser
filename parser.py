import re


def parse(path='chinese.txt'):
    with open(path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    if lines[len(lines)-1]:
        lines[len(lines)-1] += "\n"

    with open('chinese_hieroglyphs.txt', 'w', encoding="utf-8") as hieroglyphs,\
            open('chinese_pinyin.txt', 'w', encoding="utf-8") as pinyin,\
            open('chinese_translation.txt', 'w', encoding="utf-8") as translation,\
            open('chinese_word_class.txt', 'w', encoding="utf-8") as word_class:
        for i in range(len(lines)):
            current_line = lines[i]

            # removing first numbers
            first_non_digit = re.search(r'[^0-9]', current_line)
            if first_non_digit[0] == ' ':
                current_line = current_line[first_non_digit.span()[1]:]
            else:
                current_line = current_line[first_non_digit.span()[0]:]

            # removing word classes
            w_cl = ''
            ch_brackets = re.search(r'[(（]((代词|形容词|数词|名词|副词|助词|动词|专名|转名|连词|量词|疑问词|介词|叹词|疑问代词|连接词)([/／,，+]|))+[)）]', current_line)
            if ch_brackets:
                w_cl = current_line[ch_brackets.span()[0] + 1:ch_brackets.span()[1] - 1]
                current_line = current_line[0:ch_brackets.span()[0]] + current_line[ch_brackets.span()[1]:]

            # check if line has hieroglyphs
            if not re.search(r'[\u4E00-\u9FFF\uF900-\uFAFF\u2F00-\u2FDF\u3200-\u32FF\u3000-\u303F\u3200-\u32FF]', current_line):  # если иероглиф не находится в строке, ничего не записывается и цикл прерывается
                continue

            # matching =================================================================================================
            hieroglyphs_list = []
            for j in re.finditer(r'([(（]|)[\u4E00-\u9FFF\uF900-\uFAFF\u2F00-\u2FDF\u3200-\u32FF\u3000-\u303F\u3200-\u32FF]([)）]|)', current_line):
                hieroglyphs_list.append(j)
            pinyin_list = []
            if re.search(r'([(（]|)[a-zA-ZāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜüĀĒĪŌŪǕÁÉÍÓÚǗǍĚǏǑǓǙÀÈÌÒÙǛÜ]([)）]|)', current_line):
                for j in re.finditer(r'([(（]|)[a-zA-ZāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜüĀĒĪŌŪǕÁÉÍÓÚǗǍĚǏǑǓǙÀÈÌÒÙǛÜ]([)）]|)', current_line):
                    pinyin_list.append(j)
            translation_list = []
            if re.search(r'[0-9а-яА-Я]', current_line):
                for j in re.finditer(r'[0-9а-яА-Я]', current_line):
                    translation_list.append(j)

            # deleting pinyin that occurs before first hieroglyph from pinyin_list
            k = 0
            while k < len(pinyin_list):
                if pinyin_list[k].start() < hieroglyphs_list[0].start():
                    pinyin_list.pop(k)
                else:
                    k += 1

            # writing ==================================================================================================
            # Иероглиф не может идти после пиньиня или перевода (кроме первого иероглифа)
            hieroglyph_limit = len(current_line)  # позиция иероглифа должна быть < hieroglyph_limit.
            if pinyin_list:
                hieroglyph_limit = min(pinyin_list[0].start(), hieroglyph_limit)
            if translation_list:
                hieroglyph_limit = min(translation_list[0].start(), hieroglyph_limit)
            last_hieroglyph_pos = hieroglyph_limit
            for j in hieroglyphs_list:
                if j.start() < hieroglyph_limit:
                    last_hieroglyph_pos = j.end()
            hieroglyphs.write(current_line[:last_hieroglyph_pos] + '\n')

            # writing word class
            word_class.write(w_cl + '\n')

            # removing pinyin which goes after translation start
            if translation_list:
                k = 0
                while k < len(pinyin_list):
                    if pinyin_list[k].start() > translation_list[0].start():
                        pinyin_list.pop(k)
                    else:
                        k += 1

            # write pinyin
            if pinyin_list:
                pinyin.write(current_line[pinyin_list[0].start():pinyin_list[len(pinyin_list)-1].end()] + '\n')
            else:
                pinyin.write('\n')

            # write translation
            if translation_list:
                translation.write(current_line[translation_list[0].start():])
            else:
                translation.write('\n')


parse()
