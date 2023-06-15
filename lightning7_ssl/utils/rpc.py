import asyncio
import inspect
from abc import ABCMeta, abstractmethod
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import Callable

import zmq
import zmq.asyncio

_CLOSE_TOKEN = "__CLOSE__"


def expose(func: Callable):
    func.__rpc_exposed__ = True  # type: ignore
    return func


def _is_exposed(obj):
    return callable(obj) and getattr(obj, "__rpc_exposed__", False)


def _close_process(proc: Process):
    proc.join(1)
    if not proc.is_alive():
        return
    proc.terminate()
    proc.join(1)
    if not proc.is_alive():
        return
    proc.kill()


class ServiceProxy:
    """The ServiceProxy class provides a synchronous client for a Service class.

    It maintains a connection to a remote service process and allows calling the exposed
    methods of the service. It forwards method calls to the remote service and returns
    the results. It also handles exceptions raised by the remote service and re-raises
    them on the client side.

    Example:
    >>> class MyService(Service):
    ...     @expose
    ...     def echo(self, msg):
    ...         return msg
    ...
    >>> with MyService.spawn() as srv:
    ...     print(srv.echo("Hello World!"))
    'Hello World!'

    Warning:
        Always use `ServiceProxy` in a with-statement or call `close()` when you're done
        with it to make sure the remote service is properly terminated.
    """

    def __init__(self, process: Process, url: str, exposed_methods: list[str]):
        self._process = process
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(url)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._exposed_methods = exposed_methods

    def close(self):
        try:
            self._socket.send_pyobj(_CLOSE_TOKEN, flags=zmq.NOBLOCK)
        except zmq.error.ZMQError:
            pass
        self._context.destroy()
        _close_process(self._process)

    def __getattr__(self, name):
        if not self._process.is_alive() or self._context.closed:
            raise ConnectionError("Service is not running")
        if name not in self._exposed_methods:
            raise AttributeError(f"Method {name} not exposed in the service")

        def method(*args, **kwargs):
            self._socket.send_pyobj((name, args, kwargs))
            result = self._socket.recv_pyobj()
            if isinstance(result, Exception):
                raise result
            return result

        return method

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


async def monitor_process(process: Process):
    """Periodically check if the process has exited"""
    try:
        while process.is_alive():
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        pass


class AsyncServiceProxy:
    """The AsyncServiceProxy class provides an asynchronous client for a remote service.

    It maintains a connection to a remote service process and allows calling the exposed
    methods of the service. It forwards method calls to the remote service and returns
    the results. It also handles exceptions raised by the remote service and re-raises
    them on the client side.

    Example:
    >>> class MyAsyncService(AsyncService):
    ...     @expose
    ...     async def echo(self, msg):
    ...         await asyncio.sleep(0.01)  # Simulate async work
    ...         return msg
    ...
    >>> async with MyAsyncService.aspawn() as srv:
    ...     print(await srv.echo("Hello World!"))
    'Hello World!'

    Warning:
        Always use `AsyncServiceProxy` in an async with-statement or call `close()` when
        you're done with it to make sure the remote service is properly terminated.
    """

    def __init__(self, process: Process, url: str, exposed_methods: list[str], pool_size=5):
        self._process = process
        self._exposed_methods = exposed_methods
        self._context = zmq.asyncio.Context()
        self._sockets: asyncio.Queue[zmq.Socket] = asyncio.Queue()
        for _ in range(pool_size):
            socket = self._context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 0)
            socket.connect(url)
            self._sockets.put_nowait(socket)
        self._monitor = asyncio.create_task(monitor_process(process))

    async def close(self):
        if self._process.is_alive() and not self._context.closed:
            try:
                socket = await asyncio.wait_for(self._sockets.get(), timeout=1)
                await socket.send_pyobj(_CLOSE_TOKEN, flags=zmq.NOBLOCK)  # type: ignore
            except (asyncio.TimeoutError, zmq.error.ZMQError):
                pass
        self._monitor.cancel()
        if not self._context.closed:
            self._context.destroy()
        if self._process.is_alive():
            _close_process(self._process)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    def __getattr__(self, name):
        if not self._process.is_alive() or self._context.closed:
            raise ConnectionError("Service is not running")
        if name not in self._exposed_methods:
            raise AttributeError(f"Method {name} not exposed in the service")

        async def method(*args, **kwargs):
            # Asynchronously wait for a socket to become available
            socket = await self._sockets.get()
            try:
                await socket.send_pyobj((name, args, kwargs))  # type: ignore
                # Wait for the result or for the process to close
                recv_fut = socket.recv_pyobj()  # type: ignore
                done, _ = await asyncio.wait([recv_fut, self._monitor], return_when=asyncio.FIRST_COMPLETED)
                if recv_fut in done:
                    result = recv_fut.result()
                    if isinstance(result, Exception):
                        raise result
                    return result
                elif self._monitor in done:
                    raise ConnectionError("Process exited before message was received")
                else:
                    raise RuntimeError("Neither task completed")
            finally:
                await self._sockets.put(socket)

        return method


def _get_exposed_methods(cls: type) -> list[str]:
    """Return a list of exposed methods in the class"""
    return [name for name, attr in cls.__dict__.items() if _is_exposed(attr)]


def _spawn(cls: type, args: tuple, kwargs: dict) -> tuple[Process, str]:
    """Spawn a process and return the process and the url to connect to"""

    def run(url_tx: Connection, args: tuple, kwargs: dict):
        srv = cls(*args, **kwargs)
        srv._context = srv.create_context()
        srv._socket = srv._context.socket(zmq.REP)
        srv._socket.bind("tcp://*:*")
        url = srv._socket.getsockopt(zmq.LAST_ENDPOINT)
        url_tx.send(url)
        srv.main_loop()
        srv.close()

    url_tx, url_rx = Pipe()
    proc = Process(target=run, args=(url_tx, args, kwargs))
    proc.start()
    return proc, url_rx.recv()


class BaseService(metaclass=ABCMeta):
    _context: zmq.Context
    _socket: zmq.Socket

    def close(self):
        """Close the service"""
        self._socket.close()
        self._context.destroy()

    @staticmethod
    @abstractmethod
    def create_context() -> zmq.Context:
        """Create the zmq context"""
        raise NotImplementedError()

    @abstractmethod
    def main_loop(self):
        """The main loop of the service"""
        raise NotImplementedError()

    @classmethod
    def spawn(cls, *args, **kwargs):
        proc, url = _spawn(cls, args, kwargs)
        return ServiceProxy(proc, url, _get_exposed_methods(cls))

    @classmethod
    def aspawn(cls, *args, **kwargs):
        proc, url = _spawn(cls, args, kwargs)
        return AsyncServiceProxy(proc, url, _get_exposed_methods(cls))


class Service(BaseService):
    """The Service class exposes methods using the `@exposed` decorator to a remote
    client. It runs synchronously in a separate process.

    Example:
        >>> class MyService(Service):
        ...     @expose
        ...     def echo(self, msg):
        ...         return msg
        ...
        >>> srv = MyService.spawn()
        >>> srv.echo("Hello World!")
        'Hello World!'
        >>> srv.close()

    Warning:
        Make sure to call `close()` to properly terminate the service process when you
        are done using the service.
    """

    @staticmethod
    def create_context() -> zmq.Context:
        return zmq.Context()

    def main_loop(self):
        while True:
            msg = self._socket.recv_pyobj()
            if msg == _CLOSE_TOKEN:
                self._socket.close()
                break
            method_name, args, kwargs = msg
            if hasattr(self, method_name) and _is_exposed(getattr(self, method_name)):
                try:
                    result = getattr(self, method_name)(*args, **kwargs)
                except Exception as e:
                    result = e
            else:
                result = AttributeError(f"Method {method_name} not exposed in the service")
            self._socket.send_pyobj(result)


class AsyncService(BaseService):
    """The AsyncService class exposes methods using the `@exposed` decorator. It runs
     in a separate process.

    Example:
        >>> class MyAsyncService(AsyncService):
        ...     @expose
        ...     async def echo(self, msg):
        ...         await asyncio.sleep(0.01)  # Simulate async work
        ...         return msg
        ...
        >>> srv = asyncio.run(MyAsyncService.aspawn())
        >>> asyncio.run(srv.echo("Hello World!"))
        'Hello World!'
        >>> asyncio.run(srv.close())

    Warning:
        Make sure to call `close()` to properly terminate the service process when you
        are done using the service.
    """

    @staticmethod
    def create_context() -> zmq.Context:
        return zmq.asyncio.Context()

    async def async_setup(self):
        """Called before the main loop is started, can be used to setup async resources"""
        pass

    def main_loop(self):
        asyncio.run(self._async_main_loop())

    async def _async_main_loop(self):
        await self.async_setup()
        while True:
            msg = await self._socket.recv_pyobj()
            if msg == _CLOSE_TOKEN:
                self._socket.close()
                break
            method_name, args, kwargs = msg
            if hasattr(self, method_name) and _is_exposed(getattr(self, method_name)):
                method = getattr(self, method_name)
                try:
                    result = method(*args, **kwargs)
                    result = await result if inspect.isawaitable(result) else result
                except Exception as e:
                    result = e
            else:
                result = AttributeError(f"Method {method_name} not exposed in the service")
            await self._socket.send_pyobj(result)  # type: ignore
