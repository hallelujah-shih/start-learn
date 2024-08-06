import os
import asyncio
import concurrent.futures
import functools
import gzip
from typing import Dict, List
from util import timed, async_timed

cur_dir = os.path.dirname(os.path.abspath(__file__))


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(' ')
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split()
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)
    return counter


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged


def test1():
    lines = ["I know what I know",
             "I know that I know",
             "I don't know much",
             "They don't know much"]
    mapped_results = [map_frequency(line) for line in lines]
    print(functools.reduce(merge_dictionaries, mapped_results))


@timed
def test2(fname: str):
    freqs = {}
    # 解压gzip压缩的文件fname
    with gzip.open(fname, 'rb') as gfile:
        for line in gfile:
            line = line.decode()
            data = line.split()
            word = data[0]
            count = int(data[2])
            if word in freqs:
                freqs[word] += count
            else:
                freqs[word] = count


def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def partition_with_gz(f: gzip.GzipFile, chunk_size: int) -> List:
    rt = []
    for line in f:
        rt.append(line.decode())
        if len(rt) == chunk_size:
            yield rt
            rt = []
    yield rt


@async_timed()
async def main(fname: str, pattition_size: int):
    with gzip.open(fname, 'rb') as gfile:
        loop = asyncio.get_running_loop()
        tasks = []
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition_with_gz(gfile, pattition_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies, chunk)))
            intermediate_results = await asyncio.gather(*tasks)
            final_result = functools.reduce(merge_dictionaries, intermediate_results)
            print(f"Aardvark has appeared {final_result['Aardvark']}")


if __name__ == '__main__':
    data_path = os.path.join(cur_dir, 'googlebooks-eng-all-1gram-20120701-a.gz')
    test1()
    # test2(data_path)
    asyncio.run(main(data_path,60000))
