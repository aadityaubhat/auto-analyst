from ....auto_analyst import prompts


def test_render_agg_plot_prompt():
    question = "What is the average rating of all the movies?"
    prompt = prompts.render_agg_plot_prompt(question)
    assert (
        prompt
        == """
Determine whether the asked question can be answered using aggregate data or a plot. Answer aggregate or plot.
Question: How many sales were made in August?
Type: aggregate
Question: What is the average amount per transaction?
Type: aggregate
Question: Plot the timeseries of ad impressions
Type: plot
Question: Who are the top 10 customers by number of transactions?
Type: aggregate
Question: Histogram of customer age
Type: plot
Question: What is the average rating of all the movies?
Type:"""
    )
