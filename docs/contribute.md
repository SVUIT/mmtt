---
layout: default
title: Đóng góp
nav_exclude: true
search_exclude: true
---

# Đóng góp cho website

## Tài liệu học tập

Nếu bạn muốn chia sẻ tài liệu học tập với chúng mình, hãy truy cập vào Form bên dưới:

[Form](https://link.svuit.org/submit){:target="_blank" : .btn .btn-primary .btn-form .fs-5 .mb-4 .mb-md-0 .mr-2 }

Nếu các bạn có thắc mắc gì khác liên hệ chúng mình thông qua địa chỉ email **contact@svuit.org**

## Nội dung trên web

Nếu có nội dung nào đó trên web chưa được đề cập về môn học hoặc bạn cảm thấy phần nội dung nào đó chưa đúng:

- Liên hệ qua email hoặc tạo **Issue** như đã nêu ở mục [Tài liệu học tập](#tài-liệu-học-tập).
- Fork repo GitHub của chúng mình về và trực tiếp thêm chỉnh sửa của bạn vào, sau đó tạo một **Pull request** trên repo chính này.

## Bảng xếp hạng contributors

<link rel="stylesheet" href="{{ '_sass/custom/custom.scss' | relative_url }}">

{% assign sorted = site.data.contributors | sort: "files" | reverse %}
{% assign grouped = "" | split: "" %}
{% assign current_files = nil %}
{% assign group = "" | split: "" %}
{% assign top_contributors_count = 0 %}

{% for c in sorted %}
  {% if current_files == nil %}
    {% assign current_files = c.files %}
  {% endif %}
  {% if c.files == current_files %}
    {% assign group = group | push: c %}
  {% else %}
    {% assign grouped = grouped | push: group %}
    {% if grouped.size < 3 %}
      {% assign top_contributors_count = top_contributors_count | plus: group.size %}
    {% endif %}
    {% assign group = "" | split: "" | push: c %}
    {% assign current_files = c.files %}
  {% endif %}
  {% if forloop.last %}
    {% assign grouped = grouped | push: group %}
  {% endif %}
{% endfor %}

{% assign top3_groups = grouped | slice: 0, 3 %}

<div class="top3-container">
  <!-- Top 1 -->
  {% assign top1_group = top3_groups[0] %}
  <div class="top1-wrapper">
    <div class="contributor-card-top top1">
      <div class="rank-badge">
        <img src="/assets/images/Star.png" alt="Star" class="rank-star">
        <span class="rank-number-star">1</span>
      </div>
      <div class="contributor-name-wrapper">
        {% for top1 in top1_group %}
          <div class="contributor-name-top">
            {% if top1.github %}
              <a href="{{ top1.github }}" target="_blank">{{ top1.name }}</a>
            {% else %}
              {{ top1.name }}
            {% endif %}
          </div>
          {% if top1.class %}
            <div class="contributor-class-top">{{ top1.class }}</div>
          {% endif %}
        {% endfor %}
      </div>
      
      <div class="contributor-stats">
        {% if top1_group[0].submits %}
          <div class="stat-item">
            <div class="stat-number-top">{{ top1_group[0].submits }}</div>
            <div class="stat-label-top">Submits</div>
          </div>
        {% endif %}
        {% if top1_group[0].files %}
          <div class="stat-item">
            <div class="stat-number-top">{{ top1_group[0].files }}</div>
            <div class="stat-label-top">Files</div>
          </div>
        {% endif %}
      </div>
    </div>
  </div>
  
  <!-- Top 2 -->
  {% assign top2_group = top3_groups[1] %}
  <div class="top2-wrapper">
    <div class="contributor-card-top top2">
      <div class="rank-badge">
        <img src="/assets/images/Star.png" alt="Star" class="rank-star">
        <span class="rank-number-star">2</span>
      </div>

      <div class="contributor-name-wrapper">
        {% for c in top2_group %}
          <div class="contributor-name-top">
            {% if c.github %}
              <a href="{{ c.github }}" target="_blank">{{ c.name }}</a>
            {% else %}
              {{ c.name }}
            {% endif %}
          </div>
          {% if c.class %}
            <div class="contributor-class-top">{{ c.class }}</div>
          {% endif %}
        {% endfor %}
      </div>

      <div class="contributor-stats">
        {% if top2_group[0].submits %}
          <div class="stat-item">
            <div class="stat-number-top">{{ top2_group[0].submits }}</div>
            <div class="stat-label-top">Submits</div>
          </div>
        {% endif %}
        {% if top2_group[0].files %}
          <div class="stat-item">
            <div class="stat-number-top">{{ top2_group[0].files }}</div>
            <div class="stat-label-top">Files</div>
          </div>
        {% endif %}
      </div>
    </div>
  </div>

  

  <!-- Top 3 -->
  {% assign top3_group = top3_groups[2] %}
  <div class="top3-wrapper">
    <div class="contributor-card-top top3">
      <div class="rank-badge">
        <img src="/assets/images/Star.png" alt="Star" class="rank-star">
        <span class="rank-number-star">3</span>
      </div>

      <div class="contributor-name-wrapper">
        {% for c in top3_group %}
          <div class="contributor-name-top">
            {% if c.github %}
              <a href="{{ c.github }}" target="_blank">{{ c.name }}</a>
            {% else %}
              {{ c.name }}
            {% endif %}
          </div>
          {% if c.class %}
            <div class="contributor-class-top">{{ c.class }}</div>
          {% endif %}
        {% endfor %}
      </div>

      <div class="contributor-stats">
        {% if top3_group[0].submits %}
          <div class="stat-item">
            <div class="stat-number-top">{{ top3_group[0].submits }}</div>
            <div class="stat-label-top">Submits</div>
          </div>
        {% endif %}
        {% if top3_group[0].files %}
          <div class="stat-item">
            <div class="stat-number-top">{{ top3_group[0].files }}</div>
            <div class="stat-label-top">Files</div>
          </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>


### Những contributors khác

<div class="contributors-grid">
  {% assign top3_total_count = 0 %}
  {% for group in top3_groups %}
    {% assign top3_total_count = top3_total_count | plus: group.size %}
  {% endfor %}
  {% assign others = sorted | slice: top3_total_count, sorted.size %}
  {% assign previous_score = nil %}
  {% assign rank = 3 %}
  {% assign display_rank = 4 %}
  {% for c in others %}
    {% assign current_score = c.files | default: 0 %}
    {% if current_score != previous_score %}
      {% assign rank = rank | plus: 1 %}
      {% assign display_rank = rank %}
    {% endif %}
    {% assign previous_score = current_score %}
    <div class="contributor-card">
      <div class="contributor-name">
        <span class="rank-number">{{ display_rank }}</span>
        {% if c.github %}
          <a href="{{ c.github }}" target="_blank">{{ c.name }}</a>
        {% else %}
          {{ c.name }}
        {% endif %}
      </div>
      {% if c.class %}
        <div class="contributor-class">{{ c.class }}</div>
      {% else %}
        <div class="contributor-class"></div>
      {% endif %}
      <div class="contributor-submits">
        <div class="stat-number">{{ c.submits | default: 0 }}</div>
        <div class="stat-label">Submits</div>
      </div>
      <div class="contributor-files">
        <div class="stat-number">{{ c.files | default: 0 }}</div>
        <div class="stat-label">Files</div>
      </div>
    </div>
  {% endfor %}

  Và những bạn đóng góp ẩn danh.
</div>
