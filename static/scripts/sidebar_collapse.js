document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');
    const mainContent = document.querySelector('.main-content');

    if (!sidebar || !toggleBtn || !mainContent) {
        console.error("Sidebar, toggle button, or main content not found! Check IDs.");
        return;
    }

    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('hidden');
        mainContent.classList.toggle('expanded');
    });
});
