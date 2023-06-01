import asyncio
import time
import unittest

from lightning7_ssl.utils.rpc import AsyncService, Service, expose

# Random sleep durations
sleep_durations = [
    0.015991589910069293,
    0.07649321873469903,
    0.0936746363155998,
    0.07557689289669528,
    0.05985670051458402,
    0.007736726626289991,
    0.07014793939257776,
    0.08449027381996104,
    0.02533322884131681,
    0.08074233532700889,
    0.04677285622435522,
    0.06974804956422175,
    0.05366566782351415,
    0.0252571999931432,
    0.06068394488874987,
    0.03653063217229796,
    0.07236856481973999,
    0.06775018802773527,
    0.09509934854260056,
    0.05683239593048072,
    0.027153737628735286,
    0.08906071243544904,
    0.031647478207949487,
    0.003380605173263651,
    0.05452572106475848,
    0.06065546827145553,
    0.08334092949262574,
    0.0513112904043391,
    0.08998047480376961,
    0.07547212759878779,
    0.011022263080324135,
    0.016353208166127342,
    0.04986870035850698,
    0.05986483296238613,
    0.017792722145669737,
    0.02152000690246988,
    0.018660238031464194,
    0.01677321172807701,
    0.0782164099367236,
    0.08391158465634222,
    0.05163548013679812,
    0.05722998164250788,
    0.008402330514508494,
    0.006066548788912951,
    0.030221047098525045,
    0.0659995399630056,
    0.017081898317801358,
    0.04755065296222377,
    0.06650986493923471,
    0.05646068738401305,
    0.07313205260758735,
    0.024891874045121953,
    0.06853396028352493,
    0.040300148332041297,
    0.03682597702585231,
    0.007917947319465213,
    0.0053122354993862086,
    0.05014800118770144,
    0.00179080275882757,
    0.05100583800269017,
    0.021070269341929548,
    0.026973531809210116,
    0.06696126562544229,
    0.07355866034764608,
    0.012416070694441728,
    0.02791626347798579,
    0.0862330765176663,
    0.02685501449607577,
    0.03029187147613157,
    0.07687337464629512,
    0.01678244895167308,
    0.035142183626302315,
    0.01532174069140062,
    0.0634054498223895,
    0.03987701804645851,
    0.08545165425737887,
    0.07942408836356741,
    0.02651902886219488,
    0.04995410480907104,
    0.09284891613570988,
    0.03396358977805022,
    0.03319882447197148,
    0.0512621646703604,
    0.003324570799820614,
    0.005027055093454469,
    0.09386912260124185,
    0.09259428367430205,
    0.03465867204817258,
    0.009201227493816333,
    0.0012042380702125932,
    0.08461006603431604,
    0.019642956050788696,
    0.08494541668682316,
    0.049894161715000784,
    0.09890930695259689,
    0.05175195306325878,
    0.013333389638508952,
    0.06448706475925139,
    0.08574550075793786,
    0.07495860278609994,
]


class TestAsyncServiceAsyncProxy(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        class MyAsyncService(AsyncService):
            @expose
            async def echo(self, msg: str) -> str:
                await asyncio.sleep(0.01)
                return msg

            @expose
            async def raise_exception(self):
                await asyncio.sleep(0.01)
                raise Exception("Test exception")

            @expose
            def non_async(self):
                return "Non async"

            @expose
            def crash(self):
                import os

                os._exit(1)

        self.srv = MyAsyncService.aspawn()

    async def asyncTearDown(self):
        await self.srv.close()

    async def echo_task(self, idx: int, proxy):
        await asyncio.sleep(sleep_durations[idx])
        msg = f"Message {idx}"
        res = await proxy.echo(msg)
        self.assertEqual(res, msg)

    async def test_many_simultaneous_calls(self):
        tasks = [self.echo_task(i, self.srv) for i in range(100)]
        await asyncio.gather(*tasks)

    async def test_cannot_call_not_exposed(self):
        with self.assertRaises(AttributeError):
            await self.srv.not_exposed()

    async def test_exception_is_propagated(self):
        with self.assertRaises(Exception):
            await self.srv.raise_exception()

    async def test_non_async_method_is_handled(self):
        self.assertEqual(await self.srv.non_async(), "Non async")

    async def test_close(self):
        await self.srv.close()
        with self.assertRaises(ConnectionError):
            await self.srv.echo("Message")

    async def test_process_crash(self):
        with self.assertRaises(ConnectionError):
            await self.srv.crash()


class TestSyncServiceAsyncProxy(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        class MyService(Service):
            @expose
            def echo(self, msg: str) -> str:
                time.sleep(0.01)
                return msg

            @expose
            def raise_exception(self):
                time.sleep(0.01)
                raise Exception("Test exception")

            @expose
            def crash(self):
                import os

                os._exit(1)

        self.srv = MyService.aspawn()

    async def asyncTearDown(self):
        await self.srv.close()

    async def echo_task(self, idx: int, proxy):
        await asyncio.sleep(idx * 0.01)  # Stagger the start times
        msg = f"Message {idx}"
        res = await proxy.echo(msg)
        self.assertEqual(res, msg)

    async def test_many_simultaneous_calls(self):
        tasks = [self.echo_task(i, self.srv) for i in range(100)]
        await asyncio.gather(*tasks)

    async def test_cannot_call_not_exposed(self):
        with self.assertRaises(AttributeError):
            await self.srv.not_exposed()

    async def test_exception_is_propagated(self):
        with self.assertRaises(Exception):
            await self.srv.raise_exception()

    async def test_close(self):
        await self.srv.close()
        with self.assertRaises(ConnectionError):
            await self.srv.echo("Message")

    async def test_process_crash(self):
        with self.assertRaises(ConnectionError):
            await self.srv.crash()


class TestAsyncServiceSyncProxy(unittest.TestCase):
    def setUp(self):
        class MyAsyncService(AsyncService):
            @expose
            async def echo(self, msg: str) -> str:
                await asyncio.sleep(0.01)
                return msg

            @expose
            async def raise_exception(self):
                await asyncio.sleep(0.01)
                raise Exception("Test exception")

        self.srv = MyAsyncService.spawn()

    def tearDown(self):
        self.srv.close()

    def test_many_calls(self):
        for i in range(100):
            msg = f"Message {i}"
            res = self.srv.echo(msg)
            self.assertEqual(res, msg)

    def test_cannot_call_not_exposed(self):
        with self.assertRaises(AttributeError):
            self.srv.not_exposed()

    def test_exception_is_propagated(self):
        with self.assertRaises(Exception):
            self.srv.raise_exception()


class TestSyncServiceSyncProxy(unittest.TestCase):
    def setUp(self):
        class MyService(Service):
            @expose
            def echo(self, msg: str) -> str:
                time.sleep(0.01)
                return msg

            @expose
            def raise_exception(self):
                time.sleep(0.01)
                raise Exception("Test exception")

        self.srv = MyService.spawn()

    def tearDown(self):
        self.srv.close()

    def test_many_calls(self):
        for i in range(100):
            msg = f"Message {i}"
            res = self.srv.echo(msg)
            self.assertEqual(res, msg)

    def test_cannot_call_not_exposed(self):
        with self.assertRaises(AttributeError):
            self.srv.not_exposed()

    def test_exception_is_propagated(self):
        with self.assertRaises(Exception):
            self.srv.raise_exception()
