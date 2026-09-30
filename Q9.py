import threading
import heapq

class Job:
    def __init__(self, arrival, job_id, priority, duration, resources, order):
        self.arrival = arrival
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources
        self.order = order

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.order < other.order


w, n = map(int, input().split())

jobs = []

for i in range(n):
    arrival, job_id, priority, duration, resources = input().split()

    job = Job(
        int(arrival),
        job_id,
        int(priority),
        int(duration),
        int(resources),
        i
    )

    jobs.append(job)

jobs.sort(key=lambda x: x.arrival)

workers = [0] * w
worker_lock = threading.Lock()
results = []
waiting_times = []


def execute_job(job, worker_id, start_time):
    finish_time = start_time + job.duration

    with worker_lock:
        results.append(
            (job.job_id, worker_id, start_time, finish_time)
        )
        waiting_times.append(start_time - job.arrival)

    return finish_time


current_time = 0
index = 0
queue = []

while index < n or queue:

    if not queue and index < n:
        current_time = max(current_time, jobs[index].arrival)

    while index < n and jobs[index].arrival <= current_time:
        heapq.heappush(queue, jobs[index])
        index += 1

    available_workers = []

    for i in range(w):
        if workers[i] <= current_time:
            available_workers.append(i)

    while queue and available_workers:
        job = heapq.heappop(queue)
        worker_id = available_workers.pop(0)

        start_time = max(current_time, workers[worker_id])

        thread = threading.Thread(
            target=execute_job,
            args=(job, worker_id + 1, start_time)
        )

        thread.start()
        thread.join()

        workers[worker_id] = start_time + job.duration

    if queue:
        current_time = min(workers)

    elif index < n:
        current_time = max(current_time, jobs[index].arrival)


results.sort(key=lambda x: x[2])

for job_id, worker_id, start, finish in results:
    print(job_id, "W" + str(worker_id), start, finish)

average_wait = sum(waiting_times) / len(waiting_times)

print("AVG_WAIT", f"{average_wait:.2f}")
