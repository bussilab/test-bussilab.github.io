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

See also our timelines on [Bluesky](https://bsky.app/profile/bussilab.bsky.social) (new)
and [Twitter/X](https://x.com/bussilab) (old).

<script>
  const allowedDomains = ['disq.us', 'bit.ly', 't.co']; // Whitelisted domains for partial URLs
  const maxDisplayLength = 25; // Maximum characters to display for long links

  document.addEventListener("DOMContentLoaded", function () {
    const posts = document.querySelectorAll(".post-text");
    posts.forEach(post => {
      post.innerHTML = post.innerHTML.replace(
        /(?<!href="|">)((https?:\/\/[\w.-]+\.[a-z]{2,}(\/\S*)?)|([\w.-]+\.[a-z]{2,}\/\S*))/g,
        (match, fullUrl, protocolUrl, path, partialUrl) => {
          if (protocolUrl) {
            // Remove https:// or http:// for display text
            const displayUrl = protocolUrl.replace(/https?:\/\//, "");
            const shortenedDisplay = displayUrl.length > maxDisplayLength
              ? displayUrl.slice(0, maxDisplayLength) + "..."
              : displayUrl;
            return `<a href="${protocolUrl}" target="_blank">${shortenedDisplay}</a>`;
          } else if (partialUrl) {
            // Partial URL, check whitelist
            const domain = partialUrl.split('/')[0]; // Extract domain from partial URL
            if (allowedDomains.includes(domain)) {
              const fullLink = `https://${partialUrl}`;
              const shortenedDisplay = partialUrl.length > maxDisplayLength
                ? partialUrl.slice(0, maxDisplayLength) + "..."
                : partialUrl;
              return `<a href="${fullLink}" target="_blank">${shortenedDisplay}</a>`;
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
