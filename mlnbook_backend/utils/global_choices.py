# coding=utf-8
# 语言使用排名 https://www.ethnologue.com/
LANGUAGE_CODE_CHOICES = (
    ("en_US", "英语"),
    ("zh_CN", "简体中文"),
    ("fr_FR", "法语"),
    ("es_ES", "西班牙语"),
    ("ar_AE", "阿拉伯语"),
    ("ru_RU", "俄语"),
    # 以上为联合国6种官方语言
    ("pt_BR", "葡萄牙语"),
    ("ja_JP", "日语"),
    ("de_DE", "德语"),
    ("ko_KR", "韩语"),
    ("in_ID", "印尼语"),
    ("ms_MY", "马来语"),
    ("th_TH", "泰语"),
    ("hi_IN", "北印度语"),
    # 印度有多种语言，暂忽略 ("mr_IN", "印度马拉地语"),
    ("tr_TR", "土耳其语"),
    ("it_IT", "意大利语"),
    ("cs_CZ", "捷克语"),
    ("da_DK", "丹麦语"),
    ("nl_NL", "荷兰语"),
    ("no_NO", "挪威语"),
    ("pl_PL", "波兰语"),
    ("ro_RO", "罗马尼亚语"),
    ("sv_SE", "瑞典语"),
    ("tl_PH", "他加禄语-菲律宾"),
)

LANGUAGE_LEVEL = (
    ("A1", "入门级，可以做简单的互动与交流"),
    ("A2", "基础级，能理解并使用熟悉的日常表达法，基本词汇以求满足具体的需求"),
    ("B1", "进阶级，能理解大部分日常生活中常用句子和表达法"),
    ("B2", "高阶级，能在与以目标语言为母语的对象做互动时保持一定流畅度"),
    ("C1", "流利运用级，在社交上、学术上及专业的场合中，皆能灵活的有效地运用语言资源"),
    ("C2", "精通级，能流利、准确、并即兴的表达自己的意见，并且在较为复杂的情况下亦能有效地表达或区别出言外之意"),
)

PHASE_LEVEL = (
    ("preschool", "学前班"),  # 体验式教育，游戏和保育为主
    ("kindergarten", "幼儿园"),  # 课本教育，小学知识预输入；一般持续1年。
    ("primary", "小学"),
    ("middle", "初中"),
    ("high", "高中"),
    ("university", "大学"),
)

GRADE_LEVEL = (
    ("age1-preschool", "学前1岁"),
    ("age2-preschool", "学前2岁"),
    ("age3-preschool", "学前3岁"),
    ("age4-preschool", "学前4岁"),
    ("age5-preschool", "学前5岁"),
    ("kindergarten", "幼儿园"),  # 课本教育，小学知识预输入；一般持续1-2年。
    ("grade1-primary", "小学一年级"),
    ("grade2-primary", "小学二年级"),
    ("grade3-primary", "小学三年级"),
    ("grade4-primary", "小学四年级"),
    ("grade5-primary", "小学五年级"),
    ("grade6-primary", "小学六年级"),  # 部分地区无六年级
    ("grade7-middle", "初中一年级"),
    ("grade8-middle", "初中二年级"),
    ("grade9-middle", "初中三年级"),
    ("grade10-high", "高中一年级"),
    ("grade11-high", "高中二年级"),
    ("grade12-high", "高中三年级"),
    ("freshman-university", "大学一年级"),
    ("sophomore-university", "大学二年级"),
    ("junior-university", "大学三年级"),
    ("senior-university", "大学四年级"),
)
