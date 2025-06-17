from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


class Module(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def get_module_item(self, module_item, **kwargs):
        """
        Retrieve a module item by ID.

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show>`_

        :param module_item: The object or ID of the module item.
        :type module_item: :class:`canvasapi.module.ModuleItem` or dict

        :rtype: :class:`canvasapi.module.ModuleItem`
        """
        module_item_id = obj_or_id(module_item, "module_item", (ModuleItem,))

        response = self._requester.request(
            "GET",
            "courses/{}/modules/{}/items/{}".format(
                self.course_id, self.id, module_item_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_item_json = response.json()
        module_item_json.update({"course_id": self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def get_module_items(self, **kwargs):
        """
        List all of the items in this module.

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index>`_

        :rtype: :class:`canvasapi-get.paginated_list.PaginatedList` of
            :class:`canvasapi-get.module.ModuleItem`
        """
        return PaginatedList(
            ModuleItem,
            self._requester,
            "GET",
            "courses/{}/modules/{}/items".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )


class ModuleItem(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)
