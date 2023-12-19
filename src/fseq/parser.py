
class ParserError(Exception):
    pass


def int_from_bytes(bytes):
    # TODO: only valid in python 3.2+
    return int.from_bytes(bytes, 'little')


def compression_type_from_num(n):
    if n == 0:
        return 'none'
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
            frame_offsets,
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
        self.frame_offsets = frame_offsets
        self.sparse_ranges = sparse_ranges
        self.variable_headers = variable_headers

    def get_frame(self, frame):
        if frame >= self.number_of_frames:
            raise ValueError('frame index out of bounds')

        curblock = 0
        while frame >= self.frame_offsets[curblock + 1][0]:
            curblock += 1

        offset = self.frame_offsets[curblock][1]
        self.file.seek(offset, 0)

        if self.compression_type == 'zstd':
            import zstandard as zstd
            dctx = zstd.ZstdDecompressor()

            length = self.frame_offsets[curblock + 1][1] - self.frame_offsets[curblock][1]
            block = self.file.read(length)
            block = dctx.stream_reader(block).readall()

            fidx = (frame - self.frame_offsets[curblock][0]) * self.channel_count_per_frame
            data = block[fidx:fidx+self.channel_count_per_frame]
            return data
        else:
            block = self.file.read()
            fidx = frame * self.channel_count_per_frame
            data = block[fidx:fidx+self.channel_count_per_frame]
            return data
        

    def _expand_sparse_ranges(self, data):
        # TODO
        pass



def parse(f):
    magic = f.read(4)
    if magic != b'PSEQ':
        raise ParserError('invalid fseq file magic: %s', magic)

    channel_data_start = int_from_bytes(f.read(2))

    minor_version = int_from_bytes(f.read(1))
    major_version = int_from_bytes(f.read(1))

    version = (major_version, minor_version)
    if major_version != 2:
        raise ParserError('unrecognized fseq file version: %s' % version)

    standard_header_length = int_from_bytes(f.read(2))

    channel_count_per_frame = int_from_bytes(f.read(4))

    number_of_frames = int_from_bytes(f.read(4))

    step_time_in_ms = int_from_bytes(f.read(1))

    bit_flags = int_from_bytes(f.read(1))
    if bit_flags != 0:
        raise ParserError('unrecognized bit flags: %d' % bit_flags)

    compression_type = compression_type_from_num(int_from_bytes(f.read(1)))
    if compression_type == 'gzip':
        raise ParserError('unsupported compression type: %s' % compression_type)

    num_compression_blocks = int_from_bytes(f.read(1))
    num_sparse_ranges = int_from_bytes(f.read(1))

    bit_flags = int_from_bytes(f.read(1))
    if bit_flags != 0:
        raise ParserError('unrecognized bit flags: %d' % bit_flags)

    unique_id = f.read(8)

    offset = channel_data_start
    frame_offsets = []
    if compression_type == 'none':
        frame_offsets.append((0, offset))
    for i in range(num_compression_blocks):
        frame_number = int_from_bytes(f.read(4))
        length_of_block = int_from_bytes(f.read(4))

        if length_of_block > 0:
            frame_offsets.append((frame_number, offset))
            offset += length_of_block
    frame_offsets.append((number_of_frames, offset))

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
        frame_offsets=frame_offsets,
        sparse_ranges=sparse_ranges,
        variable_headers=variable_headers,
    )
