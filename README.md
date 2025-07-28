# Benchmarking Compression Algorithms: Zstandard, Gzip, and a Custom Hybrid Method

## Introduction

Data compression is crucial for efficient storage and transmission of large datasets. Historically, Gzip (using the DEFLATE algorithm) has been widely adopted for compressing text and binary files. More recently, Zstandard (zstd) has been developed to offer higher throughput and better compression ratios. This report presents a systematic benchmark comparing three methods: Zstd, Gzip, and a custom hybrid compressor that chains together LZ78, delta encoding, arithmetic coding, and a second LZ78 pass. We focus on three key metrics:

- **Compression Ratio**: Original size / Compressed size
- **Compression Time**
- **Decompression Time**

## System Specifications

All tests were performed on a dedicated workstation under controlled conditions. The machine specifications are as follows:

- **CPU**: Ryzen 7 7735HS (8 cores, 16 threads, up to 5.0 GHz)
- **RAM**: 32 GB DDR5 4800 MHz
- **Storage**: 2 TB SSD
- **Operating System**: Windows 11 (64-bit)
- **Python Version**: 3.10

The benchmarking process was conducted with the system in an idle state, and each test was repeated 5 times to ensure consistency. The results were averaged to minimize variability.

## Algorithms Overview

### Zstandard (zstd)

Zstd is a modern, lossless compression algorithm developed by Facebook. It offers superior compression ratios compared to older algorithms like DEFLATE, with the added benefit of fast decompression speeds. Zstd provides 19 compression levels, allowing users to fine-tune the balance between compression ratio and speed. Zstd is known for its excellent performance in real-time applications.

### Gzip (DEFLATE)

Gzip uses the DEFLATE algorithm, combining LZ77-style substring matching with Huffman coding. While Gzip is widely used, it typically achieves lower compression ratios and slower speeds compared to Zstd. Decompression in Gzip is fast but generally slower than Zstd.

### Custom Hybrid Method

The custom hybrid method used in this benchmark processes data using the following sequence:

1. **LZ78**: Separates data into two streams—one for numbers and another for symbols.
2. **Arithmetic Coding**: Compresses the symbol stream based on symbol probabilities.
3. **Delta Encoding**: Compresses the number stream by storing differences between consecutive values.
4. **Second LZ78 Pass**: Re-applies LZ78 compression to the output of the delta encoding to capture additional patterns.

This hybrid approach is intended to exploit data structure for improved compression but introduces complexity.

## Benchmarking Methodology

### Benchmark Setup Overview

A mixed dataset was used for testing, including both highly repetitive data (e.g., small files with repetitive patterns) and larger, structured text files (English and Hungarian poems). The dataset size ranged from 2,600 bytes to 26 MB. The following metrics were measured:

- **Compression Ratio**: The ratio of original file size to compressed file size.
- **Compression Time**: The elapsed wall-clock time to compress the file.
- **Decompression Time**: The time taken to decompress the file back to its original form.

### Compression Tools and Settings

- **Gzip**: Run at its default compression level.
- **Zstd**: Run at its default compression level.
- **Custom Algorithm**: Run at its default settings.

### Output Format

The compressed data was saved in plain text format (`.txt`) for consistency in reporting results. Compression and decompression operations were executed using Python 3.10 scripts, and timing was measured with high-resolution timers.

## Results

### Compression Ratio

Zstd consistently outperformed Gzip and the custom method in terms of compression ratio. For highly repetitive data, Zstd achieved ratios as high as 9818 (e.g., 2.7 MB file compressed to 275 bytes), while Gzip reached 424 and the custom method achieved 49. For structured text (e.g., English and Hungarian poems), Zstd still maintained much better ratios compared to Gzip and the custom method.

### Compression Time

Zstd was the fastest compressor, achieving results in milliseconds for large files. Gzip was slower, while the custom method, due to its complexity, was the slowest, often taking tens of seconds for files that Zstd compressed in a fraction of a second.

### Decompression Time

Zstd was the fastest decompressor, consistently achieving speeds greater than 1500 MB/s. Gzip also performed well, although slower than Zstd. The custom hybrid method was the slowest, with decompression times an order of magnitude slower than both Zstd and Gzip.

## Conclusion

This benchmark confirms that **Zstandard (Zstd)** offers the best overall performance in terms of both compression efficiency and speed. Zstd outperforms Gzip in both compression ratios and processing time, making it the clear choice for most general-purpose compression tasks. 

The **custom hybrid method**, despite its interesting design, did not outperform standard algorithms. It resulted in larger outputs and significantly slower performance, making it impractical for general use.

Thus, for typical workloads where speed and compression ratio are critical, **Zstd** is the recommended choice. Gzip remains relevant for compatibility and simplicity, while the custom algorithm may find niche applications in specialized scenarios.

## Sources

Key properties of Zstandard and example performance numbers are taken from the official Zstd repository and documentation. DEFLATE (gzip) is documented in standard references, and descriptions of LZ78, delta encoding, and arithmetic coding are based on standard algorithms literature. The performance comparisons between Zstd and Gzip align with prior benchmark reports.
