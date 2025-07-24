import asyncio
import aiofiles
from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.background_loop import BackgroundLoop


class File(CanvasObject):
    def __str__(self):
        return "{}".format(self.display_name)

    def download(self, location):
        """
        Download the file to specified location.

        :param location: The path to download to.
        :type location: str
        """
        response = self._requester.request("GET", _url=self.url)

        # Use async-safe file I/O to prevent blocking the event loop
        async def _async_write_file(path, content):
            """Write file using aiofiles to avoid blocking the event loop."""
            async with aiofiles.open(path, "wb") as file_out:
                await file_out.write(content)
        
        # Execute file I/O through background loop to avoid blocking
        BackgroundLoop.run(_async_write_file(location, response.content))

    def get_contents(self, binary=False):
        """
        Download the contents of this file.
        Pass binary=True to return a bytes object instead of a str.

        :rtype: str or bytes
        """
        response = self._requester.request("GET", _url=self.url)
        if binary:
            return response.content
        else:
            return response.text
