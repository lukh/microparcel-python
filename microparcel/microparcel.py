# -*- coding: utf-8 -*-

from enum import Enum


class Message(object):
    def __init__(self, size=0, data=None):
        assert (data is None or isinstance(data, list))
        self.data = [0 for i in range(size)] if data is None else data

    @property
    def size(self):
        return len(self.data)

class Frame(object):
    kSOF = 0xAA
    def __init__(self):
        self.SOF = 0
        self.message = Message(0)
        self.checksum = 0

    @property
    def size(self):
        return  self.message.size + 2


def make_parser_cls(message_size):
    class Parser(object):
        MsgSize = message_size
        FrameSize = message_size + 2
        class Status(Enum):
            Complete = 0
            NotComplete = 1
            Error = 2

        class State(Enum):
            Idle = 0
            Busy = 1

        def __init__(self):
            self._state = self.State.Idle
            self._status = self.Status.NotComplete

            self._buffer = 0

        def _isCheckSumValid(self):
            if len(self._buffer) != self.FrameSize:
                raise ValueError()

            return (sum(self._buffer[0: -1]) & 0xFF) == self._buffer[-1]

        def parse(self, in_byte, out_msg):
            if self._state == self.State.Idle:
                #when receiving a byte in idle, reset
                self._buffer = []

                # valid start of frame
                if in_byte == Frame.kSOF:
                    self._status = self.Status.NotComplete
                    self._state = self.State.Busy

                    self._buffer.append(in_byte)

                else:
                    self._status = self.Status.Error

            
            else:
                self._buffer.append(in_byte)

                if len(self._buffer) == self.FrameSize:
                    if self._isCheckSumValid():
                        self._status = self.Status.Complete

                        out_msg.data = self._buffer[1:self.FrameSize-1]

                    else:
                        self._status = self.Status.Error

                    self._state = self.State.Idle


                else:
                    self._status = self.Status.NotComplete

            return self._status


        def encode(self, in_msg):
            assert(in_msg.size == self.MsgSize)

            frame = Frame()
            frame.SOF = Frame.kSOF
            frame.message = in_msg
            frame.checksum = (frame.SOF + sum(frame.message.data)) & 0xFF

            return frame



    return Parser