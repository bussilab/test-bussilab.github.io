---
title: News Archive
layout: default
---

<h1>News Archive</h1>

<!-- Search Box -->
<input type="text" id="search-box" placeholder="Search news..." oninput="filterPosts()">

Search arbitrary text or use common hashtags, such as ([#openreview](./news-archive?query=%23openreview) or [#preprint](./news-archive?query=%23preprint)).
Search arbitrary text or use common hashtags, such as ([#openreview](./news-archive) or [#preprint](./news-archive)).

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
  // Populate the search box with query parameter value on load
  document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("query");
    if (query) {
      const searchBox = document.getElementById('search-box');
      searchBox.value = query;
      filterPosts(); // Perform search with pre-filled value
    }
  });

  // JavaScript for search functionality
  function filterPosts() {
    const searchBox = document.getElementById('search-box');
    const query = searchBox.value.toLowerCase();
    const posts = document.querySelectorAll('.post');
    let anyVisible = false;

    posts.forEach(post => {
      const text = post.getAttribute('data-text').toLowerCase();
      if (text.includes(query)) {
        post.style.display = 'block';
        anyVisible = true;
      } else {
        post.style.display = 'none';
      }
    });

    // Update URL query parameter
    const url = new URL(window.location);
    if (query) {
      url.searchParams.set('query', query);
    } else {
      url.searchParams.delete('query');
    }
    window.history.replaceState({}, '', url);
  }
</script>

<style>
  #search-box {
    margin-bottom: 20px;
    padding: 10px;
    width: 100%;
    max-width: 400px;
    font-size: 16px;
  }

  .post {
    margin-bottom: 20px;
  }

  .post-date {
    font-weight: bold;
  }
</style>

