import os
from fseq import parse


def test_main():
    path = os.path.join(os.path.dirname(__file__), 'test.fseq')
    fseq_obj = parse(open(path, 'rb'))

    assert fseq_obj is not None
    assert fseq_obj.version == (2, 0)
    assert fseq_obj.channel_data_start == 2144
    assert fseq_obj.channel_count_per_frame == 17372
    assert fseq_obj.number_of_frames == 9563
    assert fseq_obj.step_time_in_ms == 25
    assert fseq_obj.compression_type == 'zstd'
    assert fseq_obj.unique_id == b'\xb0\xf2\xb8\xb3g\x82\x05\x00'
    assert fseq_obj.variable_headers == [
        ('mf', b'/Users/nico/Domencia/multimedia files/the-chemical-brothers-star-guitar.mp3\0')
    ]
    assert len(fseq_obj.compression_blocks) > 0
    assert fseq_obj.sparse_ranges == []


    assert fseq_obj.frame_at(0) is not None
