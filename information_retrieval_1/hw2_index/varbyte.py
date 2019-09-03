# -*- coding: utf-8 -*-
import bitstream


def to_binary_8bits(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])


def compress(dl):
    bs = bitstream.BitstreamWriter()

    for index in range(len(dl)):
        if (index == 0):
            gap = dl[index]
        else:
            gap = dl[index] - dl[index - 1]

        byte_end_counter = 0
        if gap == 0:
            for i in range(7):
                bs.add(0)
            byte_end_counter = 7
        while(gap):
            bs.add(gap & 1)
            gap = gap >> 1
            byte_end_counter += 1

            # last byte first bit c = 1; other bytes c = 0
            if (byte_end_counter == 7):
                if gap:
                    bs.add(0)  # 7 bits already added and it's not last byte
                byte_end_counter = 0

        if (byte_end_counter > 0):
            while(byte_end_counter < 7):
                bs.add(0)  # leading zeros
                byte_end_counter += 1

        bs.add(1)  # end of number

    return bs.getbytes()


def decompress(s):
    bs = bitstream.BitstreamReader(s)
    dl = []

    bit_counter = 0
    previous_numbers = 0
    number = 0
    while (not bs.finished()):

        for i in range(7):  # read byte
            bit = bs.get()
            number += (bit << bit_counter)
            bit_counter += 1
        if(bs.get()):
            bit_counter = 0  # end of number
            dl.append(number + previous_numbers)
            previous_numbers += number
            number = 0

    return dl


def print_string_as_binary(s):
    print ' '.join(format(ord(x), '08b') for x in s)


# test_list = [0, 3, 5, 8, 199]
# print_string_as_binary(compress(test_list))
# print decompress(compress(test_list))

