---
title: People
---

<style>
.people-container {
  display: grid;
  gap: 20px; /* Space between cards */
  justify-content: center; /* Center-align grid */
  align-items: center; /* Center-align items vertically (optional) */
  padding: 10px;
}

@media (max-width: 768px) {
  .people-container {
    grid-template-columns: 1fr; /* Single column on smaller screens */
    justify-items: center; /* Center cards horizontally */
  }
}

@media (min-width: 769px) and (max-width: 1200px) {
  .people-container {
    grid-template-columns: repeat(2, 1fr); /* Two columns on medium screens */
  }
}

@media (min-width: 1201px) {
  .people-container {
    grid-template-columns: repeat(3, 1fr); /* Three columns on larger screens */
    max-width: 1200px; /* Optional: Limit max width */
  }
}

@media (min-width: 1600px) {
  .people-container {
    grid-template-columns: repeat(4, 1fr); /* Four columns on extra-large screens */
    max-width: 1400px; /* Optional: Limit max width */
  }
}

.person-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 300px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.person-card img {
  border-radius: 50%;
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin-bottom: 15px;
}

.person-info h3 {
  font-size: 1.2em;
  margin: 0 0 10px;
}

.person-role {
  font-weight: bold;
  color: #555;
  margin-bottom: 10px;
}

.person-research {
  font-size: 0.9em;
  color: #777;
  margin-bottom: 15px;
}

.person-funds {
  font-size: 0.9em;
  color: #777;
  margin-bottom: 15px;
}

.person-links a {
  color: #007acc;
  margin: 0 5px;
  font-size: 1.2em;
  text-decoration: none;
}

.person-links a:hover {
  color: #005bb5;
}

</style>


## Our group

<div class="people-container">
  {% for person in site.data.people %}
  <div class="person-card" id="{{ person.name | slugify }}">
    <div class="person-pic">
      {% if person.pic %}
      <img src="{{ person.pic }}" alt="Picture of {{ person.name }}">
      {% endif %}
    </div>
    <div class="person-info">
      <h3>{{ person.name }}</h3>
      <p class="person-role">{{ person.role }}</p>
      {% if person.funds %}
      <p class="person-funds">Funded by: {{ person.funds }}</p>
      {% else %}
      <p class="person-funds">Funded by: SISSA</p>
      {% endif %}
      <p class="person-research">{{ person.research | markdownify }}</p>
      <div class="person-links">
        {% if person.email %}
        <a href="mailto:{{ person.email }}" target="_blank" aria-label="Email" title="Email"><i class="fas fa-envelope"></i></a>
        {% endif %}
        {% if person.phone %}
        <a href="tel:{{ person.phone }}" target="_blank" aria-label="Phone" title="Phone"><i class="fas fa-phone"></i></a>
        {% endif %}
        {% if person.orcid %}
        <a href="https://orcid.org/{{ person.orcid }}" target="_blank" aria-label="ORCID" title="ORCID"><i class="fab fa-orcid"></i></a>
        {% endif %}
        {% if person.scholar %}
        <a href="{{ person.scholar }}" target="_blank" aria-label="Google Scholar" title="Google Scholar"><i class="fas fa-graduation-cap"></i></a>
        {% endif %}
        {% if person.prereview && person.orcid %}
        <a href="https://prereview.org/profiles/{{ person.orcid }}" target="_blank" aria-label="PREreview" title="PREreview"><i class="fas fa-clipboard"></i></a>
        {% endif %}
        {% if person.bluesky %}
        <a href="{{ person.bluesky }}" target="_blank" aria-label="Bluesky" title="Bluesky"><i class="fab fa-bluesky"></i></a>
        {% endif %}
        {% if person.twitter %}
        <a href="{{ person.twitter }}" target="_blank" aria-label="Twitter/X" title="Twitter/X"><i class="fab fa-x-twitter"></i></a>
        {% endif %}
        {% if person.linkedin %}
        <a href="{{ person.linkedin }}" target="_blank" aria-label="LinkedIn" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
        {% endif %}
        {% if person.github %}
        <a href="{{ person.github }}" target="_blank" aria-label="GitHub" title="GitHub"><i class="fab fa-github"></i></a>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>


## Guests

Some former members are participating as regular guests to our group activities. Currently:

- Mattia Bernetti (Università degli Studi di Urbino Carlo Bo, Italy)
- Thorben Fröhlking (Université de Genève, Switzerland)
- Valerio Piomponi (Area Science Park, Trieste, Italy)

## Previous members

Previous members of the group at listed in [this page](people-previous.md).

