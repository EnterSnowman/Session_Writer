from pathlib import Path
from queue import Queue
from time import time
import cv2 as cv
import pandas as pd
from threading import Thread
from session_writer.dummy_source import DummyVideoSource, DummyTableSource
from session_writer.base_source import VIDEO_SOURCE_TYPE, TABLE_SOURCE_TYPE


class SessionWriter:
    """

    SessionWriter object receives data from different sources. Data from particular source stores in separate queue.
    All available data records in session folder, in file per source, depending on type of source.

    Attributes
    ----------
    path_to_write : pathlib.Path
        Path to folder where sessions data stores
    sources : list of session_writer.base_source.BaseSource
        List of objects, which represents information about data sources, which will be used during session.
    queues : dict of {str : queue.Queue}
        Dict of queues, each of them stores data from source. Key is name of source.
    recording : bool
        If True, thread or threads recording data or waiting for data from data sources.

    """
    def __init__(self, path_to_write, sources):
        """

        Initializes parameters for session writer.

        Parameters
        ----------
        path_to_write : str
            Path to folder where sessions data stores.
        sources : list of session_writer.base_source.BaseSource
            List of objects, which represents information about data sources, which will be used during session.
        """
        self.path_to_write = Path(path_to_write)
        self.sources = sources
        self.queues = {}
        for s in sources:
            self.queues[s.name] = Queue()
        self.recording = False

    def start(self, is_single_thread=False):
        """

        Starts session writing. Creates folder with current time as name, where data from sources will be recorded.
        Writing ends after calling self.stop().

        Parameters
        ----------
        is_single_thread : bool
            If True, all recording process will be in single thread. Otherwise, for each data source will be created
            separate thread.

        """
        self.recording = True
        self.current_session_directoty = self.path_to_write / str(time())
        self.current_session_directoty.mkdir(parents=True, exist_ok=True)
        if is_single_thread:
            t = Thread(target=self.__all_queues_writer)
            t.start()

            # join() ?
        else:
            threads = [Thread(target=self.__queue_writer, args=(s,)) for s in self.sources]
            for t in threads:
                t.start()
                # join() ?

    def __all_queues_writer(self):
        """

        Target for thread object, if self.start(is_single_thread=True) called. Records all available data from all
        non-table sources.

        """
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        writers = {}
        for s in self.sources:
            if s.type_of_source == VIDEO_SOURCE_TYPE:
                source_writer = cv.VideoWriter(str(self.current_session_directoty / (s.name + '.avi')), fourcc, 20.0,
                                               (s.frame_width, s.frame_height), isColor=s.is_color)
                writers[s.name] = source_writer
        while True and self.recording:
            for s_name, writer in writers.items():
                if not self.queues[s_name].empty():
                    writer.write(self.queues[s_name].get())
            sleep(0.2)

    def __queue_writer(self, source):
        """

        Target for thread object, if self.start(is_single_thread=False) called. Records all available data from given
        non-table source.

        Parameters
        ----------
        source : session_writer.base_source.BaseSource
            Information of source of data.

        """
        source_writer = None
        if source.type_of_source == VIDEO_SOURCE_TYPE:
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            source_writer = cv.VideoWriter(str(self.current_session_directoty / (source.name + '.avi')), fourcc, 20.0,
                                           (source.frame_width, source.frame_height), isColor=source.is_color)
        elif source.type_of_source == TABLE_SOURCE_TYPE:
            source_writer = None
        if source_writer is not None:
            while True and self.recording:
                if not self.queues[source.name].empty():
                    frame = self.queues[source.name].get()
                    source_writer.write(frame)
                sleep(0.2)
            source_writer.release()
            print("Writer for", source.name, "released!")
        else:
            print("Data for {} source will be recorded after stop".format(source.name))

    def stop(self):
        """

        Stops writing process. If in current session used table data sources, records all data from this sources in
        session folder.

        """
        print("Session stop")
        self.recording = False
        for s in self.sources:
            if s.type_of_source == TABLE_SOURCE_TYPE:
                df = pd.DataFrame(list(self.queues[s.name].queue))
                df.to_csv(str(self.current_session_directoty / (s.name + '.csv')))
        print("Table data recorded")

    def add_item_to_source_queue(self, source_name, item):
        """

        Parameters
        ----------
        source_name : str
            Name of data source.
        item : object
            Single object, received from data source with given name.

        """
        self.queues[source_name].put(item)


def generate_and_write_random_frames(session_writer, dummy_source, source_name, number_of_frames=50):
    for frame in dummy_source.start_generate_data(number_of_frames):
        session_writer.add_item_to_source_queue(source_name, frame)


if __name__ == "__main__":
    num_sources = 4
    sources = [DummyVideoSource("vidos", frame_width=640, frame_height=320, is_color=False),
               DummyTableSource("text")]
    sw = SessionWriter("../temp_data", sources)
    sw.start(is_single_thread=True)
    gen_threads = []
    for source in sources:
        t = Thread(target=generate_and_write_random_frames, args=(sw, source, source.name, 300))
        gen_threads.append(t)
    for t in gen_threads:
        t.start()

    for t in gen_threads:
        t.join()

    sw.stop()
