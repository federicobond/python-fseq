FSEQ v2.0 specification (unofficial)
====================================

This spec was written partly by reading the brief reference in the Falcon
[docs](https://github.com/FalconChristmas/fpp/blob/c51adce1ff3938356bea732a71047ab95eb38446/docs/FSEQ_Sequence_File_Format.txt)
and partly by reverse-engineering the official C++ code from the
Falcon Player [repo](https://github.com/FalconChristmas/fpp/tree/master/src/fseq).
As such it may not reflect exactly the intentions of the original author.

All numbers are encoded little endian.

## File header

| Bytes | Description                                                        |
| ----- | ------------------------------------------------------------------ |
| 0-3   | Magic file identifier, must be 'PSEQ'                              |
| 4-5   | Offset to the start of channel data                                |
| 6     | Minor version, should be 0                                         |
| 7     | Major version, should be 2                                         |
| 8-9   | Standard header length/index to first variable header              |
| 10-13 | Channel count per frame (\*)                                       |
| 14-17 | Number of frames                                                   |
| 18    | Step time in ms, usually 25 or 50                                  |
| 19    | Bit flags/reserved should be 0                                     |
| 20    | Compression type 0 for uncompressed, 1 for zstd, 2 for libz/gzip   |
| 21    | Number of compression blocks, 0 if uncompressed                    |
| 22    | Number of sparse ranges, 0  if none                                |
| 23    | Bit flags/reserved, unused right now, should be 0                  |
| 24-31 | 64-bit unique identifier, likely a timestamp or uuid               |

## Compressed block index

If the files is compressed, a sequence of tuples containing the compression
index will follow. Each tuple contains the index of the first compressed frame
in the block and its size. To access a frame data, look for last block with a
frame number smaller than the frame you want and decompress it. Then advance
the pointer N times by the number of channels in each block, where N is the
difference between the frame index you want and the frame index at the start
of the block.


| Bytes | Description     |
| ----- | --------------- |
| 0-3   | Frame number    |
| 4-7   | Length of block |

## Sparse ranges

After the block index, a sequence of sparse ranges follows. Each sparse range
is defined by a start channel number and a number of channels.

| Bytes | Description          |
| ----- | -------------------- |
| 0-2   | Start channel number |
| 3-5   | Number of channels   |
