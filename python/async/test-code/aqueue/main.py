import asyncio
import logging
from asyncio import Queue
from random import randrange
from typing import List
from mlog import get_logger

_logger = get_logger(__name__)
finished = False


class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


total_products = [
    Product('beer', 2),
    Product('bread', 1),
    Product('milk', 3),
    Product('chips', 4),
    Product('soda', 2),
    Product('candy', 1),
    Product('cookie', 2),
    Product('chocolate', 3),
    Product('apple', 1),
    Product('orange', 2),
    Product('banana', 1),
    Product('pear', 2),
    Product('water', 1),
    Product('tea', 2),
]


class Customer:
    def __init__(self, id: int, products: List[Product]):
        self.id = id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    while not finished:
        if queue.empty():
            await asyncio.sleep(0.5)
            continue

        customer: Customer = await queue.get()
        _logger.info(f"Cashier {cashier_number} is serving customer {customer.id}")
        for product in customer.products:
            await asyncio.sleep(product.checkout_time)
            _logger.info(f"Cashier {cashier_number} is checking out {product.name}")
        _logger.info(f"Cashier {cashier_number} is finished serving customer {customer.id}")
        queue.task_done()


async def product_customer(queue: Queue, total_consumers: int):
    global finished
    _logger.info("into product_customer")
    for _ in range(total_consumers):
        customer = Customer(queue.qsize(), [total_products[randrange(len(total_products))] for _ in range(randrange(len(total_products)))])
        await queue.put(customer)
        _logger.info(f"New customer {customer.id} is added to the queue")
    finished = True


async def main():
    queue = Queue(maxsize=1)
    cashiers = [asyncio.create_task(checkout_customer(queue, i)) for i in range(3)]
    await asyncio.gather(queue.join(), *cashiers, product_customer(queue, 10))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    asyncio.run(main())
