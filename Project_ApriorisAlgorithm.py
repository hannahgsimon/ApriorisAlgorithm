from itertools import combinations
import sys

# @author hannahgsimon
# This code assumes that items in each transaction are in numerical order.
# Duplicates in one transaction inherently aren't accounted for in this algorithm

class Apriori:
    def __init__(self, transactions, min_sup):
        self.transactions = transactions
        self.min_sup = min_sup
        self.freq_itemsets = []

    def find_freq_1_itemsets(self):
        item_counts = {}
        for transaction in self.transactions:
            for item in transaction:
                if item in item_counts:
                    item_counts[item] += 1
                else:
                    item_counts[item] = 1
        return [(item,) for item, count in item_counts.items() if count >= self.min_sup] #tuple

    def apriori_gen(self, prev_freq_itemsets):
        candidates = set()
        for i in range(len(prev_freq_itemsets)):
            for j in range(i + 1, len(prev_freq_itemsets)):
                l1, l2 = prev_freq_itemsets[i], prev_freq_itemsets[j]
                if l1[:-1] == l2[:-1]:
                    candidate = tuple(sorted(set(l1).union(l2)))
                    if not self.has_infreq_subset(candidate, prev_freq_itemsets):
                        candidates.add(candidate)
        return list(candidates)

    def has_infreq_subset(self, candidate, prev_freq_itemsets):
        k_minus_1_subsets = list(combinations(candidate, len(candidate) - 1))
        for subset in k_minus_1_subsets:
            if subset not in prev_freq_itemsets:
                return True 
        return False

    def count_support(self, candidates):
        candidate_counts = {candidate: 0 for candidate in candidates}
        transactions_set = [set(transaction) for transaction in self.transactions]
        for transaction_set in transactions_set:
            for candidate in candidates:
                if set(candidate).issubset(transaction_set):
                    candidate_counts[candidate] += 1
        return candidate_counts

    def remove_freq_subsets(self, freq_itemsets_k_plus_1, freq_itemsets):
        itemsets_to_remove = set()
        for item in freq_itemsets_k_plus_1:
             k_subsets = [tuple(combination) for combination in combinations(item, len(item) - 1)]
             for subset in k_subsets:
                if subset in freq_itemsets:
                    itemsets_to_remove.add(subset)
        freq_itemsets_set = set(freq_itemsets)
        freq_itemsets_set.difference_update(itemsets_to_remove)
        return list(freq_itemsets_set)

    def run(self):
        freq_itemsets = []
        freq_k_itemsets = self.find_freq_1_itemsets()
        k = 1 #size of itemsets being considered
        while freq_k_itemsets:
            freq_itemsets.extend(freq_k_itemsets)
            candidates = self.apriori_gen(freq_k_itemsets)
            freq_k_itemsets.clear()
            if candidates:
                candidate_counts = self.count_support(candidates)
                freq_itemsets_k_plus_1 = [candidate for candidate, count in candidate_counts.items() if count >= self.min_sup]
                freq_itemsets = self.remove_freq_subsets(freq_itemsets_k_plus_1, freq_itemsets)
                freq_k_itemsets = freq_itemsets_k_plus_1
                k += 1  
        freq_itemsets = sorted(freq_itemsets, key=lambda x: (len(x), sorted(x)))
        return freq_itemsets

if __name__ == '__main__':
    print("Apriori Algorithm Project\nAuthor Info: Hannah Simon\n")
    file_name = '1000-out1.csv'
    file_path = rf'C:\Users\Hannah\Desktop\{file_name}'
    transactions = []

    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            if len(row) > 1:
                items = row[1:]
                try:
                    transaction = tuple(int(item.strip()) for item in items if item.strip())
                except ValueError as e:
                    print(f"Error: {e} - Non-integer data type in file.")
                    sys.exit(1)
                if transaction:
                    transactions.append(transaction)

    """
    for transaction in transactions:
        print(transaction)
    print(len(transactions))
    """

    min_sup = 20
    freq_itemsets = Apriori(transactions, min_sup).run()

    print("File Run:", file_path)
    print("Minimum Support:", min_sup)
    if not freq_itemsets:
        print("No itemsets in dataset meeting prevalence of", min_sup)
    else:
        for itemset in freq_itemsets:
            if len(itemset) == 1:
                print(f"({itemset[0]})")
            else:
                print(itemset)
    print("End - Total Items:", len(freq_itemsets))
