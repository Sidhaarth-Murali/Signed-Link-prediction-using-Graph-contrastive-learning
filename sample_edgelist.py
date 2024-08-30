import os
import random
from collections import defaultdict
import argparse

def load_edgelist(filename):
    pos_out_edgelists = defaultdict(list)
    neg_out_edgelists = defaultdict(list)
    pos_in_edgelists = defaultdict(list)
    neg_in_edgelists = defaultdict(list)
    
    with open(filename) as f:
        for line in f.readlines():
            x, y, z = line.split()
            x = int(x)
            y = int(y)
            z = int(z)
            if z == 1:
                pos_out_edgelists[x].append(y)
                pos_in_edgelists[y].append(x)
            else:
                neg_out_edgelists[x].append(y)
                neg_in_edgelists[y].append(x)
                
    return pos_in_edgelists, pos_out_edgelists, neg_in_edgelists, neg_out_edgelists

def sample_edgelist(pos_out_edgelists, neg_out_edgelists, sample_size=None, sample_fraction=None):
    sampled_pos_edges = []
    sampled_neg_edges = []
    
    if sample_fraction:
        sample_size_pos = int(sample_fraction * sum(len(v) for v in pos_out_edgelists.values()))
        sample_size_neg = int(sample_fraction * sum(len(v) for v in neg_out_edgelists.values()))
    else:
        sample_size_pos = sample_size // 2
        sample_size_neg = sample_size // 2
    
    all_pos_edges = [(x, y, 1) for x, ys in pos_out_edgelists.items() for y in ys]
    all_neg_edges = [(x, y, 0) for x, ys in neg_out_edgelists.items() for y in ys]
    
    sampled_pos_edges = random.sample(all_pos_edges, sample_size_pos)
    sampled_neg_edges = random.sample(all_neg_edges, sample_size_neg)
    
    return sampled_pos_edges + sampled_neg_edges

def save_sampled_edgelist(sampled_edges, output_filename):
    with open(output_filename, 'w') as f:
        for x, y, z in sampled_edges:
            f.write(f"{x} {y} {z}\n")

def rename_original_file(filename):
    dirname, basename = os.path.split(filename)
    new_filename = os.path.join(dirname, f"original_{basename}")
    os.rename(filename, new_filename)
    return new_filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, help='Dataset name')
    parser.add_argument('--k', type=int, default=1, help='Fold number')
    parser.add_argument('--sample_size', type=int, default=None, help='Number of edges to sample')
    parser.add_argument('--sample_fraction', type=float, default=None, help='Fraction of edges to sample')
    args = parser.parse_args()
    
    # Define the filenames
    train_filename = f'./experiment-data/{args.dataset}/{args.dataset}-train-{args.k}.edgelist'
    test_filename = f'./experiment-data/{args.dataset}/{args.dataset}-test-{args.k}.edgelist'

    # Load and sample the training edgelist
    pos_in_edgelists, pos_out_edgelists, neg_in_edgelists, neg_out_edgelists = load_edgelist(train_filename)
    rename_original_file(train_filename)
    sampled_edges = sample_edgelist(pos_out_edgelists, neg_out_edgelists, sample_size=args.sample_size, sample_fraction=args.sample_fraction)
    save_sampled_edgelist(sampled_edges, train_filename)  # Save the sampled edgelist with the original filename

    # Load and sample the testing edgelist
    pos_in_edgelists, pos_out_edgelists, neg_in_edgelists, neg_out_edgelists = load_edgelist(test_filename)
    rename_original_file(test_filename)
    sampled_edges = sample_edgelist(pos_out_edgelists, neg_out_edgelists, sample_size=args.sample_size, sample_fraction=args.sample_fraction)
    save_sampled_edgelist(sampled_edges, test_filename)  # Save the sampled edgelist with the original filename

if __name__ == "__main__":
    main()
