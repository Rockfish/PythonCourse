
from micro_server import MicroServer
from datetime import datetime

class MyWebApp(MicroServer):
    """A small web application built from the Micro server"""

    def __init__(self):
        # Set the root so the server knows where to find the pages.
        self.root = "simple_site"

        # Set the routes that map request paths to methods
        self.routes = {
                '/': self.index,
                '/hello': self.say_hello,
                '/time': self.get_date,
                '/environment': self.get_environment,
            }

        # Call the base class initializer to make sure
        # everything it set correctly.
        super().__init__()

    def index(self):
        self.static('index.html')

    def say_hello(self):
        self.static('hi.html')

    def get_date(self):
        """Creates a tiny html page with the time"""

        time = datetime.now()
        page = "<htm><body>Time: {}</body></html>"
        html = page.format(time)
        self.response.write(html)

    def get_environment(self):
        """Gets the environment variables as a sorted list of key value pairs
        and renders them to HTML using a template."""

        parts = sorted(self.request.environ.items())
        self.render_response('environment.html', dict(parts=parts))


# Create a webapp object and run it.
app = MyWebApp()
app.run(8000)

