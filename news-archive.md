---
title: News Archive
layout: default
permalink: /news-archive/
---

<h1>News Archive</h1>

<!-- Search Box -->
<input type="text" id="search-box" placeholder="Search news..." oninput="filterPosts()">

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
  // JavaScript for search functionality
  function filterPosts() {
    const query = document.getElementById('search-box').value.toLowerCase();
    const posts = document.querySelectorAll('.post');
    posts.forEach(post => {
      const text = post.getAttribute('data-text').toLowerCase();
      post.style.display = text.includes(query) ? 'block' : 'none';
    });
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

