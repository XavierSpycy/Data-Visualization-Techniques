import plotly.express as px

def parallel_coordinates(hd_data, threshold=3.5, filter="Global_Sales", category="Genre"):
    hd_data = hd_data[hd_data[filter] >= threshold]
    genre = set(hd_data[category])
    genre_to_color = {}
    color = 0
    for g in genre:
        color += 1
        genre_to_color[g] = color
    dims = hd_data.columns
    dims = dims[1:-1]
    sales = dims[0:5]
    score = dims[5:8:2]
    count = dims[6:9:2]
    dims = list(count) + list(sales) + list(score)
    hd_data = hd_data.assign(code=[genre_to_color[g] for g in hd_data[category]])

    fig = px.parallel_coordinates(hd_data, color="code", dimensions=dims)
    fig.write_html("parallel_coordinates.html")

def sunburst(individual_data, threshold=3.5, platform="X360", subject='Platform', tree_path=['Platform', 'Genre', 'Publisher', 'Name'], size="Global_Sales"):
    df_tree = individual_data[individual_data[subject]==platform]
    path_and_size = tree_path +[size]
    df_tree = df_tree[path_and_size]
    filter_condition = df_tree[size]>=threshold
    df_tree = df_tree[filter_condition]
    fig = px.sunburst(df_tree, path= tree_path, values=size)
    fig.write_html("sunburst.html")