import pandas as pd
import networkx as nx

def load_individual_dataset(group_dataset, individual_dataset):
    df = pd.read_csv(group_dataset)
    df["Year_of_Release"] = df["Year_of_Release"].apply(lambda x: int(x))
    df = df[df["Year_of_Release"] > 2005]
    individual_data = df
    df.to_csv(individual_dataset, index=False)
    return individual_data

def csv_to_json(input_file, output_file, header=["Publisher", "Genre", "Name", "Global_Sales"]):
    import csv
    import json
    data = {"name": header[0], "children": []}
    with open(input_file, 'r', encoding="latin-1") as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=header)
        next(csvreader)
        for row in csvreader:
            label_node = next((node for node in data['children'] if node['name'] == row[header[0]]), None)
            if label_node is None:
                label_node = {"name": row[header[0]], "children": []}
                data['children'].append(label_node)
            L2_node = next((node for node in label_node['children'] if node['name'] == row[header[1]]), None)
            if L2_node is None:
                L2_node = {"name": row[header[1]], "children": []}
                label_node['children'].append(L2_node)
            L3_node = {"name": row[header[2]], "size": float(row[header[3]])}
            L2_node['children'].append(L3_node)
    with open(output_file, 'w') as jsonfile:
        json.dump(data, jsonfile)

def load_tree_graph(individual_data, input_file="tree_dataset.csv", output_file="tree_dataset.json", size="Global_Sales", threshold=3.5, tree_path=["Publisher", "Genre", "Name", "Global_Sales"]):
    filter_condition = individual_data[size]>=threshold
    df = individual_data[filter_condition]
    df_tree = df[tree_path]
    df_tree.to_csv(input_file, index=False)
    csv_to_json(input_file, output_file)
    return df_tree

def load_network_graph(individual_data, subject_pairs=["Publisher", "Developer"], occurence_threshold=3):
    sub1 = individual_data[subject_pairs[0]]
    sub2 = individual_data[subject_pairs[1]]
    g = nx.Graph()
    co_occurence = {}
    occurence_threshold = 3

    for p, d in zip(sub1, sub2):
        if p == d:
            continue
        edge = tuple(sorted((p, d)))
        if edge in co_occurence:
            co_occurence[edge] += 1
        else:
            co_occurence[edge] = 1
        if co_occurence[edge] >= occurence_threshold:
            g.add_edge(p, d)
    return g

def load_high_dimensional_dataset(individual_data, columns=["Genre", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales", "Critic_Score", "Critic_Count", "User_Score", "User_Count", "Rating"]):
    hd_data = individual_data[columns]
    return hd_data

def load_dynamic_dataset(individual_data, custimized_dataset, year="Year_of_Release", subject="Publisher", stream_data="Critic_Count"):
    count_by_year = individual_data[[year, subject, stream_data]]
    count_by_year = count_by_year.groupby([year, subject]).mean()
    count_by_year = count_by_year.unstack(subject)
    critic_count = count_by_year[stream_data]
    critic_count = critic_count.drop(critic_count.index[-1])
    critic_count = critic_count.dropna(axis=1)
    critic_count.index.name = "year"
    critic_count.to_csv(custimized_dataset)
    return critic_count