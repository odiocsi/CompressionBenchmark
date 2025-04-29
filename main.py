import gzip
import zstandard as zstd
import time
import os
import own_compression.compressor as comp
import matplotlib.pyplot as plt
import shutil

runs = 5

def clear_cache():
    shutil.rmtree("compressed_files", ignore_errors=True)
    os.makedirs("compressed_files", exist_ok=True)

def compress_gzip(data):
    times = []
    compressed = ""
    for _ in range(runs):
        start = time.perf_counter()
        compressed = gzip.compress(data)
        end = time.perf_counter()
        times.append(end-start)
    return compressed, sum(times)/len(times)

def compress_zstd(data):
    times = []
    compressed = ""
    cctx = zstd.ZstdCompressor()
    for _ in range(runs):
        start = time.perf_counter()
        compressed = cctx.compress(data)
        end = time.perf_counter()
        times.append(end-start)
    return compressed, sum(times)/len(times)

def compress_own(data):
    times = []
    compressed = ""
    cmp = comp.Compressor()
    for _ in range(runs):
        start = time.perf_counter()
        compressed = cmp.compress(data)
        end = time.perf_counter()
        times.append(end-start)
    return compressed, sum(times)/len(times)

def decompress_gzip():
    times = []
    decompressed = ""
    with open("compressed_files/gzip_compressed.txt", "rb") as f:
        compressed_data = f.read()
        for _ in range(runs):
            start = time.perf_counter()
            decompressed = gzip.decompress(compressed_data)
            end = time.perf_counter()
            times.append(end-start)
        return decompressed, end-start

def decompress_zstd():
    times = []
    decompressed = ""
    with open("compressed_files/zstd_compressed.txt", "rb") as f:
        compressed_data = f.read()
        dctx = zstd.ZstdDecompressor()
        for _ in range(runs):
            start = time.perf_counter()
            decompressed = dctx.decompress(compressed_data)
            end = time.perf_counter()
            times.append(end-start)
        return decompressed, end-start

def decompress_own():
    times = []
    decompressed = ""
    with open("compressed_files/own_compressed.txt", "r") as f:
        compressed_data = f.read()
        cmp = comp.Compressor()
        for _ in range(runs):
            start = time.perf_counter()
            decompressed = cmp.decompress(compressed_data)
            end = time.perf_counter()
            times.append(end-start)
        return decompressed, end-start

def plot_compression_ratios(compression_ratios, filenames, output_file):
    fig, ax = plt.subplots(figsize=(13, 5))
    gzip_ratios, zstd_ratios, own_ratios = zip(*compression_ratios)
    index = range(len(filenames))

    bar_width = 0.25
    ax.bar([i - bar_width for i in index], gzip_ratios, bar_width, label="Gzip", color='skyblue')
    ax.bar(index, zstd_ratios, bar_width, label="Zstd", color='lightgreen')
    ax.bar([i + bar_width for i in index], own_ratios, bar_width, label="Own", color='salmon')

    ax.set_title(f'Compression Ratios (Avg of {runs} runs)')
    ax.set_ylabel('Compression Ratio (higher is better)')
    ax.set_xlabel('Files')
    ax.set_xticks(index)
    ax.set_xticklabels(filenames)
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_compression_times(compression_times, filenames, output_file):
    fig, ax = plt.subplots(figsize=(13, 5))
    gzip_times, zstd_times, own_times = zip(*compression_times)
    index = range(len(filenames))

    bar_width = 0.25
    ax.bar([i - bar_width for i in index], gzip_times, bar_width, label="Gzip", color='skyblue')
    ax.bar(index, zstd_times, bar_width, label="Zstd", color='lightgreen')
    ax.bar([i + bar_width for i in index], own_times, bar_width, label="Own", color='salmon')

    ax.set_title(f'Compression Times  (Avg of {runs} runs)')
    ax.set_ylabel('Time (seconds) (lower is better)')
    ax.set_xlabel('Files')
    ax.set_xticks(index)
    ax.set_xticklabels(filenames)
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_decompression_times(decompression_times, filenames, output_file):
    fig, ax = plt.subplots(figsize=(13, 5))
    gzip_decompress, zstd_decompress, own_decompress = zip(*decompression_times)
    index = range(len(filenames))

    bar_width = 0.25
    ax.bar([i - bar_width for i in index], gzip_decompress, bar_width, label="Gzip", color='skyblue')
    ax.bar(index, zstd_decompress, bar_width, label="Zstd", color='lightgreen')
    ax.bar([i + bar_width for i in index], own_decompress, bar_width, label="Own", color='salmon')

    ax.set_title(f'Decompression Times (Avg of {runs} runs)')
    ax.set_ylabel('Time (seconds) (lower is better)')
    ax.set_xlabel('Files')
    ax.set_xticks(index)
    ax.set_xticklabels(filenames)
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

compression_ratios = []
compression_times = []
decompression_times = []
filenames = []

clear_cache()

for filename in os.listdir("text_files"):
    filepath = os.path.join("text_files", filename)
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()

        data_bytes = data.encode('utf-8')
        original_size = os.path.getsize(filepath)

        print(f"\n📄 File: {filename}")
        print(f"Original size: {original_size} bytes")

        gzip_data, gzip_time = compress_gzip(data_bytes)
        with open("compressed_files/gzip_compressed.txt", "wb") as f:
            f.write(gzip_data)

        zstd_data, zstd_time = compress_zstd(data_bytes)
        with open("compressed_files/zstd_compressed.txt", "wb") as f:
            f.write(zstd_data)

        own_data, own_time = compress_own(data)
        with open("compressed_files/own_compressed.txt", "w") as f:
            f.write(str(own_data))

        gzip_size = os.path.getsize("compressed_files/gzip_compressed.txt")
        zstd_size = os.path.getsize("compressed_files/zstd_compressed.txt")
        own_size = os.path.getsize("compressed_files/own_compressed.txt")

        gzip_ratio = original_size / gzip_size
        zstd_ratio = original_size / zstd_size
        own_ratio = original_size / own_size

        print(f"\n🔹Compression (Average of {runs} runs)")
        print(f"Gzip: {gzip_size} bytes, Ratio: 1/{gzip_ratio:.0f}, Time: {gzip_time:.6f} sec")
        print(f"Zstd: {zstd_size} bytes, Ratio: 1/{zstd_ratio:.0f}, Time: {zstd_time:.6f} sec")
        print(f"Own: {own_size} bytes, Ratio: 1/{own_ratio:.0f}, Time: {own_time:.6f} sec,")

        gzip_data, gzip_time_decompress = decompress_gzip()
        zstd_data, zstd_time_decompress = decompress_zstd()
        own_data, own_time_decompress = decompress_own()

        print(f"\n🔹Decompression (Average of {runs} runs)")
        print(f"Gzip match: {gzip_data == data_bytes}, Time: {gzip_time_decompress:.6f} sec")
        print(f"Zstd match: {zstd_data == data_bytes}, Time: {zstd_time_decompress:.6f} sec")
        print(f"Own match: {own_data == data}, Time: {own_time_decompress:.6f} sec")

        compression_ratios.append([gzip_ratio, zstd_ratio, own_ratio])
        compression_times.append([gzip_time, zstd_time, own_time])
        decompression_times.append([gzip_time_decompress, zstd_time_decompress, own_time_decompress])
        filenames.append(filename)

plot_compression_ratios(compression_ratios, filenames, "output/compression_ratios.png")
plot_compression_times(compression_times, filenames, "output/compression_times.png")
plot_decompression_times(decompression_times, filenames, "output/decompression_times.png")
