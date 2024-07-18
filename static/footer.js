document.addEventListener("DOMContentLoaded", function() {
    function createFooter() {
        const footerHTML = `
        <!-- Bootstrap Footer -->
        <footer class="footer bg-light py-3">
            <div class="footer-container text-center">
                Made <i class="fa fa-heart heart"></i> by the <a href="#" target="_blank">CabinetCalc Team</a>.
            </div>
        </footer>
        `;
        document.getElementById('footer-container').innerHTML = footerHTML;
    }

    createFooter();
});