import functools
import logging
import sys


logging.basicConfig(filename='/tmp/collaudo.log', filemode='w', level=logging.INFO, format='%(message)s')


class _LogDeep:
    def __init__(self):
        self._last_frame = None

    def tracer(self, frame, event, *extras):
        if event == 'return':
            self._last_frame = frame

    @property
    def last_frame(self):
        return self._last_frame


def logging_auto(fn):
    '''Decorator che permette di loggare l'intero call stack della
    funzione una volta terminata l'esecuzione.
    '''
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        log_tracer = _LogDeep()
        sys.setprofile(log_tracer.tracer)
        try:
            result = fn(*args, **kwargs)
        finally:
            sys.setprofile(None)
        frame = log_tracer.last_frame

        _locals = {}
        for k, v in frame.f_locals.items():
            _locals[k] = repr(v)
        logging.info("")
        logging.info(f"Test {inner.__name__.upper()}:")
        logging.info("In seguito le principali variabili di collaudo:")
        for key in _locals:
            logging.info(f"- {key} = {_locals[key]}")
        logging.info("TEST RESULTS:")
        val = ["Risultato test: ", "Valore test: ", "Valore minimo: ", "Valore massimo: "]
        for element, tt in zip(result, val):
            logging.info(f"- {tt}{element}")

        return result
    return inner





