---
title: News Archive
layout: default
---

<h1>News Archive</h1>

<!-- Search and Filter Controls -->
<div>
  <input type="text" id="search-box" placeholder="Search news or hashtags (e.g., #openreview, #preprint)" oninput="filterPosts()">
  <label for="max-posts">Show:</label>
  <input type="number" id="max-posts" value="5" min="1" oninput="filterPosts()" style="width: 60px;">
</div>

More posts can be visualized and searched in the [News archive](news-archive).
See also our timelines on [Bluesky](https://bsky.app/profile/bussilab.bsky.social) (new)
and [Twitter/X](https://x.com/bussilab) (old).

<!-- No Results Message -->
<p id="no-results" style="display: none; color: red;">No posts found.</p>

<!-- Posts List -->
<div id="posts">
  {% for post in site.data.posts %}
    <div class="post" data-text="{{ post.text | escape }}">
      <p class="post-date">{{ post.date }}</p>
      <p class="post-text">
        {{ site.data.posts_preformatted_text[post.url] | safe | default: post.text | markdownify }}
      </p>
      {% if post.url %}
        <a class="post-link" href="{{ post.url }}" target="_blank">View Post</a>
      {% endif %}
    </div>
  {% endfor %}
</div>

<script>
  // Populate the search box and max-posts field with query parameters on load
  document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("query");
    const maxPosts = urlParams.get("maxPosts") || 10; // Default to 10 posts

    document.getElementById('max-posts').value = maxPosts;

    if (query) {
      const searchBox = document.getElementById('search-box');
      searchBox.value = query;
    }

    filterPosts(); // Perform search and apply max posts filter
  });

  // JavaScript for search and filtering functionality
  function filterPosts() {
    const query = document.getElementById('search-box').value.toLowerCase();
    const maxPosts = parseInt(document.getElementById('max-posts').value, 10);
    const posts = document.querySelectorAll('.post');

    let visibleCount = 0;

    posts.forEach(post => {
      const text = post.getAttribute('data-text').toLowerCase();
      const matchesQuery = text.includes(query);

      if (matchesQuery && visibleCount < maxPosts) {
        post.style.display = 'block';
        visibleCount++;
      } else {
        post.style.display = 'none';
      }
    });

    // Show/hide "No Results" message
    document.getElementById('no-results').style.display = visibleCount > 0 ? 'none' : 'block';

    // Update query parameters
    const url = new URL(window.location);
    if (query) {
      url.searchParams.set('query', query);
    } else {
      url.searchParams.delete('query');
    }
    url.searchParams.set('maxPosts', maxPosts);
    window.history.replaceState({}, '', url);
  }
</script>

<style>
  #search-box, #max-posts {
    margin-bottom: 20px;
    padding: 10px;
    font-size: 16px;
  }

  #search-box::placeholder {
    color: #999; /* Light gray */
    font-style: italic; /* Optional */
  }

  #max-posts {
    margin-left: 10px;
    width: 70px;
  }

  .post {
    margin-bottom: 20px;
  }

  .post-date {
    font-weight: bold;
  }

  #no-results {
    font-size: 18px;
  }

</style>

