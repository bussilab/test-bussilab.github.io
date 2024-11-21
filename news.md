---
title: News
---

Recent news:

<div class="timeline">
  {% for post in site.data.posts | slice: 0, 10%}
    {% if post.text %}
    <div class="post">
      {% if post.date %}
      <p class="post-date">{{ post.date }}</p>
      {% endif %}
      <p class="post-text">{{ post.text | newline_to_br }}</p>
      {% if post.url %}
      <a class="post-link" href="{{ post.url }}" target="_blank">View on Bluesky</a>
      {% endif %}
    </div>
    {% endif %}
  {% endfor %}
</div>

More on [our Bluesky timeline](https://bsky.app/profile/bussilab.bsky.social).

<style>
  .timeline {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 20px auto;
      max-width: 800px;
  }
  .post {
      border-bottom: 1px solid #ddd;
      padding: 10px 0;
  }
  .post:last-child {
      border-bottom: none;
  }
  .post-date {
      color: #888;
      font-size: 0.9rem;
      margin-bottom: 5px;
  }
  .post-text {
      font-size: 1.1rem;
      margin-bottom: 10px;
  }
  .post-link {
      text-decoration: none;
      color: #007acc;
  }
  .post-link:hover {
      text-decoration: underline;
  }
</style>
