import gzip
import zstandard as zstd
import time
import os
import own_compression.compressor as comp

def compress_gzip(data):
    start = time.time()
    compressed = gzip.compress(data)
    end = time.time()
    return compressed, end - start

def compress_zstd(data):
    cctx = zstd.ZstdCompressor()
    start = time.time()
    compressed = cctx.compress(data)
    end = time.time()
    return compressed, end - start

def compress_own(data):
    cmp = comp.Compressor()
    start = time.time()
    compressed = cmp.compress(data)
    end = time.time()
    return compressed, end - start

def decompress_gzip():
    with open("compressed_files/gzip_compressed.txt", "rb") as f:
        compressed_data = f.read()
        start = time.time()
        decompressed_data = gzip.decompress(compressed_data)
        end = time.time()
        return decompressed_data, end-start

def decompress_zstd():
    with open("compressed_files/zstd_compressed.txt", "rb") as f:
        compressed_data = f.read()
        dctx = zstd.ZstdDecompressor()
        start = time.time()
        decompressed_data = dctx.decompress(compressed_data)
        end = time.time()
        return decompressed_data, end-start

def decompress_own():
    with open("compressed_files/own_compressed.txt", "r") as f:
        compressed_data = f.read()
        cmp = comp.Compressor()
        start = time.time()
        decompressed_data = cmp.decompress(compressed_data)
        end = time.time()
        return decompressed_data, end-start

for filename in os.listdir("text_files"):
    filepath = os.path.join("text_files", filename)
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            data = f.read()

        data_bytes = data.encode('utf-8')

        print(f"\n📄 File: {filename}")
        print(f"Original size: {len(data_bytes)} bytes")

        print("\n🔹Compression")
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

        decompressed_gzip, decompress_gzip_time = decompress_gzip()
        decompressed_zstd, decompress_zstd_time = decompress_zstd()
        decompressed_own, decompress_own_time = decompress_own()


        print("\n🔹Decompression")
        print(f"Gzip match: {decompressed_gzip == data_bytes}, Time: {decompress_gzip_time:.6f} sec")
        print(f"Zstd match: {decompressed_zstd == data_bytes}, Time: {decompress_zstd_time:.6f} sec")
        print(f"Own match: {decompressed_own == data}, Time: {decompress_own_time:.6f} sec")

