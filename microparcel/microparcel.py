# -*- coding: utf-8 -*-

from enum import Enum


class Message(object):
    def __init__(self, size=0, data=None):
        assert (data is None or isinstance(data, list))
        self.data = [0 for i in range(size)] if data is None else data


    def get(self, offset, bitsize):
        assert (bitsize <= 16)
        assert (bitsize > 0)
        assert ((offset+bitsize) <= 8*self.size)
        
        assert((bitsize <= 8) or ((bitsize > 8) and (offset & 0x3) == 0))


        if bitsize <= 8:
            # on one byte
            if((offset & 0x7) + bitsize <= 8):
                mask = (1<<bitsize) - 1
                byte_idx = offset >> 3
                byte_shift = offset & 0x7
                return (self.data[byte_idx] >> byte_shift) & mask
            else:
                mask = (1<<bitsize) - 1
                byte_idx = offset >> 3
                byte_shift = offset & 0x7
                mask_lsb = mask & ( (1 << (8 - byte_shift)) - 1)
                mask_msb = mask >> (8 - byte_shift)

                lsb_part = (self.data[byte_idx] >> byte_shift) & mask_lsb
                msb_part = self.data[byte_idx+1] & mask_msb

                return lsb_part | (msb_part << (8 - byte_shift))

        else:
            mask = (1<<bitsize) - 1
            byte_idx = offset >> 3

            return (self.data[byte_idx] & (mask&0xFF)) | ((self.data[byte_idx+1] & (mask>>8)) << 8)


    def set(self, offset, bitsize, value):
        assert (bitsize <= 16)
        assert (bitsize > 0)
        assert ((offset+bitsize) <= 8*self.size)
        
        assert((bitsize <= 8) or ((bitsize > 8) and (offset & 0x3) == 0))

        if bitsize <= 8:
            # on one byte
            if((offset & 0x7) + bitsize <= 8):
                mask = (1<<bitsize) - 1
                byte_idx = offset >> 3
                byte_shift = offset & 0x7
                self.data[byte_idx] &= ~(mask << byte_shift)
                self.data[byte_idx] |= (value & mask) << byte_shift
                return

            else:
                mask = (1<<bitsize) - 1
                byte_idx = offset >> 3
                lsb_byte_shift = offset & 0x7
                msb_byte_shift = 8 - lsb_byte_shift
                mask_lsb = mask & ( (1 << msb_byte_shift) - 1)
                mask_msb = mask >> msb_byte_shift

                # lsb
                self.data[byte_idx] &= ~( mask_lsb << lsb_byte_shift )
                self.data[byte_idx] |= (value & mask_lsb) << lsb_byte_shift
                # msb
                self.data[byte_idx+1] &= ~mask_msb
                self.data[byte_idx+1] |= (value >> msb_byte_shift) & mask_msb
                return #lsb_part | (msb_part << (8 - byte_shift))

        else:
            mask = (1<<bitsize) - 1
            byte_idx = offset >> 3

            self.data[byte_idx] &= ~(mask & 0xFF)
            self.data[byte_idx] |= (value & 0xFF)
            
            self.data[byte_idx+1] &= ~(mask >> 8)
            self.data[byte_idx+1] |= (value >> 8)

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