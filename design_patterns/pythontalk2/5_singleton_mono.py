from log import logger

class GitFetcher:
    _current_tag = None

    def __init__(self, tag):
        self.current_tag = tag

    @property
    def current_tag(self):
        if self._current_tag is None:
            raise AttributeError("tag was never set")
        return self._current_tag

    @current_tag.setter
    def current_tag(self, new_tag):
        self.__class__._current_tag = new_tag

    def pull(self):
        logger.info("pulling from %s", self.current_tag)
        return self.current_tag

if __name__ == '__main__':
    f1 = GitFetcher(0.2)
    f2 = GitFetcher(0.2)
    f1.current_tag = 0.3
    op2 = f2.pull()
    print(op2)
    op1 = f1.pull()
    print(op1)