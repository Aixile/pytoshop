# -*- coding: utf-8 -*-


import io
import os


import numpy as np
import pytest


import psdwriter
from psdwriter import enums
from psdwriter.user import nested_layers


DATA_PATH = os.path.join(os.path.dirname(__file__), 'psd_files')


def test_nested_layers():
    filename = os.path.join(DATA_PATH, 'group.psd')
    with open(filename, 'rb') as fd:
        psd = psdwriter.PsdFile.read(fd)

    layers = nested_layers.psd_to_nested_layers(psd)

    nested_layers.pprint_layers(layers)

    psd2 = nested_layers.nested_layers_to_psd(layers)

    fd = io.BytesIO()
    psd2.write(fd)


def test_nested_layers_no_adjust():
    filename = os.path.join(DATA_PATH, 'group.psd')
    with open(filename, 'rb') as fd:
        psd = psdwriter.PsdFile.read(fd)

    layers = nested_layers.psd_to_nested_layers(psd)

    psd2 = nested_layers.nested_layers_to_psd(
        layers, size=(psd.width, psd.height))

    fd = io.BytesIO()
    psd2.write(fd)


def test_errors():
    with pytest.raises(TypeError):
        nested_layers.psd_to_nested_layers(None)


@pytest.mark.parametrize("vector_mask", (True, False))
def test_from_scratch(vector_mask):
    from psdwriter.user.nested_layers import Group, Image

    img1 = np.empty((100, 80), dtype=np.uint8)
    img2 = np.empty((100, 80), dtype=np.uint8)
    img3 = np.empty((100, 80), dtype=np.uint8)
    img4 = np.empty((2, 100, 80), dtype=np.uint8)

    layers = [
        Group(
            layers=[
                Image(channels={0: img1},
                      top=0, left=0, bottom=100, right=80),
                Image(channels=img2,
                      top=15, left=15),
                Image(channels=img4,
                      top=42, left=43),
                Image(channels=[img1, img1],
                      top=-5, left=49)
            ]),
        Image(channels={0: img3})
    ]

    psd = nested_layers.nested_layers_to_psd(
        layers, color_mode=enums.ColorMode.grayscale,
        vector_mask=vector_mask)

    buff = io.BytesIO()
    psd.write(buff)

    buff.seek(0)

    psdwriter.read(buff)


