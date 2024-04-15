import os
import random
import re
import sys
import copy

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
    num_pages = len(corpus)
    num_links = len(corpus[page])

    # If page has no links then return equal probabilities.
    if num_links == 0:
        dict_no_link = dict()
        for page in corpus:
            dict_no_link.update({page: 1 / num_pages})
        return dict_no_link

    transition_probabilities = dict()
    # First divide probabilities equally based on total number of pages.
    for p in corpus:
        transition_probabilities.update({p: (1 - damping_factor) / num_pages})

    # Then update the probabilities of each page based on the number of links a page has on another page.
    for link in corpus[page]:
        transition_probabilities[link] += damping_factor / num_links

    return transition_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Populate dictionary of all pages with count set to 0.
    pagerank_dict = dict()
    for page in corpus:
        pagerank_dict.update({page: 0}) 

    # First page will be randomnly chosen from all pages available.
    current_page = random.choice(list(pagerank_dict.keys()))

    for _ in range(n):
        # Increment count with 1 as the page has been visited.
        pagerank_dict[current_page] += 1

        # Calculate the probabilities based on transitional model, given the current page.
        probabilities = transition_model(corpus, current_page, damping_factor)

        # Based on the probability pick a page as the new current page (see random.choices documentation). 
        # The [0] at the end is placed there because we want the value and not the list random.choices returns.
        current_page = random.choices(population=list(probabilities.keys()), weights=list(probabilities.values()))[0]
    
    # Normalize for total amount of samples.
    for page in pagerank_dict:
        pagerank_dict[page] /= n

    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Start with a "base" rank for every page. Calculated as 1 / number of pages in corpus.
    iterate_dict = dict()
    for page in corpus:
        iterate_dict.update({page: (1 / len(corpus))}) 

    new_rank_dict = dict()

    # While True, for ecyer page in corpus calculate first part of formula.
    # Set diff to zero.
    while True:
        diff = 0    
        for page in corpus:
            new_rank_dict[page] = ((1 - damping_factor) / len(corpus))

            for ref_page, links in corpus.items():
                
                # If page is not linked by any other page, num_links is total number of pages in corpus.
                # As from that page there is an equal probability to go to either one of the pages in corpus, including itself.
                if len(links) == 0:
                    num_links = len(corpus.items())
                    new_rank_dict[page] += (damping_factor * (iterate_dict[ref_page] / num_links))

                # Else if page is found to be linked by another page, use the number of total links on those pages as num_links.
                elif page in links:
                    num_links = len(links)
                    new_rank_dict[page] += (damping_factor * (iterate_dict[ref_page] / num_links))

        # Calculate difference between "base" rank and new rank, if below 0.001 break. Thus breaking while True.
            diff += abs(new_rank_dict[page] - iterate_dict[page])
        
        if diff < 0.001:
            break

        # Copy the resulting new_dank_dict as the iterate_dict
        iterate_dict = copy.deepcopy(new_rank_dict)

    return iterate_dict


if __name__ == "__main__":
    main()