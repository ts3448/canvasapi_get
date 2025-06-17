from canvasapi_get.canvas_object import CanvasObject


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

        with open(location, "wb") as file_out:
            file_out.write(response.content)

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
