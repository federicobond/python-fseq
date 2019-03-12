python-fseq
===========

A Falcon Pi Player fseq (v2) sequence file parser.

### Installation

    pip install fseq


### Usage

To use the project:

    import fseq

    f = open('filename.fseq')
    fseq.parse(f)


The `parse` function returns a `Fseq` object with the following properties:

 * `file`: the underlying file object
 * `version`: a 2-tuple of numbers containing major and minor version
 * `minor_version`: the minor version number
 * `major_version`: the major version number
 * `channel_count_per_frame`: the amount of channels in each frame
 * `number_of_frames`: the total number of frames in this sequence
 * `step_time_in_ms`: the number of milliseconds between each frame
 * `unique_id`: a unique indentified
 * `compression_type`: the compression type used for frames, either `none`, `zstd`, `zlib`
 * `variable_headers`: an array of 2-tuples containing key-value pairs describing additional headers for the sequence file

To access a single frame data use the `get_frame(index)` method on the `Fseq`
object.


### Development

To run the all tests run:

    tox


### TODO

 * Add support for fseq files without compression
 * Add support for fseq files with Zlib compression
 * Add support for fseq files with sparse ranges
 * Add support for writing fseq files


### License

MIT

## Author

Federico Bond
