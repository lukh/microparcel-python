=====
Usage
=====

The Message is the Payload, transmitted via a serial line (UART, I2C), byte by byte.

The Message object holds a Data buffer (an array of bytes), the size is defined by a class template parameter.
And provides methods to access a specific part of the message (a specific bitfield in the message):
It uses offset, in bits, and a bitmask

.. code-block:: py

    import microparcel

    # creates a message with a 8 bytes payload
    msg = microparcel.Message(size=8)

    # set the 5th, 6th, 7th bits of the payload (5,6,7 of the first byte) at the value "2"
    msg.set(5, 3, 2)

    # set the 13th, 14th, 15th bits of the payload (5,6,7 of the second byte) at the value "3"
    msg.set(13, 3, 3)

    # set the 6th, 7th, 8th, 9th bits of the payload; eg:
    # bits 6 and 7 of the first byte, bits 0 and 1 of the second
    # at the value "1"
    msg.set(6, 4, 1)


    # for bisize higher that 8 (one byte), the offset must be aligned on a byte
    # bitsize is limited to 16; and the rettype should be change to uint16_t
    msg.set(24, 16, 0xFFAF)


    # getter works in the same way:
    msg.get(5, 3)
    msg.get(24, 16)



Frame
-----

A Frame encapsulate the Message between a StartOfFrame (SOF) and a CheckSum.

The SOF is an arbitrary value (in our case, 0xAA),
and the CheckSum is the sum of all bytes, including the SOF, truncated to 8bits.

It allows a lighweight and fast data integrity validation.


Parser
------

The Parser takes bytes, and builds up a Message from the data stream.

.. code-block:: py

    import microparcel


    serial = serial.Serial(serial_port, serial_baudrate)

    # a Parser Class for Message with a Payload of 6.
    TParser = microparcel.make_parser_cls(6)
    parser = TParser()

    # main loop
    while not stop:
        ser_in = serial.read()
        if ser_in == "":
            continue

        raw_byte = ord(ser_in)

        msg = microparcel.Message(size=6)

        # parse byte
        status = parser.parse(raw_byte, msg)
        if status == parser.Status.Complete:
            pass # Handles the message here
            
        if status == parser.Status.Error:
            print("Error in parsing Serial Message: recv byte = {}, current msg = {}".format(raw_byte, msg.data))

    serial.close()


The Parser also encodes Message into Frames for sending data

.. code-block:: py

    import microparcel

    serial = serial.Serial(serial_port, serial_baudrate)

    # a Parser Class for Message with a Payload of 6.
    TParser = microparcel.make_parser_cls(6)
    parser = TParser()

    def sendMsg(msg):
        if serial is None:
            raise FrontendError("Can't send message to the hardware, serial port not opened")

        frame = parser.encode(msg)
        buff = bytearray()
        for d in frame.data:
            buff.append(d)
        serial.write(buff)


    # creates a message with a 8 bytes payload
    msg = microparcel.Message(size=6)

    # set the 5th, 6th, 7th bits of the payload (5,6,7 of the first byte) at the value "2"
    msg.set(5, 3, 2)
    # set the 13th, 14th, 15th bits of the payload (5,6,7 of the second byte) at the value "3"
    msg.set(13, 3, 3)
    # ...

    sendMsg(msg)