import time
import numpy as np
import cv2 as cv
from random import randint

from session_writer.base_source import BaseSource, VIDEO_SOURCE_TYPE, TABLE_SOURCE_TYPE


class DummyVideoSource(BaseSource):
    def __init__(self, name, frame_width=640, frame_height=320, **kwargs):
        super().__init__(name, VIDEO_SOURCE_TYPE, **kwargs)
        self.frame_width = frame_width
        self.frame_height = frame_height

    def start_generate_data(self, number_of_items=None):
        sleep_time = 1. / 30
        if number_of_items is None:
            while True:
                time.sleep(sleep_time)
                yield np.random.randint(0, 256, (self.frame_height, self.frame_width), dtype=np.uint8)
        else:
            i = 0
            while i < number_of_items:
                time.sleep(sleep_time)

                frame = np.random.randint(0, 256, (self.frame_height, self.frame_width), dtype=np.uint8)
                cv.putText(frame, str(i), (int(self.frame_width / 2), int(self.frame_height / 2)),
                           cv.FONT_HERSHEY_SIMPLEX, 3,
                           (255, 255, 0), 4)
                i += 1
                yield frame


class DummyTableSource(BaseSource):
    def __init__(self, name, **kwargs):
        super().__init__(name, TABLE_SOURCE_TYPE, **kwargs)

    def start_generate_data(self, number_of_items=None):
        sleep_time = 1. / 30
        if number_of_items is None:
            while True:
                time.sleep(sleep_time)
                yield [str(randint(1, 100)) for j in range(10)]
        else:
            i = 0
            while i < number_of_items:
                time.sleep(sleep_time)
                i += 1
                yield [str(randint(1, 100)) for j in range(10)]


if __name__ == "__main__":
    ds = DummyVideoSource("2", frame_width=640, frame_height=320, is_color=False)
