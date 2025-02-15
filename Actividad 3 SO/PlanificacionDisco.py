def fcfs(requests, head):
    sequence = [head] + requests
    total_distance = sum(abs(sequence[i] - sequence[i+1]) for i in range(len(sequence) - 1))
    return sequence, total_distance

def sstf(requests, head):
    sequence = [head]
    pending = requests[:]
    total_distance = 0
    
    while pending:
        closest = min(pending, key=lambda x: abs(x - head))
        total_distance += abs(head - closest)
        head = closest
        sequence.append(head)
        pending.remove(head)
    
    return sequence, total_distance

def scan(requests, head, disk_size=199):
    sequence = [head]
    requests.sort()
    total_distance = 0
    
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    for r in right:
        total_distance += abs(head - r)
        head = r
        sequence.append(head)
    
    if head != disk_size:
        total_distance += abs(head - disk_size)
        head = disk_size
        sequence.append(head)
    
    for r in reversed(left):
        total_distance += abs(head - r)
        head = r
        sequence.append(head)
    
    return sequence, total_distance

def main():
    requests = [95, 180, 34, 119, 11, 123, 62, 64]
    head = 50

    results = {
        'FCFS': fcfs(requests, head),
        'SSTF': sstf(requests, head),
        'SCAN': scan(requests, head)
    }

    for algo, (sequence, distance) in results.items():
        print(f"{algo} - Secuencia: {sequence} - Total recorrido: {distance}")

if __name__ == "__main__":
    main()
