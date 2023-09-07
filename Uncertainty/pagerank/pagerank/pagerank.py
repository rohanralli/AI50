import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dict = {}
    for p in corpus:
        prob_dict[p] = 0
    if corpus[page] == None:
        for p in prob_dict:
            prob_dict[p] = 1/len(corpus)
        return prob_dict
    for p in prob_dict:
        if p in corpus[page]:
            prob_dict[p] = damping_factor/len(corpus[page])
        prob_dict[p] += (1-damping_factor)/len(corpus)
    return prob_dict
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    divider = n
    pages = []
    my_dict = {}
    sample_list = []
    for p in corpus:
        pages.append(p)
        my_dict[p] = 0.0
    page = random.choices(pages, k = 1)[0]
    n -=1
    
    while n > 0:
        prob_dict = transition_model(corpus, page, damping_factor)
        prob_dict_pages = []
        percentages = []
        for p in prob_dict:
            prob_dict_pages.append(p)
            percentages.append(prob_dict[p])
        page = random.choices(prob_dict_pages, percentages, k = 1)[0]
        sample_list.append(page)
        n -= 1
    for p in sample_list:
        for p_match in my_dict:
            if p == p_match:
                my_dict[p_match] += 1/divider
    return my_dict



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {}
    page_ranks_new = {}
    num_links_i = {}
    for p in corpus:
        page_ranks_new[p] = 1/len(corpus)
        num_links_i[p] = 0
    not_converged = True
    while not_converged:
        for p in page_ranks_new:
            page_ranks[p] = page_ranks_new[p]
        num1 = (1-damping_factor) / len(corpus)
        for p in page_ranks_new:
            links_to_p = set()
            num_links_i = {}
            for page in corpus:
                if p in corpus[page]:
                    links_to_p.add(page)
                    num_links_i[page] = len(corpus[page])
                elif len(corpus[page]) == 0:
                    links_to_p.add(page)
                    num_links_i[page] = len(corpus)
            num2 = 0
            for link in links_to_p:
                num2 += page_ranks[link]/num_links_i[link]
            num2 *= damping_factor
            page_ranks_new[p] = num1 + num2
        not_converged = False
        for p in page_ranks_new:
            #print(page_ranks_new[p] - page_ranks[p])
            if -.001 > page_ranks_new[p] - page_ranks[p] or page_ranks_new[p] - page_ranks[p] > .001:
                not_converged = True
    return page_ranks_new
    
            
            
if __name__ == "__main__":
    main()