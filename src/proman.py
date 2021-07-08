import pathlib
import subprocess
import collections as cs


class Process:
    def __init__(self, cwd, executable):
        self.cwd = pathlib.Path(cwd)
        self.executable = pathlib.Path(executable)
        self.io_fname = self.cwd / self.executable.stem

        self._fname_stdin = self.cwd / self.io_fname.with_suffix('.in')
        self._fname_stdout = self.cwd / self.io_fname.with_suffix('.out')
        self._fname_stderr = self.cwd / self.io_fname.with_suffix('.err')

        self._stdin = None
        self._stdout = None
        self._stderr = None

        self._process = None

    @property
    def stdin(self):
        if self._stdin is None:
            self._stdin = open(self._fname_stdin)
        return self._stdin

    @property
    def stdout(self):
        if self._stdout is None:
            self._stdout = open(self._fname_stdout, 'w+')
        return self._stdout

    # @property
    # def has_run(self):
    #     """Arbitrary measure in order to avoid re-running"""
    #     by_number = int(self.cwd.stem) < 141
    #     has_stdout = self._fname_stdout.is_file()
    #     has_stderr = self._fname_stderr.is_file()
    #     if by_number or has_stdout or has_stderr:
    #         return True

    @property
    def stderr(self):
        if self._stderr is None:
            self._stderr = open(self._fname_stderr, 'w+')
        return self._stderr

    @property
    def finished(self) -> bool:
        # if self.has_run:
        #     return True
        if self._process is None:
            return False
        return self._process.poll() is not None

    def start(self) -> None:
        # if self.has_run:
        #     return

        if self._process is not None:
            return
        self._process = subprocess.Popen(
            self.executable,
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=self.stderr,
            cwd=self.cwd,
        )

    @property
    def started(self) -> bool:
        # if self.has_run:
        #     return True
        return self._process is not None

    @property
    def running(self):
        # if self.has_run:
        #     return False

        return self.started and not self.finished
    
    def cleanup(self) -> int:
        if self.running:
            return

        if self._stdin is not None and not self._stdin.closed:
            self._stdin.close()

        if self._stdout is not None and not self._stdout.closed:
            self._stdout.close()

        if self._stderr is not None and not self._stderr.closed:
            self._stderr.close()

        self.io_fname.with_suffix('.done').touch()


class ProcessHandler:
    def __init__(self, cwd):
        self.cwd = cwd

        self.queue = cs.deque()
        self.current = None
        self._has_run = []
        self._index = 0

    def run_next(self):
        if self.empty:
            return

        if self.active:
            return

        # Store the previous process, if present
        if self.current is not None:
            self._has_run.append(self.current)

        # Start the next process
        self.current = self.queue.popleft()
        self.current.start()
        self._index += 1

    def add_process(self, executable):
        self.queue.append(Process(self.cwd, executable))

    def cleanup(self):
        if self.current is not None and not self.current.running:
            self._has_run.append(self.current)
        for process in self._has_run:
            process.cleanup()

    @property
    def index(self):
        return self._index if not self.completed else 0

    @property
    def empty(self):
        return len(self.queue) == 0

    @property
    def active(self):
        return self.current is not None and self.current.running

    @property
    def ready(self):
        return not self.empty and not self.active

    @property
    def completed(self):
        return self.empty and not self.active
