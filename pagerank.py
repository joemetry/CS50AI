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

    model = {}
    links = corpus[page]
    n = len(corpus)
    
    if len(links) == 0:
        # Distribute the PageRank evenly among all pages if there are no outbound links
        for p in corpus:
            model[p] = 1 / n
    else:
        # Calculate PageRank for pages with outbound links
        for p in corpus:
            model[p] = (1 - damping_factor) / n
            if p in links:
                model[p] += damping_factor / len(links)
    
    return model

    
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = {page: 1/N for page in corpus}
    new_rank = page_rank.copy()

    # Loop until convergence
    while True:
        for page in corpus:
            sum_rank = 0
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    sum_rank += page_rank[possible_page] / len(corpus[possible_page])
                elif len(corpus[possible_page]) == 0:
                    sum_rank += page_rank[possible_page] / N
            new_rank[page] = (1 - damping_factor) / N + damping_factor * sum_rank
        
        if all(abs(new_rank[page] - page_rank[page]) < 0.001 for page in corpus):
            break
        
        page_rank = new_rank.copy()

    return new_rank


import random


def sample_pagerank(corpus, damping_factor, n):
    page_rank = {page: 0 for page in corpus}
    sample_page = random.choice(list(corpus.keys()))  # Start with a random page

    for _ in range(n):
        page_rank[sample_page] += 1
        next_pages = transition_model(corpus, sample_page, damping_factor)

        random_value = random.random()
        if random_value < damping_factor and len(corpus[sample_page]) > 0:
            sample_page = random.choices(list(next_pages.keys()), weights=next_pages.values(), k=1)[0]
        else:
            sample_page = random.choice(list(corpus.keys()))

    # Normalize the page ranks
    page_rank = {page: rank / n for page, rank in page_rank.items()}
    return page_rank


if __name__ == "__main__":
    main()
