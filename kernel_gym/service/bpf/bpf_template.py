class BPFTemplate(object):
    BPF_FUN_TEMPLATE = """
    {% set ns = namespace(index=start_index) %}
    int kprobe__{{ function.function_name }}(struct pt_regs *ctx,
    {%- for argument in function.arg_observer_list -%}
    {{ argument.arg_type }} {{ argument.arg_name }}
    {%- endfor -%}
    ) {
    {%- for argument in function.arg_observer_list %}
    {%- if argument.extractor_list|length %}
    {%- for extractor in argument.extractor_list%}
        int obs_{{ ns.index }} = {{ argument.arg_name }}->{{ extractor.prop }};
        int index_{{ ns.index }} = {{ ns.index }};
        {{ map_name }}.update(&index_{{ ns.index }}, &obs_{{ ns.index }});
        {%- set ns.index = ns.index + 1 -%}
    {% endfor %}
    {% else -%}
        int obs_{{ ns.index }} = {{ argument.arg_name }};
        int index_{{ ns.index }} = {{ ns.index }};
        {{ map_name }}.update(&index_{{ ns.index }}, &obs_{{ ns.index }});
        {%- set ns.index = ns.index + 1 -%}
    {% endif -%}
    {% endfor %}
        return 0;
    }
    """

    BPF_PROG_TEMPLATE = """
    {% for header in headers %}
    #include<{{header}}>
    {% endfor %}
    BPF_HASH({{ map_name }}, int, int, 1024);
    {{- prog -}}
    """
