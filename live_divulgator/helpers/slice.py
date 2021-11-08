from typing import Generator


def slice_queue(queue: list[str], initial_slice=0, chunk_size=100) -> Generator:
    """
    Slices a queue into chunks of size `chunk_size`
    """
    length = len(queue)

    while initial_slice < length:
        if initial_slice + chunk_size > length:
            chunk_size = length - initial_slice

        queue_slice = queue[initial_slice : initial_slice + chunk_size]

        yield queue_slice

        initial_slice += chunk_size
