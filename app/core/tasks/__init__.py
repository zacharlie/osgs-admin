from redis import Redis
from rq import Queue, Worker

# redis = Redis(host="redis", port=6379, db=0, password=None, socket_timeout=None)
# redis = Redis.from_url("redis://redis:6379")
redis = Redis(host="redis", port=6379)

q = Queue("main", connection=redis)
# q = Queue("main", connection=Redis.from_url("redis://redis:6379"))

workers = Worker.all(queue=q)
for worker in workers:
    worker.register_death()

# worker1 = Worker(q, connection=Redis.from_url("redis://redis:6379"))
# worker1 = Worker(q, connection=Redis.from_url("redis://redis:6379"), name="worker-01")
# worker1 = Worker("main", connection=redis, name="worker-01")
# worker1 = Worker([q], connection=Redis.from_url("redis://redis:6379"), name="worker-01")
worker1 = Worker([q], connection=redis, name="worker-01")
worker1.register_birth()
# worker2 = Worker([q], connection=redis, name="worker-02")
# worker2.register_birth()
# worker3 = Worker([q], connection=redis, name="worker-03")
# worker3.register_birth()
# worker4 = Worker([q], connection=redis, name="worker-04")
# worker4.register_birth()
