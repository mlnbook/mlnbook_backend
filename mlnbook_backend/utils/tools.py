

def gen_seq_queryset(id_seq_list, model):
    id_seq_cfg = {}
    seq = 1
    for each in id_seq_list:
        id_seq_cfg.update({each: seq})
        seq += 1
    queryset = model.objects.filter(id__in=id_seq_list)
    for item in queryset:
        item.seq = id_seq_cfg[item.id]
    return queryset
