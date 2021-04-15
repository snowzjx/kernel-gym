bpf_template = '''
{% for header in function.header_list %}
#include<{{header}}>
{% endfor %}

int kprobe__{{ function.function_name }}(struct pt_regs *ctx,
{%- for argument in function.arg_observer_list -%}
{{ argument.arg_type }} {{ argument.arg_name }}
{%- endfor -%}
) {
{%- for argument in function.arg_observer_list %}
{% set outer_loop = loop %}
{%- if argument.extractor_list|length %}
{%- for extractor in argument.extractor_list%}
    int obs_{{outer_loop.index}}_{{loop.index}} = {{ argument.arg_name }}->{{ extractor.prop }};
{% endfor %}
{% else -%}
    int obs_{{loop.index}} = {{ argument.arg_name }};
{% endif -%}
{% endfor %}
    return 0;
}
'''
