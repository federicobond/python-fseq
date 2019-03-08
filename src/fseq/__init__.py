__version__ = '0.1.0'

import zstandard as zstd


class ParserError(Exception):
    pass


def int_from_bytes(bytes):
    # TODO: only valid in python 3.2+
    return int.from_bytes(bytes, 'little')


def compression_type_from_num(n):
    if n == 0:
        return None
    if n == 1:
        return 'zstd'
    if n == 2:
        return 'gzip'
    raise ParserError('unrecognized compression type: %d' % n)


class Fseq:
    def __init__(
            self,
            file,
            minor_version,
            major_version,
            channel_data_start,
            channel_count_per_frame,
            number_of_frames,
            step_time_in_ms,
            unique_id,
            compression_type,
            compression_blocks,
            sparse_ranges,
            variable_headers):

        self.file = file
        self.minor_version = minor_version
        self.major_version = major_version
        self.version = (major_version, minor_version)

        self.channel_data_start = channel_data_start
        self.channel_count_per_frame = channel_count_per_frame
        self.number_of_frames = number_of_frames
        self.step_time_in_ms = step_time_in_ms
        self.unique_id = unique_id
        self.compression_type = compression_type
        self.compression_blocks = compression_blocks
        self.sparse_ranges = sparse_ranges
        self.variable_headers = variable_headers

    def frame_at(self, index):
        if index >= self.number_of_frames:
            raise ValueError('frame index out of bounds')

        offset = self.channel_data_start + index * self.channel_count_per_frame
        self.file.seek(offset, 0)
        # data = self.file.read(self.channel_count_per_frame)
        # return [b for b in data]


def parse(f):
    magic = f.read(4)
    if magic != b'PSEQ':
        raise ParserError('invalid fseq file magic')

    channel_data_start = int_from_bytes(f.read(2))

    minor_version = int_from_bytes(f.read(1))
    major_version = int_from_bytes(f.read(1))

    version = (major_version, minor_version)
    if version != (2, 0):
        raise ParserError('unrecognized fseq file version: %s' % version)

    standard_header_length = int_from_bytes(f.read(2))

    channel_count_per_frame = int_from_bytes(f.read(4))

    number_of_frames = int_from_bytes(f.read(4))

    step_time_in_ms = int_from_bytes(f.read(1))

    bit_flags = int_from_bytes(f.read(1))
    if bit_flags != 0:
        raise ParserError('unrecognized bit flags: %d' % bit_flags)

    compression_type = compression_type_from_num(int_from_bytes(f.read(1)))
    num_compression_blocks = int_from_bytes(f.read(1))
    num_sparse_ranges = int_from_bytes(f.read(1))

    bit_flags = int_from_bytes(f.read(1))
    if bit_flags != 0:
        raise ParserError('unrecognized bit flags: %d' % bit_flags)

    unique_id = f.read(8)

    compression_blocks = []
    for i in range(num_compression_blocks):
        frame_number = int_from_bytes(f.read(4))
        length_of_block = int_from_bytes(f.read(4))
        compression_blocks.append((frame_number, length_of_block))


    sparse_ranges = []
    for i in range(num_sparse_ranges):
        start_channel_number = int_from_bytes(f.read(3))
        number_of_channels = int_from_bytes(f.read(3))
        sparse_ranges.append((start_channel_number, number_of_channels))

    variable_headers = []
    start = f.tell()

    while start < channel_data_start - 4:
        length = int_from_bytes(f.read(2))
        if length == 0:
            break

        vheader_code = f.read(2).decode('ascii')
        vheader_data = f.read(length - 4)
        variable_headers.append((vheader_code, vheader_data))

        start += length

    return Fseq(
        file=f,
        minor_version=minor_version,
        major_version=major_version,
        channel_data_start=channel_data_start,
        channel_count_per_frame=channel_count_per_frame,
        number_of_frames=number_of_frames,
        step_time_in_ms=step_time_in_ms,
        unique_id=unique_id,
        compression_type=compression_type,
        compression_blocks=compression_blocks,
        sparse_ranges=sparse_ranges,
        variable_headers=variable_headers,
    )
