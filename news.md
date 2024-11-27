---
title: News
---

<!-- Search Box -->
<input type="text" id="search-box" placeholder="Search by text or hashtags (e.g., #preprint)" oninput="filterPosts()">

<!-- Posts List -->
<div id="posts-container" style="display: none;">
  {% for post in site.data.posts %}
    <div class="post-data" data-text="{{ post.text | escape }}">
      <p class="post-date">{{ post.date }}</p>
      <p class="post-text">
        {{ site.data.posts_preformatted_text[post.url] | safe | default: post.text | markdownify }}
      {% if post.url %}
        <a class="post-link" href="{{ post.url }}" target="_blank">(view post)</a>
      {% endif %}</p>
    </div>
  {% endfor %}
</div>
<div id="posts">
  <!-- Filtered posts will be dynamically rendered here -->
</div>

<!-- Pagination Buttons -->
<div id="pagination-controls" class="pagination-bar">
  <button id="prev-button" onclick="paginate(-1)" disabled>Previous</button>
  <button id="next-button" onclick="paginate(1)">Next</button>
</div>

<!-- Posts Per Page -->
<div id="posts-per-page-controls">
  <label for="posts-per-page">Posts per page:</label>
  <select id="posts-per-page" onchange="updateMaxPosts()">
    <option value="5" selected>5</option>
    <option value="20">20</option>
    <option value="100">100</option>
  </select>
</div>

<script>
let maxPosts = 5; // Default posts per page
let skipPosts = 0; // Default start at the first post
let filteredPosts = []; // Store filtered posts after search

document.addEventListener("DOMContentLoaded", () => {
  // Fetch all posts from the hidden container
  const allPostsContainer = document.getElementById('posts-container');
  const allPosts = Array.from(allPostsContainer.querySelectorAll('.post-data'));

  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get("query") || "";
  maxPosts = parseInt(urlParams.get("maxPosts") || 5, 10);
  skipPosts = parseInt(urlParams.get("skipPosts") || 0, 10);

  document.getElementById("search-box").value = query;
  document.getElementById("posts-per-page").value = maxPosts;

  // Attach the input listener to the search box
  document.getElementById("search-box").addEventListener("input", () => {
    filterPosts(allPosts);
  });

  // Filter and render posts initially
  filterPosts(allPosts);
});

function filterPosts(allPosts) {
  const query = document.getElementById('search-box').value.toLowerCase();

  // Update the query parameter in the URL
  const url = new URL(window.location);
  url.searchParams.set("query", query);
  url.searchParams.set("maxPosts", maxPosts);
  url.searchParams.set("skipPosts", skipPosts);
  window.history.replaceState({}, '', url);

  // Filter posts based on the query
  filteredPosts = allPosts.filter(post => {
    const text = post.getAttribute('data-text').toLowerCase();
    const andGroups = query.split(/\s*&\s*/); // Split by "&" for "AND"
    return andGroups.every(andGroup => {
      const orTerms = andGroup.split(/\s*\|\s*/); // Split by "|" for "OR"
      return orTerms.some(term => text.includes(term.trim()));
    });
  });

  // Immediately render posts after filtering
  renderPosts();
}

function renderPosts() {
  const postsContainer = document.getElementById('posts');
  postsContainer.innerHTML = ''; // Clear current posts

  const start = skipPosts;
  const end = skipPosts + maxPosts;

  // Render the subset of filtered posts
  filteredPosts.slice(start, end).forEach(post => {
    const clonedPost = post.cloneNode(true); // Clone original post structure
    postsContainer.appendChild(clonedPost);
  });

  // Enable/disable pagination buttons
  document.getElementById("prev-button").disabled = skipPosts <= 0;
  document.getElementById("next-button").disabled = end >= filteredPosts.length;

  // Update query parameters for pagination
  const url = new URL(window.location);
  const query = document.getElementById('search-box').value;
  url.searchParams.set("query", query);
  url.searchParams.set("maxPosts", maxPosts);
  url.searchParams.set("skipPosts", skipPosts);
  window.history.replaceState({}, '', url);
}

function paginate(direction) {
  skipPosts += direction * maxPosts;
  renderPosts();
}

function updateMaxPosts() {
  maxPosts = parseInt(document.getElementById("posts-per-page").value, 10);
  skipPosts = 0; // Reset to the first page
  renderPosts();
}

</script>


<style>

#posts {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 20px auto;
    max-width: 800px;
}

#posts .post-data {
    border-bottom: 1px solid #ddd;
    padding: 10px 0;
}

#posts .post-data:last-child {
    border-bottom: none; /* Remove the border for the last post */
}

#posts .post-date {
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 5px;
}

#posts .post-text {
    font-size: 1.1rem;
    margin-bottom: 10px;
}

#posts .post-link {
    text-decoration: none;
    color: #007acc;
}

#posts .post-link:hover {
    text-decoration: underline;
}

#search-box {
  margin-bottom: 20px;
  padding: 10px;
  width: 100%; /* Full width */
  font-size: 16px;
}

#posts-per-page-controls {
  margin-top: 20px;
  text-align: center;
}

#pagination-controls {
  margin-top: 20px;
  text-align: center;
}

#pagination-controls button {
  background-color: white;
  border: 2px solid #1e6bb8; /* Match the blue border */
  color: #1e6bb8; /* Match the blue text */
  padding: 10px 20px;
  font-size: 16px;
  margin: 5px;
  border-radius: 5px; /* Rounded corners */
  cursor: pointer;
  transition: all 0.3s ease; /* Smooth hover effect */
}

#pagination-controls button:hover {
  background-color: #1e6bb8; /* Blue background on hover */
  color: white; /* White text on hover */
}

#pagination-controls button:disabled {
  background-color: #ccc; /* Gray background for disabled state */
  color: #666; /* Slightly darker gray text */
  cursor: not-allowed;
}

.pagination-bar {
  border-top: 1px solid #ddd; /* Horizontal line */
  padding-top: 10px; /* Add spacing between the line and the buttons */
  margin-top: 20px; /* Add spacing from the last post */
}


</style>
