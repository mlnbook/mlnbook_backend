

def gen_seq_queryset(id_seq_list, model):
    id_list = []
    id_seq_cfg = {}
    for each in id_seq_list:
        id_list.append(each["id"])
        id_seq_cfg.update({each["id"]: each["seq"]})
    queryset = model.objects.filter(id__in=id_list)
    seq = 1
    for item in queryset:
        item.seq = 1
        seq += 1
        item.seq = seq
    return queryset
