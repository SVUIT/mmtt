function updateSidebar(url) {
  var navLinks = document.querySelectorAll('#site-nav a');

  navLinks.forEach(function(link) {
    var linkUrl = new URL(link.href, window.location.origin).pathname;

    if (linkUrl === url) {
      link.classList.add('active'); // Thêm lớp 'active' cho liên kết tương ứng
    } else {
      link.classList.remove('active'); // Loại bỏ lớp 'active' khỏi tất cả các mục khác
    }
  });
}

function saveSidebarState() {
  // Lưu trạng thái mở rộng của các mục có danh mục con
  var expandedItems = [];
  var expandableItems = document.querySelectorAll('.nav-list-expander[aria-pressed="true"]');

  expandableItems.forEach(function(item) {
    var parentItem = item.closest('li');
    if (parentItem) {
      expandedItems.push(parentItem.dataset.id); // Giả sử bạn có `data-id` cho các mục sidebar
    }
  });

  return expandedItems;
}

function restoreSidebarState(expandedItems) {
  // Phục hồi trạng thái mở rộng của các mục dựa trên danh sách đã lưu
  expandedItems.forEach(function(id) {
    var item = document.querySelector('li[data-id="' + id + '"] .nav-list-expander');
    if (item) {
      item.setAttribute('aria-pressed', 'true');
      item.closest('li').classList.add('expanded'); // Hoặc lớp tùy chỉnh của bạn để mở rộng
    }
  });
}

function loadContent(url) {
  // Lưu trạng thái sidebar trước khi thay thế nội dung
  var expandedItems = saveSidebarState();

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

      // Cập nhật nội dung chính
      var newContent = tempDiv.querySelector('.main-content').innerHTML;
      document.querySelector('.main-content').innerHTML = newContent;

      // Cập nhật sidebar nếu có thay đổi
      var newSidebar = tempDiv.querySelector('.side-bar');
      if (newSidebar) {
        document.querySelector('.side-bar').innerHTML = newSidebar.innerHTML;

        // Phục hồi trạng thái sidebar
        restoreSidebarState(expandedItems);
      }

      // Cập nhật URL trên thanh địa chỉ
      window.history.pushState({}, '', url);

      // Cập nhật trạng thái sidebar
      updateSidebar(url);

      // Gắn lại các sự kiện click cho các liên kết sau khi nội dung được cập nhật
      attachLinkEvents();
    })
    .catch(error => console.error('Error:', error));
}

function attachLinkEvents() {
  var navLinks = document.querySelectorAll('#site-nav a');

  navLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
      event.preventDefault();

      var url = this.getAttribute('href');
      loadContent(url);  // Load cả sidebar và main content
    });
  });

  // Gắn sự kiện cho các mục có thể mở rộng/thu gọn
  var expanders = document.querySelectorAll('.nav-list-expander');
  expanders.forEach(function(expander) {
    expander.addEventListener('click', function() {
      var parentItem = this.closest('li');
      var isExpanded = this.getAttribute('aria-pressed') === 'true';

      // Chuyển đổi trạng thái của mục
      this.setAttribute('aria-pressed', !isExpanded);
      parentItem.classList.toggle('expanded', !isExpanded);
    });
  });
}

document.addEventListener('DOMContentLoaded', function() {
  // Gắn sự kiện click cho các liên kết khi DOM đã được tải
  attachLinkEvents();

  window.addEventListener('popstate', function(event) {
    var url = window.location.pathname;
    loadContent(url);  // Load cả sidebar và main content khi sử dụng nút quay lại
  });
});
