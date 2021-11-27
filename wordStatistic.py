import logging
import sys

''' 统计英文文本文件中单词词频 
1. 文件可能很大
2. 文本可能不分行
'''

block_size = 100 * 1024
word_seps = '\n\t ,.;:\'\"\\-_+=*&^$#@!~`|%1234567890?/<>()[]{}'
word_map = {}


def multi_split(buf, seps=[' ', ]):
    """多分割字符的字符串分割"""
    word = ''
    words = []
    word_end = 0
    word_start = word_end

    for word_end in range(len(buf)):
        if buf[word_end] not in seps:
            continue
        else:
            word = buf[word_start:word_end]
            words.append(word) if word else 0
            word_start = word_end + 1

    # 末尾处理
    if word_start <= word_end:
        word = buf[word_start:word_end + 1]
        words.append(word) if word else 0

    return words


def count_word(words):
    for word in words:
        word = word.lower()
        word_map.setdefault(word, 0)
        word_map[word] += 1


def statistic_output():
    word_list = [[word, count] for word, count in word_map.items()]
    word_list.sort(key=lambda x: x[1], reverse=1)
    for word, count in word_list:
        print("%s : %d" % (word.rjust(30), count))
        logging.warning("%s : %d" % (word.rjust(30), count))
    print("Total %d words." % len(word_list))
    logging.warning("Total %d words." % len(word_list))


def statistic(path_file):
    try:
        f = open(path_file)
    except FileNotFoundError:
        print("Error: file %s not exist!" % path_file)
        return

    left_, _right, end_word = False, False, ''
    block = f.read(block_size)
    while block:
        # 最后一个词可能被按块读截断了
        _right = True if block[0] not in word_seps else False
        left_ = True if block[-1] not in word_seps else False
        words = multi_split(block, list(word_seps))
        logging.debug('READ:\n' + format(words))
        if end_word:
            if _right:
                end_word += words[0]
                del words[0]
            words.insert(0, end_word)
            end_word = ''
            logging.info('FORWARD:' + format(words))
        if left_:
            end_word = words[-1]
            del words[-1]
            logging.info('BACKWARD:' + format(words))

        # 按词计数
        count_word(words)
        block = f.read(block_size)

    if end_word:
        count_word([end_word, ])

    # 按序输出
    f.close()
    statistic_output()


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        filename='log.txt',
                        filemode='w',)
    path_file = sys.argv[1] if len(sys.argv) > 1 else input()
    path_file = path_file if path_file else '1.txt'
    logging.warning("Starting...")
    statistic(path_file)
