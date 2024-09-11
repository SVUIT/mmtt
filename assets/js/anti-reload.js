document.addEventListener('DOMContentLoaded', function() {
  // Gắn sự kiện cho container chứa các liên kết thay vì từng liên kết
  document.querySelector('#site-nav').addEventListener('click', function(event) {
    // Kiểm tra xem mục nhấp có phải là liên kết hay không
    if (event.target.tagName === 'A') {
      event.preventDefault();

      var url = event.target.getAttribute('href');
      loadContent(url); // Load cả sidebar và main content
    }
  });

  // Khôi phục trạng thái của sidebar
  restoreSidebarState();

  // Xử lý khi người dùng sử dụng nút quay lại
  window.addEventListener('popstate', function(event) {
    var url = window.location.pathname;
    loadContent(url); // Load cả sidebar và main content
  });
});

function updateSidebar(url) {
  var navLinks = document.querySelectorAll('#site-nav a');

  navLinks.forEach(function(link) {
    var linkUrl = new URL(link.href, window.location.origin).pathname;

    if (linkUrl === url) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

function loadContent(url) {
  if (!url || url.endsWith('/null')) {
    url = '/index.html'; // Chuyển đến trang chủ
  }

  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(html => {
      var tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;

      var newContent = tempDiv.querySelector('.main-content').innerHTML;
      document.querySelector('.main-content').innerHTML = newContent;

      var newSidebarSection = tempDiv.querySelector('.sidebar-section-to-update');
      if (newSidebarSection) {
        document.querySelector('.sidebar-section-to-update').innerHTML = newSidebarSection.innerHTML;
      }

      window.history.pushState({}, '', url);

      updateSidebar(url);
    })
    .catch(error => console.error('Error:', error));
}

function saveSidebarState() {
  var expanders = document.querySelectorAll('.nav-list-expander');
  var state = {};

  expanders.forEach(function(expander) {
    var isExpanded = expander.classList.contains('expanded');
    var id = expander.getAttribute('data-id');
    state[id] = isExpanded;
  });

  localStorage.setItem('sidebarState', JSON.stringify(state));
}

function restoreSidebarState() {
  var state = JSON.parse(localStorage.getItem('sidebarState')) || {};
  var expanders = document.querySelectorAll('.nav-list-expander');

  expanders.forEach(function(expander) {
    var id = expander.getAttribute('data-id');
    if (state[id]) {
      expander.classList.add('expanded');
      var targetList = expander.nextElementSibling;
      if (targetList) {
        targetList.classList.add('open');
      }
    }
  });

  expanders.forEach(function(expander) {
    expander.addEventListener('click', function() {
      var targetList = this.nextElementSibling;
      if (targetList) {
        targetList.classList.toggle('open');
        this.classList.toggle('expanded');
        saveSidebarState();
      }
    });
  });
}
