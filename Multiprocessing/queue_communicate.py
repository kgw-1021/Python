from multiprocessing import Process, Queue, current_process
import time
import os

## multiprocess에서 프로세스 간 데이터를 주고 받는 통신 (IPC) 중 queue를 이용히여 구현한 예제
## IPC 참고 : https://dar0m.tistory.com/233
# https://docs.python.org/3/library/multiprocessing.html#exchanging-objects-between-processes

# 실행 함수
def worker(id, baseNum, q):

    process_id = os.getpid()
    process_name = current_process().name
    print(f"Process ID: {process_id}, Process Name: {process_name}")

    # 누적
    sub_total = 0

    # 계산
    for i in range(baseNum):
        sub_total += 1
        # time.sleep(0.1)

    # Produce
    q.put(sub_total)

    # 정보 출력
    print(f"*** Sub Result : {sub_total},")

def main():

    # 부모 프로세스 아이디
    parent_process_id = os.getpid()
    # 출력
    print(f"Parent process ID {parent_process_id}")

    # 프로세스 리스트  선언
    processes = list()

    # 시작 시간
    start_time = time.time()

    # Queue 선언
    q = Queue()

     # 프로세스 생성 및 실행
    for i in range(40): # 1 ~ 100 적절히 조절
        # 생성
        t = Process(name=str(i).zfill(2), target=worker, args=(i, 100000000, q))

        # 배열에 담기
        processes.append(t)

        # 시작
        t.start()

    # Join
    for process in processes:
        process.join()

    # 순수 계산 시간
    print("--- %s seconds ---" % (time.time() - start_time))

    # 종료 플래그
    q.put('exit')

    total = 0

    # 대기
    while True:
        tmp = q.get()
        if tmp == 'exit':
            break
        else:
            total += tmp

    print()

    print("Main-Processing Total_count={}".format(total))
    print("Main-Processing Done!")


if __name__ == "__main__":
    main()