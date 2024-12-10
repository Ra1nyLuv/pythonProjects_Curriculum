// static/assets/js/search.js
document.addEventListener("DOMContentLoaded", function () {
  // 获取所有表格行
  const rows = Array.from(document.querySelectorAll('.table tbody tr'));

  // 获取搜索框元素
  const searchBox = document.querySelector('.search-box');

  // 定义过滤函数
  function filterData(query) {
    const lowerCaseQuery = query.toLowerCase();

    rows.forEach(row => {
      const code = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
      const name = row.querySelector('td:nth-child(2)').textContent.toLowerCase();

      if (code.includes(lowerCaseQuery) || name.includes(lowerCaseQuery)) {
        row.style.display = ''; // 显示匹配的行
      } else {
        row.style.display = 'none'; // 隐藏不匹配的行
      }
    });
  }

  // 监听输入事件，实时过滤数据
  searchBox.addEventListener('input', function () {
    const query = this.value.trim();
    filterData(query);
  });

  // 监听回车键触发过滤
  searchBox.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
      const query = this.value.trim();
      filterData(query);
    }
  });
});