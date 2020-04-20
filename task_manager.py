 
from multiprocessing import Process, Pipe, current_process


class TaskManager:
    def __init__(self):
        self._taskname = ""
        self._taskdata = {}

    def create(self, name, func, args=None):
        try:
            if not name in self._taskdata:
                if args == None:
                    self._taskdata[name] = Process(name=name, target=func)
                else:
                    self._taskdata[name] = Process(name=name, target=func, args=args)
        except (KeyError):
            print("Key Error..")

    def terminate(self, name):
        if name in self._taskdata:
            self._taskdata[name].terminate()
            self._taskdata[name] = None
            del self._taskdata[name]
            #print("delete task : {}".format(name))

    def start(self, name):
        if name in self._taskdata:
            #print("Start : {} task".format(name))
            #print("Task : {} is {} ".format(name, self._taskdata[name].is_alive()))
            if self._taskdata[name].is_alive() == False:
                self._taskdata[name].start()
            else:
                print("Task {} is dead".format(name))

    def is_task_created(self, name):
        if name in self._taskdata:
            result = 1
        else :
            result = 0

        return result

    def is_alive(self, name):
        result = False
        if name in self._taskdata:
            #print("Task : {} is {} ".format(name, self._taskdata[name].is_alive()))
            result = self._taskdata[name].is_alive()
        return result

    def print_task_data(self):
        for task in self._taskdata:
            print("data : {} ".format(task))


class Message:
    def __init__(self):
        self.parent_pipes = []
        self.child_pipes = []

    def register(self, parent_pipe, child_pipe):
        self.parent_pipes.append(parent_pipe)
        self.child_pipes.append(child_pipe)

    def send(self, pipe_id=None, pipe_lists=None, msg=None, payload=None):
        _send_data = {
            "source" : current_process().name,
            "msg" : msg,
            "payload" : None
        }

        if payload != None:
            _send_data['payload'] = payload

        if pipe_lists != None:
            for pipe_list in pipe_lists:
                pipe_list.send(_send_data)
        else:
            pipe_id.send(_send_data)


    def receive(self, pipe_lists):
        
        data = {"source": "", "msg": "", "payload": {}}
        for r in pipe_lists:
            source, msg , payload = None, None, None
            if r.poll():
                data = r.recv()
                source = data['source']
                msg = data['msg']
                payload = data['payload']
                yield source, msg, payload
            else :
                yield source, msg, payload