from abc import ABC, abstractmethod
import enum
from __future__ import annotations
import json

class MessageType(enum):
    USER_REQUEST = 0,
    PREDICTION_REQUEST = 1,
    PREDICTION_RESPONSE = 2,
    USER_RESPONSE = 3



class Protocol:

    _curr_seq = 0


    @property
    def seq(cls):
        Protocol._curr_seq += 1
        return Protocol._curr_seq