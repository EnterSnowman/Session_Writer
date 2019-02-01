import time
import numpy as np
import cv2 as cv
from random import randint

from session_writer.base_source import BaseSource, VIDEO_SOURCE_TYPE, TABLE_SOURCE_TYPE


class DummyVideoSource(BaseSource):
    """

    Class represents dummy video source. Created for test purposes.

    Attributes
    ----------
    frame_width : int
        Pixel width of video frame.
    frame_height : int
        Pixel height of video frame.
    is_color : bool
        If True, video source gives color frames, and gray frames otherwise.

    """
    def __init__(self, name, frame_width=640, frame_height=320, is_color=False, **kwargs):
        """

        Initializes dummy video source object with given parameters.

        Parameters
        ----------
        name : str
            Name of data source
        frame_width : int
            Pixel width of video frame.
        frame_height : int
            Pixel height of video frame.
        is_color : bool
            If True, video source gives color frames, and gray frames otherwise.
        **kwargs
            Arbitrary keyword arguments. Stores additional information about data source.
        """

        super().__init__(name, VIDEO_SOURCE_TYPE, **kwargs)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.is_color = is_color

    def start_generate_data(self, number_of_items=None):
        """

        Generator, which yields random frames.

        Parameters
        ----------
        number_of_items : int or None
            Number of elements, which will be created during one method call. If None, method generates frames
            infinitely.

        Yields
        -------
        frame : ndarray
            Grayscale frame with shape (self.frame_height, self.frame_width) with random pixel values.

        """
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
    """

    Class represents dummy table source. Created for test purposes.

    """
    def __init__(self, name, **kwargs):
        """

        Initializes dummy table source object with given parameters.

        Parameters
        ----------
        name : str
            Name of data source
        **kwargs
            Arbitrary keyword arguments. Stores additional information about data source.
        """
        super().__init__(name, TABLE_SOURCE_TYPE, **kwargs)

    def start_generate_data(self, number_of_items=None):
        """

        Generator, which yields list with length of 10. Each item of list is random string.

        Parameters
        ----------
        number_of_items : int or None
            Number of elements, which will be created during one method call. If None, method generates frames
            infinitely.

        Yields
        -------
        list of str
            List of length 10.

        """
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
