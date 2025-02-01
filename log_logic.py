"""Module where everything connected to logs is written."""
import logging
import os
import sys
import queue
from logging.handlers import QueueHandler, QueueListener
import hashlib
import httpx
import websocket 
from collections.abc import Iterable, Mapping
import json
import time

class NonShitQueueHandler(QueueHandler):
    def prepare(self, record):
        return record

class WSLogHandler(logging.Handler):
    """
    Dummy logging handler that sends log records to a specified HTTP URL.
    """
    def __init__(self, url, username=None, password=''):
        super().__init__()
        self.url = url
        self.headers = None
        if username:
            self.headers =\
            [f"Authorization: {hashlib.md5(f'{username}:{password}'.encode('utf-8')).hexdigest()}"]
        self.socket: websocket.WebSocket = None
        self._reconnect()
    
    def _reconnect(self):
        if self.socket is None or self.socket.connected == False:
            self.socket = websocket.create_connection(self.url, header = self.headers)

    def emit(self, record):
        for trie in range(5):
            try:
                self._reconnect()
                data = json.dumps(self.format(record), ensure_ascii= False, indent= 0)
                self.socket.send(data)
                return
            except:
                time.sleep(0.5)

        
        self.handleError(record)

def textify_exceptions(m: Mapping, formatter):
    for k, v in m.items():
        if isinstance(v, Exception):
            m[k] = f'[{type(v)}] : {v}\n{formatter(v)}'
        elif isinstance(v, Mapping):
            textify_exceptions(v, formatter)

        
class HttpHandler(logging.Handler):
    """
    Dummy logging handler that sends log records to a specified HTTP URL.
    """
    def __init__(self, url, username=None, password=''):
        super().__init__()
        self.url = url
        self.client = httpx.Client()
        if username:
            self.client.headers = {"Authorization": hashlib.md5(f'{username}:{password}'.encode('utf-8')).hexdigest()}
    def emit(self, record):
        jsondata = self.format(record)
        for trie in range(5):
            try:
                self.client.post(self.url, json=jsondata)
                return
            except:
                time.sleep(0.5)
        self.handleError(record)

class TextFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Start with the basic log format
        base_message = super().format(record)
        # Check if "kwargs" attribute exists in the log `record`. If yes, format and append them
        if isinstance(record.args, Mapping):
            formatted_kwargs = " || " + ", ".join(f"{key}: {value}" for key, value in record.args.items())
            return base_message + formatted_kwargs
        else:
            return base_message
        
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> dict:
        data = dict(level = record.levelno,
                    message = record.message, 
                    levelname = record.levelname,
                    timestamp = self.formatTime(record, self.datefmt),
                    funcName = record.funcName,
                    extras = {}
                    )
        if record.exc_info:
            data['error'] = self.formatException(record.exc_info)
        if record.args:
            if isinstance(record.args, Mapping):
                data['extras'] = record.args
            elif isinstance(record.args, Iterable):
                data['extras'] = {f'arg{i}':v for i, v in enumerate(record.args)}
        return data


def setup_logger(name: str = 'default',
                encoding: str = 'utf-8',
                stdout: bool = True,
                filepath: str | None = None,
                logserver_url: str | None = None,
                text_format: str = '%(asctime)s | %(funcName)s | %(levelname)s | %(message)s',
                datefmt: str = '%Y-%m-%dT%H:%M:%S%z',
                level: int | str = 20,
                **kwargs
                 ):
    main_logger = logging.getLogger(name)
    main_logger.setLevel(level=level)
    if main_logger.hasHandlers():
        main_logger.handlers.clear()

    log_queue = queue.Queue(-1)
    queue_handler = NonShitQueueHandler(log_queue)
    main_logger.addHandler(queue_handler)

    if filepath or stdout:
        txtformatter = TextFormatter(fmt= text_format, datefmt=datefmt)

    handlers = []
    if filepath:
        dir = os.path.dirname(filepath)
        os.makedirs(dir, exist_ok=True)
        fileh = logging.FileHandler(filepath, encoding= encoding)
        fileh.setFormatter(txtformatter)
        handlers.append(fileh)
    
    if stdout:
        stdouth = logging.StreamHandler(sys.stdout)
        stdouth.setFormatter(txtformatter)
        handlers.append(stdouth)

    if logserver_url:
        handler_type = WSLogHandler if logserver_url.startswith('ws') else HttpHandler
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        logserverh = handler_type(url= logserver_url, username=username, password=password)
        jsfmt = JsonFormatter(datefmt=datefmt)
        logserverh.setFormatter(jsfmt)
        handlers.append(logserverh)

    listener = QueueListener(log_queue, *handlers)
    listener.start()
    main_logger.listener = listener
    return main_logger
    



if __name__ == "__main__":
    import time, os, sys, datetime
    suffix = 'mybot' # Суффикс в имени лога
    pwd = os.path.abspath(os.curdir) # папка, где запущен интерпретатор
    logs_fodlder = f'{pwd}/logs' # в дочернюю папку logs в ней
    os.makedirs(logs_fodlder, exist_ok=True) # сделаем, чтоб не было ошибок, если ее нет
    logs_file = f'{logs_fodlder}/log-{datetime.date.today()}-{suffix}.log' # полное имя файла куда лог

    logger = setup_logger(  name= 'myname', # имя, по которому логгер можно достать в других модулях
                            filepath=logs_file, # если надо писать в файл - указываем, в какой
                           stdout=True, # надо, или не надо писать в консоль

                           # настройки подключения к логсерверу
                           # logserver_url - ссылка до ручки logserver ноды, может быть websocket или http
                           logserver_url='wss://worker.agicotech.ru/logs/logpipe',
                           username = 'test',
                           password = 'testtest',

                           level = 20
                           )
    
    # logger = logging.getLogger('myname') - так вот можно достать настроенный логгер в любом модуле в составе проекта

    logger.info('This is a simple message')


    # поля, по которым будут строиться графики, надо передавать словариком
    # для одинаковых событий основное сообщение стоит делать одинаковым, константным
    # а все данные о событии передавать словарем
    # они автоматически отформатируются в строку для текстовых выводов, а в elastic уйдут в виде json
    logger.warning('We\'v fucked', dict(
        reason = 'some shit failed',
        session_id = 1488777,
        client_id = 666
    ))

    def bullshit():
        try:
            raise Exception('AAAAAAAAAAAAAA')
        except Exception as e:
            logger.error('Exception occured!', dict(
                current_important_id = 7
            ))
            # передаем данные о событии, при котором случилась ошибка
            logger.error(e, exc_info= True)
            # передаем трейсбек исключения

    bullshit() # логгер записывает так же и имя функции, в которой произошел эмит лога

    for i in range (7):
        logger.info('counter incr', {'i': i})
        time.sleep(0.2)

    # если код не является демоном, а завершает свою работу в известный момент после запуска
    #  - лучше добавить небольшую задержку, чтобы фоновый процесс успел дослать все логи из очереди
    time.sleep(0.1)

"""
На выходе скрипта получим
2024-12-13T12:05:48+0000 | <module> | INFO | This is a simple message
2024-12-13T12:05:48+0000 | <module> | WARNING | We'v fucked || reason: some shit failed, session_id: 1488777, client_id: 666
2024-12-13T12:05:48+0000 | bullshit | ERROR | Exception occured! || current_important_id: 7
2024-12-13T12:05:48+0000 | bullshit | ERROR | AAAAAAAAAAAAAA
Traceback (most recent call last):
  File "/home/agicotech/vpnbot/log_logic.py", line 198, in bullshit
    raise Exception('AAAAAAAAAAAAAA')
Exception: AAAAAAAAAAAAAA
2024-12-13T12:05:48+0000 | <module> | INFO | counter incr || i: 0
2024-12-13T12:05:48+0000 | <module> | INFO | counter incr || i: 1
2024-12-13T12:05:49+0000 | <module> | INFO | counter incr || i: 2
2024-12-13T12:05:49+0000 | <module> | INFO | counter incr || i: 3
2024-12-13T12:05:49+0000 | <module> | INFO | counter incr || i: 4
2024-12-13T12:05:49+0000 | <module> | INFO | counter incr || i: 5
2024-12-13T12:05:49+0000 | <module> | INFO | counter incr || i: 6
"""