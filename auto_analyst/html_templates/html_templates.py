import jinja2

environment = jinja2.Environment()


output_component_template = environment.from_string(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div id="accordion">
    {% for question, answer in question_answer %}
      <div class="card css-8u98yl exg6vvm0">
        <div class="card-header" id="heading{{ loop.index }}">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapse{{ loop.index }}" aria-expanded="true" aria-controls="collapse{{ loop.index }}">
            {{ question}}
            </button>
          </h5>
        </div>
        <div id="collapse{{ loop.index }}" class="collapse show" aria-labelledby="heading{{ loop.index }}" data-parent="#accordion">
          <div class="card-body">
            {{ answer }}
          </div>
        </div>
      </div>
        {% endfor %}
    </div>
    """
)


def render_output_component(question_answer):
    return output_component_template.render(question_answer=question_answer)


dataframe_template = environment.from_string(
    """
<div class="dvn-underlay"><canvas data-testid="data-grid-canvas" tabindex="0" width="805"
        height="248"
        style="contain: strict; display: block; cursor: default; width: 805px; height: 248px;">
        <table role="grid" aria-rowcount="101" aria-multiselectable="true"
            aria-colcount="15">
            <thead role="rowgroup">
                <tr role="row" aria-rowindex="1">
                    <th role="columnheader" aria-selected="false" aria-colindex="1"
                        tabindex="-1"></th>
                    {% for column in columns %}
                    <th role="columnheader" aria-selected="false" aria-colindex="{{ loop.index + 1 }}"
                        tabindex="-1">{{ column }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody role="rowgroup">
              {% for row in rows %}
                <tr role="row" aria-selected="false" aria-rowindex="{{ loop.index + 1}}">
                    <td role="gridcell" aria-colindex="1" aria-selected="false"
                        aria-readonly="true" id="glide-cell-0-0"
                        data-testid="glide-cell-0-0" tabindex="-1">{{ loop.index }}</td>
                  {% for value in row %}
                    <td role="gridcell" aria-colindex="{{ loop.index + 1 }}" aria-selected="false"
                        aria-readonly="true" id="glide-cell-0-0"
                        data-testid="glide-cell-0-0" tabindex="-1">{{ value }}</td>
                </tr>{% endfor %}{% endfor %}
            </tbody>
          </table>
        </canvas><canvas width="805" height="36"
        style="position: absolute; top: 0px; left: 0px; width: 805px; height: 36px;"></canvas>
    <div id="shadow-y"
        style="position: absolute; top: 35px; left: 0px; width: 805px; height: 248px; opacity: 0.04; pointer-events: none; box-shadow: rgba(0, 0, 0, 0.2) 0px 13px 10px -13px inset;">
    </div>
</div>
<div draggable="false" class="dvn-scroller glideDataEditor"
    style="width: 805px; height: 248px; cursor: default;">
    <div class="dvn-scroll-inner hidden">
        <div class="dvn-stack">
            <div style="width: 1678px; height: 0px;"></div>
            <div style="width: 0px; height: 3535px;"></div>
        </div>
    </div>
</div>
"""
)


def render_html_table(columns, rows):
    return dataframe_template.render(columns=columns, rows=rows)
