import os
from fseq import parse


def test_parse():
    path = os.path.join(os.path.dirname(__file__), 'test.fseq')
    fseq_obj = parse(open(path, 'rb'))

    assert fseq_obj is not None
    assert fseq_obj.version == (2, 0)
    assert fseq_obj.channel_data_start == 2144
    assert fseq_obj.channel_count_per_frame == 17372
    assert fseq_obj.number_of_frames == 9563
    assert fseq_obj.step_time_in_ms == 25
    assert fseq_obj.compression_type == 'zstd'
    assert fseq_obj.unique_id == b'\xb1,t\x15\xb9\x82\x05\x00'
    assert fseq_obj.variable_headers == [
        ('mf', b'/Users/nico/Domencia/multimedia files/the-chemical-brothers-star-guitar.mp3\0')
    ]
    assert len(fseq_obj.frame_offsets) > 0
    assert fseq_obj.sparse_ranges == []

    assert fseq_obj.frame_offsets[27] == (998, 884415)
    assert fseq_obj.frame_offsets[28] == (1036, 922791)

    frame = fseq_obj.get_frame(1000)
    expected_frame_start = [0,0,0,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,255,255,255,0,0,0,0,0,0,255,255,255,255,255,255,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255]
    assert [d for d in frame[:len(expected_frame_start)]] == expected_frame_start


def test_examples():
    for example in ('test2.fseq', 'test3.fseq', 'test4.fseq'):
        path = os.path.join(os.path.dirname(__file__), example)
        parse(open(path, 'rb'))
