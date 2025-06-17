from __future__ import annotations

import re
from typing import Iterable, Iterator, Type, TypeVar

T = TypeVar("T")


class PaginatedList(Iterable[T]):
    """
    Abstracts `pagination of Canvas API \
    <https://canvas.instructure.com/doc/api/file.pagination.html>`_.
    """

    def __getitem__(self, index: int | slice) -> T | Iterable[T]:
        assert isinstance(index, (int, slice))
        if isinstance(index, int):
            if index < 0:
                raise IndexError("Cannot negative index a PaginatedList")
            self._get_up_to_index(index)
            return self._elements[index]
        else:
            return self._Slice(self, index)

    def __init__(
        self,
        content_class: Type[T],
        requester,
        request_method,
        first_url,
        extra_attribs=None,
        _root=None,
        _url_override=None,
        **kwargs,
    ):
        """
        :param content_class: The expected type to return in the list.
        :type content_class: class
        :param requester: The requester to pass HTTP requests through.
        :type requester: :class:`canvasapi_get.requester.Requester`
        :param request_method: HTTP request method
        :type request_method: str
        :param first_url: Canvas endpoint for the initial request
        :type first_url: str
        :param extra_attribs: Extra data to include in the request
        :type extra_attribs: dict
        :param _root: Specify a nested property from Canvas to use for the resulting list.
        :type _root: str
        :param _url_override: "new_quizzes" or "graphql" for specific Canvas endpoints.
                                Other URLs may be specified for third-party requests.
        :type _url_override: str
        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of type content_class
        """
        self._elements: list[T] = []

        self._requester = requester
        self._content_class = content_class
        self._first_url = first_url
        self._first_params = kwargs or {}
        self._first_params["per_page"] = kwargs.get("per_page", 100)
        self._next_url = first_url
        self._next_params = self._first_params
        self._extra_attribs = extra_attribs or {}
        self._request_method = request_method
        self._root = _root
        self._url_override = _url_override

        # Greedy pagination: fetch all pages immediately
        while self._has_next():
            self._grow()

    def __iter__(self) -> Iterator[T]:
        for element in self._elements:
            yield element
        # In case _has_next() became False after init, this loop is a no-op
        while self._has_next():
            new = self._grow()
            for elem in new:
                yield elem

    def __repr__(self) -> str:
        return f"<PaginatedList of type {self._content_class.__name__}>"

    def _get_next_page(self) -> list[T]:
        response = self._requester.request(
            self._request_method,
            self._next_url,
            _url=self._url_override,
            **self._next_params,
        )
        data = response.json()
        # Determine next link
        if response.links:
            next_link = response.links.get("next")
        elif isinstance(data, dict) and "meta" in data:
            try:
                next_link = {"url": data["meta"]["pagination"]["next"], "rel": "next"}
            except KeyError:
                next_link = None
        else:
            next_link = None

        regex = rf"(?:{re.escape(self._requester.base_url)}|{re.escape(self._requester.new_quizzes_url)})(.*)"
        self._next_url = (
            re.search(regex, next_link["url"]).group(1) if next_link else None
        )
        self._next_params = {}

        if self._root:
            try:
                data = data[self._root]
            except KeyError as exc:
                raise ValueError(
                    f"The key <{self._root}> does not exist in the response."
                ) from exc

        content: list[T] = []
        for element in data:
            if element is not None:
                element.update(self._extra_attribs)
                content.append(self._content_class(self._requester, element))

        return content

    def _get_up_to_index(self, index: int) -> None:
        while len(self._elements) <= index and self._has_next():
            self._grow()

    def _grow(self) -> list[T]:
        new_elements = self._get_next_page()
        self._elements.extend(new_elements)
        return new_elements

    def _has_next(self) -> bool:
        return self._next_url is not None

    def _is_larger_than(self, index: int) -> bool:
        return len(self._elements) > index or self._has_next()

    class _Slice(Iterable[T]):
        def __init__(self, the_list: PaginatedList[T], the_slice: slice):
            self._list = the_list
            self._start = the_slice.start or 0
            self._stop = the_slice.stop
            self._step = the_slice.step or 1

            if self._start < 0 or (self._stop is not None and self._stop < 0):
                raise IndexError("Cannot negative index a PaginatedList slice")

        def __iter__(self) -> Iterator[T]:
            index = self._start
            while not self._finished(index):
                if self._list._is_larger_than(index):
                    try:
                        yield self._list[index]
                    except IndexError:
                        return
                    index += self._step
                else:
                    return

        def _finished(self, index: int) -> bool:
            return self._stop is not None and index >= self._stop
