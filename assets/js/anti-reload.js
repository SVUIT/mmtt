document.addEventListener('DOMContentLoaded', function() {
  // Đường dẫn cơ sở của trang web
  //Sẽ thay đổi đối dựa trên baseUrl của mỗi web
  var baseUrl = '/mmtt'; 

  // Xử lý các liên kết trong menu điều hướng
  var navLinks = document.querySelectorAll('#site-nav a');

  navLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
      event.preventDefault();

      var url = this.getAttribute('href');

      if (!url || url === 'null') {
        url = baseUrl + '/index.html';
      } else if (!url.startsWith(baseUrl)) {
        url = baseUrl + url;
      }

      // Chuyển đến URL mà không reload trang
      fetch(url, { method: 'GET' })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.text();
        })
        .then(html => {
          // Tạo một div tạm thời để chứa nội dung mới
          var tempDiv = document.createElement('div');
          tempDiv.innerHTML = html;

          // Lấy nội dung của phần tử chính trong HTML mới
          var newContent = tempDiv.querySelector('.main-content').innerHTML;

          // Cập nhật nội dung trang
          document.querySelector('.main-content').innerHTML = newContent;

          // Cập nhật URL trên thanh địa chỉ
          window.history.pushState({}, '', url);
        })
        .catch(error => console.error('Error:', error));
    });
  });

  // Xử lý sự kiện khi người dùng nhấn nút Back hoặc Forward trên trình duyệt
  window.addEventListener('popstate', function(event) {
    var url = window.location.pathname;

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
      })
      .catch(error => console.error('Error:', error));
  });
});