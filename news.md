---
title: News
---

Recent news:

<div class="timeline">
  {% assign recent_posts = site.data.posts | slice: 0, 10 %}
  {% for post in recent_posts %}
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
  const allowedDomains = ['disq.us', 'bit.ly', 't.co', 'doi.org']; // Whitelisted domains for partial URLs
  const maxDisplayLength = 25; // Maximum characters to display for long links

  document.addEventListener("DOMContentLoaded", function () {
    const posts = document.querySelectorAll(".post-text");
    posts.forEach(post => {
      let originalContent = post.innerHTML;

      // Temporarily remove <a> tags and their content
      const anchorPlaceholders = [];
      originalContent = originalContent.replace(/<a [^>]+>.*?<\/a>/gi, (match) => {
        anchorPlaceholders.push(match);
        return `ANCHOR_PLACEHOLDER_${anchorPlaceholders.length - 1}`;
      });

      // Process remaining text for URLs
      originalContent = originalContent.replace(
        /(?<!href="|">)((https?:\/\/[\w.-]+\.[a-z]{2,}(\/\S*)?)|([\w.-]+\.[a-z]{2,}\/\S*))/g,
        (match, fullUrl) => {
          // Extract and preserve trailing punctuation
          const trailingPunctuationMatch = fullUrl.match(/[.,:!]+$/);
          const trailingPunctuation = trailingPunctuationMatch ? trailingPunctuationMatch[0] : "";
          const urlWithoutTrailingPunctuation = fullUrl.replace(/[.,:!]+$/, ""); // Remove trailing punctuation

          // Format display URL
          const displayUrl = urlWithoutTrailingPunctuation.replace(/https?:\/\//, ""); // Remove protocol for display
          const shortenedDisplay = displayUrl.length > maxDisplayLength
            ? displayUrl.slice(0, maxDisplayLength) + "..."
            : displayUrl;

          // Determine if the URL needs "https://" prepended
          const isFullUrl = fullUrl.startsWith("http://") || fullUrl.startsWith("https://");
          const finalUrl = isFullUrl ? urlWithoutTrailingPunctuation : `https://${urlWithoutTrailingPunctuation}`;

          // Return the clickable link with preserved punctuation
          return `<a href="${finalUrl}" target="_blank">${shortenedDisplay}</a>${trailingPunctuation}`;
        }
      );

      // Restore original <a> tags
      originalContent = originalContent.replace(/ANCHOR_PLACEHOLDER_(\d+)/g, (_, index) => anchorPlaceholders[index]);

      // Update post content
      post.innerHTML = originalContent;
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
