from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


class EPortfolio(CanvasObject):
    def __str__(self):
        return "{}".format(self.name)

    def get_eportfolio_pages(self, **kwargs):
        """
        Return a list of pages for an ePortfolio.

        :calls: `GET /api/v1/eportfolios/:eportfolio_id/pages \
            <https://canvas.instructure.com/doc/api/e_portfolios.html#method.eportfolios_api.pages>`_

        :returns: List of ePortfolio pages.
        :rtype: :class:`canvasapi-get.paginated_list.PaginatedList` of
            :class:`canvasapi-get.eportfolio.EPortfolioPage`
        """

        return PaginatedList(
            EPortfolioPage,
            self._requester,
            "GET",
            "eportfolios/{}/pages".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )


class EPortfolioPage(CanvasObject):
    def __str__(self):
        return "{}. {}".format(self.position, self.name)
