from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = [line.strip() for line in file.readlines()]
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):
        priority = int(args[0])
        task = args[1]
        if priority in self.current_items.keys():
            while priority in self.current_items.keys():
                temp = self.current_items[priority]
                self.current_items[priority] = task
                priority += 1
                task = temp
            self.current_items[priority] = task
        else:
            self.current_items[priority] = task
        self.write_current()
        print(f'Added task: "{args[1]}" with priority {args[0]}')

    def done(self, args):
        key = int(args[0])
        if key in self.current_items.keys():
            completed = self.current_items.pop(int(args[0]))
            self.write_current()
            self.completed_items.append(completed)
            self.write_completed()
            print("Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {key} exists.")

    def delete(self, args):
        key = int(args[0])
        if key in self.current_items.keys():
            self.current_items.pop(int(args[0]))
            print(f"Deleted item with priority {key}")
            self.write_current()
        else:
            print(f"Error: item with priority {key} does not exist. Nothing deleted.")

    def ls(self):
        items = self.current_items
        for index, key in enumerate(items):
            print(f"{index+1}. {items[key]} [{key}]")

    def report(self):
        items = self.current_items
        print(f"Pending : {len(items)}")
        for index, key in enumerate(items):
            print(f"{index+1}. {items[key]} [{key}]")
        items = self.completed_items
        print(f"\nCompleted : {len(items)}")
        for index, item in enumerate(items):
            print(f"{index+1}. {item}")

    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        return "<h1> Show Incomplete Tasks Here </h1>"

    def render_completed_tasks(self):
        # Complete this method to return all completed tasks as HTML
        return "<h1> Show Completed Tasks Here </h1>"


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()

        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
