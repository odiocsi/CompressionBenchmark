import gzip
import zstandard as zstd
import time
import os
import own_compression.compressor as comp

runs = 5
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

for filename in os.listdir("text_files"):
    filepath = os.path.join("text_files", filename)
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()

        data_bytes = data.encode('utf-8')

        print(f"\n📄 File: {filename}")
        print(f"Original size: {len(data_bytes)} bytes")

        print(f"\n🔹Compression (Average of {runs} runs)")
        gzip_data, gzip_time = compress_gzip(data_bytes)
        with open("compressed_files/gzip_compressed.txt", "wb") as f:
            f.write(gzip_data)

        zstd_data, zstd_time = compress_zstd(data_bytes)
        with open("compressed_files/zstd_compressed.txt", "wb") as f:
            f.write(zstd_data)

        own_data, own_time = compress_own(data)
        with open("compressed_files/own_compressed.txt", "w") as f:
            f.write(str(own_data))

        print(f"Gzip: {len(gzip_data)} bytes, Time: {gzip_time:.6f} sec")
        print(f"Zstd: {len(zstd_data)} bytes, Time: {zstd_time:.6f} sec")
        print(f"Own: {len(str(own_data))} bytes, Time: {own_time:.6f} sec")

        gzip_data, gzip_time = decompress_gzip()
        zstd_data, zstd_time = decompress_zstd()
        own_data, own_time = decompress_own()

        print(f"\n🔹Decompression (Average of {runs} runs)")
        print(f"Gzip match: {gzip_data == data_bytes}, Time: {gzip_time:.6f} sec")
        print(f"Zstd match: {zstd_data == data_bytes}, Time: {zstd_time:.6f} sec")
        print(f"Own match: {own_data == data}, Time: {own_time:.6f} sec")

