from __future__ import print_function

import array
import png
import json

from st2actions.runners.pythonrunner import Action

__all__ = [
    'ImageDecoder'
]


def _get_image_array(image_path):
    with open(image_path, 'rb') as image_fd:
        image_reader = png.Reader(file=image_fd)

        image_map = image_reader.read()[2]

        return list(image_map)


def _get_bit_stream(message):
    for char in message:
        char_int = ord(char)

        for i in range(8):
            yield char_int >> i & 1


def _assemble_bit_stream(message_array):
    return message_array


def _encode_image(image, bit_stream):
    new_image = []
    for byte_array in image:
        new_byte_array = array.array('B')
        for byte in byte_array:
            try:
                bit = bit_stream.next()
            except StopIteration:
                bit = 0

            new_byte = byte & int('11111110', 2) | int('0000000%s' % bit, 2)

            new_byte_array.append(new_byte)

        new_image.append(new_byte_array)

    return new_image


def _decode_image(image):
    return image


def _save_image(name, image_map):
    image = png.from_array(image_map, mode='RGBA')
    image.save(name)


def _encode(image, output_image, message):
    for arg in [image, output_image, message]:
        if not isinstance(arg, str):
            raise TypeError("Argument must be string.")

        if arg == '':
            raise ValueError("Argument cannot be empty.")

    image_map = _get_image_array(image)
    bit_generator = _get_bit_stream(message)
    encoded_array = _encode_image(image_map, bit_generator)
    _save_image(output_image, encoded_array)


def _remove_null(output):
    try:
        output = output[:output.index(u'\u0000')]

    except ValueError:
        return

    return output


def _decode(image):
    if not isinstance(image, str):
        raise TypeError("Argument must be string.")

    if image == '':
        raise ValueError("Argument cannot be empty.")

    image_map = _get_image_array(image)
    bit_stream = _decode_image(image_map)
    output = _assemble_bit_stream(bit_stream)

    return _remove_null(output)


class ImageDecoder(Action):
    def run(self, encode, image, output_image=None, message=None):
        if encode:
            _encode(
                str(image),
                str(output_image),
                str(message)
            )

            return True

        elif not encode:
            result = {
                'message': str(_decode(str(image)))
            }

            return json.dumps(result)
