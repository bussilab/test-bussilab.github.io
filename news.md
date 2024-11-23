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
      <p class="post-text">{{ post.text | newline_to_br }}
      {% if post.url %}
      (<a class="post-link" href="{{ post.url }}" target="_blank">view post</a>)
      {% endif %}</p>
    </div>
    {% endif %}
  {% endfor %}
</div>

For more news, check [our Bluesky timeline](https://bsky.app/profile/bussilab.bsky.social).
Older posts are [on X](https://x.com/bussilab).

<script>
  const allowedDomains = ['disq.us', 'bit.ly', 't.co']; // Whitelisted domains for partial URLs

  document.addEventListener("DOMContentLoaded", function () {
    const posts = document.querySelectorAll(".post-text");
    posts.forEach(post => {
      post.innerHTML = post.innerHTML.replace(
        /(?<!href="|">)((https?:\/\/[\w.-]+\.[a-z]{2,}(\/\S*)?)|([\w.-]+\.[a-z]{2,}\/\S*))/g,
        (match, fullUrl, protocolUrl, path, partialUrl) => {
          if (protocolUrl) {
            // Generic HTTP/HTTPS URL
            return `<a href="${protocolUrl}" target="_blank">${protocolUrl}</a>`;
          } else if (partialUrl) {
            // Partial URL, check whitelist
            const domain = partialUrl.split('/')[0]; // Extract domain from partial URL
            if (allowedDomains.includes(domain)) {
              return `<a href="https://${partialUrl}" target="_blank">${partialUrl}</a>`;
            }
          }
          // Leave unmatched URLs as is
          return match;
        }
      );
    });
  });
</script>


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
