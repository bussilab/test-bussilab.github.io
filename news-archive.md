---
title: News Archive
layout: default
permalink: /news-archive/
---

<h1>News Archive</h1>

<!-- Search Box and Clear Button -->
<div>
  <input type="text" id="search-box" placeholder="Search news..." oninput="filterPosts()">
  <button id="clear-button" onclick="clearSearch()">Clear</button>
</div>

<!-- No Results Message -->
<p id="no-results" style="display: none; color: red;">No posts found.</p>

<!-- Posts List -->
<div id="posts"></div>

<!-- Loading Indicator -->
<p id="loading" style="display: none; text-align: center;">Loading more posts...</p>

<script>
  const posts = {{ site.data.posts | jsonify }};
  const preformattedPosts = {{ site.data.posts_preformatted_text | jsonify }};
  const postsPerPage = 10; // Number of posts to load per scroll
  let currentPage = 1;

  // Render posts dynamically
  function renderPosts(filteredPosts) {
    const postsContainer = document.getElementById('posts');
    const start = (currentPage - 1) * postsPerPage;
    const end = currentPage * postsPerPage;
    const postsToRender = filteredPosts.slice(start, end);

    postsToRender.forEach(post => {
      const postElement = document.createElement('div');
      postElement.className = 'post';
      postElement.setAttribute('data-text', post.text);

      let postText = preformattedPosts[post.url] || post.text;

      postElement.innerHTML = `
        <p class="post-date">${post.date}</p>
        <p class="post-text">${highlightMatch(postText, document.getElementById('search-box').value)}</p>
        ${post.url ? `<a class="post-link" href="${post.url}" target="_blank">View Post</a>` : ''}
      `;

      postsContainer.appendChild(postElement);
    });

    currentPage++;
    toggleLoading(false);
  }

  // Highlight matching terms
  function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
  }

  // Filter posts
  function filterPosts() {
    const query = document.getElementById('search-box').value.toLowerCase();
    const filteredPosts = posts.filter(post => post.text.toLowerCase().includes(query));

    // Reset posts container and reload filtered posts
    document.getElementById('posts').innerHTML = '';
    currentPage = 1;
    renderPosts(filteredPosts);

    // Show/hide "No Results" message
    document.getElementById('no-results').style.display = filteredPosts.length ? 'none' : 'block';

    // Update query parameter
    const url = new URL(window.location);
    if (query) {
      url.searchParams.set('query', query);
    } else {
      url.searchParams.delete('query');
    }
    window.history.replaceState({}, '', url);
  }

  // Clear search box and reset posts
  function clearSearch() {
    document.getElementById('search-box').value = '';
    filterPosts();
  }

  // Infinite scrolling
  function loadMore() {
    const postsContainer = document.getElementById('posts');
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
      toggleLoading(true);

      const query = document.getElementById('search-box').value.toLowerCase();
      const filteredPosts = posts.filter(post => post.text.toLowerCase().includes(query));

      if ((currentPage - 1) * postsPerPage < filteredPosts.length) {
        renderPosts(filteredPosts);
      } else {
        toggleLoading(false);
      }
    }
  }

  // Toggle loading indicator
  function toggleLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
  }

  // Initialize page
  document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get("query");
    if (query) {
      document.getElementById('search-box').value = query;
    }
    filterPosts();

    window.addEventListener('scroll', loadMore);
  });
</script>

<style>
  #search-box {
    margin-bottom: 20px;
    padding: 10px;
    width: 100%;
    max-width: 400px;
    font-size: 16px;
  }

  #clear-button {
    margin-left: 10px;
    padding: 10px;
    font-size: 16px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  #clear-button:hover {
    background-color: #d32f2f;
  }

  .post {
    margin-bottom: 20px;
  }

  .post-date {
    font-weight: bold;
  }

  .highlight {
    background-color: yellow;
    font-weight: bold;
  }

  #no-results {
    font-size: 18px;
  }

  #loading {
    font-size: 16px;
    color: gray;
  }
</style>

