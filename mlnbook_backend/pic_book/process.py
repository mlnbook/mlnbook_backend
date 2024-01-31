# coding=utf-8
from mlnbook_backend.pic_book.models import LayoutTemplate
from mlnbook_backend.pic_book.serializers import LayoutTemplateSerializer, TypesetSerializer, CustomTypesetSerializer


def gen_typeset_layouts(layout_ids):
    # layout_ids = set([layout_id for layout_id in setting])
    queryset = LayoutTemplate.objects.filter(id__in=layout_ids)
    layout_data = LayoutTemplateSerializer(queryset, many=True).data
    return layout_data


def get_book_typesets(pic_book, request=None):
    queryset = pic_book.typeset_set.all()
    typeset_list = []
    for typeset_obj in queryset:
        if typeset_obj.c_type == "norm":
            layout_data = TypesetSerializer(typeset_obj, context={"request": request}).data
            layout_data["chapter_typesets"] = []
            layout_cfg = gen_typeset_layouts(set(layout_data["setting"]))
            layout_data["layout_cfg"] = layout_cfg
        else:
            layout_data = CustomTypesetSerializer(typeset_obj, context={"request": request}).data
            layout_ids = []
            for each in layout_data["chapter_typesets"]:
                layout_ids.extend(each["setting"])
            layout_cfg = gen_typeset_layouts(set(layout_ids))
            layout_data["layout_cfg"] = layout_cfg
        typeset_list.append(layout_data)
    return typeset_list
