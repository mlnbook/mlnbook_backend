

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


def gen_para_ssml(para_content, para_ssml, voice_name):
    if not para_ssml:
        para_ssml_string = """
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
            <voice name="{{voice_name}}">
                <mstts:express-as  style="angry" >
                    <prosody rate="0%" pitch="0%">
                    {{para_content}}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """.format(para_content=para_content, voice_name=voice_name)
        return para_ssml_string
    elif para_ssml.startswith("<voice"):
        para_ssml_string = """
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
            {{para_ssml}}
        </speak>
        """.format(para_ssml=para_ssml)
        return para_ssml_string
    else:
        para_ssml_string = """
        <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
            <voice name="{{voice_name}}">
                {{para_ssml}}
            </voice>
        </speak>
        """.format(para_ssml=para_ssml, voice_name=voice_name)
        return para_ssml_string
