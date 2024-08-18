from threading import Thread
import queue
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

    def set_busy(self):
        self.is_busy = True

    def set_free(self):
        self.is_busy = False


class Cafe:
    def __init__(self, tables):
        self.queue = queue.Queue()  
        self.tables = tables

    def customer_arrival(self):
        customer_number = 1
        while customer_number <= 10:
            print(f'Посетитель номер {customer_number} прибыл')
            customer = Customer(customer_number, self)
            customer.start()
            customer_number += 1
            sleep(1)

    def serve_customer(self, customer_number):
        for table in self.tables:
            if not table.is_busy:
                table.set_busy()
                print(f'Посетитель номер {customer_number} сел за стол {table.number}')
                sleep(5)  
                print(f'Посетитель номер {customer_number} покушал и ушёл')
                table.set_free()
                self.check_queue()
                return
        else:
            self.queue.put(customer_number)
            print(f'Посетитель номер {customer_number} ожидает свободный стол')

    def check_queue(self):
        if not self.queue.empty():
            customer_number = self.queue.get()
            self.serve_customer(customer_number)


class Customer(Thread):
    def __init__(self, num, cafe):
        super().__init__()
        self.num = num
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self.num)


# Создаем столы
tables = [Table(i + 1) for i in range(3)]

# Создаем кафе
cafe = Cafe(tables)

# Запускаем поток прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ждем завершения потока
customer_arrival_thread.join()
